#!/usr/bin/env python3
import argparse
import logging
import logging.handlers
import os
import sys
from typing import List, Union
from audiobot.cli import Argsmain
from .imagepy.converter import ImageConverter

from utils.colors import foreground, background
from utils.formats import (
    SUPPORTED_AUDIO_FORMATS_DIRECT,
    SUPPORTED_AUDIO_FORMATS_SHOW,
    SUPPORTED_DOC_FORMATS,
    SUPPORTED_IMAGE_FORMATS_SHOW,
)
from . import warnings_handler
from .audiopy.audio import AudioConverter
from .audiopy.pyTTS import FileSynthesis
from .audiopy.Extractor import ExtractAudio
from .pydocs import DocConverter, Scanner
from .imagepy.compress import Compress_Size
from .OCR.Extractor import ExtractText
from .pdf.Page_Extractor import _entry
from .Simple_v_Analyzer import SA
from .videopy.pyVideo import VideoConverter
from .imagepy.image_extractor import process_files


fcl = foreground()
bcl = background()
RESET = fcl.RESET


warnings_handler
logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

"""If the input file in convert_doc argument is a directory, walk throught the directory and
converter all the surported files to the target format"""


class _DIR_CONVERSION_:
    def __init__(self, _dir_, _format_, no_resume, threads, _isolate_=None):
        self._dir_ = _dir_
        self._format_ = _format_
        self._isolate_ = _isolate_
        self.no_resume = no_resume
        self.threads = threads
        # Handle isolation and non isolation modes distinctively
        self._ls_ = (
            ["pdf", "docx", "doc", "xlsx", "ppt", "pptx" "xls", "txt"]
            if _isolate_ is None
            else [_isolate_]
        )
        if self._isolate_:
            print(
                f"INFO\t {fcl.FMAGENTA_FG}Isolate {fcl.DCYAN_FG}{self._isolate_}{RESET}"
            )

    def _unbundle_dir_(self):
        if self._format_ in SUPPORTED_AUDIO_FORMATS_DIRECT:
            return Batch_Audiofy(self._dir_, self.no_resume, self.threads)
        try:
            for root, dirs, files in os.walk(self._dir_):
                for file in files:
                    _ext_ = file.split(".")[-1]

                    _path_ = os.path.join(root, file)

                    if _ext_ in self._ls_ and os.path.exists(_path_):
                        print(f"INFO\t {fcl.FYELLOW_FG}Parse {
                            fcl.BLUE_FG}{_path_}{RESET}")
                        init = Eval(_path_, self._format_)
                        init.document_eval()

        except FileNotFoundError as e:
            print(e)

        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)

        except Exception as e:
            print(e)
            pass


def _isolate_(_dir_, target):
    try:
        isolated_files = []
        for root, dirs, files in os.walk(_dir_):
            for file in files:
                if file.lower().endswith(target):
                    _path_ = os.path.join(root, file)
                    isolated_files.append(_path_)
        return isolated_files
    except FileNotFoundError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nQuit!")
        sys.exit(1)
    except Exception as e:
        print(e)


class Batch_Audiofy:
    def __init__(
        self,
        obj: Union[os.PathLike, str, List[Union[os.PathLike, str]]],
        no_resume: bool,
        threads: int = 3,
    ):
        self.folder = obj
        self.no_resume = no_resume
        self.threads = threads
        self.worker()

    def worker(self):
        conv = FileSynthesis(self.folder, resume=self.no_resume)
        inst = conv.THAudio(conv)
        inst.audiofy(num_threads=self.threads)


class Eval:
    """
    Class to handle document conversions based on their extensions and the target
        output document format
    """

    def __init__(self, file, outf):
        self.file = file
        self.outf = outf

    def spreedsheet(self, conv):
        if self.outf.lower() == "csv":
            conv.convert_xlsx_to_csv()
        elif self.outf.lower() in ("txt", "text"):
            conv.convert_xls_to_text()
        elif self.outf.lower() in list(self.doc_ls):
            conv.convert_xls_to_word()
        elif self.outf.lower() == "db":
            conv.convert_xlsx_to_database()
        else:
            print(f"{fcl.RED_FG}Unsupported output format❌{RESET}")

    def word(self, conv):
        if self.outf.lower() in ("txt", "text"):
            conv.word_to_txt()
        elif self.outf.lower() == "pdf":
            conv.word_to_pdf()
        elif self.outf.lower() in ("pptx", "ppt"):
            conv.word_to_pptx()
        elif self.outf.lower() in ("audio", "ogg"):
            conv = FileSynthesis(self.file)
            conv.audiofy()
        else:
            print(f"{fcl.RED_FG}Unsupported output format❌{RESET}")

    def text(self, conv):
        if self.outf.lower() == "pdf":
            conv.txt_to_pdf()
        elif self.outf.lower() in ("doc", "docx", "word"):
            conv.text_to_word()
        elif self.outf.lower() in ("audio", "ogg"):
            conv = FileSynthesis(self.file)
            conv.audiofy()
        else:
            print(f"{fcl.RED_FG}Unsupported output format❌{RESET}")

    def ppt(self, conv):
        if self.outf.lower() in ("doc", "docx", "word"):
            conv.ppt_to_word()
        elif self.outf.lower() in ("text", "txt"):
            word = conv.ppt_to_word()
            conv = DocConverter(word)
            conv.word_to_txt()
        elif self.outf.lower() in ("pptx"):
            conv.convert_ppt_to_pptx(self.file)
        elif self.outf.lower() in ("audio", "ogg", "mp3", "wav"):
            conv = FileSynthesis(self.file)
            conv.audiofy()
        else:
            print(f"{fcl.RED_FG}Unsupported output format❌{RESET}")

    def pdf(self, conv):
        if self.outf.lower() in ("doc", "docx", "word"):
            conv.pdf_to_word()
        elif self.outf.lower() in ("txt", "text"):
            conv.pdf_to_txt()
        elif self.outf.lower() in ("audio", "ogg", "mp3", "wav"):
            conv = FileSynthesis(self.file)
            conv.audiofy()
        else:
            print(f"{fcl.RED_FG}Unsupported output format❌{RESET}")

    def document_eval(self):
        self.doc_ls = ["docx", "doc"]
        sheetls = ["xlsx", "xls"]
        try:
            conv = DocConverter(self.file)
            if self.file.lower().endswith(tuple(sheetls)):
                self.spreedsheet(conv=conv)

            elif self.file.lower().endswith(tuple(self.doc_ls)):
                self.word(conv=conv)

            elif self.file.endswith("txt"):
                self.text(conv=conv)

            elif self.file.split(".")[-1].lower() in ("ppt", "pptx"):
                self.ppt(conv)

            elif self.file.lower().endswith("pdf"):
                self.pdf(conv)

            elif self.file.lower().endswith("csv"):
                if self.outf.lower() in ("xls", "xlsx", "excel"):
                    conv.convert_csv_to_xlsx()

            else:
                print(f"{fcl.fcl.BYELLOW_FG}Unsupported Conversion type❌{RESET}")
                pass
        except Exception as e:
            logger.error(e)


def Cmd_arg_Handler():
    """Define main functions to create commandline arguments for different operations"""
    parser = argparse.ArgumentParser(
        description="Filemac: A file management tool with audio effects. Supporting wide range of Multimedia Operations",
        epilog=f"{fcl.BLUE_FG}When using {fcl.MAGENTA_FG}-SALI{fcl.BLUE_FG} long images have maximum height that can be processed{RESET}",
    )

    parser.add_argument(
        "--convert_doc",
        nargs="+",
        help=f"Converter document file(s) to different format ie pdf_to_docx.\
       example: {fcl.BYELLOW_FG}filemac --convert_doc example.docx -tff pdf{RESET}",
    )

    parser.add_argument(
        "--convert_audio",
        help=f"Convert audio file(s) to and from different format ie mp3 to wav\
        example: {fcl.BYELLOW_FG}filemac --convert_audio example.mp3 -tff wav{RESET}",
    )

    parser.add_argument(
        "--convert_video",
        help=f"Convert video file(s) to and from different format ie mp4 to mkv.\
        example: {fcl.BYELLOW_FG}filemac --convert_video example.mp4 -tf mkv{RESET}",
    )

    parser.add_argument(
        "--convert_image",
        help=f"Convert image file(s) to and from different format ie png to jpg.\
        example: {fcl.BYELLOW_FG}filemac --convert_image example.jpg -tf png{RESET}",
    )

    parser.add_argument(
        "--convert_doc2image",
        help=f"Convert documents to images ie png to jpg.\
        example: {fcl.BYELLOW_FG}filemac --convert_doc2image example.pdf -tf png{RESET}",
    )

    parser.add_argument(
        "-xA",
        "--extract_audio",
        help=f"Extract audio from a video.\
                        example: {fcl.BYELLOW_FG}filemac -xA example.mp4 {RESET}",
    )

    parser.add_argument(
        "-iso",
        "--isolate",
        help=f"Specify file types to isolate\
                        for conversion, only works if directory is provided as input for the {fcl.FCYAN_FG}convert_doc{RESET} argument example: {fcl.BYELLOW_FG}filemac --convert_doc /home/user/Documents/ --isolate pdf -tf txt{RESET}",
    )

    parser.add_argument(
        "-Av",
        "--Analyze_video",
        help=f"Analyze a given video.\
        example: {fcl.BYELLOW_FG}filemac --analyze_video example.mp4 {RESET}",
    )

    parser.add_argument(
        "-tf", "--target_format", help="Target format for conversion (optional)"
    )

    parser.add_argument(
        "--resize_image",
        help=f"change size of an image compress/decompress \
        example: {fcl.BYELLOW_FG}filemac --resize_image example.png -tf_size 2mb -tf png {RESET}",
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
                        example: {fcl.BYELLOW_FG}filemac --scan example.pdf {RESET}",
    )

    parser.add_argument(
        "-doc2L",
        "--doc_long_image",
        help=f"Convert pdf file to long image\
                        example: {fcl.BYELLOW_FG}filemac --doc_long_image example.pdf {RESET}",
    )

    parser.add_argument(
        "-SA",
        "--scanAsImg",
        help=f"Convert pdf to image then extract text\
                        example: {fcl.BYELLOW_FG}filemac --scanAsImg example.pdf {RESET}",
    )

    parser.add_argument(
        "-SALI",
        "--scanAsLong_Image",
        help=f"Scan {fcl.CYAN_FG}[doc, docx, pdf]\
        {RESET} file and extract text by first converting them to long image,-> very effective\
                    example: {fcl.BYELLOW_FG}filemac --scanAsImg example.pdf {RESET}",
    )

    parser.add_argument(
        "--OCR",
        nargs="+",
        help=f"Extract text from an image.\
        example: {fcl.BYELLOW_FG}filemac --OCR image.png{RESET}",
    )

    """Audio join  arguements"""
    # Accept 0 or more arguements
    parser.add_argument(
        "--AudioJoin",
        "-AJ",
        nargs="*",
        help=f"{fcl.YELLOW_FG}Join Audio files{RESET} into one master file.\
            Provide a {fcl.BLUE_FG}list{RESET} of audio file paths.  If no paths are provided, the program will still run.",
        metavar="audio_file_path",
    )

    """'arguements for Advanced text to word conversion"""
    parser.add_argument(
        "-AT2W",
        "--Atext2word",
        help=f"Advanced Text to word conversion i.e:{
            fcl.BYELLOW_FG}filemac --Atext2word example.txt --font_size 12 --font_name Arial{RESET}",
    )

    # Add arguments that must accompany the "obj" command
    parser.add_argument(
        "--font_size",
        type=int,
        default=12,
        help=f"Font size to be used default: {fcl.CYAN_FG}12{RESET}",
    )
    parser.add_argument(
        "--font_name",
        type=str,
        default="Times New Roman",
        help=f"Font name default: {fcl.FCYAN_FG}Times New Roman{RESET}",
    )

    """Alternative sequence args, critical redundancy measure"""
    parser.add_argument(
        "-X",
        "--use_extras",
        action="store_true",
        help=f"Use alternative conversion method: Overides\
                        default method i.e: {fcl.BYELLOW_FG}filemac --convert_doc example.docx --use_extras -tf pdf{RESET}",
    )

    """Pdf join arguements--> Accepts atleast 1 arguement"""
    parser.add_argument("--pdfjoin", "-pj", nargs="+", help="Join Pdf file to one file")
    parser.add_argument(
        "--order",
        type=str,
        default="AAB",
        help=f"Order of pages when joining the pdf use: {fcl.BYELLOW_FG}filemac\
                        -pj help for more details{RESET}",
    )
    parser.add_argument(
        "--extract_pages",
        "-p",
        nargs="+",
        help=f"Extract given pages from pdf: {
            fcl.BYELLOW_FG}filemac --extract_pages file.pdf 6 10{RESET} for one page: {fcl.BYELLOW_FG}filemac --extract_pages file.pdf 5{RESET}",
    )

    parser.add_argument(
        "--audio_effect",
        "-af",
        action="store_true",
        help=f"Change audio voice/apply effects/reduce noise{fcl.BYELLOW_FG}-MA --help for options{RESET}",
    )
    parser.add_argument(
        "--audio_help", action="store_true", help="Show help for audiobot"
    )
    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="no_resume",
        help=f"Don't Resume previous File operation {fcl.BYELLOW_FG}filemac --convert_doc simpledir --no-resume{RESET}",
    )

    parser.add_argument(
        "--t",
        "-threads",
        type=int,
        default=3,
        help=f"Number of threads for text to speech  {fcl.BYELLOW_FG}filemac --convert_doc simpledir --no-resume -t 2{RESET}",
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
        help=f"Convert Images to pdf. {fcl.BWHITE_FG}Accepts image list or dir/folder{RESET} e.g `{fcl.BYELLOW_FG}filemac --image2pdf image1 image2{RESET}`",
    )
    parser.add_argument(
        "--image2word",
        nargs="+",
        help=f"Convert Images to word document. {fcl.BWHITE_FG}Accepts image list or dir/folder{RESET} e.g `{fcl.BYELLOW_FG}filemac --image2word image1 image2{RESET}`",
    )
    parser.add_argument(
        "--image2gray",
        nargs="+",
        help=f"Convert Images to grayscale. {fcl.BWHITE_FG}Accepts image list or dir/folder{RESET} e.g `{fcl.BYELLOW_FG}filemac --image2gray image1 image2{RESET}`",
    )
    parser.add_argument(
        "-vt",
        "--voicetype",
        action="store_true",
        help=f"Use your voice to type text. e.g `{fcl.BYELLOW_FG}filemac --voicetype{RESET}`",
    )

    parser.add_argument(
        "-IeX",
        "--image_extractor",
        nargs="+",
        help=f"Convert Images to pdf. {fcl.BWHITE_FG}Accepts file list {RESET} e.g `{fcl.BYELLOW_FG}filemac --image_extractor file1 file2{RESET}`",
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
        help=f"Dimensions for images to be saved by extractor eg {fcl.BBLUE_FG}256x82{fcl.RESET}",
    )
    parser.add_argument(
        "--walk",
        action="store_true",
        help="Do an operation on a dirctory and it's subdirectories.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help=f"Clean file/dir after an operation eg after {fcl.BMAGENTA_FG}image2pdf clean image dirs{fcl.RESET}.",
    )
    # Use parse_known_args to allow unknown arguments (for later tunneling)
    args, remaining_args = parser.parse_known_args()
    mapper = argsOPMaper(parser, args, remaining_args)
    mapper.run()


class argsOPMaper:
    def __init__(self, parser, args, remaining_args) -> None:
        self.parser = parser
        self.args = args
        self.remaining_args = remaining_args
        self.SUPPORTED_IMAGE_FORMATS_SHOW = SUPPORTED_IMAGE_FORMATS_SHOW
        self.SUPPORTED_DOC_FORMATS = SUPPORTED_DOC_FORMATS
        self.SUPPORTED_AUDIO_FORMATS_SHOW = SUPPORTED_AUDIO_FORMATS_SHOW
        self.SUPPORTED_AUDIO_FORMATS_DIRECT = SUPPORTED_AUDIO_FORMATS_DIRECT
        self.Argsmain = Argsmain
        self.VideoConverter = VideoConverter
        self.AudioConverter = AudioConverter
        self.ExtractAudio = ExtractAudio
        self.Scanner = Scanner
        self.DocConverter = DocConverter
        self.Compress_Size = Compress_Size
        self.ExtractText = ExtractText
        self.SA = SA
        self._entry = _entry
        self.ImageConverter = ImageConverter
        self.Batch_Audiofy = Batch_Audiofy
        self._DIR_CONVERSION_ = _DIR_CONVERSION_
        self.Eval = Eval

    def ensure_target_format(self):
        print(
            f"{bcl.YELLOW_BG}[Warning]{fcl.YELLOW_FG}Please provide target format{RESET}"
        )
        return

    def pdfjoin(self):
        from .pdf.combine import pdfmaster

        if self.args.pdfjoin[0].lower().strip() == "help":
            from .pdf.combine import helpmaster

            opts, helper, example = helpmaster()
            print(f"{opts}\n {helper}\n {example}")
            sys.exit(0)
        init = pdfmaster(self.args.pdfjoin, None, None, self.args.order)
        init.controller()

    def image_converter(self):
        if self.args.target_format is None:
            self.ensure_target_format()
            return
        if self.args.convert_image == "help":
            print(self.SUPPORTED_IMAGE_FORMATS_SHOW)
            return
        if self.args.target_format is None:
            print(
                f"{fcl.RED_FG}Please provide output format specified by{fcl.CYAN_FG} '-tf'{RESET}"
            )
            return
        conv = self.ImageConverter(self.args.convert_image, self.args.target_format)
        conv.convert_image()

    def doc_converter(self):
        if self.args.target_format is None:
            self.ensure_target_format()
            return
        if self.args.use_extras:
            self.DocConverter.word2pdf_extra(self.args.convert_doc)
        if (
            len(self.args.convert_doc) <= 1
            and not os.path.isdir(self.args.convert_doc[0])
            and isinstance(self.args.convert_doc, list)
            and self.args.target_format in self.SUPPORTED_AUDIO_FORMATS_DIRECT
        ):
            self.Batch_Audiofy(
                self.args.convert_doc, self.args.no_resume, self.args.threads
            )
        elif os.path.isdir(self.args.convert_doc[0]):
            conv = self._DIR_CONVERSION_(
                self.args.convert_doc[0],
                self.args.target_format,
                self.args.no_resume,
                self.args.threads,
                self.args.isolate,
            )
            conv._unbundle_dir_()
        elif os.path.isfile(self.args.convert_doc[0]):
            ev = self.Eval(self.args.convert_doc[0], self.args.target_format)
            ev.document_eval()

    def handle_help(self):
        if not self.args and not self.remaining_args:
            self.parser.print_help()
            return

    def handle_audio_help(self):
        if self.args.audio_help:
            self.Argsmain(["--help"])
        return

    def handle_audio_effect(self):
        self.Argsmain(self.remaining_args)
        return

    def handle_doc_conversion_help(self):
        if self.args.convert_doc and self.args.convert_doc[0] == "help":
            print(self.SUPPORTED_DOC_FORMATS)
        return

    def handle_video_conversion_help(self):
        if self.args.convert_video and self.args.convert_video == "help":
            print(self.SUPPORTED_VIDEO_FORMATS_SHOW)
        return

    def handle_video_conversion(self):
        if self.agrs.target_format is None:
            self.ensure_target_format()
            return
        ev = self.VideoConverter(self.args.convert_video, self.args.target_format)
        ev.CONVERT_VIDEO()

    def handle_image_resize(self):
        res = self.Compress_Size(self.args.resize_image)
        res.resize_image(self.args.t_size)

    def handle_doc_to_image_conversion(self):
        conv = self.DocConverter(self.args.convert_doc2image)
        conv.doc2image(self.args.target_format)

    def handle_audio_conversion_help(self):
        if self.args.convert_audio == "help":
            print(self.SUPPORTED_AUDIO_FORMATS_SHOW)
        return

    def handle_audio_conversion(self):
        if self.agrs.target_format is None:
            self.ensure_target_format()
            return
        ev = self.AudioConverter(self.args.convert_audio, self.args.target_format)
        ev.pydub_conv()

    def handle_audio_extraction(self):
        vi = self.ExtractAudio(self.args.extract_audio)
        vi.moviepyextract()

    def handle_scan_pdf(self):
        sc = self.Scanner(self.args.scan)
        sc.scanPDF()

    def handle_scan_images(self):
        sc = self.Scanner(self.args.scanAsImg, self.args.no_strip)
        sc.scanAsImgs()

    def handle_scan_long_image(self):
        sc = self.Scanner(self.args.scanAsLong_Image, self.args.separator)
        sc.scanAsLongImg()

    def handle_doc_to_long_image(self):
        from .longImg import LImage

        conv = LImage(self.args.doc_long_image)
        conv.preprocess()

    def handle_ocr(self):
        ocr = self.ExtractText(self.args.OCR, self.args.separator)
        ocr.run()

    def handle_video_analysis(self):
        analyzer = self.SA(self.args.Analyze_video)
        analyzer.SimpleAnalyzer()

    def handle_audio_join(self):
        from .audiopy.Join import JoinAudios

        joiner = JoinAudios(self.args.AudioJoin)
        joiner.worker()

    def handle_advanced_text_to_word(self):
        init = self.AdvancedT2word(
            self.args.Atext2word, None, self.args.font_size, self.args.font_name
        )
        init.text_to_word()

    def handle_extract_pages(self):
        self._entry(self.args.extract_pages)

    def ImageExtractor(self):
        if self.args.size:
            size = tuple([int(x) for x in self.args.size.lower().split("x")])
            process_files(self.args.image_extractor, tsize=size)
        else:
            process_files(self.args.image_extractor)

    def image2pdf(self):
        from .Imagepdfpy.image_to_pdf import ImageToPdfConverter

        _input = (
            list(self.args.image2pdf)
            if not isinstance(self.args.image2pdf, list)
            else self.args.image2pdf
        )
        if isinstance(_input, list):
            if len(_input) > 1 or os.path.isfile(os.path.abspath(_input[0])):
                converter = ImageToPdfConverter(image_list=_input)
            else:
                converter = ImageToPdfConverter(
                    input_dir=_input[0],
                    order=self.args.sort,
                    base=self.args.base,
                    walk=self.args.walk,
                    clean=self.args.clean,
                )
        converter.run()

    def image2word(self):
        from .Image2docx.image_to_word import ImageToDocxConverter

        _input = self.args.image2word
        if isinstance(_input, list):
            if len(_input) > 1:
                converter = ImageToDocxConverter(image_list=_input)
            else:
                converter = ImageToDocxConverter(input_dir=_input[0])
        converter.run()

    def image2grayscale(self):
        from .imagepy.grayscale import Grayscale

        _input = self.args.image2gray

        if isinstance(_input, list):
            converter = Grayscale(_input) if len(_input) > 1 else Grayscale(_input[0])
            converter.run()

    def display_version(self):
        version = "1.1.7"

        return print(f"{fcl.BLUE_FG}filemac: V-{fcl.BGREEN_FG}{version}{RESET}")

    def voicetype(self):
        from voice.VoiceType import VoiceTypeEngine

        try:
            engine = VoiceTypeEngine()
            engine.start()
        except KeyboardInterrupt:
            print("Quit")
            return
        except Exception as e:
            logging.critical("Critical failure: %s", e)
            print(
                f"{bcl.YELLOW_BG}{bcl.BRED_BG}Critical error:{RESET} {fcl.RED_FG}{str(e)}{RESET}"
            )
            return

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
            args.voicetype: self.voicetype,
            tuple(args.OCR)
            if isinstance(args.OCR, list)
            else args.OCR: self.handle_ocr,
            args.Analyze_video: self.handle_video_analysis,
            tuple(args.AudioJoin)
            if isinstance(args.AudioJoin, list)
            else args.AudioJoin: self.handle_audio_join,
            args.Atext2word: self.handle_advanced_text_to_word,
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
        }

        # Find the first non-empty key in method_mapper and execute its corresponding method
        try:
            """
            audio effects must take precedence due to thenested arguments which
            might possibly conflict with the original arguments
            """
            if args.audio_effect:
                self.handle_audio_effect()
                return
            method = next((method_mapper[key] for key in method_mapper if key), None)
            if method:
                method()
        except Exception as e:
            raise
            # Handle any exceptions that occur during method execution
            print(f"An error occurred: {e}")

        return


if __name__ == "__main__":
    Cmd_arg_Handler()
