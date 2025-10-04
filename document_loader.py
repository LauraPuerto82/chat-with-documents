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
    with open(filepath, "r") as file:
        return file.read()


def load_pdf(filepath):
    """
    Load and extract text content from a PDF file.

    Args:
        filepath (str): Path to the .pdf file

    Returns:
        str: The extracted text content from all pages
    """
    reader = PdfReader(filepath)
    content = "\n".join(page.extract_text() or "" for page in reader.pages)
    return content


def load_docx(filepath):
    """
    Load and extract text content from a DOCX file.

    Args:
        filepath (str): Path to the .docx file

    Returns:
        str: The extracted text content from all paragraphs
    """
    document = Document(filepath)
    content = "\n".join([p.text for p in document.paragraphs])
    return content


def load_odt(filepath):
    """
    Load and extract text content from an ODT file.

    Args:
        filepath (str): Path to the .odt file

    Returns:
        str: The extracted text content from all paragraphs
    """
    document = load(filepath)

    all_paragraphs = [
        teletype.extractText(p) for p in document.getElementsByType(text.P)
    ]
    content = "\n".join(all_paragraphs)
    return content


if __name__ == "__main__":
    print("---TXT---")
    print(load_txt("data/test.txt"))
    print("\n" * 2)
    print("---PDF---")
    print(load_pdf("data/test.pdf"))
    print("\n" * 2)
    print("---DOCX---")
    print(load_docx("data/test.docx"))
    print("\n" * 2)
    print("---ODT---")
    print(load_odt("data/test.odt"))
