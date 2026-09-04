"""Main-window extension that embeds photogrammetry photo QA controls."""

from __future__ import annotations

from PySide6.QtWidgets import QSplitter

from avatar_studio.main_window import MainWindow
from avatar_studio.photo_quality_panel import PhotoQualityPanel
from avatar_studio.store import ProjectStore


class EnhancedMainWindow(MainWindow):
    """Avatar Studio window with contextual photo QA/preprocessing panel."""

    def __init__(self, store: ProjectStore) -> None:
        self.photo_quality_panel: PhotoQualityPanel | None = None
        super().__init__(store)
        root_layout = self.centralWidget().layout()
        splitter = root_layout.itemAt(1).widget()
        if not isinstance(splitter, QSplitter):
            raise RuntimeError("Avatar Studio main layout does not contain the expected pipeline splitter")
        center = splitter.widget(1)
        center_layout = center.layout()
        self.photo_quality_panel = PhotoQualityPanel(self.store, center)
        center_layout.insertWidget(2, self.photo_quality_panel)
        self._update_current_view()

    def _update_current_view(self) -> None:
        super()._update_current_view()
        if self.photo_quality_panel is None:
            return
        stage_id = self._current_stage_id()
        self.photo_quality_panel.setVisible(
            stage_id in {"01-reference-acquisition", "02-photogrammetry"}
        )

    def _switch_workspace(self) -> None:
        previous_workspace = self.store.workspace
        super()._switch_workspace()
        if self.photo_quality_panel is not None and self.store.workspace != previous_workspace:
            self.photo_quality_panel.set_store(self.store)
            self._update_current_view()
