"""
Style application logic for different CSS properties
"""

from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from typing import Dict
import re

from ..utils.color_utils import ColorConverter


class StyleApplier:
    """Applies CSS styles to DOCX elements"""

    def __init__(self):
        self.color_converter = ColorConverter()

    def apply_text_styles(self, run, styles: Dict[str, str]):
        """Apply text-related styles to a run"""
        for prop, value in styles.items():
            self._apply_text_style(run, prop, value)

    def _apply_text_style(self, run, prop: str, value: str):
        """Apply a single text style property"""
        try:
            if prop == "color":
                color = self.color_converter.parse_color(value)
                if color:
                    run.font.color.rgb = color

            elif prop == "font-size":
                size = self._parse_font_size(value)
                if size:
                    run.font.size = Pt(size)

            elif prop == "font-family":
                run.font.name = value.split(",")[0].strip().strip("\"'")

            elif prop == "font-weight":
                if value in ["bold", "bolder", "700", "800", "900"]:
                    run.font.bold = True
                elif value in ["normal", "lighter", "400"]:
                    run.font.bold = False

            elif prop == "font-style":
                if value == "italic":
                    run.font.italic = True
                elif value == "normal":
                    run.font.italic = False

            elif prop == "text-decoration":
                if "underline" in value:
                    run.font.underline = True
                if "line-through" in value:
                    run.font.strike = True

            elif prop == "text-transform":
                if value == "uppercase":
                    run.text = run.text.upper()
                elif value == "lowercase":
                    run.text = run.text.lower()
                elif value == "capitalize":
                    run.text = run.text.title()

        except Exception:
            pass

    def _parse_font_size(self, size_str: str) -> float:
        """Parse font size to points"""
        try:
            if "px" in size_str:
                return float(size_str.replace("px", "").strip()) * 0.75
            elif "pt" in size_str:
                return float(size_str.replace("pt", "").strip())
            elif "em" in size_str:
                return float(size_str.replace("em", "").strip()) * 11  # Default size
            elif "%" in size_str:
                return (float(size_str.replace("%", "").strip()) / 100) * 11
            else:
                return float(size_str)
        except (ValueError, TypeError):
            return None
