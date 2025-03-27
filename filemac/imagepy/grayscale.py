import os
from PIL import Image
import cv2
import logging
from typing import Optional, Union
from utils.dirbuster import Unbundle
from utils.decorators import Decorators
from utils.colors import foreground
from utils.formats import SUPPORTED_IMAGE_FORMATS
from utils.namerule import modify_filename_if_exists

fcl = foreground()
RESET = fcl.RESET

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)


class Grayscale:
    """
    Class for converting images to grayscale and saving the processed output.

    Attributes:
        input_obj (Optional[Union[list[str], str, os.PathLike]]): Input file(s) or directory.
        output_file (Optional[Union[list[str], str, os.PathLike]]): Output file path or directory.
    """

    def __init__(
        self,
        input_obj: Optional[Union[list[str], str, os.PathLike]],
        output_file: Optional[Union[list[str], str, os.PathLike]] = None,
    ):
        """
        Initializes the Grayscale object.

        Args:
            input_obj: Input file(s) or directory.
            output_file: Output file path or directory.
        """
        self.input_obj = input_obj
        self.output_file = output_file

    def get_output_file(
        self, image_path: Optional[Union[str, os.PathLike]] = None
    ) -> Union[str, os.PathLike]:
        """
        Computes the correct output file path for a given input file.

        Args:
            image_path: Path to the input file.

        Returns:
            The computed output file path.
        """
        logger.info(f"{fcl.BWHITE_FG}Obtaining output file name{RESET}")
        if self.output_file and self.output_file.endswith(
            tuple(SUPPORTED_IMAGE_FORMATS.values())
        ):
            return os.path.abspath(self.output_file)
        if self.output_file:
            return os.path.abspath(os.path.splitext(self.output_file)[0] + ".png")
        if image_path:
            return os.path.abspath(
                os.path.splitext(os.path.basename(image_path))[0] + ".png"
            )
        return "default_output.txt"

    def run(self):
        """
        Runs the image to grayscale conversion operation on the input files.

        Applies the for_loop_decorator to process each image in the input list.
        """
        file_list = Unbundle(self.input_obj).run()

        @Decorators().for_loop_decorator(file_list)
        def process_image(self, image_path):
            """Processes a single image, converting it to grayscale and saving."""
            try:
                logger.info(
                    f"{fcl.YELLOW_FG}Processing {fcl.CYAN_FG}{image_path}{RESET}"
                )
                img = cv2.imread(image_path)
                if img is None:
                    raise FileNotFoundError(f"Could not read image: {image_path}")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                self.save_pil_image(thresh, image_path)
            except FileNotFoundError as e:
                logger.error(f"{fcl.RED_FG}{e}{RESET}")
            except Exception as e:
                raise
                logger.error(f"An unexpected error occurred: {fcl.RED_FG}{e}{RESET}")

        process_image(self)

    def save_pil_image(self, thresh, image_path):
        """
        Saves a NumPy array representing a grayscale image as a PIL Image.

        Args:
            thresh: The NumPy array representing the grayscale image.
            image_path: The path of the original image, used to derive the output filename.
        """
        try:
            img_pil = Image.fromarray(thresh)
            filename = self.get_output_file(image_path)
            filename = modify_filename_if_exists(filename)
            img_pil.save(filename)
            logger.info(f"{fcl.GREEN_FG}Image saved as {fcl.BLUE_FG}{filename}{RESET}")
        except Exception as e:
            raise
            logger.error(f"Unable to save the image: {fcl.RED_FG}{e}{RESET}")
