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

    # Handle empty string
    if not filename:
        return filename

    # Preserve leading dot for dotfiles (e.g., .gitignore)
    leading_dot = ""
    if filename.startswith("."):
        leading_dot = "."
        filename = filename[1:]

    # Split into name and extension
    if "." in filename:
        parts = filename.rsplit(".", 1)
        name, extension = parts[0], parts[1]
    else:
        name, extension = filename, ""

    # Sanitize the name part: replace invalid chars with underscores
    sanitized_name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # Collapse multiple underscores into one
    sanitized_name = re.sub(r"_+", "_", sanitized_name)
    # Remove leading/trailing underscores from name
    sanitized_name = sanitized_name.strip("_")

    # Sanitize extension: only allow alphanumeric characters
    sanitized_extension = re.sub(r"[^a-zA-Z0-9]", "", extension)

    # Reconstruct filename
    if sanitized_extension:
        result = f"{sanitized_name}.{sanitized_extension}"
    else:
        result = sanitized_name

    # Add back leading dot if present
    return leading_dot + result
