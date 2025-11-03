"""
HTML parsing functionality with CSS style extraction
"""

import re
import html as html_parser
from typing import Dict, List, Any, Tuple
from ..utils.validation import validate_html


class HTMLParser:
    """Advanced HTML parser with CSS style extraction"""

    def __init__(self):
        self.styles = {}
        self.prev_element = {}  # Store previous element for line breaks

        # Block-level elements that should have automatic line breaks
        self.block_elements = {
            "div",
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            # "ul",
            # "ol",
            # "li",
            "section",
            "article",
            "header",
            "footer",
            "nav",
            "aside",
            "main",
            "figure",
            "figcaption",
        }

    def parse(self, html_content: str) -> Dict[str, Any]:
        """
        Parse HTML content and extract structure and styles

        Returns:
            Dict with 'elements' and 'styles' keys
        """
        validate_html(html_content)

        # Clean HTML
        cleaned_html = self._clean_html(html_content)

        # Extract CSS styles
        self.styles = self._extract_styles(cleaned_html)

        # Remove style tags from content
        content_html = self._remove_style_tags(cleaned_html)

        # Parse HTML structure
        elements = self._parse_structure(content_html)

        return {"elements": elements, "styles": self.styles}

    def strip_comments(self, html):
        # Remove HTML comments
        html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

        # Remove JS comments within <script>...</script> blocks
        html = re.sub(
            r"(<script[^>]*>)(.*?)(</script>)",
            lambda m: m.group(1)
            + re.sub(r"(?m)//.*?$|/\*.*?\*/", "", m.group(2), flags=re.DOTALL)
            + m.group(3),
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        return html

    def _clean_html(self, html: str) -> str:
        """Clean and normalize HTML content"""
        # Remove <!DOCTYPE html>
        html = html.replace("<!DOCTYPE html>", "")
        html = html.replace("<!doctype html>", "")

        # Remove comments
        # html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
        # Remove js comments
        # html = re.sub(r"(?m)//.*?$|/\*.*?\*/", "", html, flags=re.DOTALL)
        html = self.strip_comments(html)

        # Preserve line breaks by replacing them with markers
        html = re.sub(r"\n+", "", html)
        # html = html.replace("-", "—")  # Replace - with —

        # Remove title
        html = re.sub(
            r"<title[^>]*>.*?</title>",
            "",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove multiple spaces but preserve single spaces
        # html = re.sub(r"[ \t]+", " ", html)

        # Remove multiple spaces and newlines
        html = re.sub(r"\s+", " ", html)

        # Ensure proper tag formatting
        html = html.replace("<br>", "<br/>").replace("<hr>", "<hr/>")

        # Handle self-closing tags
        html = re.sub(r"<(img|br|hr|input)([^>]*)(?<!/)>", r"<\1\2/>", html)

        # Decode HTML entities
        html = html_parser.unescape(html)
        return html.strip()

    def _extract_styles(self, html: str) -> Dict[str, Dict]:
        """Extract CSS styles from style tags and inline styles"""
        styles = {}

        # Extract from style tags
        style_matches = re.findall(
            r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE
        )
        for style_content in style_matches:
            styles.update(self._parse_css_rules(style_content))

        return styles

    def _parse_css_rules(self, css_content: str) -> Dict[str, Dict]:
        """Parse CSS rules into a dictionary"""
        styles = {}

        # Remove comments
        css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)

        # Parse rules
        rules = re.findall(r"([^{]+)\{([^}]+)\}", css_content)

        for selector, properties in rules:
            selector = selector.strip()
            style_dict = self._parse_css_properties(properties)

            if selector:
                styles[selector] = style_dict

        return styles

    def _parse_css_properties(self, css_properties: str) -> Dict[str, str]:
        """Parse CSS properties string into dictionary"""
        properties = {}
        declarations = [d.strip() for d in css_properties.split(";") if d.strip()]

        for declaration in declarations:
            if ":" in declaration:
                prop, value = declaration.split(":", 1)
                prop = prop.strip().lower()
                value = value.strip()
                properties[prop] = value

        return properties

    def _remove_style_tags(self, html: str) -> str:
        """Remove style tags from HTML"""
        return re.sub(
            r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE
        )

    def _parse_structure(self, html: str) -> List[Dict]:
        """Parse HTML structure into a tree of elements and with automatic line breaks for block elements"""
        tokens = self._tokenize_html(html)
        elements, _ = self._build_element_tree(tokens)
        return elements

    def _tokenize_html(self, html: str) -> List[Dict]:
        """Tokenize HTML into tags and text while preserving line breaks"""
        tokens = []
        pos = 0

        # First, normalize line breaks and preserve them with markers
        html = self._preserve_line_breaks(html)

        while pos < len(html):
            # Find next tag
            tag_match = re.search(r"</?(\w+)([^>]*)>", html[pos:])

            if not tag_match:
                # Add remaining text
                if pos < len(html):
                    text_content = html[pos:]
                    text_content = self._restore_line_breaks(text_content)
                    if text_content.strip():
                        tokens.append({"type": "text", "content": text_content})
                break

            tag_start = tag_match.start() + pos
            tag_end = tag_match.end() + pos

            # Add text before tag
            if tag_start > pos:
                text_content = html[pos:tag_start]
                text_content = self._restore_line_breaks(text_content)
                if text_content.strip():
                    tokens.append({"type": "text", "content": text_content})

            # Extract tag information
            full_tag = html[tag_start:tag_end]
            tag_name = tag_match.group(1).lower()
            attributes = self._parse_attributes(tag_match.group(2))
            is_closing = full_tag.startswith("</")
            is_self_closing = full_tag.endswith("/>")

            current_element = {
                "type": "tag",
                "name": tag_name,
                "full_tag": full_tag,
                "attributes": attributes,
                "is_closing": is_closing,
                "is_self_closing": is_self_closing,
            }

            # Add automatic line break logic
            self._add_auto_line_break(tokens, current_element)

            tokens.append(current_element)
            self.prev_element = current_element
            pos = tag_end

        return tokens

    def _add_auto_line_break(self, tokens: List[Dict], current_element: Dict):
        """Automatically add line breaks between block elements when needed"""
        if not self.prev_element:
            return

        prev_name = self.prev_element.get("name", "")
        current_name = current_element.get("name", "")
        prev_is_closing = self.prev_element.get("is_closing", False)
        current_is_closing = current_element.get("is_closing", False)

        # Case 1: Closing block element followed by another block element
        if (
            prev_is_closing
            and prev_name in self.block_elements
            and not current_is_closing
            and current_name in self.block_elements
        ):
            # Add line break between block elements
            line_break = {
                "type": "tag",
                "name": "br",
                "full_tag": "<br/>",
                "attributes": {},
                "is_closing": False,
                "is_self_closing": True,
            }
            tokens.append(line_break)
            self.prev_element = line_break

        # Case 2: Closing block element followed by text (content within same block)
        elif (
            prev_is_closing
            and prev_name in self.block_elements
            and current_element["type"] == "text"
            and current_element.get("content", "").strip()
        ):
            # This handles content that should be on new lines within the same block
            line_break = {
                "type": "tag",
                "name": "br",
                "full_tag": "<br/>",
                "attributes": {},
                "is_closing": False,
                "is_self_closing": True,
            }
            tokens.append(line_break)
            self.prev_element = line_break

        # Case 3: Text followed by opening block element
        elif (
            self.prev_element["type"] == "text"
            and not current_is_closing
            and current_name in self.block_elements
        ):
            # Add line break before new block element
            line_break = {
                "type": "tag",
                "name": "br",
                "full_tag": "<br/>",
                "attributes": {},
                "is_closing": False,
                "is_self_closing": True,
            }
            tokens.append(line_break)
            self.prev_element = line_break

    def _preserve_line_breaks(self, html: str) -> str:
        """Preserve line breaks by converting them to markers"""
        # Replace line breaks with a unique marker that won't interfere with HTML parsing
        html = html.replace("\r\n", "\n")  # Normalize Windows line endings
        html = html.replace("\r", "\n")  # Normalize Mac line endings

        # Use a unique marker that won't appear in normal text
        html = html.replace("\n", "⏎")  # Using a special character as marker
        return html

    def _restore_line_breaks(self, text: str) -> str:
        """Restore line breaks from markers"""
        return text.replace("⏎", "\n")

    def _parse_attributes(self, attribute_string: str) -> Dict[str, str]:
        """Parse HTML attributes string into dictionary"""
        attributes = {}

        # Find all attribute=value pairs
        pattern = r'(\w+)\s*=\s*["\']([^"\']*)["\']'
        matches = re.findall(pattern, attribute_string)

        for key, value in matches:
            attributes[key.lower()] = value

        # Also look for boolean attributes
        boolean_attrs = re.findall(r"(\w+)(?=\s+|>)", attribute_string)
        for attr in boolean_attrs:
            if attr.lower() not in attributes:
                attributes[attr.lower()] = "true"

        return attributes

    def _add_multiple_line_breaks(self, count: int):
        """Add multiple line breaks"""
        if count <= 0:
            return

        for i in range(count):
            self._add_line_break()

    def _build_element_tree(
        self, tokens: List[Dict], start_index: int = 0
    ) -> Tuple[List[Dict], int]:
        """Build a tree structure from tokens"""
        elements = []
        i = start_index

        while i < len(tokens):
            token = tokens[i]

            if token["type"] == "text":
                elements.append({"type": "text", "content": token["content"]})
                i += 1

            elif token["type"] == "tag":
                if token["is_closing"]:
                    # Return when we hit a closing tag
                    return elements, i + 1

                elif token["is_self_closing"]:
                    # Self-closing tag - add as element with no children
                    elements.append(
                        {
                            "type": "element",
                            "tag": token["name"],
                            "attributes": token["attributes"],
                            "children": [],
                        }
                    )
                    i += 1

                else:
                    # Opening tag - recursively process children
                    child_elements, next_index = self._build_element_tree(tokens, i + 1)

                    elements.append(
                        {
                            "type": "element",
                            "tag": token["name"],
                            "attributes": token["attributes"],
                            "children": child_elements,
                        }
                    )

                    i = next_index

            else:
                i += 1

        return elements, i
