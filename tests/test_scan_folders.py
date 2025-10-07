# type: ignore

"""
Unit tests for scan_folders.py

Tests recursive directory scanning functionality to ensure proper
file discovery across nested directory structures.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scan_folders import scan_folders


class TestScanFolders:
    """Test suite for recursive folder scanning"""

    def test_scan_empty_directory(self, tmp_path):
        """Test that scanning an empty directory returns empty list"""
        result = scan_folders(str(tmp_path))
        assert result == []

    def test_scan_single_file(self, tmp_path):
        """Test scanning directory with one file"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = scan_folders(str(tmp_path))

        assert len(result) == 1
        assert result[0].endswith("test.txt")

    def test_scan_multiple_files(self, tmp_path):
        """Test scanning directory with multiple files"""
        (tmp_path / "file1.txt").write_text("content 1")
        (tmp_path / "file2.pdf").write_text("content 2")
        (tmp_path / "file3.docx").write_text("content 3")

        result = scan_folders(str(tmp_path))

        assert len(result) == 3

    def test_scan_nested_directories(self, tmp_path):
        """Test recursive scanning finds files in subdirectories"""
        # Directory structure:
        # tmp_path/
        #   ├── file1.txt
        #   └── subdir/
        #       ├── file2.txt
        #       └── deep/
        #           └── file3.txt
        (tmp_path / "file1.txt").write_text("root file")

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("subdir file")

        deep = subdir / "deep"
        deep.mkdir()
        (deep / "file3.txt").write_text("deep file")

        result = scan_folders(str(tmp_path))

        assert len(result) == 3

    def test_scan_ignores_directories(self, tmp_path):
        """Test that only files are returned, not directory names"""
        (tmp_path / "file.txt").write_text("file")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "another_dir").mkdir()

        result = scan_folders(str(tmp_path))

        assert len(result) == 1
        assert result[0].endswith("file.txt")

    def test_scan_mixed_file_types(self, tmp_path):
        """Test scanning finds all file types (.pdf, .txt, .docx, etc.)"""
        (tmp_path / "document.pdf").write_text("pdf")
        (tmp_path / "text.txt").write_text("txt")
        (tmp_path / "word.docx").write_text("docx")
        (tmp_path / "odt.odt").write_text("odt")
        (tmp_path / "image.png").write_text("png")

        result = scan_folders(str(tmp_path))

        assert len(result) == 5

    def test_scan_nonexistent_directory_returns_empty(self):
        """Test that scanning a non-existent directory returns empty list without errors"""
        fake_path = "C:\\this\\path\\does\\not\\exist\\xyz123"
        result = scan_folders(fake_path)

        assert result == []

    def test_default_data_directory(self):
        """Test that function defaults to 'data' directory when no argument provided"""
        result = scan_folders()

        assert isinstance(result, list)


def test_scan_folders_returns_list():
    """Test that scan_folders always returns a list type"""
    result = scan_folders("nonexistent")
    assert isinstance(result, list)


def test_scan_folders_with_special_characters_in_path(tmp_path):
    """Test that filenames with spaces and special characters are handled correctly"""
    test_file = tmp_path / "my document (1).txt"
    test_file.write_text("content")

    result = scan_folders(str(tmp_path))

    assert len(result) == 1
    assert "my document (1).txt" in result[0]
