# convert pdf to long image
import os
import subprocess

from .colors import DGREEN, DMAGENTA, DYELLOW, RESET, YELLOW
from .converter import MakeConversion
from pdf2image import convert_from_path
from PIL import Image  # ImageSequence


class LImage:
    def __init__(self, doc):
        self.doc = doc

    def preprocess(self):
        doc = self.doc
        ext = doc.split('.')[-1].lower()
        if ext == "pdf":
            LImage.pdf_2L_Img(doc)
        if ext == 'doc' or ext == 'docx':
            conv = MakeConversion(doc)
            pdf = conv.word_to_pdf()
            LImage.pdf_2L_Img(pdf)

        elif ext == 'odt':
            pdf_file = ext = doc.split('.')[0] + 'docx'
            pdf = subprocess.call(['soffice', '--headless', '--convert-to',
                                   'pdf', '--outdir', os.path.dirname(pdf_file),
                                   os.path.abspath(doc)])
            LImage.pdf_2L_Img(pdf)
        else:
            print(f"Unsupported format: {ext}")

    @staticmethod
    def pdf_2L_Img(pdf_file):
        print(f"{YELLOW}Read pdf ..{RESET}")
        images = convert_from_path(pdf_file)
        out_img = pdf_file[:-4] + '.png'
        heights = [img.size[1] for img in images]
        total_height = sum(heights)
        max_width = max([img.size[0] for img in images])

        new_im = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for img in images:
            new_im.paste(img, (0, y_offset))
            y_offset += img.size[1]
        print(f"{DYELLOW}Save dest: {DMAGENTA}{out_img}{RESET}")
        new_im.save(out_img)
        print(f"{DGREEN}Done{RESET}")
        return new_im


l = LImage('/home/skye/Documents/test.pdf')
l.preprocess()
