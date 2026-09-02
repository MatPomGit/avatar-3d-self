"""Lightweight artefact preview widgets for Avatar Studio."""

from __future__ import annotations

import math
from pathlib import Path

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QImageReader, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget


_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}
_MESH_SUFFIXES = {".obj", ".ply", ".stl", ".glb", ".gltf"}


class MeshPreviewWidget(QWidget):
    """Dependency-light, interactive wireframe preview backed by trimesh."""

    MAX_FACES = 3500

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._vertices: list[tuple[float, float, float]] = []
        self._faces: list[tuple[int, int, int]] = []
        self._yaw = math.radians(-25.0)
        self._pitch = math.radians(12.0)
        self._zoom = 0.9
        self._last_mouse: QPoint | None = None
        self.setMinimumHeight(260)
        self.setToolTip("Drag to rotate. Use the mouse wheel to zoom.")

    def clear(self) -> None:
        self._vertices = []
        self._faces = []
        self.update()

    def load_mesh(self, path: str | Path) -> str | None:
        """Load a mesh for preview. Returns a user-facing error string on failure."""

        try:
            import trimesh
        except ImportError:
            self.clear()
            return "3D preview requires the desktop geometry dependency 'trimesh'."

        try:
            scene = trimesh.load(Path(path), force="scene")
            geometries = list(scene.geometry.values())
            if not geometries:
                self.clear()
                return "No mesh geometry was found in this file."
            mesh = trimesh.util.concatenate(geometries)
            vertices = mesh.vertices
            faces = mesh.faces
            if len(vertices) == 0 or len(faces) == 0:
                self.clear()
                return "The mesh has no drawable triangles."

            center = vertices.mean(axis=0)
            normalized = vertices - center
            extent = float(abs(normalized).max())
            if extent <= 0:
                extent = 1.0
            normalized = normalized / extent
            self._vertices = [tuple(float(v) for v in row[:3]) for row in normalized]

            step = max(1, math.ceil(len(faces) / self.MAX_FACES))
            sampled = faces[::step]
            self._faces = [tuple(int(i) for i in row[:3]) for row in sampled]
            self._yaw = math.radians(-25.0)
            self._pitch = math.radians(12.0)
            self._zoom = 0.9
            self.update()
            return None
        except Exception as exc:
            self.clear()
            return f"3D preview failed: {exc}"

    def mousePressEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        if event.button() == Qt.LeftButton:
            self._last_mouse = event.position().toPoint()

    def mouseMoveEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        if self._last_mouse is None or not (event.buttons() & Qt.LeftButton):
            return
        point = event.position().toPoint()
        delta = point - self._last_mouse
        self._last_mouse = point
        self._yaw += delta.x() * 0.01
        self._pitch = max(-1.45, min(1.45, self._pitch + delta.y() * 0.01))
        self.update()

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        if event.button() == Qt.LeftButton:
            self._last_mouse = None

    def wheelEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1
        self._zoom = max(0.25, min(3.5, self._zoom * factor))
        self.update()

    def _project(self, vertex: tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = vertex
        cy, sy = math.cos(self._yaw), math.sin(self._yaw)
        cp, sp = math.cos(self._pitch), math.sin(self._pitch)
        x1 = cy * x + sy * z
        z1 = -sy * x + cy * z
        y2 = cp * y - sp * z1
        z2 = sp * y + cp * z1
        scale = min(self.width(), self.height()) * 0.42 * self._zoom
        return self.width() / 2 + x1 * scale, self.height() / 2 - y2 * scale, z2

    def paintEvent(self, _event) -> None:  # type: ignore[no-untyped-def]
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.palette().base())
        if not self._vertices or not self._faces:
            painter.setPen(self.palette().text().color())
            painter.drawText(self.rect(), Qt.AlignCenter, "No 3D mesh selected")
            return

        projected = [self._project(vertex) for vertex in self._vertices]
        face_depths = []
        for face in self._faces:
            try:
                depth = sum(projected[index][2] for index in face) / 3.0
            except IndexError:
                continue
            face_depths.append((depth, face))
        face_depths.sort()

        pen = QPen(self.palette().text().color())
        pen.setWidthF(0.65)
        painter.setPen(pen)
        for _depth, face in face_depths:
            points = [projected[index] for index in face]
            for first, second in ((0, 1), (1, 2), (2, 0)):
                painter.drawLine(
                    int(points[first][0]),
                    int(points[first][1]),
                    int(points[second][0]),
                    int(points[second][1]),
                )


class ArtifactPreview(QWidget):
    """Preview images and supported mesh files, with a textual fallback."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        self.image_label = QLabel("No preview")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(260)
        self.image_label.setScaledContents(False)
        self.mesh_preview = MeshPreviewWidget()
        self.message_label = QLabel("Select an artefact to preview it.")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.stack.addWidget(self.message_label)
        self.stack.addWidget(self.image_label)
        self.stack.addWidget(self.mesh_preview)
        layout.addWidget(self.stack)
        self._pixmap: QPixmap | None = None

    def clear(self) -> None:
        self._pixmap = None
        self.mesh_preview.clear()
        self.message_label.setText("Select an artefact to preview it.")
        self.stack.setCurrentWidget(self.message_label)

    def load(self, path: str | Path) -> None:
        artifact = Path(path)
        suffix = artifact.suffix.lower()
        if suffix in _IMAGE_SUFFIXES:
            reader = QImageReader(str(artifact))
            reader.setAutoTransform(True)
            image = reader.read()
            if image.isNull():
                self.message_label.setText(f"Image preview failed: {reader.errorString()}")
                self.stack.setCurrentWidget(self.message_label)
                return
            self._pixmap = QPixmap.fromImage(image)
            self._refresh_image()
            self.stack.setCurrentWidget(self.image_label)
            return
        if suffix in _MESH_SUFFIXES:
            error = self.mesh_preview.load_mesh(artifact)
            if error:
                self.message_label.setText(error)
                self.stack.setCurrentWidget(self.message_label)
            else:
                self.stack.setCurrentWidget(self.mesh_preview)
            return
        self.message_label.setText(
            "Preview is not available for this file type. Technical metadata remains available below."
        )
        self.stack.setCurrentWidget(self.message_label)

    def resizeEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        super().resizeEvent(event)
        self._refresh_image()

    def _refresh_image(self) -> None:
        if self._pixmap is None:
            return
        size = self.image_label.size()
        self.image_label.setPixmap(
            self._pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
