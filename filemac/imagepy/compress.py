from PIL import Image
import os
import sys
import logging
import logging.handlers
from utils.colors import foreground

fcl = foreground()
RESET = fcl.RESET

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)


class Compress_Size:
    def __init__(self, input_image_path):
        self.input_image_path = input_image_path

    def resize_image(self, target_size):
        try:
            input_image_path = self.input_image_path
            ext = input_image_path[-3:]
            output_image_path = (
                os.path.splitext(input_image_path)[0] + f"_resized.{ext}"
            )

            original_image = Image.open(input_image_path)
            original_size = original_image.size
            size = os.path.getsize(input_image_path)
            print(f"Original image size {fcl.YELLOW_FG}{size/1000_000:.2f}MiB{RESET}")

            # Calculate the aspect ratio of the original image
            aspect_ratio = original_size[0] / original_size[1]

            # Convert the target sixze to bytes
            tz = int(target_size[:-2])
            if target_size[-2:].lower() == "mb":
                target_size_bytes = tz * 1024 * 1024
            elif target_size[-2:].lower() == "kb":
                target_size_bytes = tz * 1024
            else:
                logger.warning(f"Invalid units. Please use either {fcl.BMAGENTA_FG}'MB'{RESET}\
        or {fcl.BMAGENTA_FG}'KB'{RESET}")

            # Calculate the new dimensions based on the target size
            new_width, new_height = Compress_Size.calculate_new_dimensions(
                original_size, aspect_ratio, target_size_bytes
            )
            print(f"{fcl.BLUE_FG}Processing ..{RESET}")
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(output_image_path, optimize=True, format="png")
            t_size = os.path.getsize(output_image_path) / 1000_000
            print(f"{fcl.BGREEN_FG}Ok{RESET}")
            print(
                f"Image resized to {fcl.BYELLOW_FG}{t_size:.2f}{RESET} and saved to {fcl.BYELLOW_FG}{output_image_path}"
            )
        except KeyboardInterrupt:
            print("\nQuit⏹️")
            sys.exit(1)
        except KeyError:
            print("KeyError")
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")

    def calculate_new_dimensions(original_size, aspect_ratio, target_size_bytes):
        try:
            # Calculate the new dimensions based on the target size in bytes
            original_size_bytes = (
                original_size[0] * original_size[1] * 3
            )  # Assuming 24-bit color depth
            scale_factor = (target_size_bytes / original_size_bytes) ** 0.5

            new_width = int(original_size[0] * scale_factor)
            new_height = int(original_size[1] * scale_factor)

            return new_width, new_height
        except KeyboardInterrupt:
            print("\nQuit⏹️")
            sys.exit(1)
        except KeyError:
            print("KeyError")
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")


if __name__ == "__main__":
    input_image_path = input("Enter the path to the input image: ")
    target_size = input("Enter the target output size (MB or KB): ")
    ext = input_image_path[-3:]
    output_image_path = os.path.splitext(input_image_path)[0] + f"_resized.{ext}"

    init = Compress_Size(input_image_path)
    init.resize_image(target_size)
