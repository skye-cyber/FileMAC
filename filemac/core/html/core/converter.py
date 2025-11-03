"""
Main converter class that orchestrates the HTML to DOCX conversion
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
import os
from typing import Dict, Any, List

from .html_parser import HTMLParser
from .style_manager import StyleManager
from ..utils.validation import validate_html, validate_file_path


class AdvancedCVConverter:
    """Main converter class that coordinates HTML parsing and DOCX generation"""

    def __init__(self, default_font: str = "Calibri", default_size: int = 11):
        self.doc = None
        self.default_font = default_font
        self.default_size = default_size
        self.html_parser = HTMLParser()
        self.style_manager = StyleManager(default_font, default_size)

        # Conversion state
        self.current_paragraph = None
        self.current_style = {}
        self.tag_stack = []

    def convert(self, html_content: str, output_path: str) -> Document:
        """
        Convert HTML content to DOCX document

        Args:
            html_content: HTML string to convert
            output_path: Path for output DOCX file

        Returns:
            Document: The created Word document
        """
        # Validate inputs
        validate_html(html_content)
        validate_file_path(output_path, "output")

        # Initialize document
        self.doc = Document()
        self.style_manager.setup_document_styles(self.doc)

        # Parse HTML and extract styles
        parsed_data = self.html_parser.parse(html_content)

        # Convert to DOCX
        self._convert_elements(parsed_data["elements"], parsed_data["styles"])

        # Save document
        self.doc.save(output_path)
        return self.doc

    def convert_file(self, html_file_path: str, output_path: str) -> Document:
        """
        Convert HTML file to DOCX document

        Args:
            html_file_path: Path to HTML file
            output_path: Path for output DOCX file

        Returns:
            Document: The created Word document
        """
        validate_file_path(html_file_path, "input")

        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        return self.convert(html_content, output_path)

    def _convert_elements(self, elements: List[Dict], styles: Dict):
        """Convert parsed HTML elements to DOCX format"""
        for element in elements:
            self._convert_element(element, styles)

    def _convert_element(self, element: Dict, styles: Dict):
        """Convert a single HTML element to DOCX"""
        element_type = element["type"]
        tag_name = element.get("tag", "").lower()

        if element_type == "text":
            self._add_text_element(element, styles)
        elif element_type == "element":
            self._handle_html_element(element, styles)

    def _handle_html_element(self, element: Dict, styles: Dict):
        """Handle HTML element based on tag type"""
        tag_name = element["tag"].lower()

        # Push to stack for styling
        self.tag_stack.append(element)

        try:
            if tag_name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                self._add_heading(element, styles)
            elif tag_name == "p":
                self._add_paragraph(element, styles)
            elif tag_name == "div":
                self._add_div(element, styles)
            elif tag_name == "span":
                self._add_span(element, styles)
            elif tag_name == "br":
                self._add_line_break()
            elif tag_name == "hr":
                self._add_horizontal_rule()
            elif tag_name == "ul":
                self._start_list(element, styles)
            elif tag_name == "ol":
                self._start_numbered_list(element, styles)
            elif tag_name == "li":
                self._add_list_item(element, styles)
            elif tag_name == "strong" or tag_name == "b":
                self._add_bold_text(element, styles)
            elif tag_name == "em" or tag_name == "i":
                self._add_italic_text(element, styles)
            elif tag_name == "u":
                self._add_underline_text(element, styles)
            elif tag_name == "pre":
                self._add_preformatted_text(element, styles)
            else:
                # Process children for unknown tags
                self._convert_elements(element.get("children", []), styles)

        finally:
            # Always pop from stack
            if self.tag_stack and self.tag_stack[-1] == element:
                self.tag_stack.pop()

    def _add_preformatted_text(self, element: Dict, styles: Dict):
        """Add preformatted text with preserved whitespace"""
        if not self.current_paragraph:
            self.current_paragraph = self.doc.add_paragraph()

        # Process all text content in pre tag
        self._process_preformatted_content(element.get("children", []), styles)
        self.current_paragraph = None

    def _process_preformatted_content(self, elements: List[Dict], styles: Dict):
        """Process content for pre tags with preserved formatting"""
        for element in elements:
            if element["type"] == "text":
                text = element.get("content", "")
                if text:
                    # Preserve all whitespace in pre tags
                    run = self.current_paragraph.add_run(text)
                    self.style_manager.apply_styles_to_run(run, self.tag_stack, styles)
            elif element["type"] == "element":
                self._handle_html_element(element, styles)

    def _add_text_element(self, element: Dict, styles: Dict):
        """Add text element with proper styling and line breaks"""
        if not self.current_paragraph:
            self.current_paragraph = self.doc.add_paragraph()

        text = element.get("content", "")

        # Handle text with line breaks
        if "\n" in text:
            lines = text.split("\n")
            for i, line in enumerate(lines):
                if line.strip():  # Only add non-empty lines
                    run = self.current_paragraph.add_run(line.strip())
                    self.style_manager.apply_styles_to_run(run, self.tag_stack, styles)

                # Add line break except for the last line
                if i < len(lines) - 1 and line.strip():
                    self._add_line_break()
        else:
            # Single line of text
            if text.strip():
                run = self.current_paragraph.add_run(text.strip())
                self.style_manager.apply_styles_to_run(run, self.tag_stack, styles)

    def _add_heading(self, element: Dict, styles: Dict):
        """Add heading with appropriate level"""
        level = element["tag"][1]  # Extract number from h1, h2, etc.
        self.current_paragraph = self.doc.add_paragraph()

        # Apply heading style
        self.style_manager.apply_heading_style(
            self.current_paragraph, level, element, styles
        )

        # Process children
        self._convert_elements(element.get("children", []), styles)

        self.current_paragraph = None

    def _add_paragraph(self, element: Dict, styles: Dict):
        """Add paragraph"""
        self.current_paragraph = self.doc.add_paragraph()
        self.style_manager.apply_paragraph_style(
            self.current_paragraph, element, styles
        )

        # Process children
        self._convert_elements(element.get("children", []), styles)

        self.current_paragraph = None

    def _add_div(self, element: Dict, styles: Dict):
        """Add div element - ensure new paragraph for block-level elements"""
        # For divs that contain block-level content, start a new paragraph
        has_block_content = any(
            child.get("tag") in ["p", "div", "h1", "h2", "h3", "ul", "ol"]
            for child in element.get("children", [])
            if child["type"] == "element"
        )

        if has_block_content and self.current_paragraph:
            self.current_paragraph = None

        self._convert_elements(element.get("children", []), styles)

    def _add_span(self, element: Dict, styles: Dict):
        """Add span with inline styling"""
        self._convert_elements(element.get("children", []), styles)

    def _add_line_break(self):
        """Add line break"""
        if self.current_paragraph:
            self.current_paragraph.add_run().add_break(WD_BREAK.LINE)
        else:
            self.doc.add_paragraph()

    def _add_horizontal_rule(self):
        """Add horizontal rule"""
        self.doc.add_paragraph().add_run("_" * 50)

    def _start_list(self, element: Dict, styles: Dict):
        """Start unordered list"""
        self._convert_elements(element.get("children", []), styles)

    def _start_numbered_list(self, element: Dict, styles: Dict):
        """Start ordered list"""
        self._convert_elements(element.get("children", []), styles)

    def _add_list_item(self, element: Dict, styles: Dict):
        """Add list item"""
        self.current_paragraph = self.doc.add_paragraph(style="List Bullet")
        self._convert_elements(element.get("children", []), styles)
        self.current_paragraph = None

    def _add_bold_text(self, element: Dict, styles: Dict):
        """Add bold text"""
        self._convert_elements(element.get("children", []), styles)

    def _add_italic_text(self, element: Dict, styles: Dict):
        """Add italic text"""
        self._convert_elements(element.get("children", []), styles)

    def _add_underline_text(self, element: Dict, styles: Dict):
        """Add underline text"""
        self._convert_elements(element.get("children", []), styles)
