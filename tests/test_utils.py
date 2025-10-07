# type: ignore

"""
Unit tests for utils.py

Tests the sanitize_filename function to ensure filenames are properly
sanitized for cross-platform compatibility and storage system constraints.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import sanitize_filename


class TestSanitizeFilename:
    """Test suite for sanitize_filename function"""

    def test_valid_filename_unchanged(self):
        """Test that valid filenames pass through unchanged"""
        filename = "valid_file.txt"
        result = sanitize_filename(filename)
        assert result == "valid_file.txt"

    def test_spaces_replaced_with_underscores(self):
        """Test that spaces become underscores"""
        filename = "my file name.pdf"
        result = sanitize_filename(filename)
        assert result == "my_file_name.pdf"

    def test_special_characters_removed(self):
        """Test that special characters like !, @, # are removed"""
        filename = "file!@#$%.txt"
        result = sanitize_filename(filename)
        assert result == "file.txt"

    def test_slashes_replaced(self):
        """Test that slashes (Windows/Linux paths) are replaced"""
        filename = "path/to/file.doc"
        result = sanitize_filename(filename)
        assert result == "path_to_file.doc"

    def test_multiple_underscores_from_special_chars(self):
        """Test that multiple special characters become underscores"""
        filename = "file   with   spaces.txt"
        result = sanitize_filename(filename)
        assert result == "file_with_spaces.txt"

    def test_leading_trailing_underscores_removed(self):
        """Test that underscores at start/end are removed"""
        filename = "___file___.txt"
        result = sanitize_filename(filename)        
        assert result == "file.txt"

    def test_only_extension_preserved(self):
        """Test that dotfiles (e.g., .gitignore) are preserved correctly"""
        filename = ".gitignore"
        result = sanitize_filename(filename)
        assert result == ".gitignore"

    def test_empty_string_handling(self):
        """Test that empty string input returns empty string"""
        filename = ""
        result = sanitize_filename(filename)
        assert result == ""

    def test_invalid_type_raises_error(self):
        """Test that non-string input raises TypeError"""
        with pytest.raises(TypeError):
            sanitize_filename(123)

        with pytest.raises(TypeError):
            sanitize_filename(None)

        with pytest.raises(TypeError):
            sanitize_filename(["list"])


def test_sanitize_real_world_example():
    """Test Windows path with special characters gets properly sanitized"""
    filename = "C:\\Users\\Documents\\My File (1).docx"
    result = sanitize_filename(filename)
    assert result == "C_Users_Documents_My_File_1.docx"


def test_sanitize_preserves_numbers():
    """Test that numbers are preserved"""
    filename = "report2024_v2.pdf"
    result = sanitize_filename(filename)
    assert result == "report2024_v2.pdf"
