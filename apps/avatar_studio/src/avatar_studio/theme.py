"""Visual theme for the Avatar Studio desktop application."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication


STYLESHEET = """
QWidget {
    color: #e7edf7;
    background: #111722;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}
QMainWindow, QDialog { background: #0b1018; }
QMenuBar { background: #111722; border-bottom: 1px solid #293246; padding: 3px; }
QMenuBar::item { padding: 6px 12px; border-radius: 5px; }
QMenuBar::item:selected, QMenu::item:selected { background: #26354e; }
QMenu { background: #151c29; border: 1px solid #344057; padding: 5px; }
QMenu::item { padding: 7px 24px; border-radius: 4px; }
QFrame#appHeader, QFrame#panel {
    background: #151c29;
    border: 1px solid #293246;
    border-radius: 10px;
}
QLabel#productName { color: #f7f9fc; font-size: 22px; font-weight: 700; }
QLabel#productTagline { color: #91a0b7; font-size: 12px; }
QLabel#sectionTitle { color: #aebbd0; font-size: 11px; font-weight: 700; }
QLabel#statusBadge {
    color: #70e1c1;
    background: #153b38;
    border: 1px solid #28645b;
    border-radius: 9px;
    padding: 4px 10px;
    font-weight: 600;
}
QListWidget, QTableWidget, QTextBrowser, QPlainTextEdit, QLineEdit {
    background: #0f1520;
    border: 1px solid #2a3549;
    border-radius: 7px;
    selection-background-color: #315caa;
    selection-color: white;
}
QListWidget { padding: 5px; outline: none; }
QListWidget::item { padding: 9px 8px; margin: 2px; border-radius: 6px; }
QListWidget::item:hover { background: #1b2638; }
QListWidget::item:selected { background: #294c87; }
QHeaderView::section {
    background: #1a2332;
    color: #aebbd0;
    border: 0;
    border-bottom: 1px solid #344057;
    padding: 7px;
    font-weight: 600;
}
QPushButton {
    background: #26354e;
    border: 1px solid #3b4b65;
    border-radius: 7px;
    padding: 8px 13px;
    font-weight: 600;
}
QPushButton:hover { background: #324663; border-color: #52709b; }
QPushButton:pressed { background: #1c293d; }
QPushButton:disabled { color: #68758a; background: #171e2a; border-color: #252e3e; }
QPushButton#primaryButton { background: #3976db; border-color: #5c91e8; color: white; }
QPushButton#primaryButton:hover { background: #4b86e5; }
QPushButton#dangerButton { color: #ffb5bd; }
QProgressBar {
    background: #0e141e;
    border: 1px solid #2d394d;
    border-radius: 6px;
    min-height: 12px;
    text-align: center;
    color: white;
}
QProgressBar::chunk { background: #3d80e7; border-radius: 5px; }
QSplitter::handle { background: transparent; width: 7px; }
QToolTip { color: #f4f7fb; background: #202b3d; border: 1px solid #44536c; padding: 5px; }
"""


def apply_theme(application: QApplication) -> None:
    """Apply the consistent dark studio theme to an application instance."""

    application.setStyle("Fusion")
    application.setStyleSheet(STYLESHEET)
