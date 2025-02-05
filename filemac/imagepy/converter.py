###############################################################################
# Convert images file to from one format to another
###############################################################################
import os
import sys
from tqdm import tqdm
from PIL import Image
import cv2
from ..formats import SUPPORTED_IMAGE_FORMATS
from .colors import (
    BWHITE,
    DGREEN,
    DMAGENTA,
    DYELLOW,
    ICYAN,
    RED,
    RESET,
)


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
            print("File not found❕")
            sys.exit(1)

    def convert_image(self):
        try:
            input_list = self.preprocess()
            out_f = self.out_format.upper()
            input_list = [
                item
                for item in input_list
                if any(
                    item.lower().endswith(ext)
                    for ext in SUPPORTED_IMAGE_FORMATS.values()
                )
            ]

            for file in tqdm(input_list):
                if out_f.upper() in SUPPORTED_IMAGE_FORMATS:
                    _ = os.path.splitext(file)[0]
                    output_filename = _ + SUPPORTED_IMAGE_FORMATS[out_f].lower()
                else:
                    print("Unsupported output format")
                    sys.exit(1)
                """Load the image using OpenCV: """
                print(f"{DYELLOW}Reading input image..{RESET}")
                img = cv2.imread(file)
                """Convert the OpenCV image to a PIL image: """
                print(f"{DMAGENTA}Converting to PIL image{RESET}")
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                """Save the PIL image to a different format: """
                print(f"\033[1;36mSaving image as {output_filename}{RESET}")
                pil_img.save(output_filename, out_f)
                print(f"{DGREEN}Done ✅{RESET}")
                """Load the image back into OpenCV: """
                # print(f"{DMAGENTA}Load and display image{RESET}")
                # opencv_img = cv2.imread(output_filename)
                """Display the images: """
                # cv2.imshow('OpenCV Image', opencv_img)
                # opencv_img.show()
                """Wait for the user to press a key and close the windows: """
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit(1)
        except AssertionError:
            print("Assertion failed.")
        except KeyError:
            print(
                f"{RED}ERROR:\tPending Implementation for{ICYAN} {out_f} {BWHITE}format{RESET}"
            )
        except Exception as e:
            print(f"{RED}{e}{RESET}")
