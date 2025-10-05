import os


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
