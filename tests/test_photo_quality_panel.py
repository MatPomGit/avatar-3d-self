import os
from pathlib import Path

import pytest


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from avatar_studio.enhanced_main_window import EnhancedMainWindow  # noqa: E402
from avatar_studio.store import ProjectStore  # noqa: E402


def test_photo_quality_panel_is_embedded_and_contextual(tmp_path: Path) -> None:
    app = QApplication.instance() or QApplication([])
    window = EnhancedMainWindow(ProjectStore(tmp_path))

    assert window.photo_quality_panel is not None
    assert window.photo_quality_panel.photos_field is not None
    assert window.photo_quality_panel.background_field is not None
    assert window.photo_quality_panel.output_field is not None
    assert window.photo_quality_panel.analyze_button.text() == "Analyze batch"
    assert window.photo_quality_panel.preprocess_button.text() == "Create preprocessed copies"

    window.stage_list.setCurrentRow(0)
    app.processEvents()
    assert window.photo_quality_panel.isVisibleTo(window)

    window.stage_list.setCurrentRow(2)
    app.processEvents()
    assert not window.photo_quality_panel.isVisibleTo(window)

    window.close()
    app.processEvents()
