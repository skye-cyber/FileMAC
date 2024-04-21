#############################################################################
import logging
import logging.handlers
# import math
import os
import re
import sqlite3
import subprocess
import sys
import time
import traceback
# import pdfminer.high_level
# from typing import Iterable
from pdf2image import convert_from_path
import cv2
import pandas as pd
import pydub
import PyPDF2
# import pytesseract
import requests
import speedtest
from docx import Document
# from pydub.playback import play
from gtts import gTTS
# from PyPDF2 import PdfFileReader
from moviepy.editor import VideoFileClip
from pdf2docx import parse
from PIL import Image
from pptx import Presentation
from pydub import AudioSegment
from .colors import (RESET, GREEN, DGREEN, YELLOW, DYELLOW, CYAN, BLUE, DBLUE,
                     MAGENTA, DMAGENTA, RED, DRED, ICYAN)
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate

from .formats import (SUPPORTED_AUDIO_FORMATS, SUPPORTED_IMAGE_FORMATS,
                      SUPPORTED_VIDEO_FORMATS)

# import pygame
# from aspose.words import Document as aspose_document
# from aspose.slides import Presentation as aspose_presentation
# from show_progress import progress_show
# from PIL import ImageDraw, ImageFont
###############################################################################

PYGAME_DETECT_AVX2 = 1
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


class MakeConversion:

    '''Initialize the class'''

    def __init__(self, input_file):
        self.input_file = input_file

    '''Check input object whether it's a file or a directory if a file append
    the file to a set and return it otherwise append directory full path
    content to the set and return the set file. The returned set will be
    evaluated in the next step as required on the basis of requested operation
    For every requested operation, the output file if any is automatically
    generated on the basis of the input filename and saved in the sam
    directory as the input file
    '''

    def preprocess(self):
        try:
            files_to_process = []

            if os.path.isfile(self.input_file):
                files_to_process.append(self.input_file)
            elif os.path.isdir(self.input_file):
                if os.listdir(self.input_file) is None:
                    print("Cannot work with empty folder")
                    sys.exit(1)
                for file in os.listdir(self.input_file):
                    file_path = os.path.join(self.input_file, file)
                    if os.path.isfile(file_path):
                        files_to_process.append(file_path)

            return files_to_process
        except Exception as e:
            print(e)

###############################################################################
# Convert word file to pdf document (docx)
###############################################################################
    def word_to_pdf(self):
        word_list = self.preprocess()
        ls = ["doc", "docx"]
        word_list = [
            item for item in word_list if any(item.lower().endswith(ext) for ext in ls)]
        for word_file in word_list:
            if word_file.lower().endswith("doc"):
                pdf_file = word_file[:-3] + "pdf"
            elif word_file.lower().endswith("docx"):
                pdf_file = word_file[:-4] + "pdf"

            try:
                print(
                    f'{BLUE}Converting: {RESET}{word_file} {BLUE}to {RESET}{pdf_file}')
                if os.name == 'posix':  # Check if running on Linux
                    # Use subprocess to run the dpkg and grep commands
                    result = subprocess.run(
                        ['dpkg', '-l', 'libreoffice'], stdout=subprocess.PIPE, text=True)
                    if result.returncode != 0:
                        print(
                            "Please install libreoffice to use this functionality !")
                        sys.exit(1)
                    subprocess.run(['soffice', '--convert-to',
                                   'pdf', word_file, pdf_file])
                    # print(f"{DMAGENTA} Successfully converted {word_file} to {pdf_file}{RESET}")
                elif os.name == "nt":
                    try:
                        from docx2pdf import convert
                    except ImportError:
                        print("Run pip install docx2pdf for this function to work")
                        sys.exit(1)
                    convert(word_file, pdf_file)
                    print(
                        f"{DMAGENTA} Successfully converted {word_file} to {pdf_file}{RESET}")

            except Exception as e:
                print(f"Error converting {word_file} to {pdf_file}: {e}")

###############################################################################
# Convert pdf file to word document (docx)
###############################################################################
    def pdf_to_word(self):
        pdf_list = self.preprocess()
        pdf_list = [item for item in pdf_list if item.lower().endswith("pdf")]
        for pdf_file in pdf_list:
            if pdf_file.lower().endswith("pdf"):
                word_file = pdf_file[:-3] + "docx"

            try:

                parse(pdf_file, word_file, start=0, end=None)

                print(f'{GREEN}Converting to word..{RESET}', end='\r')

                logger.info(f"{DMAGENTA} Successfully converted{pdf_file} \
to {word_file}{RESET}")
            except KeyboardInterrupt:
                print("\nExiting..")
                sys.exit(1)
            except Exception as e:
                logger.info(f'{DRED}All conversion attempts have failed: \
{e}{RESET}')

###############################################################################
# Convert text file(s) to pdf document (docx)
###############################################################################
    def txt_to_pdf(input_file, output_file):
        """Convert a .txt file to a PDF."""

        # Read the contents of the input .txt file
        with open(input_file, 'r', encoding='utf-8') as file:
            text_contents = file.readlines()

        # Initialize the PDF document
        doc = SimpleDocTemplate(output_file, pagesize=letter)

        # Create a story to hold the elements of the PDF
        story = []

        # Iterate through each line in the input .txt file and add it to the PDF
        for line in text_contents:
            story.append(Paragraph(line.strip(), style="normalText"))

        # Build and write the PDF document
        doc.build(story)

###############################################################################
# Convert word file(s) to pptx document (pptx/ppt)
###############################################################################
    def word_to_pptx(self):
        word_list = self.preprocess()
        word_list = [item for item in word_list if item.lower().endswith(
            "docx") or item.lower().endswith("doc")]

        for word_file in word_list:

            if word_list is None:
                print("Please provide appropriate file type")
                sys.exit(1)
            if word_file.lower().endswith("docx"):
                pptx_file = word_file[:-4] + "pptx"
            elif word_file.lower().endswith("doc"):
                pptx_file = word_file[:-3] + "pptx"
            try:
                # Load the Word document
                print(F"{DYELLOW}Load the Word document..{RESET}")
                doc = Document(word_file)

                # Create a new PowerPoint presentation
                print(F"{DYELLOW}Create a new PowerPoint presentation..{RESET}")
                prs = Presentation()

                # Iterate through each paragraph in the Word document
                print(
                    f"{DGREEN}Populating pptx slides with {DYELLOW}{len(doc.paragraphs)}{DGREEN} entries..{RESET}")
                count = 0
                for paragraph in doc.paragraphs:
                    count += 1
                    perc = (count/len(doc.paragraphs))*100
                    print(
                        f"{DMAGENTA}Progress:: \033[1;36m{perc:.2f}%{RESET}", end="\r")
                    # Create a new slide in the PowerPoint presentation
                    slide = prs.slides.add_slide(prs.slide_layouts[1])

                    # Add the paragraph text to the slide
                    slide.shapes.title.text = paragraph.text

                # Save the PowerPoint presentation
                prs.save(pptx_file)
                print(f"\n{DGREEN}Done{RESET}")
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(1)
            except KeyboardInterrupt:
                print("\nExiting..")
                sys.exit(1)
            except Exception as e:
                logger.error(e)

###############################################################################
# Convert word file to txt file'''
###############################################################################

    def word_to_txt(self):
        word_list = self.preprocess()
        word_list = [item for item in word_list if item.lower().endswith(
            "docx") or item.lower().endswith("doc")]
        for file_path in word_list:
            if file_path.lower().endswith("docx"):
                txt_file = file_path[:-4] + "txt"
            elif file_path.lower().endswith("doc"):
                txt_file = file_path[:-3] + "txt"
            try:
                doc = Document(file_path)
                print("INFO Processing...")

                with open(txt_file, 'w', encoding='utf-8') as f:
                    Par = 0
                    for paragraph in doc.paragraphs:
                        f.write(paragraph.text + '\n')
                        Par += 1

                        print(f"Par:{BLUE}{Par}/{len(doc.paragraphs)}{RESET}", end='\r')
                    logger.info(f"{DMAGENTA}Conversion of file to txt success{RESET}")

            except KeyboardInterrupt:
                print("\nExit")
                sys.exit()
            except Exception as e:
                logger.error(
                    f"Dear user something went amiss while attempting the conversion:\n {e}")
                with open("conversion.log", "a") as log_file:
                    log_file.write(f"Couldn't convert {file_path} to {txt_file}:\
REASON->{e}")

###############################################################################
# Convert pdf file to text file
###############################################################################
    def pdf_to_txt(self):
        pdf_list = self.preprocess()
        pdf_list = [item for item in pdf_list if item.lower().endswith("pdf")]
        for file_path in pdf_list:
            txt_file = file_path[:-3] + "txt"
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                    logger.info(f"{DMAGENTA}Successfully converted {file_path} to \
{txt_file}{RESET}")
            except Exception as e:
                logger.error(
                    f"Oops somethin went astray while converting {file_path} \
to {txt_file}: {e}")
                with open("conversion.log", "a") as log_file:
                    log_file.write(
                        f"Error converting {file_path} to {txt_file}: {e}\n")

###############################################################################
# Convert ppt file to word document
###############################################################################
    def ppt_to_word(self):
        ppt_list = self.preprocess()
        ppt_list = [item for item in ppt_list if item.lower().endswith(
            "pptx") or item.lower().endswith("ppt")]
        for file_path in ppt_list:
            if file_path.lower().endswith("pptx"):
                word_file = file_path[:-4] + "docx"
            elif file_path.lower().endswith("ppt"):
                word_file = file_path[:-3] + "docx"
            try:
                presentation = Presentation(file_path)
                document = Document()

                for slide in presentation.slides:
                    for shape in slide.shapes:
                        if shape.has_text_frame:
                            text_frame = shape.text_frame
                            for paragraph in text_frame.paragraphs:
                                new_paragraph = document.add_paragraph()
                                for run in paragraph.runs:
                                    new_run = new_paragraph.add_run(run.text)
                                    # Preserve bold formatting
                                    new_run.bold = run.font.bold
                                    # Preserve italic formatting
                                    new_run.italic = run.font.italic
                                    # Preserve underline formatting
                                    new_run.underline = run.font.underline
                                    # Preserve font name
                                    new_run.font.name = run.font.name
                                    # Preserve font size
                                    new_run.font.size = run.font.size
                                    try:
                                        # Preserve font color
                                        new_run.font.color.rgb = run.font.color.rgb
                                    except AttributeError:
                                        # Ignore error and continue without
                                        # setting the font color
                                        pass
                            # Add a new paragraph after each slide
                            document.add_paragraph()
                document.save(word_file)
                logger.info(f"{DMAGENTA}Successfully converted {file_path} to \
        {word_file}{RESET}")
            except Exception as e:
                logger.error(
                    f"Oops somethin gwent awry while attempting to convert \
        {file_path} to {word_file}:\n>>>{e}")
                with open("conversion.log", "a") as log_file:
                    log_file.write(
                        f"Oops something went astray while attempting \
        convert {file_path} to {word_file}:{e}\n")

###############################################################################
# Convert text file to word
###############################################################################
    def text_to_word(self):
        flist = self.preprocess()
        flist = [item for item in flist if item.lower().endswith("txt")]
        for file_path in flist:
            if file_path.lower().endswith("txt"):
                word_file = file_path[:-3] + "docx"

            try:
                # Read the text file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    text_content = file.read()

                # Filter out non-XML characters
                filtered_content = re.sub(
                    r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]+', '', text_content)

                # Create a new Word document
                doc = Document()
                # Add the filtered text content to the document
                doc.add_paragraph(filtered_content)

                # Save the document as a Word file
                doc.save(word_file)
                logger.info(f"{DMAGENTA}Successfully converted {file_path} to \
        {word_file}{RESET}")
            except FileExistsError as e:
                logger.error(f"{str(e)}")
            except Exception as e:
                logger.error(
                    f"Oops Unable to perfom requested conversion: {e}\n")
                with open("conversion.log", "a") as log_file:
                    log_file.write(
                        f"Error converting {file_path} to {word_file}: \
{e}\n")

###############################################################################
# Convert xlsx file(s) to word file(s)
###############################################################################
    def convert_xls_to_word(self):
        xls_list = self.preprocess()
        ls = ["xlsx", "xls"]
        xls_list = [item for item in xls_list if any(
            item.lower().endswith(ext) for ext in ls)]
        print(F"{DGREEN}Initializing conversion sequence{RESET}")
        for xls_file in xls_list:
            if xls_file.lower().endswith("xlsx"):
                word_file = xls_file[:-4] + "docx"
            elif xls_file.lower().endswith("xls"):
                word_file = xls_file[:-3] + "docx"
            try:
                '''Read the XLS file using pandas'''

                df = pd.read_excel(xls_file)

                '''Create a new Word document'''
                doc = Document()

                '''Iterate over the rows of the dataframe and add them to the
                Word document'''
                logger.info(f"{ICYAN}Converting {xls_file}..{RESET}")
                # time.sleep(2)
                total_rows = df.shape[0]
                for _, row in df.iterrows():
                    current_row = _ + 1
                    percentage = (current_row / total_rows)*100
                    for value in row:
                        doc.add_paragraph(str(value))
                    print(f"Row {DYELLOW}{current_row}/{total_rows} \
{DBLUE}{percentage:.1f}%{RESET}", end="\r")
                    # print(f"\033[1;36m{row}{RESET}")

                # Save the Word document
                doc.save(word_file)
                print(F"{DGREEN}Conversion successful!{RESET}", end="\n")
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(1)
            except Exception as e:
                print("Oops Conversion failed:", str(e))

###############################################################################
    '''Convert xlsx/xls file/files to text file format'''
###############################################################################

    def convert_xls_to_text(self):
        xls_list = self.preprocess()
        ls = ["xlsx", "xls"]
        xls_list = [
            item for item in xls_list if any(item.lower().endswith(ext)
                                             for ext in ls)]
        print(F"{DGREEN}Initializing conversion sequence{RESET}")
        for xls_file in xls_list:
            if xls_file .lower().endswith("xlsx"):
                txt_file = xls_file[:-4] + "txt"
            elif xls_file .lower().endswith("xls"):
                txt_file = xls_file[:-3] + "txt"
            try:
                # Read the XLS file using pandas
                logger.info(f"Converting {xls_file}..")
                df = pd.read_excel(xls_file)

                # Convert the dataframe to plain text
                text = df.to_string(index=False)
                chars = len(text)
                words = len(text.split())
                lines = len(text.splitlines())

                print(
                    f"Preparing to write: {DYELLOW}{chars} \033[1;30m \
characters{DYELLOW} {words}\033[1;30m words {DYELLOW}{lines}\033[1;30m \
lines {RESET}", end="\n")
                # Write the plain text to the output file
                with open(txt_file, 'w') as file:
                    file.write(text)

                print(F"{DGREEN}Conversion successful!{RESET}", end="\n")
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(1)
            except Exception as e:
                print("Oops Conversion failed:", str(e))

###############################################################################
    '''Convert xlsx/xls file to csv(comma seperated values) format'''
###############################################################################

    def convert_xlsx_to_csv(self):
        xls_list = self.preprocess()
        ls = ["xlsx", "xls"]
        xls_list = [
            item for item in xls_list if any(item.lower().endswith(ext)
                                             for ext in ls)]
        for xls_file in xls_list:
            if xls_file.lower().endswith("xlsx"):
                csv_file = xls_file[:-4] + "csv"
            elif xls_file.lower().endswith("xls"):
                csv_file = xls_file[:-3] + "csv"
            try:
                '''Load the Excel file'''
                print(F"{DGREEN}Initializing conversion sequence{RESET}")
                df = pd.read_excel(xls_file)
                logger.info(f"Converting {xls_file}..")
                total_rows = df.shape[0]
                print(f"Writing {DYELLOW}{total_rows} rows {RESET}", end="\n")
                for i in range(101):
                    print(f"Progress: {i}%", end="\r")
                '''Save the DataFrame to CSV'''
                df.to_csv(csv_file, index=False)
                print(F"{DMAGENTA} Conversion successful{RESET}")
            except KeyboardInterrupt:
                print("Exiting")
                sys.exit(1)
            except Exception as e:
                print(e)

###############################################################################
# Convert xlsx file(s) to sqlite
###############################################################################

    def convert_xlsx_to_database(self):
        xlsx_list = self.preprocess()
        ls = ["xlsx", "xls"]
        xlsx_list = [
            item for item in xlsx_list if any(item.lower().endswith(ext)
                                              for ext in ls)]
        for xlsx_file in xlsx_list:
            if xlsx_file.lower().endswith("xlsx"):
                sqlfile = xlsx_file[:-4]
            elif xlsx_file.lower().endswith("xls"):
                sqlfile = xlsx_file[:-3]
            try:
                db_file = input(
                    F"{DBLUE}Please enter desired sql filename: {RESET}")
                table_name = input(
                    "Please enter desired table name: ")
                # res = ["db_file", "table_name"]
                if any(db_file) == "":
                    db_file = sqlfile + "sql"
                    table_name = sqlfile
                if not db_file.endswith(".sql"):
                    db_file = db_file + ".sql"
                column = 0
                for i in range(20):
                    column += 0
                # Read the Excel file into a pandas DataFrame
                print(f"Reading {xlsx_file}...")
                df = pd.read_excel(xlsx_file)
                print(f"{DGREEN}Initializing conversion sequence{RESET}")
                print(f"{DGREEN} Connected to sqlite3 database::{RESET}")
                # Create a connection to the SQLite database
                conn = sqlite3.connect(db_file)
                print(F"{DYELLOW} Creating database table::{RESET}")
                # Insert the DataFrame into a new table in the database
                df.to_sql(table_name, column, conn,
                          if_exists='replace', index=False)
                print(
                    f"Operation successful{RESET} file saved as \033[32{db_file}{RESET}")
                # Close the database connection
                conn.close()
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(1)
            except Exception as e:
                logger.error(f"{e}")

    def doc2image(self, outf="png"):
        outf_list = ['png', 'jpg']
        if outf not in outf_list:
            outf = "png"
        path_list = self.preprocess()
        ls = ["pdf"]
        file_list = [
            item for item in path_list if any(item.lower().endswith(ext)
                                              for ext in ls)]
        for file in file_list:
            if file.lower().endswith("pdf"):
                # Convert the PDF to a list of PIL image objects
                print("Generate image objects ..")
                images = convert_from_path(file)

                # Save each image to a file
                fname = file[:-4]
                print(f"{YELLOW}Target images{BLUE} {len(images)}{RESET}")
                for i, image in enumerate(images):
                    print(f"{DBLUE}{i}{RESET}", end="\r")
                    image.save(f"{fname}_{i+1}.{outf}")
                print(f"{GREEN}mOk{RESET}")


class Scanner:

    def __init__(self, input_file):
        self.input_file = input_file

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

    def scanPDF(self):
        pdf_list = self.preprocess()
        pdf_list = [item for item in pdf_list if item.lower().endswith("pdf")]

        for pdf in pdf_list:
            out_f = pdf[:-3] + 'txt'
            print(f"{YELLOW}Read pdf ..{RESET}")

            with open(pdf, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''

                pg = 0
                for page_num in range(len(reader.pages)):
                    pg += 1

                    print(f"{DYELLOW}Progress:{RESET}", end="")
                    print(f"{CYAN}{pg}/{len(reader.pages)}{RESET}", end="\r")
                    page = reader.pages[page_num]
                    text += page.extract_text()

            print(f"\n{text}")
            print(F"\n{YELLOW}Write text to {GREEN}{out_f}{RESET}")
            with open(out_f, 'w') as f:
                f.write(text)

            print(F"{DGREEN}Ok{RESET}")


class FileSynthesis:

    def __init__(self, input_file):
        self.input_file = input_file
        # self.CHUNK_SIZE = 20_000

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

    @staticmethod
    def join_audios(files, output_file):
        masterfile = output_file + "_master.mp3"
        print(
            f"{DBLUE}Create a master file {DMAGENTA}{masterfile}{RESET}", end='\r')
        # Create a list to store files
        ogg_files = []
        # loop through the directory while adding the ogg files to the list
        print(files)
        for filename in files:
            print(f"Join {DBLUE}{len(files)}{RESET} files")
            # if filename.endswith('.ogg'):
            # ogg_file = os.path.join(path, filename)
            ogg_files.append(AudioSegment.from_file(filename))

        # Concatenate the ogg files
        combined_ogg = ogg_files[0]
        for i in range(1, len(files)):
            combined_ogg += ogg_files[i]

        # Export the combined ogg to new mp3 file or ogg file
        combined_ogg.export(output_file + "_master.ogg", format='ogg')
        print(F"{DGREEN}Master file:Ok                                                                             {RESET}")

    def Synthesise(self, text: str, output_file: str, CHUNK_SIZE: int = 20_000, ogg_folder: str = 'tempfile', retries: int = 5) -> None:
        """Converts given text to speech using Google Text-to-Speech API."""
        out_ls = []
        try:
            if not os.path.exists(ogg_folder):
                os.mkdir(ogg_folder)
            print(f"{DYELLOW}Get initial net speed..{RESET}")
            st = speedtest.Speedtest()  # get initial network speed
            st.get_best_server()
            download_speed: float = st.download()  # Keep units as bytes
            logger.info(

                f"{GREEN} Conversion to mp3 sequence initialized start\
speed {CYAN}{download_speed/1_000_000:.2f}Kbps{RESET}")

            for attempt in range(retries):
                try:
                    '''Split input text into smaller parts and generate
                    individual gTTS objects'''
                    counter = 0
                    for i in range(0, len(text), CHUNK_SIZE):
                        chunk = text[i:i+CHUNK_SIZE]
                        output_filename = f"{output_file}_{counter}.ogg"
                        counter += 1
                        # print(output_filename)
                        if os.path.exists(output_filename):
                            output_filename = f"{output_file}_{counter+1}.ogg"
                        # print(output_filename)
                        tts = gTTS(text=chunk, lang='en', slow=False)
                        tts.save(output_filename)
                        out_ls.append(output_filename)
                    break
                    # print(out_ls)
                    '''Handle any network related issue gracefully'''
                except Exception in (ConnectionError, ConnectionAbortedError,
                                     ConnectionRefusedError,
                                     ConnectionResetError) as e:
                    logger.error(f"Sorry boss connection problem encountered: {e} in {attempt+1}/{retries}:")
                    time.sleep(5)  # Wait 5 seconds before retrying

                # Handle connectivity/network error
                except requests.exceptions.RequestException as e:
                    logger.error(f"{e}")
                except Exception as e:
                    logger.error(f'{DRED} Error during conversion attempt \
{attempt+1}/{retries}:{e}{RESET}')
                    tb = traceback.extract_tb(sys.exc_info()[2])
                    logger.info("\n".join([f"  > {line}"
                                           for line in map(str, tb)]))
                    time.sleep(3)  # Wait 5 seconds before retrying
                    pass

            if attempt >= retries:
                logger.error(
                    f"Conversion unsuccessful after {retries} attempts.")
                sys.exit(2)

        finally:
            # print(out_ls)
            # Combine generated gTTS objects
            if len(out_ls) >= 1:
                FileSynthesis.join_audios(out_ls, output_file)

            st = speedtest.Speedtest()
            logger.info("Done")
            print("Get final speed ...")
            logger.info(

                f"{YELLOW}Final Network Speed: {st.download()/(10**6):.2f} Kbps{RESET}")

    @staticmethod
    def pdf_to_text(pdf_path):
        logger.info('''Processing the file...\n''')
        logger.info(
            F'{GREEN} Initializing pdf to text conversion sequence...{RESET}')
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                print(F"{DGREEN}Ok{RESET}")
                return text
        except Exception as e:
            logger.error(
                f"{DRED}Failed to extract text from '{YELLOW}{pdf_path}'{RESET}:\n {e}")

    @staticmethod
    def text_file(input_file):
        try:
            with open(input_file, 'r', errors='ignore') as file:
                text = file.read().replace('\n', ' ')
            return text
        except FileNotFoundError:
            logger.error("File '{}' was not found.".format(input_file))
        except Exception as e:
            logger.error(
                F"{DRED}Error converting {input_file} to text: {str(e)}\
{RESET}")

    @staticmethod
    def docx_to_text(docx_path):
        try:
            logger.info(f"{BLUE} Converting {docx_path} to text...{RESET}")
            doc = Document(docx_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(paragraphs)
        except FileNotFoundError:
            logger.error(f"File '{docx_path}' was not found.")
        except Exception as e:
            logger.error(
                F"{DRED}Error converting {docx_path} to text: {e}\
{RESET}")

    '''Handle input files based on type to initialize conversion sequence'''

    def audiofy(self):
        input_list = self.preprocess()
        extdoc = ["docx", "doc"]
        ls = {"pdf", "docx", "doc", "txt"}
        input_list = [item for item in input_list if item.lower().endswith(tuple(ls))]
        for input_file in input_list:
            if input_file.endswith('.pdf'):
                text = FileSynthesis.pdf_to_text(input_file)
                output_file = input_file[:-4]

            elif input_file.lower().endswith(tuple(extdoc)):

                text = FileSynthesis.docx_to_text(input_file)
                output_file = input_file[:-5]

            elif input_file.endswith('.txt'):
                text = FileSynthesis.text_file(input_file)
                output_file = input_file[:-4]

            else:
                logger.error('Unsupported file format. Please provide \
a PDF, txt, or Word document.')
                sys.exit(1)
            try:
                FileSynthesis.Synthesise(None, text, output_file)
            except KeyboardInterrupt:
                sys.exit(1)


###############################################################################
# Convert video file to from one format to another'''
###############################################################################


class VideoConverter:

    def __init__(self, input_file, out_format):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            if os.listdir(self.input_file) is None:
                print("Cannot work with empty folder")
                sys.exit(1)
            for file in os.listdir(self.input_file):
                file_path = os.path.join(self.input_file, file)
                if os.path.isfile(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def CONVERT_VIDEO(self):
        try:
            input_list = self.preprocess()
            out_f = self.out_format.upper()
            input_list = [item for item in input_list if any(
                item.upper().endswith(ext) for ext in SUPPORTED_VIDEO_FORMATS)]
            print(F"{DYELLOW}Initializing conversion..{RESET}")

            for file in input_list:
                if out_f.upper() in SUPPORTED_VIDEO_FORMATS:
                    _, ext = os.path.splitext(file)
                    output_filename = _ + '.' + out_f.lower()
                    print(output_filename)
                else:
                    print("Unsupported output format")
                    sys.exit(1)
                format_codec = {
                    "MP4": "mpeg4",
                    "AVI": "rawvideo",
                    # "OGV": "avc",
                    "WEBM": "libvpx",
                    "MOV": "mpeg4",
                    "MKV": "MPEG4",
                    "FLV": "flv"
                    # "WMV": "WMV"
                }
                '''Load the video file'''
                print(f"{DBLUE}oad file{RESET}")
                video = VideoFileClip(file)
                '''Export the video to a different format'''
                print(f"{DMAGENTA}Converting file to {output_filename}{RESET}")
                video.write_videofile(
                    output_filename, codec=format_codec[out_f])
                '''Close the video file'''
                print(f"{DGREEN}Done{RESET}")
                video.close()
        except KeyboardInterrupt:
            print("\nExiting..")
            sys.exit(1)
        except Exception as e:
            print(e)


###############################################################################
# Convert Audio file to from one format to another'''
###############################################################################


class AudioConverter:

    def __init__(self, input_file, out_format):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            if os.listdir(self.input_file) is None:
                print("Cannot work with empty folder")
                sys.exit(1)
            for file in os.listdir(self.input_file):
                file_path = os.path.join(self.input_file, file)
                if os.path.isfile(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def pydub_conv(self):
        input_list = self.preprocess()
        out_f = self.out_format
        input_list = [item for item in input_list if any(
            item.lower().endswith(ext) for ext in SUPPORTED_AUDIO_FORMATS)]
        print(F"{DYELLOW}Initializing conversion..{RESET}")
        for file in input_list:
            if out_f.lower() in SUPPORTED_AUDIO_FORMATS:
                _, ext = os.path.splitext(file)
                output_filename = _ + '.' + out_f
            else:
                print("Unsupported output format")
                sys.exit(1)
            fmt = ext[1:]
            print(fmt, out_f)
            audio = pydub.AudioSegment.from_file(file, fmt)
            print(f"{DMAGENTA}Converting to {output_filename}{RESET}")
            audio.export(output_filename, format=out_f)
            # new_audio = pydub.AudioSegment.from_file('output_audio.')
            print(f"{DGREEN}Done{RESET}")
            # play(new_audio)
            # new_audio.close()


###############################################################################
# Convert images file to from one format to another
###############################################################################


class ImageConverter:

    def __init__(self, input_file, out_format):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        try:
            files_to_process = []

            if os.path.isfile(self.input_file):
                files_to_process.append(self.input_file)
            elif os.path.isdir(self.input_file):
                if os.listdir(self.input_file) is None:
                    print("Cannot work with empty folder")
                    sys.exit(1)
                for file in os.listdir(self.input_file):
                    file_path = os.path.join(self.input_file, file)
                    if os.path.isfile(file_path):
                        files_to_process.append(file_path)

            return files_to_process
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

    def convert_image(self):
        try:
            input_list = self.preprocess()
            out_f = self.out_format.upper()

            input_list = [item for item in input_list if any(
                item.lower().endswith(ext) for ext in SUPPORTED_IMAGE_FORMATS[out_f])]
            for file in input_list:
                print(file)
                if out_f.upper() in SUPPORTED_IMAGE_FORMATS:
                    _, ext = os.path.splitext(file)
                    output_filename = _ + \
                        SUPPORTED_IMAGE_FORMATS[out_f].lower()
                else:
                    print("Unsupported output format")
                    sys.exit(1)
                '''Load the image using OpenCV: '''
                print(F"{DYELLOW}Reading input image..{RESET}")
                img = cv2.imread(file)
                '''Convert the OpenCV image to a PIL image: '''
                print(f"{DMAGENTA}Converting to PIL image{RESET}")
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                '''Save the PIL image to a different format: '''
                print(f"\033[1;36mSaving image as {output_filename}{RESET}")
                pil_img.save(output_filename, out_f)
                print(f"{DGREEN}Done{RESET}")
                '''Load the image back into OpenCV: '''
                print(f"{DMAGENTA}Load and display image{RESET}")
                opencv_img = cv2.imread(output_filename)
                '''Display the images: '''
                cv2.imshow('OpenCV Image', opencv_img)
                # pil_img.show()
                '''Wait for the user to press a key and close the windows: '''
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        except KeyboardInterrupt:
            print("\nExiting..")
            sys.exit(1)
