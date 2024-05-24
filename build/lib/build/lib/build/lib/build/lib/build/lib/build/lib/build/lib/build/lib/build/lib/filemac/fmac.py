#!/usr/bin/env python3.11.7
# multimedia_cli/main.py
import argparse
import logging
import logging.handlers
import sys

from . import handle_warnings
from .AudioExtractor import ExtractAudio
from .colors import CYAN, DYELLOW, RESET
from .converter import (AudioConverter, FileSynthesis, ImageConverter,
                        MakeConversion, Scanner, VideoConverter)
from .formats import (SUPPORTED_AUDIO_FORMATS_SHOW, SUPPORTED_DOC_FORMATS,
                      SUPPORTED_IMAGE_FORMATS_SHOW,
                      SUPPORTED_VIDEO_FORMATS_SHOW)
from .image_op import Compress_Size
from .OCRTextExtractor import ExtractText
from .Simple_v_Analyzer import SA

# from .formats import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS
handle_warnings
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


class Eval:

    def __init__(self, file, outf):
        self.file = file
        self.outf = outf

    def document_eval(self):
        ls = ["docx", "doc"]
        sheetls = ["xlsx", "xls"]
        try:
            conv = MakeConversion(self.file)
            if self.file.lower().endswith(tuple(sheetls)):
                if self.outf.lower() == "csv":
                    conv.convert_xlsx_to_csv()
                elif self.outf.lower() == "txt":
                    conv.convert_xls_to_text()
                elif self.outf.lower() == "doc" or self.outf == "docx":
                    conv.convert_xls_to_word()
                elif self.outf.lower() == "db":
                    conv.convert_xlsx_to_database()

            elif self.file.lower().endswith(tuple(ls)):
                if self.outf.lower() == "txt":
                    conv.word_to_txt()
                elif self.outf.lower() == "pdf":
                    conv.word_to_pdf()
                elif self.outf.lower() == "pptx":
                    conv.word_to_pptx()
                elif self.outf.lower() == "audio" or self.outf.lower() == "ogg":
                    conv = FileSynthesis(self.file)
                    conv.audiofy()

            elif self.file.endswith('txt'):
                if self.outf.lower() == "pdf":
                    conv.txt_to_pdf()
                elif self.outf.lower() == "doc" or self.outf == "docx" or self.outf == "word":
                    conv.text_to_word()
                elif self.outf.lower() == "audio" or self.outf.lower() == "ogg":
                    conv = FileSynthesis(self.file)
                    conv.audiofy()

            elif self.file.lower().endswith('ppt') or self.file.lower().endswith('pptx'):
                if self.outf.lower() == "doc" or self.outf.lower() == "docx" or self.outf == "word":
                    conv.ppt_to_word()

            elif self.file.lower().endswith('pdf'):
                if self.outf.lower() == "doc" or self.outf.lower() == "docx" or self.outf == "word":
                    conv.pdf_to_word()
                elif self.outf.lower() == "txt":
                    conv.pdf_to_txt()
                elif self.outf.lower() == "audio" or self.outf.lower() == "ogg":
                    conv = FileSynthesis(self.file)
                    conv.audiofy()

            else:
                print(f"{DYELLOW}Unsupported Conversion type{RESET}")
        except Exception as e:
            logger.error(e)


def main():
    parser = argparse.ArgumentParser(
        description="Multimedia Element Operations")

    parser.add_argument(
        "--convert_doc", help=f"Converter document file(s) to different format ie pdf_to_docx.\
       example {DYELLOW}filemac --convert_doc example.docx -t pdf{RESET}")

    parser.add_argument(
        "--convert_audio", help=f"Convert audio file(s) to and from different format ie mp3 to wav\
        example {DYELLOW}filemac --convert_audio example.mp3 -t wav{RESET}")

    parser.add_argument(
        "--convert_video", help=f"Convert video file(s) to and from different format ie mp4 to mkv.\
        example {DYELLOW}filemac --convert_video example.mp4 -t mkv{RESET}")

    parser.add_argument(
        "--convert_image", help=f"Convert image file(s) to and from different format ie png to jpg.\
        example {DYELLOW}filemac --convert_image example.jpg -t png{RESET}")

    parser.add_argument(

        "--convert_doc2image", help=f"Convert documents to images ie png to jpg.\
        example {DYELLOW}filemac --convert_doc2image example.pdf -t png{RESET}")

    parser.add_argument("-xA", "--extract_audio",
                        help=f"Extract audio from a video.\
                        example {DYELLOW}filemac -xA example.mp4 {RESET}")

    parser.add_argument(
        "-Av", "--Analyze_video", help=f"Analyze a given video.\
        example {DYELLOW}filemac --analyze_video example.mp4 {RESET}")

    parser.add_argument("-t", "--target_format",
                        help="Target format for conversion (optional)")

    parser.add_argument(
        "--resize_image", help=f"change size of an image compress/decompress \
        example {DYELLOW}filemac --resize_image example.png -t_size 2mb -t png {RESET}")

    parser.add_argument("-t_size", help="used in combination with resize_image \
                        to specify target image size")

    parser.add_argument(
        "-S", "--scan", help=f"Scan pdf file and extract text\
                        example {DYELLOW}filemac --scan example.pdf {RESET}")

    parser.add_argument(

        "-doc2L", "--doc_long_image", help=f"Convert pdf file to long image\
                        example {DYELLOW}filemac --doc_long_image example.pdf {RESET}")

    parser.add_argument(
        "-SA", "--scanAsImg", help=f"Scan pdf file and extract text\
                        example {DYELLOW}filemac --scanAsImg example.pdf {RESET}")

    parser.add_argument(
        "-SALI", "--scanAsLong_Image", help=f"Scan {CYAN}[doc, docx, pdf]\
        {RESET} file and extract text,-> very effective\
                    example {DYELLOW}filemac --scanAsImg example.pdf {RESET}")

    parser.add_argument("--OCR", help=f"Extract text from an image.\
        example {DYELLOW}filemac --OCR image.png{RESET}")

    args = parser.parse_args()


# Call function to handle document conversion inputs before begining conversion
    if args.convert_doc == 'help':
        print(SUPPORTED_DOC_FORMATS)
        sys.exit(1)
    if args.convert_doc:
        ev = Eval(args.convert_doc, args.target_format)
        ev.document_eval()


# Call function to handle video conversion inputs before begining conversion
    elif args.convert_video:
        if args.convert_video == 'help':
            print(SUPPORTED_VIDEO_FORMATS_SHOW)
            sys.exit(1)
        ev = VideoConverter(args.convert_video, args.target_format)
        ev.CONVERT_VIDEO()
# Call function to handle image conversion inputs before begining conversion

    elif args.convert_image:
        if args.convert_image == 'help':
            print(SUPPORTED_IMAGE_FORMATS_SHOW)
            sys.exit(1)
        conv = ImageConverter(args.convert_image, args.target_format)
        conv.convert_image()

# Handle image resizing
    elif args.resize_image:
        res = Compress_Size(args.resize_image)
        res.resize_image(args.t_size)

# Handle documents to images conversion
    elif args.convert_doc2image:
        conv = MakeConversion(args.convert_doc2image)
        conv.doc2image(args.target_format)

# Call function to handle audio conversion inputs before begining conversion
    elif args.convert_audio:
        if args.convert_audio == 'help':
            print(SUPPORTED_AUDIO_FORMATS_SHOW)
            sys.exit(1)
        ev = AudioConverter(args.convert_audio, args.target_format)
        ev.pydub_conv()


# Call module to evaluate audio files before making audio extraction from input video files conversion
    elif args.extract_audio:
        vi = ExtractAudio(args.extract_audio)
        vi.moviepyextract()

# Call module to scan the input and extract text
    elif args.scan:
        sc = Scanner(args.scan)
        sc.scanPDF()

# Call module to scan the input FILE as image object and extract text
    elif args.scanAsImg:
        sc = Scanner(args.scanAsImg)
        sc.scanAsImgs()

# Call module to scan the input FILE as long image object and extract text
# effective for text intengration(combining)
    elif args.scanAsLong_Image:
        sc = Scanner(args.scanAsLong_Image)
        sc.scanAsLongImg()

# convert document to long image
    elif args.doc_long_image:
        from .longImg import LImage
        conv = LImage(args.doc_long_image)
        conv.preprocess()
# Call module to handle Candidate images for text extraction inputs before begining conversion
    elif args.OCR:
        conv = ExtractText(args.OCR)
        conv.OCR()

    elif args.Analyze_video:
        analyzer = SA(args.Analyze_video)
        analyzer.SimpleAnalyzer()


if __name__ == "__main__":
    main()
