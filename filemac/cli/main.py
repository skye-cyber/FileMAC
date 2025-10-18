#!/usr/bin/env python3
import argparse
import os
import sys
from ..core.document import DocConverter
from ..core.pdf.core import PageExtractor
from ..core.exceptions import FileSystemError, FilemacError
from pathlib import Path
from ..utils.colors import fg, bg, rs

from ..utils.simple import logger

try:
    from audiobot.cli import cli as audiobot_cli
except ImportError:
    pass

_entry_ = PageExtractor._entry_

RESET = rs


def CliInit():
    """Define main functions to create commandline arguments for different operations"""
    parser = argparse.ArgumentParser(
        description="Filemac: A file management tool with audio effects. Supporting wide range of Multimedia Operations",
        add_help=False,
        epilog=f"{fg.BLUE}When using {fg.MAGENTA}-SALI{fg.BLUE} long images have maximum height that can be processed{RESET}",
    )

    parser.add_argument(
        "--convert_doc",
        nargs="+",
        help=f"Converter document file(s) to different format ie pdf_to_docx.\
       example: {fg.BYELLOW}filemac --convert_doc example.docx -tff pdf{RESET}",
    )

    parser.add_argument(
        "--convert_audio",
        help=f"Convert audio file(s) to and from different format ie mp3 to wav\
        example: {fg.BYELLOW}filemac --convert_audio example.mp3 -tff wav{RESET}",
    )

    parser.add_argument(
        "--convert_video",
        help=f"Convert video file(s) to and from different format ie mp4 to mkv.\
        example: {fg.BYELLOW}filemac --convert_video example.mp4 -tf mkv{RESET}",
    )

    parser.add_argument(
        "--convert_image",
        help=f"Convert image file(s) to and from different format ie png to jpg.\
        example: {fg.BYELLOW}filemac --convert_image example.jpg -tf png{RESET}",
    )

    parser.add_argument(
        "--convert_svg",
        help=f"Converter svg file(s) to different format ie pdf, png.\
       example: {fg.BYELLOW}filemac --convert_svg example.svg -tff pdf{RESET}",
    )

    parser.add_argument(
        "--convert_doc2image",
        help=f"Convert documents to images ie png to jpg.\
        example: {fg.BYELLOW}filemac --convert_doc2image example.pdf -tf png{RESET}",
    )

    parser.add_argument(
        "-md",
        "--markdown2docx",
        help=f"Convert Markdown to DOCX with Mermaid rendering.\
            example: {fg.BYELLOW}filemac --markdown2docx example.md{RESET}",
    )
    parser.add_argument(
        "-xA",
        "--extract_audio",
        help=f"Extract audio from a video.\
                        example: {fg.BYELLOW}filemac -xA example.mp4 {RESET}",
    )

    parser.add_argument(
        "-iso",
        "--isolate",
        help=f"Specify file types to isolate\
                        for conversion, only works if directory is provided as input for the {fg.FCYAN}convert_doc{RESET} argument example: {fg.BYELLOW}filemac --convert_doc /home/user/Documents/ --isolate pdf -tf txt{RESET}",
    )

    parser.add_argument(
        "-Av",
        "--Analyze_video",
        help=f"Analyze a given video.\
        example: {fg.BYELLOW}filemac --analyze_video example.mp4 {RESET}",
    )

    parser.add_argument(
        "-tf", "--target_format", help="Target format for conversion (optional)"
    )

    parser.add_argument(
        "--resize_image",
        help=f"change size of an image compress/decompress \
        example: {fg.BYELLOW}filemac --resize_image example.png -tf_size 2mb -tf png {RESET}",
    )

    parser.add_argument(
        "-t_size",
        help="used in combination with resize_image \
                        to specify target image size",
    )

    parser.add_argument(
        "-S",
        "--scan",
        help=f"Scan pdf file and extract text\
                        example: {fg.BYELLOW}filemac --scan example.pdf {RESET}",
    )

    parser.add_argument(
        "-doc2L",
        "--doc_long_image",
        help=f"Convert pdf file to long image\
                        example: {fg.BYELLOW}filemac --doc_long_image example.pdf {RESET}",
    )

    parser.add_argument(
        "-SA",
        "--scanAsImg",
        help=f"Convert pdf to image then extract text\
                        example: {fg.BYELLOW}filemac --scanAsImg example.pdf {RESET}",
    )

    parser.add_argument(
        "-SALI",
        "--scanAsLong_Image",
        help=f"Scan {fg.CYAN}[doc, docx, pdf]\
        {RESET} file and extract text by first converting them to long image,-> very effective\
                    example: {fg.BYELLOW}filemac --scanAsImg example.pdf {RESET}",
    )

    parser.add_argument(
        "--OCR",
        nargs="+",
        help=f"Extract text from an image.\
        example: {fg.BYELLOW}filemac --OCR image.png{RESET}",
    )

    """Audio join  arguements"""
    # Accept 0 or more arguements
    parser.add_argument(
        "--AudioJoin",
        "-AJ",
        nargs="*",
        help=f"{fg.YELLOW}Join Audio files{RESET} into one master file.\
            Provide a {fg.BLUE}list{RESET} of audio file paths.  If no paths are provided, the program will still run.",
        metavar="audio_file_path",
    )

    """'arguements for Advanced text to word conversion"""
    parser.add_argument(
        "-RT2W",
        "--Richtext2word",
        help=f"Advanced Text to word conversion i.e:{
            fg.BYELLOW
        }filemac --Atext2word example.txt --font_size 12 --font_name Arial{RESET}",
    )

    # Add arguments that must accompany the "obj" command
    parser.add_argument(
        "--font_size",
        type=int,
        default=12,
        help=f"Font size to be used default: {fg.CYAN}12{RESET}",
    )
    parser.add_argument(
        "--font_name",
        type=str,
        default="Times New Roman",
        help=f"Font name default: {fg.FCYAN}Times New Roman{RESET}",
    )

    """Alternative sequence args, critical redundancy measure"""
    parser.add_argument(
        "-X",
        "--use_extras",
        action="store_true",
        help=f"Use alternative conversion method: Overides\
                        default method i.e: {fg.BYELLOW}filemac --convert_doc example.docx --use_extras -tf pdf{RESET}",
    )

    """Pdf join arguements--> Accepts atleast 1 arguement"""
    parser.add_argument("--pdfjoin", "-pj", nargs="+", help="Join Pdf file to one file")
    parser.add_argument(
        "--order",
        type=str,
        default="AAB",
        help=f"Order of pages when joining the pdf use: {fg.BYELLOW}filemac\
                        -pj help for more details{RESET}",
    )
    parser.add_argument(
        "--extract_pages",
        "-p",
        nargs="+",
        help=f"Extract given pages from pdf: {
            fg.BYELLOW
        }filemac --extract_pages file.pdf 6 10{RESET} for one page: {
            fg.BYELLOW
        }filemac --extract_pages file.pdf 5{RESET}",
    )

    parser.add_argument(
        "--audio_effect",
        "-af",
        action="store_true",
        help=f"Change audio voice/apply effects/reduce noise {fg.BYELLOW}-MA --help for options{RESET}",
    )
    parser.add_argument(
        "--audio_help", action="store_true", help="Show help for audiobot"
    )
    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="no_resume",
        help=f"Don't Resume previous File operation {fg.BYELLOW}filemac --convert_doc simpledir --no-resume{RESET}",
    )

    parser.add_argument(
        "--t",
        "-threads",
        type=int,
        default=3,
        help=f"Number of threads for text to speech  {fg.BYELLOW}filemac --convert_doc simpledir --no-resume -t 2{RESET}",
    )
    parser.add_argument(
        "-sep",
        "--separator",
        choices=["\\n", "\\t", " ", "", "newline", "space", "none", "tab"],
        default="\n",
        help="Separator to be used  in OCR eg.('\\n', ' ',  '')",
    )

    parser.add_argument(
        "--image2pdf",
        nargs="+",
        help=f"Convert Images to pdf. {fg.BWHITE}Accepts image list or dir/folder{RESET} e.g `{fg.BYELLOW}filemac --image2pdf image1 image2{RESET}`",
    )
    parser.add_argument(
        "--image2word",
        nargs="+",
        help=f"Convert Images to word document. {fg.BWHITE}Accepts image list or dir/folder{RESET} e.g `{fg.BYELLOW}filemac --image2word image1 image2{RESET}`",
    )
    parser.add_argument(
        "--image2gray",
        nargs="+",
        help=f"Convert Images to grayscale. {fg.BWHITE}Accepts image list or dir/folder{RESET} e.g `{fg.BYELLOW}filemac --image2gray image1 image2{RESET}`",
    )
    parser.add_argument(
        "-vt",
        "--voicetype",
        action="store_true",
        help=f"Use your voice to type text. e.g `{fg.BYELLOW}filemac --voicetype{RESET}`",
    )

    parser.add_argument(
        "-IeX",
        "--image_extractor",
        nargs="+",
        help=f"Convert Images to pdf. {fg.BWHITE}Accepts file list {RESET} e.g `{fg.BYELLOW}filemac --image_extractor file1 file2{RESET}`",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show software version and exit.",
    )

    parser.add_argument(
        "--sort",
        action="store_true",
        help="Order pages by last int before extension.",
    )
    parser.add_argument(
        "--base",
        action="store_true",
        help="Base name for image2pdf output",
    )
    parser.add_argument(
        "--size",
        type=str,
        help=f"Dimensions for images to be saved by extractor eg {fg.BBLUE}256x82{fg.RESET}",
    )
    parser.add_argument(
        "--walk",
        action="store_true",
        help="Do an operation on a dirctory and it's subdirectories.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help=f"Clean file/dir after an operation eg after {fg.BMAGENTA}image2pdf clean image dirs{fg.RESET}.",
    )
    parser.add_argument("--record", action="store_true", help="Record Audio from mic")

    parser.add_argument(
        "-h", "--help", action="store_true", help="Show this help message and exit."
    )

    # Use parse_known_args to allow unknown arguments (for later tunneling)
    args, remaining_args = parser.parse_known_args()
    mapper = OperationMapper(parser, args, remaining_args)
    mapper.run()


class OperationMapper:
    def __init__(self, parser, args, remaining_args) -> None:
        self.parser = parser
        self.args = args
        self.remaining_args = remaining_args

    def ensure_target_format(self):
        print(f"{bg.YELLOW}[Warning]{fg.YELLOW}Please provide target format{RESET}")
        return

    def pdfjoin(self):
        from ..core.pdf.core import PDFCombine

        if self.args.pdfjoin[0].lower().strip() == "help":
            from ..utils.helpmaster import pdf_combine_help

            opts, helper, example = pdf_combine_help()
            print(f"{opts}\n {helper}\n {example}")
            sys.exit(0)
        init = PDFCombine(self.args.pdfjoin, None, None, self.args.order)
        init.controller()

    def image_converter(self):
        if self.args.convert_image == "help":
            from ..utils.formats import SUPPORTED_IMAGE_FORMATS_SHOW

            print(SUPPORTED_IMAGE_FORMATS_SHOW)
            return
        if self.args.target_format is None:
            self.ensure_target_format()
            return
        if self.args.target_format is None:
            print(
                f"{fg.RED}Please provide output format specified by{fg.CYAN} '-tf'{RESET}"
            )
            return
        from ..core.image.core import ImageConverter

        conv = ImageConverter(self.args.convert_image, self.args.target_format)
        conv.convert_image()

    def doc_converter(self):
        from ..utils.formats import SUPPORTED_AUDIO_FORMATS_DIRECT
        from .converter import MethodMappingEngine, DirectoryConverter, Batch_Audiofy

        if self.args.target_format is None:
            self.ensure_target_format()
            return
        if self.args.use_extras:
            DocConverter.word2pdf_extra(self.args.convert_doc)
        if (
            len(self.args.convert_doc) <= 1
            and not os.path.isdir(self.args.convert_doc[0])
            and isinstance(self.args.convert_doc, list)
            and self.args.target_format in SUPPORTED_AUDIO_FORMATS_DIRECT
        ):
            Batch_Audiofy(self.args.convert_doc, self.args.no_resume, self.args.threads)
        elif os.path.isdir(self.args.convert_doc[0]):
            conv = DirectoryConverter(
                self.args.convert_doc[0],
                self.args.target_format,
                self.args.no_resume,
                self.args.threads,
                self.args.isolate,
            )
            conv._unbundle_dir_()
        elif os.path.isfile(self.args.convert_doc[0]):
            ev = MethodMappingEngine(self.args.convert_doc[0], self.args.target_format)
            ev.document_eval()

    def handle_help(self):
        if not self.args and not self.remaining_args:
            self.parser.print_help()
            return

    def handle_audio_help(self):
        if self.args.audio_help:
            audiobot_cli(["--help"])
        return

    def handle_audio_effect(self):
        audiobot_cli(self.remaining_args)
        return

    def handle_doc_conversion_help(self):
        if self.args.convert_doc and self.args.convert_doc[0] == "help":
            from ..utils.formats import SUPPORTED_DOC_FORMATS

            print(SUPPORTED_DOC_FORMATS)
        return

    def handle_video_conversion_help(self):
        if self.args.convert_video and self.args.convert_video == "help":
            from ..utils.formats import SUPPORTED_VIDEO_FORMATS_SHOW

            print(SUPPORTED_VIDEO_FORMATS_SHOW)
        return

    def handle_video_conversion(self):
        if hasattr(self, "agrs") and self.agrs.target_format is None:
            self.ensure_target_format()
            return
        from ..core.video.core import VideoConverter

        ev = VideoConverter(self.args.convert_video, self.args.target_format)
        ev.CONVERT_VIDEO()

    def handle_svg(self):
        from ..core.svg.core import SVGConverter

        converter = SVGConverter()
        _map_ = {
            "png": converter.to_png,
            "pdf": converter.to_pdf,
            "svg": converter.to_svg,
        }
        target = _map_.get(self.args.target_format, None)
        if not target:
            raise FilemacError("Target format not valid for svg input.")
        from ..utils.file_utils import generate_filename

        output = generate_filename(
            ext=self.args.target_format, basedir=Path(self.args.convert_svg)
        )
        target(
            input_svg=self.args.convert_svg,
            output_path=output.as_posix(),
            is_string=False,
        )
        print(f"Saved To:{output}")

    def handle_image_resize(self):
        from ..core.image.core import ImageCompressor

        res = ImageCompressor(self.args.resize_image)
        res.resize_image(self.args.t_size)

    def handle_doc_to_image_conversion(self):
        conv = DocConverter(self.args.convert_doc2image)
        conv.doc2image(self.args.target_format)

    def handle_audio_conversion_help(self):
        if self.args.convert_audio == "help":
            from ..utils.formats import SUPPORTED_AUDIO_FORMATS_SHOW

            print(SUPPORTED_AUDIO_FORMATS_SHOW)
        return

    def handle_audio_conversion(self):
        if self.agrs.target_format is None:
            self.ensure_target_format()
            return
        from ..core.audio.core import AudioConverter

        ev = AudioConverter(self.args.convert_audio, self.args.target_format)
        ev.pydub_conv()

    def handle_audio_extraction(self):
        from ..core.audio.core import AudioExtracter

        vi = AudioExtracter(self.args.extract_audio)
        vi.moviepyextract()

    def handle_scan_pdf(self):
        sc = PageExtractor(self.args.scan)
        sc.scanPDF()

    def handle_scan_images(self):
        sc = PageExtractor(self.args.scanAsImg, self.args.no_strip)
        sc.scanAsImgs()

    def handle_scan_long_image(self):
        sc = PageExtractor(self.args.scanAsLong_Image, self.args.separator)
        sc.scanAsLongImg()

    def handle_doc_to_long_image(self):
        from ..core.pdf.core import PDF2LongImageConverter

        conv = PDF2LongImageConverter(self.args.doc_long_image)
        conv.preprocess()

    def handle_ocr(self):
        from ..core.ocr import ExtractText

        ocr = ExtractText(self.args.OCR, self.args.separator)
        ocr.run()

    def handle_video_analysis(self):
        from ..miscellaneous.video_analyzer import SimpleAnalyzer

        analyzer = SimpleAnalyzer(self.args.Analyze_video)
        analyzer.SimpleAnalyzer()

    def handle_audio_join(self):
        from ..core.audio.core import AudioJoiner

        joiner = AudioJoiner(self.args.AudioJoin)
        joiner.worker()

    def handle_advanced_text_to_word(self):
        from ..core.text.core import StyledText

        init = StyledText(
            self.args.Richtext2word, None, self.args.font_size, self.args.font_name
        )
        init.text_to_word()

    def handle_extract_pages(self):
        _entry_(self.args.extract_pages)

    def ImageExtractor(self):
        from ..core.image.extractor import process_files

        if self.args.size:
            size = tuple([int(x) for x in self.args.size.lower().split("x")])
            process_files(self.args.image_extractor, tsize=size)
        else:
            process_files(self.args.image_extractor)

    def image2pdf(self):
        from ..core.image.core import ImagePdfConverter

        _input = (
            list(self.args.image2pdf)
            if not isinstance(self.args.image2pdf, list)
            else self.args.image2pdf
        )
        if isinstance(_input, list):
            if len(_input) > 1 or os.path.isfile(os.path.abspath(_input[0])):
                converter = ImagePdfConverter(image_list=_input)
            else:
                converter = ImagePdfConverter(
                    input_dir=_input[0],
                    order=self.args.sort,
                    base=self.args.base,
                    walk=self.args.walk,
                    clean=self.args.clean,
                )
        converter.run()

    def image2word(self):
        from ..core.image.core import ImageDocxConverter

        _input = self.args.image2word
        if isinstance(_input, list):
            if len(_input) > 1:
                converter = ImageDocxConverter(image_list=_input)
            else:
                converter = ImageDocxConverter(input_dir=_input[0])
        converter.run()

    def image2grayscale(self):
        from ..core.image.core import GrayscaleConverter

        _input = self.args.image2gray

        if isinstance(_input, list):
            converter = (
                GrayscaleConverter(_input)
                if len(_input) > 1
                else GrayscaleConverter(_input[0])
            )
            converter.run()

    def display_version(self):
        version = "2.0.1"

        return print(f"{fg.BLUE}filemac: V-{fg.BGREEN}{version}{RESET}")

    def voicetype(self):
        from voice.VoiceType import VoiceTypeEngine

        try:
            engine = VoiceTypeEngine()
            engine.start()
        except KeyboardInterrupt:
            print("Quit")
            return
        except Exception as e:
            logger.critical("Critical failure: %s", e)
            print(f"{bg.YELLOW}{bg.BRED}Critical error:{RESET} {fg.RED}{str(e)}{RESET}")
            return

    def handle_recording(self):
        from ..core.recorder import SoundRecorder

        rec = SoundRecorder()
        return rec.run()

    def run(self):
        args = self.args
        """Check for help argument by calling help method"""
        self.handle_help()

        """Check for audio help argument by calling help method"""
        self.handle_audio_help()

        """Check for doc conversion help argument by calling help method"""
        self.handle_doc_conversion_help()

        """Check for video conversion help argument by calling help method"""
        self.handle_video_conversion_help()

        """Check for audio conversion help argument by calling help method"""
        self.handle_audio_conversion_help()

        method_mapper = {
            args.version: self.display_version,
            args.audio_effect: self.handle_audio_effect,
            tuple(args.convert_doc)
            if isinstance(args.convert_doc, list)
            else args.convert_doc: self.doc_converter,
            args.convert_video: self.handle_video_conversion,
            args.convert_image: self.image_converter,
            args.resize_image: self.handle_image_resize,
            args.convert_doc2image: self.handle_doc_to_image_conversion,
            args.convert_audio: self.handle_audio_conversion,
            args.extract_audio: self.handle_audio_extraction,
            args.scan: self.handle_scan_pdf,
            args.scanAsImg: self.handle_scan_images,
            args.doc_long_image: self.handle_doc_to_long_image,
            args.scanAsLong_Image: self.handle_scan_long_image,
            args.convert_svg: self.handle_svg,
            args.voicetype: self.voicetype,
            tuple(args.OCR)
            if isinstance(args.OCR, list)
            else args.OCR: self.handle_ocr,
            args.Analyze_video: self.handle_video_analysis,
            tuple(args.AudioJoin)
            if isinstance(args.AudioJoin, list)
            else args.AudioJoin: self.handle_audio_join,
            args.Richtext2word: self.handle_advanced_text_to_word,
            tuple(args.pdfjoin)
            if isinstance(args.pdfjoin, list)
            else args.pdfjoin: self.pdfjoin,
            tuple(args.extract_pages)
            if isinstance(args.extract_pages, list)
            else args.extract_pages: self.handle_extract_pages,
            tuple(args.image2pdf)
            if isinstance(args.image2pdf, list)
            else args.image2pdf: self.image2pdf,
            tuple(args.image2word)
            if isinstance(args.image2word, list)
            else args.image2word: self.image2word,
            tuple(args.image2gray)
            if isinstance(args.image2gray, list)
            else args.image2gray: self.image2grayscale,
            tuple(args.image_extractor)
            if isinstance(args.image_extractor, list)
            else args.image_extractor: self.ImageExtractor,
            args.record: self.handle_recording,
        }

        # Find the first non-empty key in method_mapper and execute its corresponding method
        try:
            """
            audio effects must take precedence due to the nested arguments which
            might possibly conflict with the original arguments
            """
            if args.audio_effect:
                return self.handle_audio_effect()

            if args.help and not args.audio_effect:
                self.parser.print_help()
                sys.exit()

            method = next((method_mapper[key] for key in method_mapper if key), None)
            if method:
                method()
            else:
                self.parser.print_help()
                raise FilemacError("Invalid arguments")
        except KeyboardInterrupt:
            logger.info("\nQuit")
            sys.exit()
        except (FilemacError, FileSystemError) as e:
            # Handle any exceptions that occur during method execution
            logger.error(e)

        except Exception as e:
            raise
            # Handle any exceptions that occur during method execution
            logger.error(f"An error occurred: {e}")

        return


if __name__ == "__main__":
    CliInit()
