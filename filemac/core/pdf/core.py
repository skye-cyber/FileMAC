import os
import subprocess
import sys

import PyPDF2
from pdf2image import convert_from_path
from PIL import Image  # ImageSequence
from tqdm.auto import tqdm
from ...utils.simple import logger
from ..document import DocConverter
from ..exceptions import FilemacError, FileSystemError
from ...utils.colors import fg, bg, rs
from ..ocr import ExtractText


RESET = rs
DEFAULT_SEPARATOR = "\n"


class PDF2LongImageConverter:
    def __init__(self, doc):
        self.document = doc

    def preprocess(self):
        ext = self.doc.split(".")[-1].lower()
        if ext == "pdf":
            long_image = self.convert(self.doc)
            return long_image
        if ext == "doc" or ext == "docx":
            conv = DocConverter(self.doc)

            path = conv.word_to_pdf()
            long_image = self.convert(path)
            return long_image
        elif ext == "odt":
            return self.subprocess_executor()

    def subprocess_executor(self):
        # pdf_file = ext = doc.split('.')[0] + 'docx'
        logger.info(f"{fg.DCYAN}Invoked soffice ..{RESET}")
        subprocess.call(
            [
                "soffice",
                "--convert-to",
                "pdf",
                self.document,
                "--outdir",
                os.path.dirname(self.document),
            ]
        )
        pdf_file = os.path.abspath(
            os.path.dirname(self.document)
            + "/"
            + (self.document.split("/")[-1].split(".")[0])
            + ".pdf"
        )
        long_image = self.convert(pdf_file)
        return long_image

    @staticmethod
    def convert(pdf_file):
        try:
            logger.info(f"{fg.BYELLOW}Read pdf{RESET}")
            images = convert_from_path(pdf_file)
            out_img = pdf_file[:-4] + ".png"
            heights = [img.size[1] for img in images]
            total_height = sum(heights)
            max_width = max([img.size[0] for img in images])

            logger.info(f"{fg.DCYAN}Draw image ..{RESET}")
            new_im = Image.new("RGB", (max_width, total_height))

            y_offset = 0
            for i, img in enumerate(images):
                logger.info(f"{fg.BBLUE}{i}{RESET}", end="\r")
                new_im.paste(img, (0, y_offset))
                y_offset += img.size[1]
            logger.info(f"{fg.BYELLOW}Save dest: {fg.BMAGENTA}{out_img}{RESET}")
            new_im.save(out_img)
            logger.info(f"{fg.BGREEN}Success😇✅{RESET}")
            return out_img
        except FileNotFoundError:
            raise FileSystemError(f"{fg.RED}File not found!{RESET}")
        except KeyboardInterrupt:
            logger.DEBUG("\nQuit❕")
            sys.exit()
        except Exception as e:
            raise FilemacError(f"{fg.RED}{e}{RESET}")


class PageExtractor:
    """
    Extract pages specified by pange range from a pdf file and save them as a new file
    Args:
        Pdf -> pdf file to be operated on.
        Llimit -> lower limit, the start page for extraction
        Ulimit -> upper limit, the end of extraction. Only one page (Llimit) is extracted ifnoUlimit is specified
        Range of pages to be extracted is given by Llimit and Ulimit inclusive
    Returns:
        outf-> the output file contsining the extracted pages
    """

    def __init__(
        self,
        pdf,
        Llimits: int,
        Ulimit: int = None,
    ):
        limits = [Llimits, Ulimit]
        self.pdf = pdf
        self.start = limits[0] - 1
        self.stop = limits[-1]

        self.outf = f"{pdf.split('.')[0]}_{self.start}_{self.stop}_extract.pdf"

        if self.stop is None:
            self.start = self.start
            self.stop = self.start + 1
            self.outf = f"{pdf.split('.')[0]}_{self.start + 1}_extract.pdf"

    def getPages(self):
        """
        Extract the the page range. Write the pages to new pdf file
        if self.stop (Ulimit) == -1 all pages are extracted from the Llimit to the last Page
        """
        try:
            reader = PyPDF2.PdfReader(self.pdf)

            if self.stop == -1:
                self.stop = len(reader.pages)

            pdf_writer = PyPDF2.PdfWriter()
            print(f"{fg.BBLUE}[🤖]{fg.BBLUE} Extracting:{RESET}")
            for page_num in range(self.start, self.stop):
                print(
                    f"{fg.BBLUE}[📄]{RESET}{fg.DCYAN}Page {page_num + 1}{RESET}"
                )
                page = reader.pages[page_num]
                pdf_writer.add_page(page)

            # Write the merged PDF to the output file
            with open(self.outf, "wb") as out_file:
                pdf_writer.write(out_file)
            print(
                f"{fg.BBLUE}[+]{RESET} {fg.BWHITE}File {fg.BMAGENTA}{self.outf}{RESET}"
            )
            return self.outf
        except KeyboardInterrupt:
            print("\n [!] Quit")
            exit(2)
        except FileNotFoundError as e:
            print(f"[{bg.BRED}-{RESET}] {fg.RED}{e}{RESET}")
        except Exception as e:
            print(e)
            # raise

    @staticmethod
    def _entry_(kwargs):
        """
        Args:
        kwargs type: list - Contains Upper and lower limit (first and last page)
        Returns:
        None
        """
        if len(kwargs) > 2:
            arg1, arg2, arg3 = kwargs
            init = PageExtractor(arg1, int(arg2), int(arg3))
            init.getPages()
        elif len(kwargs) == 2:
            (
                arg1,
                arg2,
            ) = kwargs
            init = PageExtractor(arg1, int(arg2))
            init.getPages()
        else:
            pass


class PDFCombine:
    def __init__(self, obj1, obj2=None, outf=None, order="AA"):
        self.obj1 = obj1
        self.obj2 = obj2
        self.outf = outf
        self.order = order

        if self.outf is None:
            try:
                self.outf = os.path.join(
                    os.path.join(
                        os.path.split(self.obj1[0])[0],
                        f"{os.path.split(self.obj1[0])[1].split('.')[0]}_{os.path.split(self.obj1[1])[1].split('.')[0]}_filemac.pdf",
                    )
                )
            except Exception:
                self.outf = "Filemac_pdfjoin.pdf"

    def controller(self):
        if self.order in {"AB", "BA", "ABA", "BAB"}:
            self.combine_pdfs_ABA_interleave()
        elif self.order in {"AA", "BB", "AAB", "BBA"}:
            if type(self.obj1) is list:
                self.merge_All_AAB()
            else:
                self.combine_pdfs_AAB_order()

    def combine_pdfs_ABA_interleave(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()
            # Create PdfReader objects for each input PDF file
            pdf_readers = [PyPDF2.PdfReader(file) for file in self.obj1]

            max_pages = max(len(reader.pages) for reader in pdf_readers)
            # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

            for page_num in range(max_pages):
                for reader in pdf_readers:
                    if page_num < len(reader.pages):
                        print(
                            f"{fg.CYAN}Page {fg.BBLUE}{page_num + 1}/{len(reader.pages)}{RESET}",
                            end="\r",
                        )
                        # Order pages in terms of page1-pd1, page2-pd2
                        page = reader.pages[page_num]
                        pdf_writer.add_page(page)

            with open(self.outf, "wb") as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{fg.FCYAN}PDFs combined with specified page order into{RESET}{fg.BBLUE} {self.outf.name}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fg.RED}{e}{RESET}")

    def combine_pdfs_AAB_order(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()
            reader1 = PyPDF2.PdfReader(self.obj1)
            reader2 = PyPDF2.PdfReader(self.obj2)
            # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

            print(f"{fg.CYAN}File A{RESET}")
            for p1_num in range(len(reader1.pages)):
                print(f"Page {p1_num + 1}/{len(reader1.pages)}", end="\r")
                p1 = reader1.pages[p1_num]
                # Order pages in terms of page1-pd1, page2-pd2
                pdf_writer.add_page(p1)

            print(f"\n{fg.CYAN}File B{RESET}")
            for p2_num in range(len(reader2.pages)):
                print(f"Page {p2_num + 1}/{len(reader2.pages)}", end="\r")
                p2 = reader2.pages[p2_num]
                pdf_writer.add_page(p2)

            with open(self.outf, "wb") as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{fg.FCYAN}PDFs combined with specified page order into{RESET}{fg.BBLUE} {self.outf.name}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fg.RED}{e}{RESET}")

    def merge_All_AAB(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()

            # List to store the reader objects
            pdf_readers = [PyPDF2.PdfReader(file) for file in self.obj1]

            # max_pages = max(len(reader.pages) for reader in pdf_readers)

            for reader in pdf_readers:
                for page_num in range(len(reader.pages)):
                    print(
                        f"{fg.BWHITE}Page {fg.CYAN}{page_num + 1}/{len(reader.pages)}{RESET}",
                        end="\r",
                    )
                    page = reader.pages[page_num]
                    pdf_writer.add_page(page)

            # Write the merged PDF to the output file
            with open(self.outf, "wb") as out_file:
                pdf_writer.write(out_file)
            print(
                f"\n{fg.FCYAN}PDFs combined with specified page order into{RESET}{fg.BBLUE} {self.outf}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fg.RED}{e}{RESET}")


class Scanner:
    """Implementation of scanning to extract data from pdf files and images
    input_file -> file to be scanned pdf,image
    Args:
        input_file->file to be scanned
        no_strip-> Preserves text formating once set to True, default: False
    Returns:
        None"""

    def __init__(self, input_file, sep: str = DEFAULT_SEPARATOR):
        self.input_file = input_file
        self.sep = sep

    def preprocess(self):
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            for file in os.listdir(self.input_file):
                file_path = os.path.join(self.input_file, file)
                if os.path.isfile(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def scanPDF(self, obj=None):
        """Obj - object for scanning where the object is not a list"""
        pdf_list = self.preprocess()
        pdf_list = [item for item in pdf_list if item.lower().endswith("pdf")]
        if obj:
            pdf_list = [obj]

        for pdf in pdf_list:
            out_f = pdf[:-3] + "txt"
            print(f"{fg.YELLOW}Read pdf ..{RESET}")

            with open(pdf, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""

                pg = 0
                for page_num in range(len(reader.pages)):
                    pg += 1

                    print(f"{fg.BYELLOW}Progress:{RESET}", end="")
                    print(f"{fg.CYAN}{pg}/{len(reader.pages)}{RESET}", end="\r")
                    page = reader.pages[page_num]
                    text += page.extract_text()

            print(f"\n{text}")
            print(f"\n{fg.YELLOW}Write text to {fg.GREEN}{out_f}{RESET}")
            with open(out_f, "w") as f:
                f.write(text)

            print(f"\n{fg.BGREEN}Ok{RESET}")

    def scanAsImgs(self):
        file = self.input_file
        mc = DocConverter(file)
        img_objs = mc.doc2image()

        text = ""

        for i in tqdm(img_objs, desc="Extracting", leave=False):
            extract = ExtractText(i, self.sep)
            _text = extract.OCR()

            if _text is not None:
                text += _text
                with open(f"{self.input_file[:-4]}_filemac.txt", "a") as _writer:
                    _writer.write(text)

        def _cleaner_():
            print(f"{fg.FMAGENTA}Clean")
            for obj in img_objs:
                if os.path.exists(obj):
                    print(obj, end="\r")
                    os.remove(obj)
                txt_file = f"{obj[:-4]}.txt"
                if os.path.exists(txt_file):
                    print(f"{bg.CYAN_BG}{txt_file}{RESET}", end="\r")
                    os.remove(txt_file)

        _cleaner_()
        from ...utils.screen import clear_screen

        clear_screen()
        print(f"{bg.GREEN}Full Text{RESET}")
        print(text)
        print(
            f"{fg.BWHITE}Text File ={fg.IGREEN}{self.input_file[:-4]}_filemac.txt{RESET}"
        )
        print(f"{fg.GREEN}Ok✅{RESET}")
        return text

    def scanAsLongImg(self) -> bool:
        """Convert the pdf to long image for scanning - text extraction"""

        try:
            pdf_list = self.preprocess()
            pdf_list = [item for item in pdf_list if item.lower().endswith("pdf")]
            from ..pdf.core import PDF2LongImageConverter

            for file in pdf_list:
                converter = PDF2LongImageConverter(file)
                file = converter.preprocess()

                tx = ExtractText(file, self.sep)
                text = tx.OCR()
                if text is not None:
                    # print(text)
                    print(f"{fg.GREEN}Ok{RESET}")
            return True
        except Exception as e:
            print(e)
