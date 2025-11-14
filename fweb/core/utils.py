import os
import json
import tempfile
import logging
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.conf import settings

logger = logging.getLogger("fweb")


class FileProcessor:
    """Handle file processing operations"""

    def __init__(self):
        self.storage = FileSystemStorage()
        self.media_root = settings.MEDIA_ROOT
        self.processed_dir = os.path.join(self.media_root, "processed")

        # Create processed directory if it doesn't exist
        os.makedirs(self.processed_dir, exist_ok=True)

    def save_uploaded_files(self, files):
        """Save uploaded files to temporary location"""
        saved_paths = []
        for file in files:
            # Save to temporary directory
            temp_path = os.path.join(self.processed_dir, file.name)
            with open(temp_path, "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)
            saved_paths.append(temp_path)
        return saved_paths

    def cleanup_files(self, file_paths):
        """Clean up processed files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Could not delete file {file_path}: {e}")

    def get_file_info(self, file_path):
        """Get information about a file"""
        stat = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "extension": os.path.splitext(file_path)[1].lower(),
        }


class CLIInterface:
    """Interface with the CLI functionality"""

    def __init__(self):
        # Import your CLI modules here
        try:
            # Adjust these imports based on your actual module structure
            from filemac.main import Cmd_arg_Handler, argsOPMaper

            self.cli_handler = Cmd_arg_Handler
            self.arg_mapper = argsOPMaper
        except ImportError as e:
            logger.error(f"Could not import CLI modules: {e}")
            self.cli_handler = None
            self.arg_mapper = None

    def execute_command(self, args):
        """Execute CLI command with given arguments"""
        if not self.cli_handler:
            raise ImportError("CLI modules not available")

        try:
            # Mock execution - replace with actual CLI call
            # In a real implementation, you would call your CLI functions here
            logger.info(f"Executing CLI command with args: {args}")

            # This is where you'd integrate with your actual CLI code
            # For now, return mock results
            return self._mock_execution(args)

        except Exception as e:
            logger.error(f"CLI execution failed: {e}")
            raise

    def _mock_execution(self, args):
        """Mock CLI execution for demonstration"""
        # Simulate processing time
        import time

        time.sleep(2)

        # Generate mock results
        results = []
        for arg in args:
            if arg.startswith("--") or arg.startswith("-"):
                continue
            if os.path.exists(arg):
                results.append(
                    {
                        "input": os.path.basename(arg),
                        "output": f"{os.path.splitext(arg)[0]}_converted{os.path.splitext(arg)[1]}",
                        "status": "success",
                    }
                )

        return {
            "success": True,
            "message": f"Processed {len(results)} files",
            "results": results,
        }


# Utility functions
def validate_file_type(file_path, allowed_extensions):
    """Validate file type based on extension"""
    extension = os.path.splitext(file_path)[1].lower()
    return extension in allowed_extensions


def get_supported_formats(tool_id):
    """Get supported formats for a tool"""
    format_map = {
        "convert_doc": [".pdf", ".docx", ".doc", ".txt", ".html"],
        "convert_image": [".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"],
        "convert_audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
        "convert_video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "ocr": [".png", ".jpg", ".jpeg", ".pdf", ".tiff"],
        "pdf_join": [".pdf"],
        "audio_join": [".mp3", ".wav", ".flac", ".m4a"],
    }
    return format_map.get(tool_id, [])


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"
