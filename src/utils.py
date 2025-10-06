import re


def sanitize_filename(filename: str) -> str:
    """Sanitizes a filename by removing or replacing invalid characters.

    Args:
        filename: The filename to sanitize.

    Returns:
        The sanitized filename.

    Raises:
        TypeError: If filename is not a string.

    Examples:
        sanitize_filename("My File!.txt")
        'My_File.txt'

        sanitize_filename("file with spaces.pdf")
        'file_with_spaces.pdf'

        sanitize_filename("file/with/slashes.doc")
        'file_with_slashes.doc'
    """
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")

    # Replace invalid characters with underscores
    sanitized_name = re.sub(r"[^a-zA-Z0-9_\.]", "_", filename)

    # Remove leading and trailing underscores
    sanitized_name = sanitized_name.strip("_")

    return sanitized_name
