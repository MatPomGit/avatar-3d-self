"""Piper TTS workstation adapter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from avatar_studio.adapters.base import CommandResult, ToolAdapter


class PiperAdapter(ToolAdapter):
    name = "Piper"
    executable_names = ("piper", "piper.exe")
    version_args = ("--help",)

    def synthesize(
        self,
        text: str,
        model: str | Path,
        output_wav: str | Path,
        *,
        speaker_id: int | None = None,
        length_scale: float = 1.0,
        noise_scale: float | None = None,
        noise_w_scale: float | None = None,
        overwrite: bool = False,
        timeout_s: float = 300.0,
    ) -> dict:
        """Synthesize one utterance and return provenance metadata for downstream alignment."""

        if not text.strip():
            raise ValueError("text must not be empty")
        if length_scale <= 0:
            raise ValueError("length_scale must be greater than zero")
        model_path = Path(model).resolve()
        if not model_path.is_file():
            raise FileNotFoundError(model_path)
        output = Path(output_wav).resolve()
        if output.exists() and not overwrite:
            raise FileExistsError(output)
        output.parent.mkdir(parents=True, exist_ok=True)

        args = [
            "--model",
            str(model_path),
            "--output_file",
            str(output),
            "--length_scale",
            str(length_scale),
        ]
        if speaker_id is not None:
            if speaker_id < 0:
                raise ValueError("speaker_id must be non-negative")
            args.extend(("--speaker", str(speaker_id)))
        if noise_scale is not None:
            args.extend(("--noise_scale", str(noise_scale)))
        if noise_w_scale is not None:
            args.extend(("--noise_w", str(noise_w_scale)))

        result = self.run(args, input_text=text + "\n", timeout_s=timeout_s)
        self._require_success(result, "Piper synthesis")
        if not output.is_file():
            raise RuntimeError("Piper completed without creating the expected WAV file")

        config_path = self.find_model_config(model_path)
        config = self.read_model_config(config_path) if config_path else None
        return {
            "tool": "Piper",
            "model": str(model_path),
            "model_sha256": self._sha256(model_path),
            "config": str(config_path) if config_path else None,
            "config_sha256": self._sha256(config_path) if config_path else None,
            "sample_rate_hz": self._sample_rate(config),
            "output": str(output),
            "output_sha256": self._sha256(output),
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "text_characters": len(text),
            "parameters": {
                "speaker_id": speaker_id,
                "length_scale": length_scale,
                "noise_scale": noise_scale,
                "noise_w_scale": noise_w_scale,
            },
            "command": list(result.command),
        }

    def fetch_http_alignment(
        self,
        base_url: str = "http://127.0.0.1:5000",
        *,
        timeout_s: float = 10.0,
    ) -> dict:
        """Read Piper HTTP /info and normalize the latest phoneme-duration alignment."""

        url = base_url.rstrip("/") + "/info"
        with urlopen(url, timeout=timeout_s) as response:
            payload = json.load(response)
        return self.normalize_http_info(payload, source_url=url)

    @staticmethod
    def normalize_http_info(payload: dict, *, source_url: str | None = None) -> dict:
        """Convert Piper duration alignments into canonical start/end timing records."""

        if not isinstance(payload, dict):
            raise ValueError("Piper /info response must be a JSON object")
        voice = payload.get("voice") if isinstance(payload.get("voice"), dict) else {}
        last = payload.get("last")
        if last is None:
            return {
                "tool": "Piper HTTP",
                "source_url": source_url,
                "voice": voice,
                "last_available": False,
                "phonemes": [],
            }
        if not isinstance(last, dict):
            raise ValueError("Piper /info field 'last' must be an object or null")
        alignments = last.get("alignments") or []
        if not isinstance(alignments, list):
            raise ValueError("Piper /info alignments must be a list")

        normalized = []
        cursor = 0.0
        for index, item in enumerate(alignments):
            if not isinstance(item, dict):
                raise ValueError(f"Piper alignment {index} must be an object")
            duration = float(item.get("seconds", 0.0))
            if duration < 0:
                raise ValueError(f"Piper alignment {index} has negative duration")
            symbol = str(item.get("phoneme", ""))
            end = cursor + duration
            normalized.append(
                {
                    "symbol": symbol,
                    "start_s": round(cursor, 9),
                    "end_s": round(end, 9),
                    "duration_s": duration,
                }
            )
            cursor = end

        text = str(last.get("text", ""))
        return {
            "tool": "Piper HTTP",
            "source_url": source_url,
            "voice": voice,
            "last_available": True,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "text_characters": len(text),
            "synthesize_seconds": last.get("synthesize_seconds"),
            "duration_s": round(cursor, 9),
            "phonemes": normalized,
        }

    @staticmethod
    def find_model_config(model: str | Path) -> Path | None:
        path = Path(model)
        candidates = (Path(str(path) + ".json"), path.with_suffix(".json"))
        return next((candidate for candidate in candidates if candidate.is_file()), None)

    @staticmethod
    def read_model_config(config_path: str | Path) -> dict:
        path = Path(config_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Piper model configuration must be a JSON object")
        return payload

    @staticmethod
    def _sample_rate(config: dict | None) -> int | None:
        if not config:
            return None
        audio = config.get("audio")
        if isinstance(audio, dict) and isinstance(audio.get("sample_rate"), int):
            return audio["sample_rate"]
        if isinstance(config.get("sample_rate"), int):
            return config["sample_rate"]
        return None

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def _require_success(result: CommandResult, operation: str) -> None:
        if not result.ok:
            raise RuntimeError(
                f"{operation} failed with exit code {result.returncode}: {result.stderr.strip()}"
            )
