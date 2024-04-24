'''Build package.'''
import os
import subprocess
from setuptools import find_namespace_packages, setup


def sri():
    if os.name == 'posix':
        result = subprocess.run(
                        ['dpkg', '-l', 'poppler-utils'], stdout=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Requirement poppler-utils installing")
            subprocess.run(['sudo', 'apt', 'install', 'poppler-utils'])

        result = subprocess.run(
                        ['dpkg', '-l', 'speedtest-cli'], stdout=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Requirement speedtest-cli -> installing")
            subprocess.run(['sudo', 'apt', 'install', 'speedtest-cli'])


DESCRIPTION = 'Open source Python CLI toolkit for conversion, manipulation, Analysis'
EXCLUDE_FROM_PACKAGES = ["build", "dist", "test"]

sri()

setup(
    name="filemac",
    author='wambua',
    author_email='wambuamwiky2001@gmail.com',
    version=open("version.txt").read(),
    packages=find_namespace_packages(exclude=EXCLUDE_FROM_PACKAGES),
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    entry_points={
        "console_scripts": [
            "filemac=filemac:main"
        ]},


    python_requires=">=3.6",
    install_requires=[
        'argparse',
        'pdfminer.six',
        'python-docx',
        'python-pptx',
        'gTTS',
        'pypandoc',
        'pydub',
        'requests',
        'Pillow',
        'pandas',
        'opencv-python',
        'pytesseract',
        'PyPDF2',
        'pdf2docx',
        'requests',
        'moviepy',
        'reportlab',
        'numpy',
        'pdf2image'
        ],

    include_package_data=True,
    zip_safe=False,
    license="GPL v3",
    keywords=["file-conversion", "file-analysis", "file-manipulation", "ocr", "image-conversion"],

    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],


)
