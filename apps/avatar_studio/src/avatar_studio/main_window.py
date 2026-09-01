"""Main PySide6 window for Avatar Studio."""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from avatar_studio.pipeline import STAGES, get_stage
from avatar_studio.store import ProjectStore
from avatar_studio.tooling import display_path, probe_default_tools


class MainWindow(QMainWindow):
    """Pipeline navigator, learning interface and artefact inspector."""

    def __init__(self, store: ProjectStore) -> None:
        super().__init__()
        self.store = store
        self.setWindowTitle(f"Avatar Studio — {store.workspace.name}")
        self.resize(1500, 920)
        self._build_ui()
        self._refresh_stage_list()
        if self.stage_list.count():
            self.stage_list.setCurrentRow(0)

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)

        header = QHBoxLayout()
        self.project_label = QLabel()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1000)
        header.addWidget(self.project_label, stretch=1)
        header.addWidget(self.progress_bar, stretch=2)
        root_layout.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Production pipeline"))
        self.stage_list = QListWidget()
        self.stage_list.currentItemChanged.connect(self._stage_changed)
        left_layout.addWidget(self.stage_list)
        splitter.addWidget(left)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        self.stage_details = QTextBrowser()
        self.stage_details.setOpenExternalLinks(True)
        center_layout.addWidget(self.stage_details)
        controls = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.pass_button = QPushButton("Mark passed")
        self.fail_button = QPushButton("Mark failed")
        self.start_button.clicked.connect(lambda: self._set_current_status("in_progress"))
        self.pass_button.clicked.connect(lambda: self._set_current_status("passed"))
        self.fail_button.clicked.connect(lambda: self._set_current_status("failed"))
        controls.addWidget(self.start_button)
        controls.addWidget(self.pass_button)
        controls.addWidget(self.fail_button)
        center_layout.addLayout(controls)
        splitter.addWidget(center)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Stage artefacts"))
        self.artifact_table = QTableWidget(0, 4)
        self.artifact_table.setHorizontalHeaderLabels(["File", "Size", "SHA-256", "Type"])
        self.artifact_table.horizontalHeader().setStretchLastSection(True)
        self.artifact_table.itemSelectionChanged.connect(self._artifact_selected)
        right_layout.addWidget(self.artifact_table)
        add_artifact = QPushButton("Register and inspect artefact")
        add_artifact.clicked.connect(self._register_artifact)
        right_layout.addWidget(add_artifact)
        right_layout.addWidget(QLabel("Technical parameters"))
        self.artifact_details = QPlainTextEdit()
        self.artifact_details.setReadOnly(True)
        self.artifact_details.setPlaceholderText("Select an artefact to inspect its recorded metadata.")
        right_layout.addWidget(self.artifact_details)
        splitter.addWidget(right)
        splitter.setSizes([300, 620, 580])
        root_layout.addWidget(splitter, stretch=1)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(2000)
        self.log.setPlaceholderText("Diagnostics and validation messages")
        root_layout.addWidget(self.log, stretch=0)

        self.setCentralWidget(root)
        diagnostics = self.menuBar().addMenu("Diagnostics")
        diagnostics.addAction("Probe local tools", self._probe_tools)

    def _refresh_stage_list(self) -> None:
        current_id = self._current_stage_id()
        statuses = self.store.stage_statuses()
        passed, total, percentage = self.store.progress()
        self.project_label.setText(f"{self.store.workspace.name}: {passed}/{total} stages passed")
        self.progress_bar.setValue(round(percentage * 10))
        self.progress_bar.setFormat(f"{percentage:.1f}%")

        self.stage_list.blockSignals(True)
        self.stage_list.clear()
        for stage in STAGES:
            status = statuses.get(stage.stage_id, "pending")
            marker = {"passed": "✓", "ready": "→", "in_progress": "●", "failed": "!", "blocked": "×"}.get(status, "·")
            item = QListWidgetItem(f"{marker} {stage.order:02d}  {stage.title}  [{status}]")
            item.setData(Qt.UserRole, stage.stage_id)
            self.stage_list.addItem(item)
            if stage.stage_id == current_id:
                self.stage_list.setCurrentItem(item)
        self.stage_list.blockSignals(False)
        self._update_current_view()

    def _current_stage_id(self) -> str | None:
        item = self.stage_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def _stage_changed(self, _current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        self._update_current_view()

    def _update_current_view(self) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        stage = get_stage(stage_id)
        status = self.store.stage_statuses().get(stage_id, "pending")
        dependencies = ", ".join(stage.dependencies) or "none"
        outputs = "".join(f"<li>{value}</li>" for value in stage.expected_outputs) or "<li>stage report</li>"
        self.stage_details.setHtml(
            f"<h1>{stage.order:02d}. {stage.title}</h1>"
            f"<p><b>Status:</b> {status}</p>"
            f"<p>{stage.summary}</p>"
            f"<p><b>Dependencies:</b> {dependencies}</p>"
            f"<p><b>Expected outputs:</b></p><ul>{outputs}</ul>"
            f"<p><a href='https://matpomgit.github.io/avatar-3d-self/{stage.document}'>Open full documentation</a></p>"
        )
        self.start_button.setEnabled(status in {"ready", "failed", "blocked"})
        self.pass_button.setEnabled(status == "in_progress")
        self.fail_button.setEnabled(status == "in_progress")
        self._refresh_artifacts(stage_id)

    def _set_current_status(self, status: str) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        if status == "passed" and not self.store.artifacts_for_stage(stage_id):
            answer = QMessageBox.question(
                self,
                "No registered artefact",
                "This stage has no registered output artefact. Mark it as passed anyway?",
            )
            if answer != QMessageBox.Yes:
                return
        self.store.set_stage_status(stage_id, status)
        self.log.appendPlainText(f"{stage_id}: {status}")
        self._refresh_stage_list()

    def _register_artifact(self) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Register stage artefact", str(self.store.workspace))
        if not path:
            return
        try:
            artifact_id = self.store.register_artifact(stage_id, Path(path))
        except OSError as exc:
            QMessageBox.critical(self, "Artefact registration failed", str(exc))
            return
        artifact = self.store.artifact(artifact_id)
        warnings = artifact["metadata"].get("inspection_warnings", []) if artifact else []
        self.log.appendPlainText(f"Registered and inspected artefact #{artifact_id}: {path}")
        for warning in warnings:
            self.log.appendPlainText(f"  warning: {warning}")
        self._refresh_artifacts(stage_id)
        if self.artifact_table.rowCount():
            self.artifact_table.selectRow(0)

    def _refresh_artifacts(self, stage_id: str) -> None:
        artifacts = self.store.artifacts_for_stage(stage_id)
        self.artifact_table.setRowCount(len(artifacts))
        for row_index, artifact in enumerate(artifacts):
            path = Path(artifact["path"])
            values = (
                path.name,
                f"{artifact['size_bytes'] / 1024:.1f} KiB",
                artifact["sha256"][:16] + "…",
                artifact["kind"],
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, artifact["id"])
                self.artifact_table.setItem(row_index, column, item)
        self.artifact_details.clear()

    def _artifact_selected(self) -> None:
        items = self.artifact_table.selectedItems()
        if not items:
            self.artifact_details.clear()
            return
        artifact_id = items[0].data(Qt.UserRole)
        artifact = self.store.artifact(int(artifact_id)) if artifact_id is not None else None
        if artifact is None:
            self.artifact_details.clear()
            return
        payload = {
            "id": artifact["id"],
            "path": artifact["path"],
            "kind": artifact["kind"],
            "size_bytes": artifact["size_bytes"],
            "sha256": artifact["sha256"],
            "created_at": artifact["created_at"],
            "metadata": artifact["metadata"],
        }
        self.artifact_details.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))

    def _probe_tools(self) -> None:
        self.log.appendPlainText("Local tool diagnostics:")
        for probe in probe_default_tools():
            state = "OK" if probe.available else "MISSING"
            self.log.appendPlainText(f"  [{state}] {probe.name}: {display_path(probe.executable)}")
