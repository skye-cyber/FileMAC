import logging
import os
import sys
from typing import Union, List, Optional

import cv2
import pytesseract
from PIL import Image
from rich.progress import Progress
from utils.colors import foreground, background
from utils.dirbuster import Unbundle
from utils.namerule import modify_filename_if_exists

fcl = foreground()
bcl = background()
RESET = fcl.RESET

# Define constants for better readability and maintainability
SUPPORTED_IMAGE_FORMATS = {"png", "jpg", "jpeg"}
DEFAULT_CONFIG = "-l eng --oem 3 --psm 6"
DEFAULT_SEPARATOR = "\n"

# Configure logging at the module level
logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)


class ExtractText:
    """
    Extracts text from images using OCR, with options for file/directory input,
    output file naming, and text separation.
    """

    def __init__(
        self,
        input_obj: Optional[Union[list[str], str, os.PathLike]],
        sep: str = DEFAULT_SEPARATOR,
    ):
        """
        Initializes the ExtractText object.

        Args:
            input_obj: Path to the image file or directory containing images.
            sep: Separator to use when joining extracted text.  Defaults to newline.
        """
        if not isinstance(input_obj, (str, list, os.PathLike)):
            raise TypeError(
                f"input_obj must be a string or os.PathLike, not {type(input_obj)}"
            )
        self.input_obj = input_obj
        self.sep = sep
        self.sep = (
            "\n"
            if self.sep == "newline"
            else (
                "\t"
                if self.sep == "tab"
                else (
                    " "
                    if self.sep == "space"
                    else ("" if self.sep == "none" else self.sep)
                )
            )
        )

        """
            separator_map = {
            "newline": "\n",
            "tab": "\t",
            "space": " ",
            "none": "",
            }

            self.sep = separator_map.get(self.sep, self.sep)
        """

    def _process_image(self, image_path: str, output_file: str) -> str:
        """
        Extracts text from a single image and saves it to a file.

        Args:
            image_path: Path to the image file.
            output_file: Path to the output text file.

        Returns:
            The extracted text.  Returns an empty string on error.
        """
        try:
            # Load image using OpenCV
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")

            # Preprocess image for better OCR results
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            img_pil = Image.fromarray(thresh)

            # Perform OCR using pytesseract
            self.sep = (
                self.sep.replace("\r\n", "\n")
                .replace("\\n", "\n")
                .replace("\r", "\n")
                .replace("\r\t", "\t")
                .replace("\\t", "\t")
            )

            text = pytesseract.image_to_string(img_pil, config=DEFAULT_CONFIG)
            text = self.sep.join(text.splitlines())  # handle empty lines
            logger.info("")
            logger.info(f"Extracted text from {image_path}")
            print(f"{fcl.YELLOW_FG}{text}{RESET}")

            # Save text to file
            with open(output_file, "w", encoding="utf-8") as file:  # Specify encoding
                file.write(text)
            return text

        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except IOError as e:
            logger.error(f"IOError: {e}")
        except pytesseract.TesseractError as e:
            logger.error(f"Tesseract error: {e}")
        except cv2.error as e:
            logger.error(f"OpenCV error processing {image_path}: {e}")
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while processing {image_path}: {e}"
            )

        return ""  # Return empty string on error

    def run(
        self, output_file: Optional[Union[list[str], str, os.PathLike]] = None
    ) -> Optional[List[str]]:
        """
        Runs the OCR extraction process on the input file(s) or directory.

        Args:
            output_file: Optional path to a single output file. If provided, all
                extracted text will be written to this file.  If None, output
                files will be generated based on input image names.

        Returns:
            A list of extracted texts, or None if no images were processed.
            If output_file is provided, returns a list with a single string.
        """

        image_list = Unbundle(self.input_obj).run()
        num_images = len(image_list)
        extracted_texts = []

        if num_images == 0:
            logger.warning("No images found to process.")
            return None

        try:
            if output_file:
                # Process all images and concatenate text into one output file
                all_text = ""
                with Progress() as progress:
                    task = progress.add_task(
                        "[yellow]Extracting text...", total=num_images
                    )
                    for image_path in image_list:
                        all_text += (
                            self._process_image(
                                image_path, os.path.splitext(output_file)[0] + ".txt"
                            )
                            + self.sep
                        )
                        progress.update(task, advance=1)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(all_text)
                return [all_text]  # Return a list containing the combined text

            else:
                # Process each image individually, creating separate output files
                with Progress() as progress:
                    task = progress.add_task(
                        "[yellow]Extracting text...", total=num_images
                    )
                    for image_path in image_list:
                        _output_file = (
                            os.path.splitext(os.path.basename(image_path))[0] + ".txt"
                        )
                        _output_file = modify_filename_if_exists(_output_file)
                        text = self._process_image(image_path, _output_file)
                        extracted_texts.append(text)
                        progress.update(task, advance=1)
                return extracted_texts

        except KeyboardInterrupt:
            print(
                f"\n[{bcl.YELLOW_BG}X{RESET}]Operation interrupted by {fcl.UBLUE_FG}user{RESET}.[/]"
            )
            sys.exit(0)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {bcl.RED_BG}{e}{RESET}")
            return None  # Ensure None is returned on error
