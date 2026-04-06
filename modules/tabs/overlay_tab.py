"""
overlay_tab.py - Overlay position, size, opacity, font, and preview controls
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QSlider,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal


class OverlayTab(QWidget):
    preview_requested = pyqtSignal()

    def __init__(self, config: dict):
        super().__init__()
        ov = config.get("overlay", {})
        pos = ov.get("position", {"x": 0, "y": 0})
        self._build_ui(
            x=pos.get("x", 0),
            y=pos.get("y", 0),
            width=ov.get("width", 320),
            height=ov.get("height", 230),
            opacity_pct=int(round(ov.get("opacity", 0.88) * 100)),
            font_size=ov.get("font_size", 16),
        )

    def _build_ui(self, x, y, width, height, opacity_pct, font_size):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(14)

        # --- Position ---
        left.addWidget(self._section_label("POSITION (pixels)"))
        pos_row = QHBoxLayout()
        pos_row.addWidget(self._dim_label("X"))
        self._x = self._spinbox(x, -9999, 9999)
        pos_row.addWidget(self._x)
        pos_row.addWidget(self._dim_label("Y"))
        self._y = self._spinbox(y, -9999, 9999)
        pos_row.addWidget(self._y)
        self._preview_btn = QPushButton("⊹ Preview on screen")
        self._preview_btn.setStyleSheet(
            "color: #88ccff; background: transparent; border: 1px solid #444; "
            "padding: 5px 10px; font-size: 13px; font-family: Consolas;"
        )
        self._preview_btn.clicked.connect(self.preview_requested.emit)
        pos_row.addWidget(self._preview_btn)
        pos_row.addStretch()
        left.addLayout(pos_row)
        drag_hint = QLabel("Drag the preview window to set position — fields update automatically.")
        drag_hint.setStyleSheet("color: #444; font-size: 11px;")
        left.addWidget(drag_hint)

        # --- Size ---
        left.addWidget(self._section_label("SIZE (pixels)"))
        size_row = QHBoxLayout()
        size_row.addWidget(self._dim_label("W"))
        self._width = self._spinbox(width, 100, 1920)
        size_row.addWidget(self._width)
        size_row.addWidget(self._dim_label("H"))
        self._height = self._spinbox(height, 100, 1080)
        size_row.addWidget(self._height)
        size_row.addStretch()
        left.addLayout(size_row)

        # --- Opacity ---
        self._opacity_label = QLabel(f"OPACITY  {opacity_pct}%")
        self._opacity_label.setStyleSheet("color: #aaa; font-size: 13px;")
        left.addWidget(self._opacity_label)
        self._opacity = QSlider(Qt.Horizontal)
        self._opacity.setRange(10, 100)
        self._opacity.setValue(opacity_pct)
        self._opacity.setStyleSheet(
            "QSlider::groove:horizontal { background: #333; height: 6px; border-radius: 3px; }"
            "QSlider::sub-page:horizontal { background: #ffd700; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #fff; border: 2px solid #ffd700; "
            "width: 14px; height: 14px; margin: -4px 0; border-radius: 7px; }"
        )
        self._opacity.valueChanged.connect(
            lambda v: self._opacity_label.setText(f"OPACITY  {v}%")
        )
        left.addWidget(self._opacity)

        # --- Font size ---
        left.addWidget(self._section_label("FONT SIZE"))
        font_row = QHBoxLayout()
        self._font_size = self._spinbox(font_size, 8, 32)
        font_row.addWidget(self._font_size)
        px_lbl = QLabel("px")
        px_lbl.setStyleSheet("color: #555; font-size: 13px;")
        font_row.addWidget(px_lbl)
        font_row.addStretch()
        left.addLayout(font_row)

        left.addStretch()
        outer.addLayout(left)

        # --- Right: mini preview panel ---
        right = QVBoxLayout()
        right.addWidget(self._section_label("PREVIEW"))
        preview = QFrame()
        preview.setFixedWidth(130)
        preview.setStyleSheet("background: #0d0d0d; border: 1px solid #333;")
        p_layout = QVBoxLayout(preview)
        p_layout.setContentsMargins(8, 8, 8, 8)
        p_layout.setSpacing(2)
        for text, color, bold in [
            ("RUNNING",  "#aaa",    False),
            ("DARK NOW", "#aaa",    False),
            ("Valslayer","#ffd700", True),
            ("NEXT",     "#aaa",    False),
            ("Mabi",     "#88ccff", False),
        ]:
            lbl = QLabel(text)
            size = "13px" if bold else "9px"
            weight = "bold" if bold else "normal"
            lbl.setStyleSheet(f"color: {color}; font-size: {size}; font-weight: {weight};")
            p_layout.addWidget(lbl)
        right.addWidget(preview)
        hint = QLabel("Appearance preview (static)")
        hint.setStyleSheet("color: #444; font-size: 11px;")
        right.addWidget(hint)
        right.addStretch()
        outer.addLayout(right)

    def _spinbox(self, value: int, min_v: int, max_v: int) -> QSpinBox:
        s = QSpinBox()
        s.setRange(min_v, max_v)
        s.setValue(value)
        s.setStyleSheet(
            "background: #1a1a1a; color: #fff; border: 1px solid #333; "
            "padding: 4px 8px; min-width: 60px; font-family: Consolas;"
        )
        return s

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #aaa; font-size: 13px; font-family: Consolas;")
        return lbl

    def _dim_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #555; font-size: 11px; font-family: Consolas;")
        return lbl

    # ------------------------------------------------------------------
    # Data access
    # ------------------------------------------------------------------

    def get_values(self) -> dict:
        """Return overlay config dict matching config.yaml structure.

        Note: opacity is stored as an integer percentage (10-100) in the slider
        and converted to a float here. Precision is capped at 1% increments,
        so 0.885 round-trips as 0.88. This is intentional.
        """
        return {
            "position": {"x": self._x.value(), "y": self._y.value()},
            "width": self._width.value(),
            "height": self._height.value(),
            "opacity": self._opacity.value() / 100.0,
            "font_size": self._font_size.value(),
        }

    def set_position(self, x: int, y: int):
        """Update X/Y spinboxes to reflect a new overlay position.

        Called when the overlay window is dragged. Values outside the spinbox
        range (-9999 to 9999) are silently clamped by Qt to the nearest bound.
        """
        self._x.setValue(x)
        self._y.setValue(y)
