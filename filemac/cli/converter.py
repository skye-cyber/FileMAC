import os
import sys
from typing import List, Union
from ..core.warning import default_supressor
from ..utils.simple import logger
from ..utils.colors import fg, rs
from ..core.tts.gtts import GoogleTTS
from ..utils.formats import (
    SUPPORTED_AUDIO_FORMATS_DIRECT,
)
from ..core.document import DocConverter

RESET = rs
default_supressor()


class DirectoryConverter:
    """
    If the input file in convert_doc argument is a directory, walk throught the directory and
        converter all the surported files to the target format
    """

    def __init__(self, _dir_, _format_, no_resume, threads, _isolate_=None):
        self._dir_ = _dir_
        self._format_ = _format_
        self._isolate_ = _isolate_
        self.no_resume = no_resume
        self.threads = threads
        # Handle isolation and non isolation modes distinctively
        self._ls_ = (
            ["pdf", "docx", "doc", "xlsx", "ppt", "pptxxls", "txt"]
            if _isolate_ is None
            else [_isolate_]
        )
        if self._isolate_:
            print(
                f"INFO\t {fg.FMAGENTA}Isolate {fg.DCYAN}{self._isolate_}{RESET}"
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
                        print(
                            f"INFO\t {fg.FYELLOW}Parse {fg.BLUE}{_path_}{RESET}"
                        )
                        init = MethodMappingEngine(_path_, self._format_)
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
        conv = GoogleTTS(self.folder, resume=self.no_resume)
        inst = conv.THAudio(conv)
        inst.audiofy(num_threads=self.threads)


class MethodMappingEngine:
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
            print(f"{fg.RED}Unsupported output format❌{RESET}")

    def word(self, conv):
        if self.outf.lower() in ("txt", "text"):
            conv.word_to_txt()
        elif self.outf.lower() == "pdf":
            conv.word_to_pdf()
        elif self.outf.lower() in ("pptx", "ppt"):
            conv.word_to_pptx()
        elif self.outf.lower() in ("audio", "ogg"):
            conv = GoogleTTS(self.file)
            conv.audiofy()
        else:
            print(f"{fg.RED}Unsupported output format❌{RESET}")

    def text(self, conv):
        if self.outf.lower() == "pdf":
            conv.txt_to_pdf()
        elif self.outf.lower() in ("doc", "docx", "word"):
            conv.text_to_word()
        elif self.outf.lower() in ("audio", "ogg"):
            conv = GoogleTTS(self.file)
            conv.audiofy()
        else:
            print(f"{fg.RED}Unsupported output format❌{RESET}")

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
            conv = GoogleTTS(self.file)
            conv.audiofy()
        else:
            print(f"{fg.RED}Unsupported output format❌{RESET}")

    def pdf(self, conv):
        if self.outf.lower() in ("doc", "docx", "word"):
            conv.pdf_to_word()
        elif self.outf.lower() in ("txt", "text"):
            conv.pdf_to_txt()
        elif self.outf.lower() in ("audio", "ogg", "mp3", "wav"):
            conv = GoogleTTS(self.file)
            conv.audiofy()
        else:
            print(f"{fg.RED}Unsupported output format❌{RESET}")

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
                print(f"{fg.fg.BYELLOW}Unsupported Conversion type❌{RESET}")
                pass
        except Exception as e:
            logger.error(e)


def _isolate_file(_dir_, target):
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
