"""Local SQLite project storage for Avatar Studio."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from avatar_studio.inspectors import inspect_artifact
from avatar_studio.pipeline import STAGES


VALID_STATUSES = {"pending", "ready", "in_progress", "blocked", "passed", "failed"}
SCHEMA_VERSION = 2


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ProjectStore:
    """Persist project progress, artefacts and validation metadata locally."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.state_dir = self.workspace / ".avatar-studio"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.database_path = self.state_dir / "project.sqlite3"
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS project_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS stage_state (
                    stage_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    notes TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage_id TEXT NOT NULL,
                    path TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS validation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage_id TEXT NOT NULL,
                    check_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    value_json TEXT,
                    expected TEXT,
                    message TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS tool_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage_id TEXT,
                    executable TEXT NOT NULL,
                    arguments_json TEXT NOT NULL,
                    exit_code INTEGER,
                    log_path TEXT,
                    started_at TEXT NOT NULL,
                    finished_at TEXT
                );
                """
            )
            connection.execute(
                "INSERT OR REPLACE INTO project_meta(key, value) VALUES('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            connection.execute(
                "INSERT OR IGNORE INTO project_meta(key, value) VALUES('created_at', ?)",
                (_utc_now(),),
            )
            for stage in STAGES:
                connection.execute(
                    "INSERT OR IGNORE INTO stage_state(stage_id, status, updated_at) VALUES(?, 'pending', ?)",
                    (stage.stage_id, _utc_now()),
                )
        self.refresh_readiness()

    def stage_statuses(self) -> dict[str, str]:
        """Return status for every canonical stage."""

        with self._connect() as connection:
            rows = connection.execute("SELECT stage_id, status FROM stage_state").fetchall()
        return {row["stage_id"]: row["status"] for row in rows}

    def progress(self) -> tuple[int, int, float]:
        """Return passed stages, total stages and completion percentage."""

        statuses = self.stage_statuses()
        passed = sum(status == "passed" for status in statuses.values())
        total = len(STAGES)
        percentage = (passed / total * 100.0) if total else 0.0
        return passed, total, percentage

    def set_stage_status(self, stage_id: str, status: str, notes: str = "") -> None:
        """Set a stage status and recompute readiness of dependent stages."""

        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported stage status: {status}")
        if stage_id not in {stage.stage_id for stage in STAGES}:
            raise KeyError(f"Unknown pipeline stage: {stage_id}")
        with self._connect() as connection:
            connection.execute(
                "UPDATE stage_state SET status = ?, notes = ?, updated_at = ? WHERE stage_id = ?",
                (status, notes, _utc_now(), stage_id),
            )
        self.refresh_readiness()

    def refresh_readiness(self) -> None:
        """Mark pending stages as ready when all dependencies have passed."""

        statuses = self.stage_statuses()
        with self._connect() as connection:
            for stage in STAGES:
                current = statuses.get(stage.stage_id, "pending")
                if current in {"passed", "in_progress", "failed", "blocked"}:
                    continue
                dependencies_passed = all(statuses.get(dep) == "passed" for dep in stage.dependencies)
                new_status = "ready" if dependencies_passed else "pending"
                if new_status != current:
                    connection.execute(
                        "UPDATE stage_state SET status = ?, updated_at = ? WHERE stage_id = ?",
                        (new_status, _utc_now(), stage.stage_id),
                    )

    def register_artifact(
        self,
        stage_id: str,
        path: str | Path,
        kind: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Register an existing file with SHA-256 and automatically inspected metadata."""

        if stage_id not in {stage.stage_id for stage in STAGES}:
            raise KeyError(f"Unknown pipeline stage: {stage_id}")
        artifact_path = Path(path).expanduser().resolve()
        if not artifact_path.is_file():
            raise FileNotFoundError(artifact_path)

        inspection = inspect_artifact(artifact_path)
        digest = hashlib.sha256()
        with artifact_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)

        stat = artifact_path.stat()
        automatic = {
            **inspection.metadata,
            "modified_ns": stat.st_mtime_ns,
            "inspection_warnings": list(inspection.warnings),
        }
        automatic.update(metadata or {})
        artifact_kind = kind or inspection.kind

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO artifacts(stage_id, path, kind, sha256, size_bytes, metadata_json, created_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    stage_id,
                    str(artifact_path),
                    artifact_kind,
                    digest.hexdigest(),
                    stat.st_size,
                    json.dumps(automatic, sort_keys=True),
                    _utc_now(),
                ),
            )
            return int(cursor.lastrowid)

    def artifacts_for_stage(self, stage_id: str) -> list[dict[str, Any]]:
        """Return registered artefacts for one stage, newest first."""

        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM artifacts WHERE stage_id = ? ORDER BY id DESC",
                (stage_id,),
            ).fetchall()
        return [{**dict(row), "metadata": json.loads(row["metadata_json"])} for row in rows]

    def artifact(self, artifact_id: int) -> dict[str, Any] | None:
        """Return one artefact with decoded metadata."""

        with self._connect() as connection:
            row = connection.execute("SELECT * FROM artifacts WHERE id = ?", (artifact_id,)).fetchone()
        if row is None:
            return None
        return {**dict(row), "metadata": json.loads(row["metadata_json"])}
