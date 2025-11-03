"""
Style management and application for DOCX elements
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from typing import Dict, List, Any
import re

from ..utils.color_utils import ColorConverter


class StyleManager:
    """Manages styles and applies them to DOCX elements"""

    def __init__(self, default_font: str = "Calibri", default_size: int = 11):
        self.default_font = default_font
        self.default_size = default_size
        self.color_converter = ColorConverter()

        # Style mappings
        self.heading_styles = {
            "1": {"size": 16, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.CENTER},
            "2": {"size": 14, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.LEFT},
            "3": {"size": 12, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.LEFT},
            "4": {"size": 11, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.LEFT},
            "5": {"size": 11, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.LEFT},
            "6": {"size": 11, "bold": True, "alignment": WD_ALIGN_PARAGRAPH.LEFT},
        }

    def setup_document_styles(self, doc: Document):
        """Setup default document styles"""
        # Set normal style
        style = doc.styles["Normal"]
        font = style.font
        font.name = self.default_font
        font.size = Pt(self.default_size)

        # Create custom styles
        self._create_cv_styles(doc)

    def _create_cv_styles(self, doc: Document):
        """Create custom styles for CV"""
        styles_config = {
            "Title": {
                "size": 16,
                "bold": True,
                "alignment": WD_ALIGN_PARAGRAPH.CENTER,
            },
            "Heading": {
                "size": 14,
                "bold": True,
                "alignment": WD_ALIGN_PARAGRAPH.LEFT,
            },
            "Subheading": {
                "size": 12,
                "bold": True,
                "alignment": WD_ALIGN_PARAGRAPH.LEFT,
            },
            "Contact": {
                "size": 10,
                "bold": False,
                "alignment": WD_ALIGN_PARAGRAPH.CENTER,
            },
        }

        for style_name, config in styles_config.items():
            try:
                style = doc.styles.add_style(style_name, 1)  # WD_STYLE_TYPE.PARAGRAPH
                font = style.font
                font.name = self.default_font
                font.size = Pt(config["size"])
                font.bold = config["bold"]
                style.paragraph_format.alignment = config["alignment"]
            except ValueError:
                # Style might already exist
                pass

    def apply_styles_to_run(self, run, tag_stack: List[Dict], styles: Dict):
        """Apply styles to a text run based on tag stack and CSS styles"""
        # Apply basic font
        run.font.name = self.default_font
        run.font.size = Pt(self.default_size)

        # Apply styles from tag stack and CSS
        self._apply_inline_styles(run, tag_stack, styles)
        self._apply_css_styles(run, tag_stack, styles)

    def _apply_inline_styles(self, run, tag_stack: List[Dict], styles: Dict):
        """Apply inline styles from HTML attributes"""
        for element in tag_stack:
            if element.get("type") == "element":
                attributes = element.get("attributes", {})
                style_attr = attributes.get("style", "")

                if style_attr:
                    self._apply_style_attribute(run, style_attr)

    def _apply_css_styles(self, run, tag_stack: List[Dict], styles: Dict):
        """Apply CSS styles from style definitions"""
        for element in tag_stack:
            if element.get("type") == "element":
                tag_name = element.get("tag", "")
                attributes = element.get("attributes", {})

                # Check for class-based styles
                class_attr = attributes.get("class", "")
                if class_attr:
                    for class_name in class_attr.split():
                        css_selector = f".{class_name}"
                        if css_selector in styles:
                            self._apply_css_properties(run, styles[css_selector])

                # Check for tag-based styles
                tag_selector = tag_name
                if tag_selector in styles:
                    self._apply_css_properties(run, styles[tag_selector])

    def _apply_style_attribute(self, run, style_attr: str):
        """Apply style attribute to run"""
        properties = self._parse_style_attribute(style_attr)
        self._apply_css_properties(run, properties)

    def _parse_style_attribute(self, style_attr: str) -> Dict[str, str]:
        """Parse style attribute string into properties dictionary"""
        properties = {}
        declarations = [d.strip() for d in style_attr.split(";") if d.strip()]

        for declaration in declarations:
            if ":" in declaration:
                prop, value = declaration.split(":", 1)
                properties[prop.strip().lower()] = value.strip()

        return properties

    def _apply_css_properties(self, run, properties: Dict[str, str]):
        """Apply CSS properties to a run"""
        for prop, value in properties.items():
            try:
                if prop == "font-weight":
                    if value in ["bold", "bolder", "700", "800", "900"]:
                        run.font.bold = True

                elif prop == "font-style":
                    if value == "italic":
                        run.font.italic = True

                elif prop == "text-decoration":
                    if "underline" in value:
                        run.font.underline = True

                elif prop == "color":
                    color = self.color_converter.parse_color(value)
                    if color:
                        run.font.color.rgb = color

                elif prop == "font-size":
                    size = self._parse_font_size(value)
                    if size:
                        run.font.size = Pt(size)

                elif prop == "font-family":
                    run.font.name = value.split(",")[0].strip().strip("\"'")

                elif prop == "background-color":
                    # Word doesn't directly support background color for text runs
                    # This would require more complex handling with shading
                    pass

            except Exception:
                # Continue with other properties if one fails
                continue

    def _parse_font_size(self, size_str: str) -> float:
        """Parse font size string to points"""
        try:
            # Handle pixel values (approximate conversion: 1px ≈ 0.75pt)
            if "px" in size_str:
                return float(size_str.replace("px", "").strip()) * 0.75

            # Handle point values
            elif "pt" in size_str:
                return float(size_str.replace("pt", "").strip())

            # Handle em values (approximate)
            elif "em" in size_str:
                return float(size_str.replace("em", "").strip()) * self.default_size

            # Handle percentage
            elif "%" in size_str:
                return (
                    float(size_str.replace("%", "").strip()) / 100
                ) * self.default_size

            # Handle named sizes
            elif size_str in ["xx-small", "x-small", "small", "medium"]:
                return self.default_size
            elif size_str == "large":
                return self.default_size * 1.2
            elif size_str == "x-large":
                return self.default_size * 1.5
            elif size_str == "xx-large":
                return self.default_size * 2

            # Assume points if no unit
            else:
                return float(size_str)

        except (ValueError, TypeError):
            return None

    def apply_heading_style(self, paragraph, level: str, element: Dict, styles: Dict):
        """Apply heading style to paragraph"""
        # Apply basic heading style
        if level in self.heading_styles:
            config = self.heading_styles[level]
            paragraph.style = self._get_heading_style_name(level)

        # Apply additional CSS styles
        self._apply_paragraph_css_styles(paragraph, element, styles)

    def apply_paragraph_style(self, paragraph, element: Dict, styles: Dict):
        """Apply styles to paragraph"""
        self._apply_paragraph_css_styles(paragraph, element, styles)

    def _apply_paragraph_css_styles(self, paragraph, element: Dict, styles: Dict):
        """Apply CSS styles to paragraph"""
        attributes = element.get("attributes", {})

        # Check for inline styles
        style_attr = attributes.get("style", "")
        if style_attr:
            properties = self._parse_style_attribute(style_attr)
            self._apply_paragraph_css_properties(paragraph, properties)

        # Check for class-based styles
        class_attr = attributes.get("class", "")
        if class_attr:
            for class_name in class_attr.split():
                css_selector = f".{class_name}"
                if css_selector in styles:
                    self._apply_paragraph_css_properties(
                        paragraph, styles[css_selector]
                    )

    def _apply_paragraph_css_properties(self, paragraph, properties: Dict[str, str]):
        """Apply CSS properties to paragraph"""
        for prop, value in properties.items():
            try:
                if prop == "text-align":
                    if value == "center":
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif value == "right":
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    elif value == "justify":
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    else:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

                elif prop == "margin" or prop == "margin-top":
                    # Convert margin to spacing
                    margin = self._parse_size_value(value)
                    if margin:
                        paragraph.paragraph_format.space_after = Pt(margin)

                elif prop == "margin-bottom":
                    margin = self._parse_size_value(value)
                    if margin:
                        paragraph.paragraph_format.space_after = Pt(margin)

                elif prop == "line-height":
                    if value == "normal":
                        paragraph.paragraph_format.line_spacing_rule = (
                            WD_LINE_SPACING.SINGLE
                        )
                    else:
                        try:
                            line_height = float(value)
                            paragraph.paragraph_format.line_spacing = line_height
                        except ValueError:
                            pass

            except Exception:
                continue

    def _parse_size_value(self, size_str: str) -> float:
        """Parse size value to points"""
        try:
            if "px" in size_str:
                return float(size_str.replace("px", "").strip()) * 0.75
            elif "pt" in size_str:
                return float(size_str.replace("pt", "").strip())
            elif "em" in size_str:
                return float(size_str.replace("em", "").strip()) * self.default_size
            else:
                return float(size_str)
        except (ValueError, TypeError):
            return None

    def _get_heading_style_name(self, level: str) -> str:
        """Get appropriate style name for heading level"""
        if level == "1":
            return "Title"
        elif level == "2":
            return "Heading"
        elif level == "3":
            return "Subheading"
        else:
            return "Normal"
