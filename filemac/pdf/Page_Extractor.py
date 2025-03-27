#!/usr/bin/python3
"""Extract pages specified by pange range from a pdf file and save them as a new file"""

import PyPDF2

from utils.colors import foreground, background

fcl = foreground()
bcl = background()
RESET = fcl.RESET


class Extractor:
    """
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
            print(f"[{bcl.BRED_FG}-{RESET}] {fcl.RED_FG}{e}{RESET}")
        except Exception as e:
            print(e)
            # raise


def _entry(kwargs):
    """
    Args:
    kwargs type: list - Contains Upper and lower limit (first and last page)
    Returns:
    None
    """
    if len(kwargs) > 2:
        arg1, arg2, arg3 = kwargs
        init = Extractor(arg1, int(arg2), int(arg3))
        init.getPages()
    elif len(kwargs) == 2:
        (
            arg1,
            arg2,
        ) = kwargs
        init = Extractor(arg1, int(arg2))
        init.getPages()
    else:
        pass


if __name__ == "__main__":
    pdf = "/home/skye/Documents/Reports/WAmbua_SC_Report.pdf"
    init = _entry([pdf, 5, 10])
