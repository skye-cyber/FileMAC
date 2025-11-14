"""
File utility functions for filemac.
"""

import fnmatch
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Iterator, List, Optional, Union

from tqdm.auto import tqdm

# from .colors import fg, rs
from ..core.exceptions import FileSystemError
from .colors import OutputFormater as OF
from .config import OUTPUT_DIR
from .formats import SUPPORTED_IMAGE_FORMATS
from .simple import logger


def dirbuster(_dir_):
    try:
        target = []
        for root, dirs, files in os.walk(_dir_):
            for file in files:
                ext = file.split(".")[-1]

                _path_ = os.path.join(root, file)
                if os.path.exists(_path_) and ext.lower() in ("pdf", "doc", "docx"):
                    target.append(_path_)
        return target
    except FileNotFoundError as e:
        print(e)

    except KeyboardInterrupt:
        print("\nQuit!")
        return


def generate_filename(ext, basedir=OUTPUT_DIR, postfix="filemac") -> Path:
    """
    Generate Filename given its extension
    Args:
        ext-> str
        basedir-> Path
        postfix = str
    Returns:
        path
    """

    filename = OUTPUT_DIR / f"{uuid.uuid4().hex}-{postfix}.{ext}"

    return filename


class FileSystemHandler:
    """
    Encapsulates file handling utilities required by cleaner
    """

    def __init__(self, ignore: list | tuple = None):
        self.ignore = ignore

    def find_files(self, paths, patterns, recursive=True) -> list:
        try:
            candidates = []
            for path in paths:
                path_obj = Path(path).expanduser().resolve()
                if not path_obj.exists():
                    continue
                if recursive:
                    for file in tqdm(
                        path_obj.rglob("*"), desc="Searching", leave=False
                    ):
                        if file.is_file() and any(
                            fnmatch.fnmatch(file.name, pat) for pat in patterns
                        ):
                            candidates.append(file)
                else:
                    for file in tqdm(path_obj.glob("*"), desc="Searching", leave=False):
                        if file.is_file() and any(
                            fnmatch.fnmatch(file.name, pat) for pat in patterns
                        ):
                            candidates.append(file)
            return self.ignore_pattern(candidates)
        except Exception as e:
            raise FileSystemError(e)

    def find_directories(self, paths, patterns, recursive=True, empty=True) -> list:
        try:
            candidates = []
            for path in paths:
                path_obj = Path(path).expanduser().resolve()
                if not path_obj.exists():
                    continue
                if recursive:
                    for root, dirs, files in tqdm(
                        os.walk(path_obj, followlinks=True),
                        desc="Searching",
                        leave=False,
                    ):
                        for dir in dirs:
                            if len(os.listdir(os.path.join(root, dir))) == 0:
                                candidates.append(Path(root) / dir)

                else:
                    for item in tqdm(
                        os.listdir(path_obj), desc="Searching", leave=False
                    ):
                        if os.path.isdir(item) and len(os.listdir(item)) == 0:
                            candidates.append(path_obj / item)

            return self.ignore_pattern(candidates)
        except Exception as e:
            raise FileSystemError(e)

    def ignore_pattern(self, items: list | tuple, ignore: list | tuple = None) -> list:
        ignore = self.ignore if not ignore else ignore
        candidates = []
        for item in items:
            for ig in ignore:
                _ig = ig.lower()
                if _ig in item.as_uri().lower().split(
                    "/"
                ) + item.as_uri().lower().split("\\"):
                    continue

            candidates.append(item)

        return candidates

    @staticmethod
    def _find_files(pattern: str, recursive: bool = True) -> Iterator[Path]:
        """Find files matching pattern."""
        path = Path(pattern)

        if path.exists() and path.is_file():
            yield path
            return

        # Handle glob patterns
        if recursive:
            yield from Path(".").rglob(pattern)
        else:
            yield from Path(".").glob(pattern)

    @staticmethod
    def delete_files(files) -> bool:
        try:
            for f in files:
                if f.exists():
                    f.unlink()
                    print(f"{OF.OK} Deleted: {f}")
            return True
        except (PermissionError, OSError) as e:
            raise FileSystemError(e)
        except Exception as e:
            print(f"{OF.ERR} Failed to delete {f}: {e}")
            return False

    @staticmethod
    def delete_folders(files) -> bool:
        try:
            for f in files:
                if f.exists():
                    f.rmdir()
                    print(f"{OF.OK} Deleted: {f}")
            return True
        except (PermissionError, OSError) as e:
            raise FileSystemError(e)
        except Exception as e:
            print(f"{OF.ERR} Failed to delete {f}: {e}")
            return False

    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """Ensure directory exists, create if necessary."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path
        except OSError as e:
            raise FileSystemError(f"Failed to create directory {path}: {str(e)}")

    @staticmethod
    def safe_filename(name: str, max_length: int = 255) -> str:
        """Convert string to safe filename."""
        # Replace unsafe characters
        safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in name)

        # Remove extra spaces and underscores
        safe_name = "_".join(filter(None, safe_name.split()))

        # Trim to max length
        if len(safe_name) > max_length:
            name_hash = str(hash(safe_name))[-8:]
            safe_name = safe_name[: max_length - 9] + "_" + name_hash

        return safe_name


class TemporaryFileManager:
    """Manages temporary files with proper cleanup."""

    def __init__(self, prefix: str = "kcleaner_"):
        self.temp_files = []
        self.temp_dirs = []
        self.prefix = prefix

    def create_temp_file(self, suffix: str, content: str = "") -> Path:
        """Create a temporary file with the given suffix and content."""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=suffix,
                prefix=self.prefix,
                encoding="utf-8",
                delete=False,
            ) as f:
                if content:
                    f.write(content)
                temp_path = Path(f.name)

            self.temp_files.append(temp_path)
            return temp_path

        except (OSError, IOError) as e:
            raise FileSystemError(f"Failed to create temporary file: {str(e)}")

    def create_temp_dir(self) -> Path:
        """Create a temporary directory."""
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix=self.prefix))
            self.temp_dirs.append(temp_dir)
            return temp_dir
        except OSError as e:
            raise FileSystemError(f"Failed to create temporary directory: {str(e)}")

    def cleanup(self):
        """Clean up all temporary files and directories."""
        for temp_file in self.temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_file}: {e}")

        for temp_dir in self.temp_dirs:
            try:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
            except OSError as e:
                logger.warning(f"Failed to delete temporary directory {temp_dir}: {e}")

        self.temp_files.clear()
        self.temp_dirs.clear()


class DirectoryScanner:
    def __init__(self, input_obj: Optional[Union[str, list[str], os.PathLike]]):
        self.input_obj = input_obj

    def get_dir_files(self):
        """
        Get file path list given dir/folder

        -------
        Args:
            path: path to the directory/folder
        Returns:
        -------
            list
        """
        files = [
            os.path.join(self.input_obj, f)
            for f in os.listdir(self.input_obj)
            if os.path.isfile(os.path.join(self.input_obj, f))
            and self._is_supported_image(f)
        ]
        if not files:  # Check for empty directory *after* filtering
            raise FileNotFoundError(
                f"No supported image files found in: {self.input_obj}"
            )
        return files

    def _is_supported_image(self, filename: str) -> bool:
        """Checks if a file has a supported image extension."""
        return filename.lower().endswith(tuple(SUPPORTED_IMAGE_FORMATS.values()))

    def _get_image_files(self, files: list = None) -> List[str]:
        """
        Identifies image files to process, handling both single files and directories.

        Returns:
            A list of paths to image files.  Raises FileNotFoundError if no
            valid image files are found.
        """
        files = self.input_obj if not files else files

        if isinstance(files, (str, os.PathLike)):
            if os.path.isfile(files):
                return [files]
            else:
                return self.get_dir_files(files)

        files_to_process = []
        for obj in files:
            if os.path.isfile(obj):
                if self._is_supported_image(obj):
                    files_to_process.append(obj)
                else:
                    logger.warning(f"Skipping unsupported file: {obj}")

            elif os.path.isdir(obj):
                files = self.get_dir_files(obj)
                if not files:  # Check for empty directory *after* filtering
                    raise FileNotFoundError(f"No supported image files found in: {obj}")
                files_to_process.extend(files)
            else:
                raise FileNotFoundError(
                    f"Input is not a valid file or directory: {obj}"
                )
        return files_to_process

    def run(self):
        supported_files = self._get_image_files(self.input_obj)
        return supported_files


def modify_filename_if_exists(filename):
    """
    Modifies the filename by adding "_filemac" before the extension if the original filename exists.

    Args:
        filename (str): The filename to modify.

    Returns:
        str: The modified filename, or the original filename if it doesn't exist or has no extension.
    """
    if os.path.exists(filename):
        parts = filename.rsplit(".", 1)  # Split from the right, at most once
        if len(parts) == 2:
            base, ext = parts
            return f"{base}_filemac.{ext}"
        else:
            return f"{filename}_filemac"  # handle files with no extension.
    else:
        return filename
