# convert pdf to long image
import os
import subprocess
import sys

from pdf2image import convert_from_path
from PIL import Image  # ImageSequence

from utils.colors import foreground
from .pydocs import DocConverter

fcl = foreground()
RESET = fcl.RESET


class LImage:
    def __init__(self, doc):
        self.doc = doc

    def preprocess(self):
        doc = self.doc
        ext = doc.split(".")[-1].lower()
        if ext == "pdf":
            LI = LImage.pdf_2L_Img(doc)
            return LI
        if ext == "doc" or ext == "docx":
            conv = DocConverter(doc)

            path = conv.word_to_pdf()
            LI = LImage.pdf_2L_Img(path)
            return LI
        elif ext == "odt":
            # pdf_file = ext = doc.split('.')[0] + 'docx'
            print(f"{fcl.DCYAN_FG}Call soffice and wait ..{RESET}")
            subprocess.call(
                [
                    "soffice",
                    "--convert-to",
                    "pdf",
                    doc,
                    "--outdir",
                    os.path.dirname(doc),
                ]
            )
            pdf_file = os.path.abspath(
                os.path.dirname(doc) + "/" + (doc.split("/")[-1].split(".")[0]) + ".pdf"
            )
            LI = LImage.pdf_2L_Img(pdf_file)
            return LI

    @staticmethod
    def pdf_2L_Img(pdf_file):
        try:
            print(f"{fcl.BYELLOW_FG}Read pdf{RESET}")
            images = convert_from_path(pdf_file)
            out_img = pdf_file[:-4] + ".png"
            heights = [img.size[1] for img in images]
            total_height = sum(heights)
            max_width = max([img.size[0] for img in images])

            print(f"{fcl.DCYAN_FG}Draw image ..{RESET}")
            new_im = Image.new("RGB", (max_width, total_height))

            y_offset = 0
            for i, img in enumerate(images):
                print(f"{fcl.BBLUE_FG}{i}{RESET}", end="\r")
                new_im.paste(img, (0, y_offset))
                y_offset += img.size[1]
            print(f"{fcl.BYELLOW_FG}Save dest: {fcl.BMAGENTA_FG}{out_img}{RESET}")
            new_im.save(out_img)
            print(f"{fcl.BGREEN_FG}Success😇✅{RESET}")
            return out_img
        except FileNotFoundError:
            print(f"{fcl.RED_FG}File not found!{RESET}")
        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit()
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")
            return
