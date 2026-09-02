"""Main PySide6 window for Avatar Studio."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QThread, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from avatar_studio.operations import OperationService
from avatar_studio.pipeline import STAGES, get_stage
from avatar_studio.store import ProjectStore
from avatar_studio.tooling import display_path, probe_default_tools


DOCS_BASE_URL = "https://matpomgit.github.io/avatar-studio/"


class OperationWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, operation: Callable[[], object]) -> None:
        super().__init__()
        self.operation = operation

    def run(self) -> None:
        try:
            self.finished.emit(self.operation())
        except Exception as exc:  # surfaced to the user with operation context
            self.failed.emit(str(exc))


class ToolSettingsDialog(QDialog):
    """Configure external executables without editing configuration files."""

    TOOL_NAMES = ("blender", "colmap", "ffmpeg", "piper")

    def __init__(self, store: ProjectStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("External tool settings")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.fields: dict[str, QLineEdit] = {}
        for name in self.TOOL_NAMES:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            field = QLineEdit(store.tool_path(name) or "")
            field.setPlaceholderText(f"Optional explicit path to {name}; empty uses PATH")
            browse = QPushButton("Browse…")
            browse.clicked.connect(lambda _checked=False, n=name: self._browse(n))
            row_layout.addWidget(field, stretch=1)
            row_layout.addWidget(browse)
            self.fields[name] = field
            form.addRow(name.capitalize(), row)
        layout.addLayout(form)
        info = QLabel("Leave a field empty to use automatic PATH discovery. Settings are stored only in this project workspace.")
        info.setWordWrap(True)
        layout.addWidget(info)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse(self, name: str) -> None:
        path, _ = QFileDialog.getOpenFileName(self, f"Select {name} executable")
        if path:
            self.fields[name].setText(path)

    def accept(self) -> None:
        for name, field in self.fields.items():
            self.store.set_tool_path(name, field.text())
        super().accept()


class MainWindow(QMainWindow):
    """Pipeline navigator, learning interface, operation launcher and artefact inspector."""

    def __init__(self, store: ProjectStore) -> None:
        super().__init__()
        self.store = store
        self.operations = OperationService(store)
        self.worker_thread: QThread | None = None
        self.worker: OperationWorker | None = None
        self.pending_stage_id: str | None = None
        self.setWindowTitle(f"Avatar Studio — {store.workspace.name}")
        self.resize(1580, 960)
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

        self.operation_explanation = QLabel()
        self.operation_explanation.setWordWrap(True)
        center_layout.addWidget(self.operation_explanation)
        operation_controls = QHBoxLayout()
        self.run_button = QPushButton("Run supported operation")
        self.cancel_button = QPushButton("Cancel operation")
        self.cancel_button.setEnabled(False)
        self.run_button.clicked.connect(self._run_stage_operation)
        self.cancel_button.clicked.connect(self._cancel_operation)
        operation_controls.addWidget(self.run_button)
        operation_controls.addWidget(self.cancel_button)
        center_layout.addLayout(operation_controls)

        controls = QHBoxLayout()
        self.start_button = QPushButton("Start stage")
        self.pass_button = QPushButton("Evaluate DoD and pass")
        self.fail_button = QPushButton("Mark failed")
        self.start_button.clicked.connect(lambda: self._set_current_status("in_progress"))
        self.pass_button.clicked.connect(self._pass_current_stage)
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
        right_layout.addWidget(self.artifact_details)
        splitter.addWidget(right)
        splitter.setSizes([320, 700, 560])
        root_layout.addWidget(splitter, stretch=1)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(3000)
        self.log.setPlaceholderText("Diagnostics, operation logs and validation messages")
        root_layout.addWidget(self.log)
        self.setCentralWidget(root)

        file_menu = self.menuBar().addMenu("Project")
        file_menu.addAction("Open / create workspace…", self._switch_workspace)
        tools_menu = self.menuBar().addMenu("Tools")
        tools_menu.addAction("External tool settings…", self._tool_settings)
        tools_menu.addAction("Probe local tools", self._probe_tools)

    def _switch_workspace(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Select or create Avatar Studio workspace")
        if not selected:
            return
        self.store = ProjectStore(selected)
        self.operations = OperationService(self.store)
        self.setWindowTitle(f"Avatar Studio — {self.store.workspace.name}")
        self._refresh_stage_list()

    def _tool_settings(self) -> None:
        if ToolSettingsDialog(self.store, self).exec() == QDialog.Accepted:
            self._probe_tools()

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
        if self.stage_list.currentItem() is None and self.stage_list.count():
            self.stage_list.setCurrentRow(0)
        self._update_current_view()

    def _current_stage_id(self) -> str | None:
        item = self.stage_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def _stage_changed(self, _current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        self._update_current_view()

    def _operation_text(self, stage_id: str) -> tuple[str, bool]:
        if stage_id == "02-photogrammetry":
            return ("COLMAP sparse reconstruction: feature extraction, matching and camera registration. You select the photo folder and parameters; no CLI is required.", True)
        if stage_id == "03-reconstruction":
            return ("COLMAP dense reconstruction: undistortion, PatchMatch stereo, fusion and Poisson/Delaunay meshing.", True)
        if stage_id == "19-piper-integration":
            return ("Generate speech with Piper or normalize audio with FFmpeg. The generated output and provenance report are registered in the project.", True)
        if stage_id in {f"{n:02d}-{name}" for n, name in []}:
            return ("", False)
        if stage_id.startswith(tuple(f"{n:02d}-" for n in range(4, 19))):
            return ("For Blender-based manual stages, Avatar Studio can currently perform deep inspection of a selected .blend scene and record the report. Editing remains in Blender.", True)
        return ("No automated production operation is implemented for this stage yet. Follow the linked documentation and register the resulting artefact.", False)

    def _update_current_view(self) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        stage = get_stage(stage_id)
        status = self.store.stage_statuses().get(stage_id, "pending")
        dependencies = ", ".join(stage.dependencies) or "none"
        outputs = "".join(f"<li>{value}</li>" for value in stage.expected_outputs) or "<li>stage report</li>"
        validations = self.store.validation_results(stage_id)
        failed = sum(item["status"] == "failed" for item in validations)
        waivers = len(self.store.waivers(stage_id))
        self.stage_details.setHtml(
            f"<h1>{stage.order:02d}. {stage.title}</h1>"
            f"<p><b>Status:</b> {status}</p><p>{stage.summary}</p>"
            f"<p><b>Dependencies:</b> {dependencies}</p>"
            f"<p><b>Expected outputs:</b></p><ul>{outputs}</ul>"
            f"<p><b>Validation:</b> {len(validations)} result(s), {failed} failed, {waivers} waiver(s).</p>"
            f"<p><a href='{DOCS_BASE_URL}{stage.document}'>Open full documentation</a></p>"
        )
        operation_text, supported = self._operation_text(stage_id)
        self.operation_explanation.setText(operation_text)
        self.run_button.setEnabled(supported and self.worker_thread is None)
        self.start_button.setEnabled(status in {"ready", "failed", "blocked"})
        self.pass_button.setEnabled(status == "in_progress")
        self.fail_button.setEnabled(status == "in_progress")
        self._refresh_artifacts(stage_id)

    def _set_current_status(self, status: str) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        self.store.set_stage_status(stage_id, status)
        self.log.appendPlainText(f"{stage_id}: {status}")
        self._refresh_stage_list()

    def _pass_current_stage(self) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        allowed, reasons = self.store.can_pass_stage(stage_id)
        if not allowed:
            reason_text = "\n".join(f"• {reason}" for reason in reasons)
            answer = QMessageBox.question(
                self,
                "Definition of Done not satisfied",
                f"This stage cannot pass normally:\n{reason_text}\n\nRecord a controlled waiver?",
            )
            if answer != QMessageBox.Yes:
                return
            waiver, ok = QInputDialog.getMultiLineText(
                self,
                "DoD waiver",
                "Explain why proceeding is justified, what risk remains and how it will be verified later:",
            )
            if not ok or not waiver.strip():
                return
            self.store.add_waiver(stage_id, waiver)
            if not self.store.artifacts_for_stage(stage_id):
                QMessageBox.warning(self, "Artefact still required", "A waiver cannot replace the stage output artefact. Register an artefact before passing.")
                return
        allowed, reasons = self.store.can_pass_stage(stage_id)
        if not allowed:
            QMessageBox.warning(self, "Stage blocked", "\n".join(reasons))
            return
        self.store.set_stage_status(stage_id, "passed")
        self.log.appendPlainText(f"{stage_id}: passed after DoD evaluation")
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

    def _refresh_artifacts(self, stage_id: str) -> None:
        artifacts = self.store.artifacts_for_stage(stage_id)
        self.artifact_table.setRowCount(len(artifacts))
        for row_index, artifact in enumerate(artifacts):
            path = Path(artifact["path"])
            values = (path.name, f"{artifact['size_bytes'] / 1024:.1f} KiB", artifact["sha256"][:16] + "…", artifact["kind"])
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
            return
        payload = {key: artifact[key] for key in ("id", "path", "kind", "size_bytes", "sha256", "created_at")}
        payload["metadata"] = artifact["metadata"]
        self.artifact_details.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))

    def _probe_tools(self) -> None:
        self.log.appendPlainText("Local tool diagnostics:")
        configured = {name: self.store.tool_path(name) for name in ("blender", "colmap", "ffmpeg", "piper")}
        for probe in probe_default_tools(configured):
            state = "OK" if probe.available else "MISSING"
            self.log.appendPlainText(f"  [{state}] {probe.name}: {display_path(probe.executable)}")

    def _run_stage_operation(self) -> None:
        stage_id = self._current_stage_id()
        if not stage_id:
            return
        operation: Callable[[], object] | None = None
        if stage_id == "02-photogrammetry":
            images = QFileDialog.getExistingDirectory(self, "Select source photographs", str(self.store.workspace))
            if not images:
                return
            matcher, ok = QInputDialog.getItem(self, "COLMAP matcher", "Matching strategy", ["exhaustive", "sequential", "spatial"], 0, False)
            if not ok:
                return
            operation = lambda: self.operations.colmap_sparse(images, matcher=matcher)
        elif stage_id == "03-reconstruction":
            images = QFileDialog.getExistingDirectory(self, "Select source photographs", str(self.store.workspace))
            if not images:
                return
            sparse = QFileDialog.getExistingDirectory(self, "Select COLMAP sparse model (usually sparse/0)", str(self.store.workspace / "work" / "colmap"))
            if not sparse:
                return
            mesher, ok = QInputDialog.getItem(self, "Mesher", "Mesh reconstruction", ["poisson", "delaunay"], 0, False)
            if not ok:
                return
            operation = lambda: self.operations.colmap_dense(images, sparse, mesher=mesher)
        elif stage_id == "19-piper-integration":
            mode, ok = QInputDialog.getItem(self, "Speech operation", "Choose operation", ["Piper synthesis", "FFmpeg normalize WAV"], 0, False)
            if not ok:
                return
            if mode.startswith("Piper"):
                text, ok = QInputDialog.getMultiLineText(self, "Speech text", "Text to synthesize")
                if not ok or not text.strip():
                    return
                model, _ = QFileDialog.getOpenFileName(self, "Select Piper ONNX model", str(self.store.workspace), "ONNX (*.onnx)")
                if not model:
                    return
                output, _ = QFileDialog.getSaveFileName(self, "Output WAV", str(self.store.workspace / "speech.wav"), "WAV (*.wav)")
                if not output:
                    return
                operation = lambda: self.operations.synthesize_piper(text, model, output)
            else:
                source, _ = QFileDialog.getOpenFileName(self, "Select audio", str(self.store.workspace))
                if not source:
                    return
                output, _ = QFileDialog.getSaveFileName(self, "Normalized WAV", str(self.store.workspace / "speech_normalized.wav"), "WAV (*.wav)")
                if not output:
                    return
                operation = lambda: self.operations.normalize_audio(source, output)
        elif stage_id.startswith(tuple(f"{n:02d}-" for n in range(4, 19))):
            blend, _ = QFileDialog.getOpenFileName(self, "Select Blender scene to inspect", str(self.store.workspace), "Blender (*.blend)")
            if not blend:
                return
            operation = lambda: self.operations.inspect_blend(stage_id, blend)
        if operation is not None:
            if self.store.stage_statuses().get(stage_id) == "ready":
                self.store.set_stage_status(stage_id, "in_progress")
            self._start_background_operation(stage_id, operation)

    def _start_background_operation(self, stage_id: str, operation: Callable[[], object]) -> None:
        self.pending_stage_id = stage_id
        self.worker_thread = QThread(self)
        self.worker = OperationWorker(operation)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._operation_finished)
        self.worker.failed.connect(self._operation_failed)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.failed.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self._operation_thread_finished)
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.log.appendPlainText(f"{stage_id}: operation started")
        self.worker_thread.start()

    def _cancel_operation(self) -> None:
        self.operations.cancel()
        self.log.appendPlainText("Cancellation requested. The active external process will be terminated.")
        self.cancel_button.setEnabled(False)

    def _operation_finished(self, result: object) -> None:
        stage_id = self.pending_stage_id
        if not stage_id:
            return
        report, report_path = result  # type: ignore[misc]
        self.log.appendPlainText(f"{stage_id}: operation completed; report: {report_path}")
        if stage_id == "02-photogrammetry":
            models = report.get("models", [])
            self.store.register_artifact(stage_id, report_path, kind="operation_report", metadata={"models": models})
            if models:
                metrics = self.operations._adapter.__self__ if False else None
                self.store.add_validation_result(stage_id, "sparse_model_created", "passed", value=len(models), expected=">= 1", message="COLMAP created at least one sparse model.")
            else:
                self.store.add_validation_result(stage_id, "sparse_model_created", "failed", value=0, expected=">= 1", message="No sparse reconstruction model was created.")
        elif stage_id == "03-reconstruction":
            mesh = Path(report["mesh"])
            self.store.register_artifact(stage_id, mesh, metadata={"operation_report": str(report_path)})
            self.store.add_validation_result(stage_id, "dense_mesh_created", "passed", value=mesh.stat().st_size, expected="> 0 bytes", message="Dense reconstruction produced a mesh.")
        elif stage_id == "19-piper-integration":
            output = report.get("output")
            if output and Path(output).is_file():
                self.store.register_artifact(stage_id, output, metadata={"operation_report": str(report_path)})
            else:
                self.store.register_artifact(stage_id, report_path, kind="operation_report")
            self.store.add_validation_result(stage_id, "speech_operation", "passed", message="Speech processing operation completed successfully.")
        else:
            self.store.register_artifact(stage_id, report_path, kind="inspection_report")
            self.store.add_validation_result(stage_id, "blender_inspection", "passed", message="Blender scene inspection completed successfully.")
        self._refresh_stage_list()

    def _operation_failed(self, message: str) -> None:
        stage_id = self.pending_stage_id
        self.log.appendPlainText(f"{stage_id or 'operation'}: FAILED: {message}")
        if stage_id:
            self.store.add_validation_result(stage_id, "tool_operation", "failed", message=message)
            self.store.set_stage_status(stage_id, "failed")
        QMessageBox.critical(self, "Operation failed", message)
        self._refresh_stage_list()

    def _operation_thread_finished(self) -> None:
        if self.worker is not None:
            self.worker.deleteLater()
        if self.worker_thread is not None:
            self.worker_thread.deleteLater()
        self.worker = None
        self.worker_thread = None
        self.pending_stage_id = None
        self.cancel_button.setEnabled(False)
        self._update_current_view()
