import PyPDF2
from colors import RESET, DGREEN, YELLOW, DYELLOW, CYAN


def scanPDF(pdf):
    out_f = pdf[:-4]
    print(f"{YELLOW}Read pdf ..{RESET}")
    with open(pdf, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''

        for page_num in range(len(reader.pages)):
            print(f"{DYELLOW}Progress:{RESET}", end="")
            print(f"{CYAN}{reader.pages[page_num]}/{len(reader.pages)}{RESET}", end="\r")
            page = reader.pages[page_num]
            text += page.extract_text()
    print(text)
    print(F"\n{YELLOW}write text to {out_f}{RESET}")
    with open(out_f, 'w') as f:
        f.write(text)
    print(F"{DGREEN}Ok{RESET}")


scanPDF('/home/skye/Documents/test.pdf')
