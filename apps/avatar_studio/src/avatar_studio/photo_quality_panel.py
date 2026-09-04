"""Embedded photo quality and preprocessing panel for Avatar Studio."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from avatar_studio.photo_quality import analyze_photo_batch, preprocess_photo_batch
from avatar_studio.store import ProjectStore


ProgressCallback = Callable[[int, str], None]


class _PhotoWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)
    progress = Signal(int, str)

    def __init__(self, operation: Callable[[ProgressCallback], object]) -> None:
        super().__init__()
        self.operation = operation

    def run(self) -> None:
        try:
            self.finished.emit(self.operation(self.progress.emit))
        except Exception as exc:
            self.failed.emit(str(exc))


class PhotoQualityPanel(QGroupBox):
    """GUI for batch QA and non-destructive photo preprocessing."""

    def __init__(self, store: ProjectStore, parent: QWidget | None = None) -> None:
        super().__init__("PHOTO QA AND PREPROCESSING", parent)
        self.store = store
        self.worker_thread: QThread | None = None
        self.worker: _PhotoWorker | None = None
        self._mode: str | None = None
        self._build_ui()
        self._set_defaults()

    def set_store(self, store: ProjectStore) -> None:
        self.store = store
        self._set_defaults()
        self.results.setRowCount(0)
        self.summary.setText("No analysis performed yet.")

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        description = QLabel(
            "This panel checks a photogrammetry batch before reconstruction. It estimates sharpness, "
            "exposure, clipping, contrast and sequential overlap, then marks photographs that should "
            "be reviewed or repeated. It can also create derived copies with normalized illumination, "
            "local contrast enhancement and optional static-background removal. Original photographs "
            "are never overwritten."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        form = QFormLayout()
        self.photos_field = QLineEdit()
        self.photos_field.setReadOnly(True)
        form.addRow("Photograph batch", self._path_row(self.photos_field, self._choose_photos, "Select…"))

        self.background_field = QLineEdit()
        self.background_field.setReadOnly(True)
        self.background_field.setPlaceholderText("Optional empty-scene background photograph")
        form.addRow("Background image", self._path_row(self.background_field, self._choose_background, "Select…", clear=True))

        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True)
        form.addRow("Derived output", self._path_row(self.output_field, self._choose_output, "Select…"))
        layout.addLayout(form)

        options = QHBoxLayout()
        self.normalize_lighting = QCheckBox("Normalize lighting")
        self.normalize_lighting.setToolTip(
            "Matches median luminance between photographs to reduce exposure drift across the batch."
        )
        self.improve_contrast = QCheckBox("Improve contrast")
        self.improve_contrast.setToolTip(
            "Applies conservative CLAHE on luminance. Use only on derived copies, not as a substitute for good capture."
        )
        self.remove_background = QCheckBox("Remove static background")
        self.remove_background.setToolTip(
            "Uses the selected empty-scene image to derive an alpha mask for a static camera/background setup."
        )
        options.addWidget(self.normalize_lighting)
        options.addWidget(self.improve_contrast)
        options.addWidget(self.remove_background)
        options.addStretch(1)
        layout.addLayout(options)

        actions = QHBoxLayout()
        self.analyze_button = QPushButton("Analyze batch")
        self.analyze_button.setObjectName("primaryButton")
        self.preprocess_button = QPushButton("Create preprocessed copies")
        self.analyze_button.clicked.connect(self._analyze)
        self.preprocess_button.clicked.connect(self._preprocess)
        actions.addWidget(self.analyze_button)
        actions.addWidget(self.preprocess_button)
        actions.addStretch(1)
        layout.addLayout(actions)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setFormat("No photo operation running")
        layout.addWidget(self.progress)

        self.summary = QLabel("No analysis performed yet.")
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)

        self.results = QTableWidget(0, 8)
        self.results.setHorizontalHeaderLabels(
            ["Photo", "Status", "Sharpness", "Luma", "Contrast", "Overlap", "Matches", "Recommendation"]
        )
        self.results.horizontalHeader().setStretchLastSection(True)
        self.results.setMinimumHeight(220)
        layout.addWidget(self.results)

        explanation = QLabel(
            "Interpretation: low sharpness usually indicates motion blur or defocus; abnormal luma and clipping "
            "indicate exposure problems; low contrast can reduce feature detection; low overlap means the current "
            "photograph shares too little stable visual structure with the previous one. A recapture recommendation "
            "means the image should be repeated when possible rather than repaired digitally."
        )
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

    def _path_row(
        self,
        field: QLineEdit,
        callback: Callable[[], None],
        label: str,
        *,
        clear: bool = False,
    ) -> QWidget:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        button = QPushButton(label)
        button.clicked.connect(callback)
        row_layout.addWidget(field, stretch=1)
        row_layout.addWidget(button)
        if clear:
            clear_button = QPushButton("Clear")
            clear_button.clicked.connect(lambda: field.clear())
            row_layout.addWidget(clear_button)
        return row

    def _set_defaults(self) -> None:
        source = self.store.workspace / "references" / "photos"
        output = self.store.workspace / "work" / "photos_preprocessed"
        self.photos_field.setText(str(source) if source.exists() else "")
        self.output_field.setText(str(output))
        self.background_field.clear()

    def _choose_photos(self) -> None:
        selected = QFileDialog.getExistingDirectory(
            self, "Select photogrammetry photograph batch", str(self.store.workspace)
        )
        if selected:
            self.photos_field.setText(selected)

    def _choose_background(self) -> None:
        selected, _ = QFileDialog.getOpenFileName(
            self,
            "Select empty-scene background photograph",
            str(self.store.workspace),
            "Images (*.jpg *.jpeg *.png *.tif *.tiff *.bmp *.webp)",
        )
        if selected:
            self.background_field.setText(selected)
            self.remove_background.setChecked(True)

    def _choose_output(self) -> None:
        selected = QFileDialog.getExistingDirectory(
            self, "Select output directory for derived photographs", str(self.store.workspace)
        )
        if selected:
            self.output_field.setText(selected)

    def _validate_source(self) -> Path | None:
        value = self.photos_field.text().strip()
        if not value:
            QMessageBox.warning(self, "Photographs required", "Select the directory containing the photograph batch.")
            return None
        path = Path(value)
        if not path.is_dir():
            QMessageBox.warning(self, "Invalid photograph directory", f"Directory does not exist:\n{path}")
            return None
        return path

    def _analyze(self) -> None:
        source = self._validate_source()
        if source is None:
            return
        self._mode = "analyze"
        self._start_worker(lambda progress: analyze_photo_batch(source, progress_callback=progress))

    def _preprocess(self) -> None:
        source = self._validate_source()
        if source is None:
            return
        output_text = self.output_field.text().strip()
        if not output_text:
            QMessageBox.warning(self, "Output required", "Select an output directory for derived photographs.")
            return
        background = self.background_field.text().strip() if self.remove_background.isChecked() else None
        if self.remove_background.isChecked() and not background:
            QMessageBox.warning(
                self,
                "Background image required",
                "Static-background removal is enabled. Select a photograph of the empty scene or disable this option.",
            )
            return
        self._mode = "preprocess"
        self._start_worker(
            lambda progress: preprocess_photo_batch(
                source,
                output_text,
                normalize_lighting=self.normalize_lighting.isChecked(),
                improve_contrast=self.improve_contrast.isChecked(),
                background_image=background,
                progress_callback=progress,
            )
        )

    def _start_worker(self, operation: Callable[[ProgressCallback], object]) -> None:
        if self.worker_thread is not None:
            return
        self.analyze_button.setEnabled(False)
        self.preprocess_button.setEnabled(False)
        self.progress.setValue(0)
        self.progress.setFormat("Starting… 0%")
        self.worker_thread = QThread(self)
        self.worker = _PhotoWorker(operation)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.failed.connect(self._on_failed)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.failed.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self._cleanup_worker)
        self.worker_thread.start()

    def _on_progress(self, value: int, message: str) -> None:
        value = max(0, min(100, int(value)))
        self.progress.setValue(value)
        self.progress.setFormat(f"{message} — {value}%")

    def _on_finished(self, result: object) -> None:
        if not isinstance(result, dict):
            self._on_failed("Photo operation returned an invalid result")
            return
        if self._mode == "analyze":
            self._store_analysis(result)
            self._show_analysis(result)
        elif self._mode == "preprocess":
            report_path = Path(str(result.get("report_path", "")))
            if report_path.is_file():
                self.store.register_artifact(
                    "02-photogrammetry",
                    report_path,
                    kind="photo_preprocessing_report",
                    metadata={"operations": result.get("operations", {})},
                )
            self.summary.setText(
                f"Preprocessing complete. {len(result.get('written_images', []))} derived photograph(s) written to "
                f"{result.get('output_directory', '')}. Original files were not modified."
            )
        self.progress.setValue(100)
        self.progress.setFormat("Photo operation complete — 100%")

    def _store_analysis(self, report: dict) -> None:
        reports_dir = self.store.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = reports_dir / f"01-reference-acquisition_photo_quality_{stamp}.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.store.register_artifact(
            "01-reference-acquisition",
            path,
            kind="photo_quality_report",
            metadata={"summary": report.get("summary", {})},
        )
        summary = report.get("summary", {})
        status = "passed" if int(summary.get("recapture_suggested", 0)) == 0 else "warning"
        self.store.add_validation_result(
            "01-reference-acquisition",
            "photo_batch_quality",
            status,
            value=summary,
            expected="no blocking image-quality or overlap problems",
            message=(
                "Photo batch passed automatic quality screening."
                if status == "passed"
                else "Some photographs should be reviewed or repeated before COLMAP."
            ),
        )

    def _show_analysis(self, report: dict) -> None:
        photos = list(report.get("photos", []))
        summary = report.get("summary", {})
        self.summary.setText(
            f"Analyzed {summary.get('photo_count', len(photos))} photograph(s): "
            f"{summary.get('passed', 0)} passed, {summary.get('review', 0)} require review, "
            f"{summary.get('recapture_suggested', 0)} have recapture suggested; "
            f"{summary.get('low_overlap_pairs', 0)} low-overlap pair(s)."
        )
        self.results.setRowCount(len(photos))
        for row, photo in enumerate(photos):
            metrics = photo.get("metrics", {})
            overlap = photo.get("overlap_with_previous") or {}
            reasons = list(photo.get("reasons", []))
            recommendation = "OK" if not reasons else "RECAPTURE / REVIEW: " + ", ".join(reasons)
            values = [
                str(photo.get("path", "")),
                str(photo.get("status", "")),
                self._number(metrics.get("sharpness_laplacian_variance")),
                self._number(metrics.get("mean_luma")),
                self._number(metrics.get("contrast_stddev")),
                self._number(overlap.get("overlap_score")),
                str(overlap.get("matches", "")),
                recommendation,
            ]
            for column, value in enumerate(values):
                self.results.setItem(row, column, QTableWidgetItem(value))
        self.results.resizeColumnsToContents()

    @staticmethod
    def _number(value: object) -> str:
        if value is None:
            return ""
        try:
            return f"{float(value):.3f}"
        except (TypeError, ValueError):
            return str(value)

    def _on_failed(self, message: str) -> None:
        self.progress.setFormat("Photo operation failed")
        QMessageBox.critical(self, "Photo operation failed", message)

    def _cleanup_worker(self) -> None:
        if self.worker is not None:
            self.worker.deleteLater()
        if self.worker_thread is not None:
            self.worker_thread.deleteLater()
        self.worker = None
        self.worker_thread = None
        self._mode = None
        self.analyze_button.setEnabled(True)
        self.preprocess_button.setEnabled(True)
