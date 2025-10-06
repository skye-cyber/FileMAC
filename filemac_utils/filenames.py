import uuid
from pathlib import Path
from .config import OUTPUT_DIR


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
