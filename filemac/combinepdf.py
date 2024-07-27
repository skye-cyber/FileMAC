import PyPDF2
import os


class pdfmaster:
    def __init__(self, pdf1, pdf2, outf=None, order='AA'):
        self.pdf1 = pdf1
        self.pdf2 = pdf2
        self.outf = outf
        self.order = order

        pdf_files = []
        if self.outf is None:
            # base = f"{os.path.split(self.pdf1)[1].split('.')[0]}_{os.path.split(self.pdf2)[1].split('.')[0]}"
            # self.outf = f"{os.path.join(os.path.split(self.pdf1)[0], base)}_filemac.pdf"
            self.outf = os.path.join(os.path.join(os.path.split(self.pdf1)[0], f"{os.path.split(self.pdf1)[1].split('.')[0]}_{os.path.split(self.pdf2)[1].split('.')[0]}_filemac.pdf"))

        if order == 'AA':
            pdf_files.append(self.pdf1)
            pdf_files.append(self.pdf2)

    def controller(self):
        if self.order in {'AB', 'BA', 'ABA', 'BAB'}:
            self.combine_pdfs_ABA_order()
        elif self.order in {'AA', 'AA', 'AAB', 'BBA'}:
            self.combine_pdfs_AAB_order()

    def combine_pdfs_ABA_order(self):
        pdf_writer = PyPDF2.PdfWriter()
        reader1 = PyPDF2.PdfReader(self.pdf1)
        reader2 = PyPDF2.PdfReader(self.pdf2)
        # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

        _lpdf = len(reader1.pages) if len(reader1.pages) > len(reader2.pages) else len(reader2.pages)
        for p1_num, p2_num in zip(range(len(reader1.pages)), range(len(reader2.pages))):
            print(f"Page {p1_num}______{p2_num} of {_lpdf}")
            # Order pages in terms of page1-pd1, page2-pd2
            p1 = reader1.pages[p1_num]
            pdf_writer.add_page(p1)
            p2 = reader2.pages[p2_num]
            pdf_writer.add_page(p2)

        with open(self.outf, 'wb') as self.outf:
            pdf_writer.write(self.outf)
        print(f"PDFs combined with specified page order into {self.outf.name}")

    def combine_pdfs_AAB_order(self):
        pdf_writer = PyPDF2.PdfWriter()
        reader1 = PyPDF2.PdfReader(self.pdf1)
        reader2 = PyPDF2.PdfReader(self.pdf2)
        # pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_files]

        print("File A")
        for p1_num in range(len(reader1.pages)):
            print(f"Page {p1_num}/{len(reader1.pages)}", end='\r')
            p1 = reader1.pages[p1_num]
            # Order pages in terms of page1-pd1, page2-pd2
            pdf_writer.add_page(p1)

        print("File A")
        for p2_num in range(len(reader2.pages)):
            print(f"Page {p2_num}/{len(reader2.pages)}", end='\r')
            p2 = reader2.pages[p2_num]
            pdf_writer.add_page(p2)

        '''for page_ref in page_order:
            pdf_index, page_num = page_ref
            pdf_reader = pdf_readers[pdf_index]
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)'''

        with open(self.outf, 'wb') as self.outf:
            pdf_writer.write(self.outf)
        print(f"PDFs combined with specified page order into {self.outf}")


if __name__ == "__main__":
    init = pdfmaster('/home/skye/Documents/FMAC/file2.pdf', '/home/skye/Documents/FMAC/file1.pdf', order='ABA')
    init.controller()
