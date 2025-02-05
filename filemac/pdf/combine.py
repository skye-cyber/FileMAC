import os
import sys

import PyPDF2

from .colors import BWHITE, CYAN, DBLUE, FCYAN, RED, RESET, YELLOW


class pdfmaster:
    def __init__(self, obj1, obj2=None, outf=None, order='AA'):
        self.obj1 = obj1
        self.obj2 = obj2
        self.outf = outf
        self.order = order

        if self.outf is None:
            try:
                self.outf = os.path.join(os.path.join(os.path.split(self.obj1[0])[
                                         0], f"{os.path.split(self.obj1[0])[1].split('.')[0]}_{os.path.split(self.obj1[1])[1].split('.')[0]}_filemac.pdf"))
            except Exception:
                self.outf = "Filemac_pdfjoin.pdf"

    def controller(self):
        if self.order in {'AB', 'BA', 'ABA', 'BAB'}:
            self.combine_pdfs_ABA_interleave()
        elif self.order in {'AA', 'BB', 'AAB', 'BBA'}:
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
                        print(f"{CYAN}Page {DBLUE}{page_num + 1}/{len(reader.pages)}{RESET}", end='\r')
                        # Order pages in terms of page1-pd1, page2-pd2
                        page = reader.pages[page_num]
                        pdf_writer.add_page(page)

            with open(self.outf, 'wb') as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{FCYAN}PDFs combined with specified page order into{RESET}{DBLUE} {self.outf.name}{RESET}")
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{RED}{e}{RESET}")

    def combine_pdfs_AAB_order(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()
            reader1 = PyPDF2.PdfReader(self.obj1)
            reader2 = PyPDF2.PdfReader(self.obj2)
            # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

            print(F"{CYAN}File A{RESET}")
            for p1_num in range(len(reader1.pages)):
                print(f"Page {p1_num + 1}/{len(reader1.pages)}", end='\r')
                p1 = reader1.pages[p1_num]
                # Order pages in terms of page1-pd1, page2-pd2
                pdf_writer.add_page(p1)

            print(F"\n{CYAN}File B{RESET}")
            for p2_num in range(len(reader2.pages)):
                print(f"Page {p2_num + 1}/{len(reader2.pages)}", end='\r')
                p2 = reader2.pages[p2_num]
                pdf_writer.add_page(p2)

            with open(self.outf, 'wb') as self.outf:
                pdf_writer.write(self.outf)
            print(
                f"\n{FCYAN}PDFs combined with specified page order into{RESET}{DBLUE} {self.outf.name}{RESET}")
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{RED}{e}{RESET}")

    def merge_All_AAB(self):
        try:
            pdf_writer = PyPDF2.PdfWriter()

            # List to store the reader objects
            pdf_readers = [PyPDF2.PdfReader(file) for file in self.obj1]

            # max_pages = max(len(reader.pages) for reader in pdf_readers)

            for reader in pdf_readers:
                for page_num in range(len(reader.pages)):

                    print(f"{BWHITE}Page {CYAN}{page_num + 1}/{len(reader.pages)}{RESET}", end='\r')
                    page = reader.pages[page_num]
                    pdf_writer.add_page(page)

            # Write the merged PDF to the output file
            with open(self.outf, 'wb') as out_file:
                pdf_writer.write(out_file)
            print(
                f"\n{FCYAN}PDFs combined with specified page order into{RESET}{DBLUE} {self.outf}{RESET}")
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{RED}{e}{RESET}")


def helpmaster():
    options = f'''
        _________________________
        {BWHITE}|Linear: {YELLOW}AA/BB/AAB/BBA{RESET}  |
        {BWHITE}|Shifted: {YELLOW}AB/BA/ABA/BAB{RESET} |
        _________________________'''

    helper = f'''\n\t---------------------------------------------------------------------------------------------
        {BWHITE}|Currently There are 2 supported methods: {FCYAN}Linear and Alternating/shifting.{RESET}\t\t    |
        |-------------------------------------------------------------------------------------------|
        {BWHITE}|->Linear pages are ordered in form of: {CYAN}File1Page1,...Fil1Pagen{RESET} then {CYAN}File2Page1,...Fil2Pagen{RESET}|\n\t{BWHITE}|File2 is joined at the end of the file1.\t\t\t\t\t\t    |
        |-------------------------------------------------------------------------------------------|
        {BWHITE}|->Shifting method Picks: {CYAN}File1Page1, File2Page1...File1pagen,File2Pagen{RESET}\t\t    |
        |--------------------------------------------------------------------------------------------'''

    ex = f'''\t_____________________________________________________
    \t|->{DBLUE}filemac --pdfjoin file1.pdf file2.pdf --order AAB{RESET}|
    \t-----------------------------------------------------'''
    return options, helper, ex


if __name__ == "__main__":
    init = pdfmaster('/home/skye/Documents/FMAC/file2.pdf',
                     '/home/skye/Documents/FMAC/file1.pdf', order='ABA')
    init.controller()
