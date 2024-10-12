#!/usr/bin/env python3.11.7
'''Control file (main script)'''
import argparse
import logging
import logging.handlers
import os
import sys
from typing import Union, List
# from pathlib import Path
from . import handle_warnings
from .AudioExtractor import ExtractAudio
from .colors import (BLUE, CYAN, DCYAN, DYELLOW, FBLUE, FCYAN, FMAGENTA,
                     FYELLOW, MAGENTA, RED, RESET)
from .converter import (AudioConverter, FileSynthesis, ImageConverter,
                        MakeConversion, Scanner, VideoConverter)
from .formats import (SUPPORTED_AUDIO_FORMATS_DIRECT,
                      SUPPORTED_AUDIO_FORMATS_SHOW, SUPPORTED_DOC_FORMATS,
                      SUPPORTED_IMAGE_FORMATS_SHOW,
                      SUPPORTED_VIDEO_FORMATS_SHOW)
from .image_op import Compress_Size
from .OCRTextExtractor import ExtractText
from .pdf_Page_Extractor import _entry
from .Simple_v_Analyzer import SA

handle_warnings
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
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
        self._ls_ = ["pdf", "docx", "doc", "xlsx", "ppt", "pptx" "xls",
                     "txt"] if _isolate_ is None else [_isolate_]
        if self._isolate_:
            print(f"INFO\t {FMAGENTA}Isolate {DCYAN}{self._isolate_}{RESET}")

    def _unbundle_dir_(self):
        if self._format_ in SUPPORTED_AUDIO_FORMATS_DIRECT:
            return Batch_Audiofy(self._dir_, self.no_resume, self.threads)
        try:

            for root, dirs, files in os.walk(self._dir_):
                for file in files:
                    _ext_ = file.split('.')[-1]

                    _path_ = os.path.join(root, file)

                    if _ext_ in self._ls_ and os.path.exists(_path_):
                        print(f"INFO\t {FYELLOW}Parse {
                                FBLUE}{_path_}{RESET}")
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


class Batch_Audiofy:
    def __init__(self, obj: Union[os.PathLike, str, List[Union[os.PathLike, str]]], no_resume: bool, threads: int = 3):
        self.folder = obj
        self.no_resume = no_resume
        self.threads = threads
        self.worker()

    def worker(self):
        conv = FileSynthesis(self.folder, resume=self.no_resume)
        inst = conv.THAudio(conv)
        inst.audiofy(num_threads=self.threads)


"""Class to handle document conversions based on their extensions and te targt
output fdocument format"""


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
                elif self.outf.lower() in ("txt", "text"):
                    conv.convert_xls_to_text()
                elif self.outf.lower() in list(ls):
                    conv.convert_xls_to_word()
                elif self.outf.lower() == "db":
                    conv.convert_xlsx_to_database()
                else:
                    print(F"{RED}Unsupported output format❌{RESET}")

            elif self.file.lower().endswith(tuple(ls)):
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
                    print(F"{RED}Unsupported output format❌{RESET}")

            elif self.file.endswith('txt'):
                if self.outf.lower() == "pdf":
                    conv.txt_to_pdf()
                elif self.outf.lower() in ("doc", "docx", "word"):
                    conv.text_to_word()
                elif self.outf.lower() in ("audio", "ogg"):
                    conv = FileSynthesis(self.file)
                    conv.audiofy()
                else:
                    print(F"{RED}Unsupported output format❌{RESET}")

            elif self.file.split('.')[-1].lower() in ("ppt", "pptx"):
                if self.outf.lower() in ("doc", "docx", "word"):
                    conv.ppt_to_word()
                elif self.outf.lower() in ("text", "txt"):
                    word = conv.ppt_to_word()
                    conv = MakeConversion(word)
                    conv.word_to_txt()
                elif self.outf.lower() in ("pptx"):
                    conv.convert_ppt_to_pptx(self.file)
                elif self.outf.lower() in ("audio", "ogg", "mp3", "wav"):
                    conv = FileSynthesis(self.file)
                    conv.audiofy()
                else:
                    print(F"{RED}Unsupported output format❌{RESET}")

            elif self.file.lower().endswith('pdf'):
                if self.outf.lower() in ("doc", "docx", "word"):
                    conv.pdf_to_word()
                elif self.outf.lower() in ("txt", "text"):
                    conv.pdf_to_txt()
                elif self.outf.lower() in ("audio", "ogg", "mp3", "wav"):
                    conv = FileSynthesis(self.file)
                    conv.audiofy()
                else:
                    print(F"{RED}Unsupported output format❌{RESET}")

            elif self.file.lower().endswith('csv'):
                if self.outf.lower() in ('xls', 'xlsx', 'excel'):
                    conv.convert_csv_to_xlsx()

            else:
                print(f"{DYELLOW}Unsupported Conversion type❌{RESET}")
                pass
        except Exception as e:
            logger.error(e)


def main():
    """Define main functions to create commandline arguments for different operations"""
    parser = argparse.ArgumentParser(
        description="Multimedia Element Operations", epilog=f"{BLUE}When using {MAGENTA}-SALI{BLUE} long images have maximum height that can be processed{RESET}")

    parser.add_argument(
        "--convert_doc", nargs='+', help=f"Converter document file(s) to different format ie pdf_to_docx.\
       example: {DYELLOW}filemac --convert_doc example.docx -t pdf{RESET}")

    parser.add_argument(
        "--convert_audio", help=f"Convert audio file(s) to and from different format ie mp3 to wav\
        example: {DYELLOW}filemac --convert_audio example.mp3 -t wav{RESET}")

    parser.add_argument(
        "--convert_video", help=f"Convert video file(s) to and from different format ie mp4 to mkv.\
        example: {DYELLOW}filemac --convert_video example.mp4 -t mkv{RESET}")

    parser.add_argument(
        "--convert_image", help=f"Convert image file(s) to and from different format ie png to jpg.\
        example: {DYELLOW}filemac --convert_image example.jpg -t png{RESET}")

    parser.add_argument(

        "--convert_doc2image", help=f"Convert documents to images ie png to jpg.\
        example: {DYELLOW}filemac --convert_doc2image example.pdf -t png{RESET}")

    parser.add_argument("-xA", "--extract_audio",
                        help=f"Extract audio from a video.\
                        example: {DYELLOW}filemac -xA example.mp4 {RESET}")

    parser.add_argument("-iso", "--isolate", help=f"Specify file types to isolate\
                        for conversion, only works if directory is provided as input for the {FCYAN}convert_doc{RESET} argument example: {DYELLOW}filemac --convert_doc /home/user/Documents/ --isolate pdf -t txt{RESET}")

    parser.add_argument(
        "-Av", "--Analyze_video", help=f"Analyze a given video.\
        example: {DYELLOW}filemac --analyze_video example.mp4 {RESET}")

    parser.add_argument("-tf", "--target_format",
                        help="Target format for conversion (optional)")

    parser.add_argument(
        "--resize_image", help=f"change size of an image compress/decompress \
        example: {DYELLOW}filemac --resize_image example.png -t_size 2mb -t png {RESET}")

    parser.add_argument("-t_size", help="used in combination with resize_image \
                        to specify target image size")

    parser.add_argument(
        "-S", "--scan", help=f"Scan pdf file and extract text\
                        example: {DYELLOW}filemac --scan example.pdf {RESET}")

    parser.add_argument(

        "-doc2L", "--doc_long_image", help=f"Convert pdf file to long image\
                        example: {DYELLOW}filemac --doc_long_image example.pdf {RESET}")

    parser.add_argument(
        "-SA", "--scanAsImg", help=f"Convert pdf to image then extract text\
                        example: {DYELLOW}filemac --scanAsImg example.pdf {RESET}")

    parser.add_argument(
        "-SALI", "--scanAsLong_Image", help=f"Scan {CYAN}[doc, docx, pdf]\
        {RESET} file and extract text by first converting them to long image,-> very effective\
                    example: {DYELLOW}filemac --scanAsImg example.pdf {RESET}")

    parser.add_argument("--OCR", help=f"Extract text from an image.\
        example: {DYELLOW}filemac --OCR image.png{RESET}")

    '''Audio join  arguements'''
    # Accept 0 or more arguements
    parser.add_argument("--AudioJoin", "-AJ", nargs='*',
                        help="Join Audio files into one master file")

    ''''arguements for Advanced text to word conversion'''
    parser.add_argument('-AT2W', "--Atext2word", help=f'Advanced Text to word conversion i.e:{
                        DYELLOW}filemac --Atext2word example.txt --font_size 12 --font_name Arial{RESET}')

    # Add arguments that must accompany the "obj" command
    parser.add_argument('--font_size', type=int, default=12, help=F'Font size to be used default: \
                            {CYAN}12{RESET}')
    parser.add_argument('--font_name', type=str, default="Times New Roman", help=f"Font name default: \
                            {CYAN}Times New Roman{RESET}")

    '''Alternative sequence args, critical redundancy measure'''
    parser.add_argument('--use_extras', action='store_true', help=f"Use alternative conversion method: Overides\
                        default method i.e: {DYELLOW}filemac --convert_doc example.docx --use_extras -t pdf{RESET}")

    '''Pdf join arguements--> Accepts atleast 1 arguement'''
    parser.add_argument("--pdfjoin", '-pj', nargs='+',
                        help="Join Pdf file to one file")
    parser.add_argument("--order", type=str, default='AAB', help=f"Order of pages when joining the pdf use: {DYELLOW}filemac\
                        -pj help for more details{RESET}")
    parser.add_argument('--extract_pages', '-XP', nargs='+', help=f"Extract given pages from pdf: {
                        DYELLOW}filemac --extract_pages file.pdf 6 10{RESET} for one page: {DYELLOW}filemac --extract_pages file.pdf 5{RESET}")

    parser.add_argument("--manipulate_audio", "-MA", action="store_true",
                        help=f"Change audio voice/apply effects/reduce noise{DYELLOW}-MA --help for options{RESET}")
    parser.add_argument("--no-resume", action="store_false", dest="no_resume", help=f"Don't Resume previous File operation {DYELLOW}filemac --convert_doc simpledir --no-resume{RESET}")
    parser.add_argument('--threads', "-t", type=int, default=3, help=f"Number of threads for text to speech  {DYELLOW}filemac --convert_doc simpledir --no-resume -t 2{RESET}")

    # Use parse_known_args to allow unknown arguments (for later tunneling)
    args = parser.parse_args()

# Call function to handle document conversion inputs before begining conversion
    if args.convert_doc and args.convert_doc[0] == 'help':
        print(SUPPORTED_DOC_FORMATS)
        sys.exit(1)

    if args.convert_doc and args.target_format is not None:
        if args.use_extras:
            MakeConversion.word2pdf_extra(args.convert_doc)

        if len(args.convert_doc) <= 1 and not os.path.isdir(args.convert_doc[0]) and isinstance(args.convert_doc, list) and args.target_format in SUPPORTED_AUDIO_FORMATS_DIRECT:
            Batch_Audiofy(args.convert_doc, args.no_resume, args.threads)

        elif os.path.isdir(args.convert_doc[0]):
            conv = _DIR_CONVERSION_(
                args.convert_doc[0], args.target_format, args.no_resume, args.threads, args.isolate)
            conv._unbundle_dir_()

        elif os.path.isfile(args.convert_doc[0]):
            ev = Eval(args.convert_doc[0], args.target_format)
            ev.document_eval()


# Call function to handle video conversion inputs before begining conversion
    elif args.convert_video and args.convert_video == 'help':
        print(SUPPORTED_VIDEO_FORMATS_SHOW)
        sys.exit(1)
    elif args.convert_video and args.target_format is not None:
        ev = VideoConverter(args.convert_video, args.target_format)
        ev.CONVERT_VIDEO()
# Call function to handle image conversion inputs before begining conversion

    elif args.convert_image:
        if args.convert_image == 'help':
            print(SUPPORTED_IMAGE_FORMATS_SHOW)
            sys.exit(1)
        if args.target_format is None:
            print(f"{RED}Please provide output format specified by{
                  CYAN} '-t'{RESET}")
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
    if args.convert_audio == 'help':
        print(SUPPORTED_AUDIO_FORMATS_SHOW)
        sys.exit(1)
    elif args.convert_audio and args.target_format is not None:
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

# Call joinaudio script
    elif args.AudioJoin:
        from .JoinAudios import JoinAudios
        joiner = JoinAudios(args.AudioJoin)
        joiner.worker()

# Call Advanced text to word converter
    elif args.Atext2word:
        from .AT2Word import AdvancedT2word
        init = AdvancedT2word(args.Atext2word, None,
                              args.font_size, args.font_name)
        init.text_to_word()

# call for pdf join implementation
    elif args.pdfjoin:
        from .combinepdf import pdfmaster
        '''if len(args.pdfjoin) > 2 and args.order in {'AAB', 'BBA', 'AA', 'BB'}:
            init = pdfmaster(args.pdfjoin)
            init.controller()'''

        if args.pdfjoin[0].lower().strip() == 'help':
            from .combinepdf import helpmaster
            opts, helper, example = helpmaster()
            print(f"{opts}\n {helper}\n {example}")
            sys.exit(0)

        init = pdfmaster(args.pdfjoin, None, None, args.order)
        init.controller()
    elif args.extract_pages:
        init = _entry(args.extract_pages)

    elif args.manipulate_audio:
        print("implementation underway")
        exit(1)
        command = []
        subcommand = input(f":{DYELLOW}")
        # command = [val for val in subcommand.split(' ')]
        while ';' not in str(subcommand):
            command.append(subcommand)
            subcommand = input(f":{DYELLOW}")
        print(tuple(command))


if __name__ == "__main__":
    main()
