"""
Validation utilities for the converter
"""

import os
import re
from pathlib import Path


def validate_html(html_content: str) -> bool:
    """
    Validate HTML content

    Args:
        html_content: HTML string to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If HTML content is invalid
    """
    if not html_content or not isinstance(html_content, str):
        raise ValueError("HTML content must be a non-empty string")

    if len(html_content.strip()) == 0:
        raise ValueError("HTML content cannot be empty or whitespace only")

    # Basic check for HTML tags
    if not re.search(r"<[^>]+>", html_content):
        raise ValueError("HTML content must contain valid HTML tags")

    return True


def validate_file_path(file_path: str, file_type: str = "input") -> bool:
    """
    Validate file path

    Args:
        file_path: Path to validate
        file_type: Type of file ('input' or 'output')

    Returns:
        bool: True if valid

    Raises:
        ValueError: If file path is invalid
        FileNotFoundError: If input file doesn't exist
    """
    if (
        not file_path
        or not isinstance(file_path, str)
        and not isinstance(file_path, Path)
    ):
        raise ValueError(f"{file_type} file path must be a non-empty string")

    if file_type == "input":
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(f"Input path is not a file: {file_path}")

    elif file_type == "output":
        output_dir = os.path.dirname(file_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                raise ValueError(f"Cannot create output directory: {e}")

    # Check file extension
    if not file_path.lower().endswith((".html", ".htm", ".docx")):
        raise ValueError(f"File must have .html, .htm, or .docx extension: {file_path}")

    return True


def validate_css(css_content: str) -> bool:
    """
    Validate CSS content

    Args:
        css_content: CSS string to validate

    Returns:
        bool: True if valid
    """
    if not css_content or not isinstance(css_content, str):
        raise ValueError("CSS content must be a non-empty string")

    return True
