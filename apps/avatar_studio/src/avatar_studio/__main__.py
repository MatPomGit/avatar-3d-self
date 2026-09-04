"""Command-line and GUI entry point for Avatar Studio."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Avatar Studio desktop pipeline companion")
    parser.add_argument("--workspace", type=Path, help="Local avatar project workspace")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Launch Avatar Studio and return its process exit code."""

    args = _parse_args(argv)
    from PySide6.QtWidgets import QApplication, QFileDialog

    from avatar_studio.enhanced_main_window import EnhancedMainWindow
    from avatar_studio.store import ProjectStore
    from avatar_studio.theme import apply_theme

    application = QApplication(sys.argv[:1])
    application.setApplicationName("Avatar Studio")
    application.setOrganizationName("Avatar Studio")
    apply_theme(application)
    workspace = args.workspace
    if workspace is None:
        selected = QFileDialog.getExistingDirectory(None, "Select or create Avatar Studio workspace")
        if not selected:
            return 0
        workspace = Path(selected)
    store = ProjectStore(workspace)
    window = EnhancedMainWindow(store)
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
