"""
Advanced CSS parsing functionality
"""

import re
from typing import Dict, List


class CSSParser:
    """Advanced CSS parser with support for various CSS features"""

    def __init__(self):
        self.styles = {}

    def parse_css(self, css_content: str) -> Dict[str, Dict]:
        """Parse CSS content into style dictionary"""
        # Remove comments
        css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)

        # Parse rules
        rules = re.findall(r"([^{]+)\{([^}]+)\}", css_content)

        for selector, properties in rules:
            selector = selector.strip()
            style_dict = self._parse_properties(properties)

            if selector:
                self.styles[selector] = style_dict

        return self.styles

    def _parse_properties(self, properties: str) -> Dict[str, str]:
        """Parse CSS properties string"""
        style_dict = {}
        declarations = [d.strip() for d in properties.split(";") if d.strip()]

        for declaration in declarations:
            if ":" in declaration:
                prop, value = declaration.split(":", 1)
                prop = prop.strip().lower()
                value = value.strip()
                style_dict[prop] = value

        return style_dict

    def get_styles_for_element(
        self, tag: str, classes: List[str] = None, element_id: str = None
    ) -> Dict[str, str]:
        """Get combined styles for an element based on tag, classes, and ID"""
        combined_styles = {}

        # Tag styles
        if tag in self.styles:
            combined_styles.update(self.styles[tag])

        # Class styles
        if classes:
            for class_name in classes:
                class_selector = f".{class_name}"
                if class_selector in self.styles:
                    combined_styles.update(self.styles[class_selector])

        # ID styles
        if element_id:
            id_selector = f"#{element_id}"
            if id_selector in self.styles:
                combined_styles.update(self.styles[id_selector])

        return combined_styles
