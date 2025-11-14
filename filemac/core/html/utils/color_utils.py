"""
Color conversion and parsing utilities
"""

import re
from docx.shared import RGBColor
from typing import Optional


class ColorConverter:
    """Converts various color formats to RGBColor"""

    def __init__(self):
        self.named_colors = {
            "black": RGBColor(0, 0, 0),
            "white": RGBColor(255, 255, 255),
            "red": RGBColor(255, 0, 0),
            "green": RGBColor(0, 128, 0),
            "blue": RGBColor(0, 0, 255),
            "yellow": RGBColor(255, 255, 0),
            "cyan": RGBColor(0, 255, 255),
            "magenta": RGBColor(255, 0, 255),
            "gray": RGBColor(128, 128, 128),
            "grey": RGBColor(128, 128, 128),
            "orange": RGBColor(255, 165, 0),
            "purple": RGBColor(128, 0, 128),
            "brown": RGBColor(165, 42, 42),
            "pink": RGBColor(255, 192, 203),
            "navy": RGBColor(0, 0, 128),
            "teal": RGBColor(0, 128, 128),
            "olive": RGBColor(128, 128, 0),
            "maroon": RGBColor(128, 0, 0),
            "silver": RGBColor(192, 192, 192),
            "lime": RGBColor(0, 255, 0),
            "aqua": RGBColor(0, 255, 255),
            "fuchsia": RGBColor(255, 0, 255),
        }

    def parse_color(self, color_str: str) -> Optional[RGBColor]:
        """
        Parse color string and return RGBColor

        Supports:
        - Hex: #RRGGBB, #RGB
        - RGB: rgb(r, g, b)
        - RGBA: rgba(r, g, b, a) - alpha ignored
        - Named colors: red, blue, etc.
        """
        if not color_str:
            return None

        color_str = color_str.strip().lower()

        # Named colors
        if color_str in self.named_colors:
            return self.named_colors[color_str]

        # Hex colors
        hex_match = re.match(r"#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})", color_str)
        if hex_match:
            r, g, b = [int(x, 16) for x in hex_match.groups()]
            return RGBColor(r, g, b)

        # Short hex colors
        short_hex_match = re.match(r"#([0-9a-f])([0-9a-f])([0-9a-f])", color_str)
        if short_hex_match:
            r, g, b = [int(x * 2, 16) for x in short_hex_match.groups()]
            return RGBColor(r, g, b)

        # RGB colors
        rgb_match = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", color_str)
        if rgb_match:
            r, g, b = [int(x) for x in rgb_match.groups()]
            return RGBColor(r, g, b)

        # RGBA colors (ignore alpha)
        rgba_match = re.match(
            r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*[\d.]+\s*\)", color_str
        )
        if rgba_match:
            r, g, b = [int(x) for x in rgba_match.groups()[:3]]
            return RGBColor(r, g, b)

        # HSL colors (basic conversion)
        hsl_match = re.match(r"hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)", color_str)
        if hsl_match:
            h, s, l = [int(x) for x in hsl_match.groups()]
            return self._hsl_to_rgb(h, s, l)

        return None

    def _hsl_to_rgb(self, h: int, s: int, l: int) -> RGBColor:
        """Convert HSL color to RGB (simplified)"""
        # Normalize values
        h = h % 360
        s = max(0, min(100, s)) / 100
        l = max(0, min(100, l)) / 100

        # Simplified conversion
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        return RGBColor(r, g, b)
