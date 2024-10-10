import aspose.words as aw

# pip install aspose-words
# sudo apt-get install libicu-dev


def convert_docx_to_pdf(docx_path, pdf_path):
    doc = aw.Document(docx_path)
    doc.save(pdf_path)


input_file = '/home/skye/Documents/Facial Recognition Attendance System Report.docx'
output_file = '/home/skye/Documents//your_document.pdf'
convert_docx_to_pdf(input_file, output_file)
