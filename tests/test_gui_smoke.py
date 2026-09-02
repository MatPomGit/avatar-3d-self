import os
from pathlib import Path

import pytest


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from avatar_studio.main_window import MainWindow  # noqa: E402
from avatar_studio.store import ProjectStore  # noqa: E402


def test_main_window_opens_headless(tmp_path: Path) -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow(ProjectStore(tmp_path))
    assert window.stage_list.count() == 21
    assert "Avatar Studio" in window.windowTitle()
    assert window.progress_bar.maximum() == 1000
    assert window.operation_progress.maximum() == 100
    assert window.artifact_preview is not None
    window.close()
    app.processEvents()
