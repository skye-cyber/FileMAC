import re
import sys
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
from utils.colors import foreground
import shutil

fcl = foreground()
RESET = fcl.RESET


class ImageToPdfConverter:
    """
    A class for converting images to PDF.
    """

    def __init__(
        self,
        image_list: list = None,
        input_dir=None,
        output_pdf_path=None,
        page_size=letter,
        order: bool = False,
        base: bool = False,
        walk: bool = False,
        clean: bool = False,
    ):
        self.image_list = image_list
        self.input_dir = input_dir
        self.page_size = page_size
        self.order = order
        self.base = base
        self.walk = walk
        self.clean = clean
        self.output_pdf_path = (
            output_pdf_path if output_pdf_path else self.ensure_output_file()
        )

    def ensure_output_file(self) -> os.PathLike:
        file_name = "filemac_image2pdf.pdf"
        if self.input_dir:
            base_dir = self.input_dir
            if self.base:
                one_file = os.listdir(self.input_dir)[0]
                base_name, ext = os.path.splitext(one_file)
                if "_img_" in base_name:
                    base_name = base_name.split("_img_")[0]
                    file_name = base_name + ".pdf"
                else:
                    file_name = self.input_dir.split("_imgs")[0] + ".pdf"
        else:
            base_dir = Path(self.image_list[0]).parent

        file_path = os.path.join(base_dir, file_name)

        return file_path

    def _clean(self, dirs: list):
        print(f"{fcl.UWHITE_FG}{fcl.BWHITE_FG}Clean Images Host dir{fcl.RESET}")
        for d in dirs:
            abspath = os.path.abspath(d)
            print(f"{fcl.BWHITE_FG}Nuke: {fcl.BYELLOW_FG}{abspath}{fcl.RESET}")
            # print(Path(d).is_relative_to(os.path.expanduser("~")))
            if (
                os.path.exists(d) and os.path.isdir(d)
                # and Path(d).is_relative_to(os.path.expanduser("~"))
            ):
                shutil.rmtree(abspath)

    def create_pdf_from_images(
        self, image_paths, output_pdf_path, resize_to_fit=True
    ) -> os.PathLike:
        """
        Creates a PDF from a list of image paths.

        Args:
            image_paths (list): A list of image file paths.
            output_pdf_path (str): The path to save the generated PDF.
            resize_to_fit (bool, optional): Whether to resize images to fit the page. Defaults to True.

        Raises:
            FileNotFoundError: If any image path is invalid.
            ValueError: If image_paths is empty or contains non-image files.
            Exception: for pillow image opening errors, or reportlab canvas errors.
        """

        if not image_paths:
            raise ValueError("Image paths list is empty.")

        for image_path in image_paths:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            try:
                Image.open(image_path)
            except Exception as e:
                raise ValueError(f"Error opening image {image_path}: {e}")

        try:
            c = canvas.Canvas(output_pdf_path, pagesize=self.page_size)
            width, height = self.page_size

            for image_path in image_paths:
                img = Image.open(image_path)
                img_width, img_height = img.size

                if resize_to_fit:
                    ratio = min(width / img_width, height / img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio
                    x = (width - new_width) / 2
                    y = (height - new_height) / 2
                else:
                    x = (width - img_width) / 2
                    y = (height - img_height) / 2
                    new_width = img_width
                    new_height = img_height

                c.drawImage(
                    image_path,
                    x,
                    y,
                    width=new_width,
                    height=new_height,
                    preserveAspectRatio=True,
                )
                c.showPage()

            c.save()

            return output_pdf_path
        except Exception as e:
            raise Exception(f"Error creating PDF: {e}")

    @staticmethod
    def ensure_format(input_image) -> os.PathLike:
        from ..imagepy.converter import ImageConverter

        converter = ImageConverter(input_image, "png")
        output_image = converter.convert_image()
        return output_image

    def extract_img_number(self, filename):
        match = re.search(r"_img_(\d+)", filename)
        return int(match.group(1)) if match else float("inf")

    def _sort(self, obj, ext):
        if self.order:
            if isinstance(obj, list):
                return sorted(
                    obj,
                    key=lambda f: self.extract_img_number(f),
                )
            return sorted(
                [
                    os.path.join(obj, f)
                    for f in os.listdir(obj)
                    if f.lower().endswith(ext)
                ],
                key=lambda f: self.extract_img_number(f),
            )
        else:
            return sorted(
                [
                    os.path.join(obj, f)
                    for f in os.listdir(obj)
                    if f.lower().endswith(ext)
                ]
            )

    def convert_images_in_directory_recursive(
        self, input_dir, output_pdf_path, file_extensions=(".jpg", ".jpeg", ".png")
    ):
        """
        Recursively walks through a directory and its subdirectories,
        converting images in each folder into a separate PDF.

        Args:
            input_dir (str): Root directory containing images.
            output_root (str): Directory to save the generated PDFs.
            file_extensions (tuple): Supported image extensions.
        """
        try:
            if not os.path.exists(input_dir):
                raise FileNotFoundError(f"Directory not found: {input_dir}")

            # if not os.path.exists(output_root):
            # os.makedirs(output_root)
            dclean = []
            for root, _, files in os.walk(input_dir):
                image_paths = [
                    os.path.join(root, f)
                    for f in files
                    if f.lower().endswith(file_extensions)
                ]

                if not image_paths:
                    continue  # No valid images in this directory

                # Optional: sort images with your custom logic
                image_paths = self._sort(image_paths, file_extensions)

                # Ensure formats are valid
                for index, image in enumerate(image_paths):
                    if not image.lower().endswith(file_extensions):
                        image_paths[index] = self.ensure_format(image)

                # Create a relative PDF name based on the subdir structure
                fname = os.path.split(root)[-1].split("_imgs")[0] + ".pdf"
                relative_path = os.path.join(
                    os.path.dirname((os.path.relpath(root, input_dir))), fname
                )
                # Host dir for images to be cleaned is clean is on
                dname = os.path.relpath(root, input_dir)
                dclean.append(dname)

                # pdf_name = relative_path.replace(os.sep, "_") + ".pdf"
                # pdf_output_path = os.path.join(output_root, pdf_name)

                # Create the PDF for this folder
                self.create_pdf_from_images(image_paths, relative_path)
                print(f"{fcl.BWHITE_FG}Created PDF{RESET}: {relative_path}")
            if self.clean:
                self._clean(dclean)
        except Exception as e:
            print(f"\033[31m{e}\033[0m")
            sys.exit(1)

    def convert_images_in_directory(
        self, input_dir, output_pdf_path, file_extensions=(".jpg", ".jpeg", ".png")
    ) -> os.PathLike:
        try:
            """
            Converts all images in a directory to a PDF.

            Args:
                input_dir (str): The directory containing the images.
                output_pdf_path (str): The path to save the generated PDF.
                file_extensions (tuple, optional): Tuple of image file extensions to include.
            """

            if not os.path.exists(input_dir):
                raise FileNotFoundError(f"Directory not found: {input_dir}")

            image_paths = self._sort(input_dir, ext=file_extensions)

            for index, image in enumerate(image_paths):
                if not image.endswith(file_extensions):
                    image_paths[index] = self.ensure_format(image)

            if not image_paths:
                raise ValueError(
                    f"\033[31mNo images found in directory:\033[1m {input_dir}\033[0m"
                )

            self.create_pdf_from_images(image_paths, output_pdf_path)
            return output_pdf_path
        except ValueError as e:
            print(e)
            sys.exit(1)

    def run(self) -> os.PathLike:
        """
        Runs the PDF creation based on the object's initialization parameters.
        """
        if self.image_list and self.output_pdf_path:
            if all(os.path.exists(img) for img in self.image_list):
                output_pdf_path = self.create_pdf_from_images(
                    self.image_list, self.output_pdf_path
                )
                print(f"{fcl.GREEN_FG}PDF created successfully from directory!{RESET}")
                print(
                    f"{fcl.GREEN_FG}Output:{RESET} {fcl.BLUE_FG}{output_pdf_path}{RESET}"
                )
            else:
                print(
                    f"{fcl.RED_FG}One or more images in the list do not exist.{RESET}"
                )
        elif self.input_dir and self.output_pdf_path:
            if os.path.exists(self.input_dir):
                if self.walk:
                    output_pdf_path = self.convert_images_in_directory_recursive(
                        self.input_dir, self.output_pdf_path
                    )
                else:
                    output_pdf_path = self.convert_images_in_directory(
                        self.input_dir, self.output_pdf_path
                    )
                    print(
                        f"{fcl.GREEN_FG}PDF created successfully from directory!{RESET}"
                    )
                    print(
                        f"{fcl.BWHITE_FG}Output:{RESET} {fcl.BLUE_FG}{output_pdf_path}{RESET}"
                    )
            else:
                print(
                    f"Directory {fcl.YELLOW_FG}{self.input_dir}{RESET} does not exist."
                )
        else:
            print(
                "Please provide either image_list and output_pdf_path or input_dir and output_pdf_path during object instantiation."
            )
            return
        return output_pdf_path


if __name__ == "__main__":
    # Example 1: Creating PDF from a list of image paths
    image_list = [
        "/home/skye/Desktop/.Important/interviewQuiz1.jpeg",
        "/home/skye/Desktop/.Important/interviewQuiz2.jpeg",
        "/home/skye/Desktop/.Important/interviewQuiz3.jpeg",
    ]  # Replace with your image paths.
    converter1 = ImageToPdfConverter(
        image_list=image_list, output_pdf_path="output_from_list.pdf"
    )
    converter1.run()

    """# Example 2: Creating PDF from all images in a directory
    input_directory = "images"  # Replace with your directory path.
    converter2 = ImageToPdfConverter(
        input_dir=input_directory, output_pdf_path="output_from_directory.pdf"
    )
    converter2.run()"""
