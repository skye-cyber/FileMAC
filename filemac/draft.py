import PyPDF2


def combine_pdfs(pdf_list, output_pdf):
    pdf_writer = PyPDF2.PdfWriter()

    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as out_pdf:
        pdf_writer.write(out_pdf)


if __name__ == "__main__":
    pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']  # List of PDF files to combine
    output_file = 'combined.pdf'

    combine_pdfs(pdf_files, output_file)
    print(f"PDFs combined into {output_file}")


'''To rearrange the pages of multiple PDF files as you described (e.g., 1A, 1B, 2A, 2B), you can adjust the script to specify the order of pages you want in the final output.

Page Order: The page_order list specifies which pages to include from which PDFs. Each tuple in the list represents (pdf_index, page_num), where pdf_index is the index of the PDF in pdf_files, and page_num is the page number in that PDF.
Reading PDFs: The script reads each PDF into a list of PdfReader objects (pdf_readers).
Adding Pages: It iterates through the page_order list, adding pages to the PdfWriter object according to the specified order.
Writing the Combined PDF: The combined PDF is saved to the specified output_file.
'''


def combine_pdfs_with_order(pdf_list, page_order, output_pdf):
    pdf_writer = PyPDF2.PdfWriter()
    pdf_readers = [PyPDF2.PdfReader(pdf) for pdf in pdf_list]

    for page_ref in page_order:
        pdf_index, page_num = page_ref
        pdf_reader = pdf_readers[pdf_index]
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as out_pdf:
        pdf_writer.write(out_pdf)


if __name__ == "__main__":
    pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']  # List of PDF files to combine
    page_order = [
        (0, 0),  # Page 0 from file1.pdf
        (0, 1),  # Page 1 from file1.pdf
        (1, 0),  # Page 0 from file2.pdf
        (1, 1)   # Page 1 from file2.pdf
    ]
    output_file = 'combined_rearranged.pdf'

    combine_pdfs_with_order(pdf_files, page_order, output_file)
    print(f"PDFs combined with specified page order into {output_file}")

