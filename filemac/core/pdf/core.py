import os
import subprocess
import sys
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image  # ImageSequence

from .utils.colors import foreground, background
from ..document import DocConverter
from ..exceptions import FileSystemError, FilemacError
from ...utils.simple import logger
from ...utils.helpmaster import pdf_combine_help

fcl = foreground()
bcl = background()
RESET = fcl.RESET


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
        logger.info(f"{fcl.DCYAN_FG}Invoked soffice ..{RESET}")
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
            logger.info(f"{fcl.BYELLOW_FG}Read pdf{RESET}")
            images = convert_from_path(pdf_file)
            out_img = pdf_file[:-4] + ".png"
            heights = [img.size[1] for img in images]
            total_height = sum(heights)
            max_width = max([img.size[0] for img in images])

            logger.info(f"{fcl.DCYAN_FG}Draw image ..{RESET}")
            new_im = Image.new("RGB", (max_width, total_height))

            y_offset = 0
            for i, img in enumerate(images):
                logger.info(f"{fcl.BBLUE_FG}{i}{RESET}", end="\r")
                new_im.paste(img, (0, y_offset))
                y_offset += img.size[1]
            logger.info(f"{fcl.BYELLOW_FG}Save dest: {fcl.BMAGENTA_FG}{out_img}{RESET}")
            new_im.save(out_img)
            logger.info(f"{fcl.BGREEN_FG}Success😇✅{RESET}")
            return out_img
        except FileNotFoundError:
            raise FileSystemError(f"{fcl.RED_FG}File not found!{RESET}")
        except KeyboardInterrupt:
            logger.DEBUG("\nQuit❕")
            sys.exit()
        except Exception as e:
            raise FilemacError(f"{fcl.RED_FG}{e}{RESET}")


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
            print(f"{fcl.BBLUE_FG}[🤖]{fcl.BBLUE_FG} Extracting:{RESET}")
            for page_num in range(self.start, self.stop):
                print(
                    f"{fcl.BBLUE_FG}[📄]{RESET}{fcl.DCYAN_FG}Page {page_num + 1}{RESET}"
                )
                page = reader.pages[page_num]
                pdf_writer.add_page(page)

            # Write the merged PDF to the output file
            with open(self.outf, "wb") as out_file:
                pdf_writer.write(out_file)
            print(
                f"{fcl.BBLUE_FG}[+]{RESET} {fcl.BWHITE_FG}File {fcl.BMAGENTA_FG}{self.outf}{RESET}"
            )
            return self.outf
        except KeyboardInterrupt:
            print("\n [!] Quit")
            exit(2)
        except FileNotFoundError as e:
            print(f"[{bcl.BRED_BG}-{RESET}] {fcl.RED_FG}{e}{RESET}")
        except Exception as e:
            print(e)
            # raise

    @staticmethod
    def _entry(kwargs):
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
                            f"{fcl.CYAN_FG}Page {fcl.BBLUE_FG}{page_num + 1}/{len(reader.pages)}{RESET}",
                            end="\r",
                        )
                        # Order pages in terms of page1-pd1, page2-pd2
                        page = reader.pages[page_num]
                        pdf_writer.add_page(page)

            with open(self.outf, "wb") as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{fcl.FCYAN_FG}PDFs combined with specified page order into{RESET}{fcl.BBLUE_FG} {self.outf.name}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")

    def combine_pdfs_AAB_order(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()
            reader1 = PyPDF2.PdfReader(self.obj1)
            reader2 = PyPDF2.PdfReader(self.obj2)
            # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

            print(f"{fcl.CYAN_FG}File A{RESET}")
            for p1_num in range(len(reader1.pages)):
                print(f"Page {p1_num + 1}/{len(reader1.pages)}", end="\r")
                p1 = reader1.pages[p1_num]
                # Order pages in terms of page1-pd1, page2-pd2
                pdf_writer.add_page(p1)

            print(f"\n{fcl.CYAN_FG}File B{RESET}")
            for p2_num in range(len(reader2.pages)):
                print(f"Page {p2_num + 1}/{len(reader2.pages)}", end="\r")
                p2 = reader2.pages[p2_num]
                pdf_writer.add_page(p2)

            with open(self.outf, "wb") as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{fcl.FCYAN_FG}PDFs combined with specified page order into{RESET}{fcl.BBLUE_FG} {self.outf.name}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")

    def merge_All_AAB(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()

            # List to store the reader objects
            pdf_readers = [PyPDF2.PdfReader(file) for file in self.obj1]

            # max_pages = max(len(reader.pages) for reader in pdf_readers)

            for reader in pdf_readers:
                for page_num in range(len(reader.pages)):
                    print(
                        f"{fcl.BWHITE_FG}Page {fcl.CYAN_FG}{page_num + 1}/{len(reader.pages)}{RESET}",
                        end="\r",
                    )
                    page = reader.pages[page_num]
                    pdf_writer.add_page(page)

            # Write the merged PDF to the output file
            with open(self.outf, "wb") as out_file:
                pdf_writer.write(out_file)
            print(
                f"\n{fcl.FCYAN_FG}PDFs combined with specified page order into{RESET}{fcl.BBLUE_FG} {self.outf}{RESET}"
            )
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")
