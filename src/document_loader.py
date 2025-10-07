from pypdf import PdfReader
from docx import Document
from odf.opendocument import load
from odf import text, teletype


def load_txt(filepath):
    """
    Load and extract text content from a TXT file.

    Args:
        filepath (str): Path to the .txt file

    Returns:
        str: The full text content of the file
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("The file does not exist. Please check the path or select another file.")
    except PermissionError:
        print("You don't have permission to access this file.")
    except Exception:
        print("An unexpected error occurred while trying to read the file.")
    return ""


def load_pdf(filepath):
    """
    Load and extract text content from a PDF file.

    Args:
        filepath (str): Path to the .pdf file

    Returns:
        str: The extracted text content from all pages
    """
    try:
        reader = PdfReader(filepath)
        content = "\n".join(page.extract_text() or "" for page in reader.pages)
        return content
    except FileNotFoundError:
        print("The file does not exist. Please check the path or select another file.")
    except PermissionError:
        print("You don't have permission to access this file.")
    except Exception:
        print("An unexpected error occurred while trying to read the file.")
    return ""


def load_docx(filepath):
    """
    Load and extract text content from a DOCX file.

    Args:
        filepath (str): Path to the .docx file

    Returns:
        str: The extracted text content from all paragraphs
    """
    try:
        document = Document(filepath)
        content = "\n".join([p.text for p in document.paragraphs])
        return content
    except FileNotFoundError:
        print("The file does not exist. Please check the path or select another file.")
    except PermissionError:
        print("You don't have permission to access this file.")
    except Exception:
        print("An unexpected error occurred while trying to read the file.")
    return ""


def load_odt(filepath):
    """
    Load and extract text content from an ODT file.

    Args:
        filepath (str): Path to the .odt file

    Returns:
        str: The extracted text content from all paragraphs
    """
    try:
        document = load(filepath)

        all_paragraphs = [
            teletype.extractText(p) for p in document.getElementsByType(text.P)
        ]
        content = "\n".join(all_paragraphs)
        return content
    except FileNotFoundError:
        print("The file does not exist. Please check the path or select another file.")
    except PermissionError:
        print("You don't have permission to access this file.")
    except Exception:
        print("An unexpected error occurred while trying to read the file.")
    return ""
