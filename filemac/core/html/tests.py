#!/usr/bin/env python3
"""
Test script for the CV Converter library
"""

import os
import sys

# Add the library to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "cv_converter"))

from filemac.core.html import HTML2Word
from filemac.core.html.examples.templates import Templates


def test_basic_conversion():
    """Test basic conversion"""
    print("Testing basic CV conversion...")

    converter = HTML2Word()
    html_content = Templates.get_basic_template()

    converter.convert(html_content, "test_basic_cv.docx")
    print("✓ Basic CV created: test_basic_cv.docx")


def test_advanced_conversion():
    """Test advanced conversion with styling"""
    print("Testing advanced CV conversion...")

    converter = HTML2Word()
    html_content = Templates.get_advanced_cv()

    converter.convert(html_content, "test_advanced_cv.docx")
    print("✓ Advanced CV created: test_advanced_cv.docx")


def test_file_conversion():
    """Test conversion from HTML file"""
    print("Testing file-based conversion...")

    # Create test HTML file
    with open("test_cv.html", "w", encoding="utf-8") as f:
        f.write(Templates.get_basic_template())

    converter = HTML2Word()
    converter.convert_file("test_cv.html", "test_file_cv.docx")
    print("✓ File-based CV created: test_file_cv.docx")


def main():
    """Run all tests"""
    print("CV Converter Library Test Suite")
    print("=" * 40)

    try:
        test_basic_conversion()
        test_advanced_conversion()
        test_file_conversion()

        print("\n" + "=" * 40)
        print("All tests completed successfully! 🎉")
        print("\nGenerated files:")
        for file in [
            "test_basic_cv.docx",
            "test_advanced_cv.docx",
            "test_file_cv.docx",
        ]:
            if os.path.exists(file):
                print(f"  - {file}")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # main()
    converter = HTML2Word()
    converter.convert_file("/home/skye/Downloads/MWG-CV.html", "test.docx")
