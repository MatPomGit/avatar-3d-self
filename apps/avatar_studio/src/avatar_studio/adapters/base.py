"""Shared external-tool adapter contract."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
import threading
import time
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Deterministic record of one external process invocation."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "command": list(self.command),
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


class ToolAdapter:
    """Resolve, probe, invoke and cancel one external workstation tool."""

    name = "tool"
    executable_names: tuple[str, ...] = ()
    version_args: tuple[str, ...] = ("--version",)

    def __init__(self, executable: str | Path | None = None, timeout_s: float = 30.0) -> None:
        self.explicit_executable = Path(executable) if executable else None
        self.timeout_s = timeout_s
        self._cancel_event = threading.Event()
        self._process: subprocess.Popen[str] | None = None
        self._process_lock = threading.Lock()

    def resolve(self) -> Path | None:
        if self.explicit_executable:
            return self.explicit_executable if self.explicit_executable.exists() else None
        for candidate in self.executable_names:
            resolved = shutil.which(candidate)
            if resolved:
                return Path(resolved)
        return None

    @property
    def available(self) -> bool:
        return self.resolve() is not None

    def cancel(self) -> None:
        """Request cancellation of the currently running subprocess."""

        self._cancel_event.set()
        with self._process_lock:
            process = self._process
        if process is not None and process.poll() is None:
            process.terminate()

    def run(
        self,
        args: Sequence[str],
        *,
        timeout_s: float | None = None,
        input_text: str | None = None,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
    ) -> CommandResult:
        executable = self.resolve()
        if executable is None:
            raise FileNotFoundError(f"{self.name} executable not found")
        command = (str(executable), *(str(arg) for arg in args))
        self._cancel_event.clear()
        deadline = time.monotonic() + (timeout_s or self.timeout_s)
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE if input_text is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(cwd) if cwd is not None else None,
            env=dict(env) if env is not None else None,
        )
        with self._process_lock:
            self._process = process
        pending_input = input_text
        try:
            while True:
                if self._cancel_event.is_set():
                    if process.poll() is None:
                        process.terminate()
                    try:
                        stdout, stderr = process.communicate(timeout=2.0)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        stdout, stderr = process.communicate()
                    return CommandResult(command, -15, stdout, (stderr + "\nCancelled by user.").strip())
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    process.kill()
                    stdout, stderr = process.communicate()
                    raise subprocess.TimeoutExpired(command, timeout_s or self.timeout_s, stdout, stderr)
                try:
                    stdout, stderr = process.communicate(input=pending_input, timeout=min(0.25, remaining))
                    return CommandResult(command, process.returncode, stdout, stderr)
                except subprocess.TimeoutExpired:
                    pending_input = None
        finally:
            with self._process_lock:
                self._process = None

    def version(self) -> CommandResult:
        return self.run(self.version_args)

    @staticmethod
    def write_report(report: Mapping[str, Any], path: str | Path) -> Path:
        destination = Path(path).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(dict(report), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return destination
