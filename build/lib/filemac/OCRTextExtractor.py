import os
import sys
import cv2
import pytesseract
from PIL import Image
import logging
import logging.handlers
###############################################################################
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)
###############################################################################
'''Do OCR text extraction from a given image file and display the extracted
    text
    to the screen finally save it to a text file assuming the name of the input
    file'''

###############################################################################


class ExtractText:
    def __init__(self, input_file):
        self.input_file = input_file

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

    def OCR(self):
        image_list = self.preprocess()
        ls = {'png', 'jpg'}
        image_list = [
            item for item in image_list if any(item.lower().endswith(ext)
                                               for ext in ls)]

        def ocr_text_extraction(image_path):
            '''Load image using OpenCV'''
            img = cv2.imread(image_path)

            logger.info(f"\033[5;34mprocessing {image_path}...\033[0m")

            try:
                '''Preprocess image for better OCR results'''
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                img_pil = Image.fromarray(thresh)

                '''Perform OCR using pytesseract'''
                config = ("-l eng --oem 3 --psm 6")
                text = pytesseract.image_to_string((img_pil), config=config)

                '''Remove extra whitespaces and newlines
                text = ' '.join(text.split()).strip()'''
                logger.info("\033[36mFound:\n\033[0m")
                print(text)
                current_path = os.getcwd()
                file_path = os.path.join(current_path, OCR_file)
                ''' Save the extracted text to specified file '''
                logger.info("\033[32mGenerating text file for the extracted \
text..\033[0m")

                with open(file_path, 'w') as file:
                    file.write(text)
                logger.info(
                    f"File saved as \033[32m{OCR_file}\033[0m:")
                '''If there are multiple candidate images for text extraction,
                wait for key press before proceeding to the next
                image otherwise don't wait
                size = [i for i in enumerate(image_list)]'''
                if len(image_list) >= 2:
                    input("\033[5;97mPress Enter to continue\033[0m")
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(0)
            except FileNotFoundError as e:
                logger.error(f"Error: {str(e)}")
            except IOError as e:
                logger.error(
                    f"Could not write to output file '{OCR_file}'. \
Reason: {str(e)}\033[0m")
            except Exception as e:
                logger.error(f"Error: {type(e).__name__}: {str(e)}")
            except Exception as e:
                logger.error(f"Error:>>\033[31m{e}\033[0m")
            return text

        for image_path in image_list:
            OCR_file = image_path[:-3] + "txt"
            ocr_text_extraction(image_path)
