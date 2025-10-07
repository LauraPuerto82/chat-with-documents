# type: ignore

"""
Unit tests for document_loader.py

Tests document loading functions for various file formats (TXT, PDF, DOCX, ODT)
including error handling for missing and malformed files.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from document_loader import load_txt, load_pdf, load_docx, load_odt


class TestLoadTxt:
    """Test suite for TXT file loading"""

    def test_load_simple_txt_file(self, tmp_path):
        """Test loading a simple text file with multiple lines"""
        test_file = tmp_path / "test.txt"
        content = "Hello, this is a test file.\nWith multiple lines."
        test_file.write_text(content, encoding="utf-8")

        result = load_txt(str(test_file))

        assert result == content

    def test_load_empty_txt_file(self, tmp_path):
        """Test loading an empty text file"""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding="utf-8")

        result = load_txt(str(test_file))

        assert result == ""

    def test_load_txt_with_unicode(self, tmp_path):
        """Test loading text file with Unicode characters (emoji, accents)"""
        test_file = tmp_path / "unicode.txt"
        content = "Hello 世界! Émojis: 🎉 ñoño"
        test_file.write_text(content, encoding="utf-8")

        result = load_txt(str(test_file))

        assert result == content

    def test_load_nonexistent_txt_file(self):
        """Test that loading non-existent file returns empty string"""
        result = load_txt("nonexistent_file.txt")

        assert result == ""

    def test_load_txt_multiline(self, tmp_path):
        """Test that newlines are preserved"""
        test_file = tmp_path / "multiline.txt"
        content = "Line 1\nLine 2\nLine 3"
        test_file.write_text(content, encoding="utf-8")

        result = load_txt(str(test_file))

        assert result == content
        assert result.count("\n") == 2


class TestLoadPdf:
    """Test suite for PDF file loading"""

    def test_load_nonexistent_pdf_returns_empty(self):
        """Test that loading non-existent PDF returns empty string"""
        result = load_pdf("nonexistent.pdf")
        assert result == ""

    def test_load_invalid_pdf_returns_empty(self, tmp_path):
        """Test that malformed PDF file returns empty string with error handling"""
        fake_pdf = tmp_path / "fake.pdf"
        fake_pdf.write_text("This is not a real PDF")

        result = load_pdf(str(fake_pdf))

        assert result == ""


class TestLoadDocx:
    """Test suite for DOCX file loading"""

    def test_load_nonexistent_docx_returns_empty(self):
        """Test that loading non-existent DOCX returns empty string"""
        result = load_docx("nonexistent.docx")
        assert result == ""

    def test_load_invalid_docx_returns_empty(self, tmp_path):
        """Test that malformed DOCX file returns empty string with error handling"""
        fake_docx = tmp_path / "fake.docx"
        fake_docx.write_text("This is not a real DOCX")

        result = load_docx(str(fake_docx))

        assert result == ""


class TestLoadOdt:
    """Test suite for ODT file loading"""

    def test_load_nonexistent_odt_returns_empty(self):
        """Test that loading non-existent ODT returns empty string"""
        result = load_odt("nonexistent.odt")
        assert result == ""

    def test_load_invalid_odt_returns_empty(self, tmp_path):
        """Test that malformed ODT file returns empty string with error handling"""
        fake_odt = tmp_path / "fake.odt"
        fake_odt.write_text("This is not a real ODT")

        result = load_odt(str(fake_odt))

        assert result == ""


def test_all_loaders_return_strings(tmp_path):
    """Test that all loader functions return string type (even on errors)"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    result = load_txt(str(test_file))
    assert isinstance(result, str)

    assert isinstance(load_pdf("fake.pdf"), str)
    assert isinstance(load_docx("fake.docx"), str)
    assert isinstance(load_odt("fake.odt"), str)
