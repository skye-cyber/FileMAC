"""
Custom HTML to DOCX Converter for CVs and Professional Documents
"""

from .core.converter import AdvancedCVConverter
from .core.html_parser import HTMLParser
from .core.style_manager import StyleManager
from .styles.css_parser import CSSParser
from .styles.style_applier import StyleApplier

__version__ = "1.0.0"
__all__ = [
    "AdvancedCVConverter",
    "HTMLParser",
    "StyleManager",
    "CSSParser",
    "StyleApplier",
]
