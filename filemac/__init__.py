"""
....////////   ///  ///      /////////   ///////  //////    //////   ////////
   //         ///  ///      //          //    // //  //   //    // ///
  /////////  ///  ///      ////////    //     ///   //   //----//  //
 //         ///  //////// //_____     //           //   //    //   //////////

Converter document file(s) to different format ie pdf_to_docx.
    example filemac --convert_doc example.docx -t pdf

Convert audio file(s) to and from different format ie mp3 to wav
        example filemac --convert_audio example.mp3 -t wav

Convert video file(s) to and from different format ie mp4 to mkv.
        example filemac --convert_video example.mp4 -t mkv

Convert image file(s) to and from different format ie png to jpg.
        example filemac --convert_image example.jpg -t png

Extract audio from a video. example filemac -xA example.mp4

Analyze a given video.
        example filemac --analyze_video example.mp4

hange size of an image compress/decompress
        example filemac --resize_image example.png -t_size 2mb -t png

Scan pdf file and extract text
                        example filemac --scan example.pdf

Convert pdf file to long image
                        example filemac --doc_long_image example.pdf

Scan [doc, docx, pdf]
        file and extract text,-> very effective
                    example filemac --scanAsImg example.pdf

Extract text from an image.
        example filemac --OCR image.png
"""

from audiobot.cli import cli as audiobot

from .core.image.core import (
    GrayscaleConverter,
    ImageCompressor,
    ImageConverter,
    ImageDocxConverter,
    ImagePdfConverter,
)
from .core.pdf.core import PageExtractor, PDF2LongImageConverter, PDFCombine
from .core.recorder import SoundRecorder
from .core.video.core import VideoConverter
from .cli.main import CliInit as main, OperationMapper
from .cli.converter import DocConverter
from voice.VoiceType import VoiceTypeEngine


__version__ = "2.1.0"

__all__ = [
    "audiobot",
    "GrayscaleConverter",
    "ImageConverter",
    "ImageCompressor",
    "PDF2LongImageConverter",
    "ImagePdfConverter",
    "ImageDocxConverter",
    "PDFCombine",
    "PageExtractor",
    "VideoConverter",
    "SoundRecorder",
    "DocConverter",
    "OperationMapper",
    "VoiceTypeEngine",
    "main",
]
