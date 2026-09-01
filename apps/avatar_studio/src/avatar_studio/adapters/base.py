"""Shared external-tool adapter contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
from typing import Sequence


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Deterministic record of one external process invocation."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


class ToolAdapter:
    """Resolve, probe and invoke one external workstation tool."""

    name = "tool"
    executable_names: tuple[str, ...] = ()
    version_args: tuple[str, ...] = ("--version",)

    def __init__(self, executable: str | Path | None = None, timeout_s: float = 30.0) -> None:
        self.explicit_executable = Path(executable) if executable else None
        self.timeout_s = timeout_s

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

    def run(self, args: Sequence[str], *, timeout_s: float | None = None) -> CommandResult:
        executable = self.resolve()
        if executable is None:
            raise FileNotFoundError(f"{self.name} executable not found")
        command = (str(executable), *(str(arg) for arg in args))
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_s or self.timeout_s,
            check=False,
        )
        return CommandResult(command, completed.returncode, completed.stdout, completed.stderr)

    def version(self) -> CommandResult:
        return self.run(self.version_args)
