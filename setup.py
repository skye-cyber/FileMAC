"""Build package."""

import os
import subprocess

from setuptools import find_namespace_packages, setup


def sri():
    if os.name == "posix":
        result = subprocess.run(
            ["dpkg", "-l", "poppler-utils"], stdout=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            print("Requirement poppler-utils installing")
            subprocess.run(["sudo", "apt", "install", "poppler-utils"])


def dos_req():
    if os.name == "posix":
        subprocess.run(
            ["pip", "install", "pdf2docx"], stdout=subprocess.PIPE, text=True
        )


DESCRIPTION = "Open source Python CLI toolkit for conversion, manipulation, Analysis of files (All major file operations)"
EXCLUDE_FROM_PACKAGES = ["build", "dist", "test", "src", "*~"]

sri()
dos_req()

setup(
    name="filemac",
    author="wambua",
    author_email="swskye17@gmail.com",
    version=open(os.path.abspath("version.txt")).read(),
    packages=find_namespace_packages(exclude=EXCLUDE_FROM_PACKAGES),
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/filemac/",
    entry_points={
        "console_scripts": [
            "filemac=filemac:main",
            "Filemac=filemac:main",
            "FILEMAC=filemac:main",
        ],
    },
    python_requires=">=3.6",
    install_requires=[
        "argparse",
        "pdfminer.six",
        "python-docx",
        "python-pptx",
        "gTTS",
        "pypandoc",
        "fitz",
        "pydub",
        "Pillow",
        "pandas",
        "opencv-python",
        "pytesseract",
        "PyPDF2",
        "pdf2docx",
        "requests",
        "moviepy",
        "reportlab",
        "numpy",
        "pdf2image",
        "openpyxl",
        "rich",
        "tqdm",
        "ffmpeg-python",
        "librosa",
        "python-magic",
        "matplotlib",
        "numpy",
        "soundfile",
        "SpeechRecognition",
        "colorama",
        "scipy",
        "PyMuPDF",
        "pyautogui",
        "imageio",
        "pynput",
        "pyaudio",
    ],
    include_package_data=True,
    zip_safe=False,
    license="GNU v3",
    keywords=[
        "file-conversion",
        "file-analysis",
        "file-manipulation",
        "ocr",
        "image-conversion",
        "audio_effects",
        "voice_shift",
        "pdf",
        "docx",
    ],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
