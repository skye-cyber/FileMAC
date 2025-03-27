import sys
import fitz  # PyMuPDF for PDF
from docx import Document
from PIL import Image
from io import BytesIO
from typing import List
from pathlib import Path


class ImageExtractor:
    """
    Base class for extracting images from document files.
    """

    def __init__(self, output_path: str = "extracted_images") -> None:
        """
        Initializes the ImageExtractor object.

        Args:
            output_path: Path to save the extracted images.
        """
        self.output_path = output_path
        Path(self.output_path).mkdir(
            parents=True, exist_ok=True
        )  # Ensure directory exists

    def _extract_images(self, file_path: str) -> List[Image.Image]:
        """
        Extracts images from the given file.  This is a placeholder
        for the actual extraction logic, to be implemented by
        subclasses.

        Args:
            file_path: Path to the document file.

        Returns:
            A list of PIL Image objects.  Returns an empty list if no images
            are found or if there is an error.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def extract_and_save_images(self, file_path: str) -> None:
        """
        Extracts and saves images from the given file.

        Args:
            file_path: Path to the document file.
        """
        images = self._extract_images(file_path)
        if not images:
            print(f"No images found in {file_path}")
            return

        base_filename = Path(file_path).stem
        self._save_images(images, base_filename)

    def _save_images(self, images: List[Image.Image], base_filename: str) -> None:
        """
        Saves the extracted images to the output directory.

        Args:
            images: A list of PIL Image objects.
            base_filename: The base filename to use when saving images (e.g., 'page_1').
        """
        for i, img in enumerate(images):
            try:
                # Generate a unique filename for each image
                img_format = img.format or "PNG"  # Default to PNG if format is None
                safe_filename = f"{base_filename}_img_{i + 1}.{img_format.lower()}"
                img_path = Path(self.output_path) / safe_filename
                img.save(img_path)
                print(f"Saved image: {img_path}")
            except Exception as e:
                print(f"Error saving image {i+1} from {base_filename}: {e}")


class PdfImageExtractor(ImageExtractor):
    """
    Extracts images from PDF files.
    """

    def _extract_images(self, file_path: str) -> List[Image.Image]:
        """
        Extracts images from a PDF file using PyMuPDF.

        Args:
            file_path: Path to the PDF file.

        Returns:
            A list of PIL Image objects.
        """
        images: List[Image.Image] = []
        try:
            pdf_document = fitz.open(file_path)
            for page_index in range(len(pdf_document)):
                page = pdf_document.load_page(page_index)
                image_list = page.get_images(full=True)  # Get detailed image info
                for img_index, img_info in enumerate(image_list):
                    xref = img_info[0]  # Get the XREF of the image
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    try:
                        pil_image = Image.open(BytesIO(image_bytes))
                        images.append(pil_image)
                    except Exception as e:
                        print(
                            f"Error processing image {img_index+1} from PDF page {page_index+1}: {e}"
                        )
            pdf_document.close()
        except Exception as e:
            print(f"Error processing PDF file: {file_path} - {e}")
        return images


class DocxImageExtractor(ImageExtractor):
    """
    Extracts images from DOCX files.
    """

    def _extract_images(self, file_path: str) -> List[Image.Image]:
        """
        Extracts images from a DOCX file.

        Args:
            file_path: Path to the DOCX file.

        Returns:
             A list of PIL Image objects.
        """
        images: List[Image.Image] = []
        try:
            docx_document = Document(file_path)
            for part in docx_document.part.rels.values():
                if "image" in part.target_ref:
                    image_bytes = part.target_part.blob
                    try:
                        pil_image = Image.open(BytesIO(image_bytes))
                        images.append(pil_image)
                    except Exception as e:
                        print(f"Error processing image from DOCX: {e}")
        except Exception as e:
            print(f"Error processing DOCX file: {file_path} - {e}")
        return images


def process_files(file_paths: List[str], output_path: str) -> None:
    """
    Processes the given files and extracts images from them.

    Args:
        file_paths: List of paths to the files to process.
        output_path: Path to save the extracted images.
    """
    for file_path in file_paths:
        if file_path.lower().endswith(".pdf"):
            extractor = PdfImageExtractor(output_path)
            extractor.extract_and_save_images(file_path)
        elif file_path.lower().endswith((".docx")):
            extractor = DocxImageExtractor(output_path)
            extractor.extract_and_save_images(file_path)
        else:
            print(f"Skipping unsupported file format: {file_path}")


def main(args: List[str]) -> None:
    """
    Main function to parse command line arguments and perform image extraction.

    Args:
        args: List of command line arguments.
    """
    if not args or "-h" in args or "--help" in args:
        print(
            """
            Usage: python extract_images.py [options] file1 file2 ... fileN

            Options:
                -h, --help            show this help message and exit
                -o, --output PATH     path to save the extracted images (default: extracted_images)
            """
        )
        sys.exit()

    file_paths = []
    output_path = "extracted_images"  # Default output path

    i = 1
    while i < len(args):
        if args[i] in ("-o", "--output"):
            output_path = args[i + 1]
            i += 2
        else:
            if not args[i].startswith("-"):
                file_paths.append(args[i])
                i += 1
            else:
                print(f"Unknown argument: {args[i]}")
                sys.exit(1)

    if not file_paths:
        print("No files provided for image extraction.")
        sys.exit(1)

    process_files(file_paths, output_path)


if __name__ == "__main__":
    main(sys.argv[1:])
