# type: ignore

"""
Unit tests for vector_store.py

Tests text chunking and file indexing functionality for the vector database,
including metadata generation and document splitting logic.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vector_store import chunk_text, create_file_index_chunk
from langchain.schema import Document


class TestChunkText:
    """Test suite for text chunking functionality"""

    def test_chunk_short_text(self):
        """Test that text shorter than chunk size creates single chunk"""
        text = "This is a short text."
        file = "test.txt"

        result = chunk_text(text, file)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)

    def test_chunk_creates_documents_with_metadata(self):
        """Test that chunks include source file and index in metadata"""
        text = "Test content"
        file = "source.txt"

        result = chunk_text(text, file)

        assert result[0].metadata["source"] == file
        assert "chunk" in result[0].metadata

    def test_chunk_includes_source_in_content(self):
        """Test that source file reference is prepended to chunk content"""
        text = "Test content"
        file = "myfile.txt"

        result = chunk_text(text, file)

        assert "[Source: myfile.txt]" in result[0].page_content
        assert "Test content" in result[0].page_content

    def test_chunk_long_text_creates_multiple_chunks(self):
        """Test that text longer than chunk_size (500 chars) is split"""
        text = "This is a sentence. " * 100  # ~2000 characters

        result = chunk_text(text, "long.txt")

        assert len(result) > 1

    def test_chunk_metadata_has_sequential_indices(self):
        """Test that chunk indices are assigned sequentially starting from 0"""
        text = "Sentence. " * 100

        result = chunk_text(text, "test.txt")

        for i, doc in enumerate(result):
            assert doc.metadata["chunk"] == i

    def test_chunk_empty_text(self):
        """Test that empty text input is handled gracefully"""
        text = ""
        result = chunk_text(text, "empty.txt")

        assert isinstance(result, list)

    def test_chunk_text_with_newlines(self):
        """Test that chunking respects paragraph boundaries"""
        text = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"
        result = chunk_text(text, "test.txt")

        assert len(result) >= 1
        assert isinstance(result[0], Document)


class TestCreateFileIndexChunk:
    """Test suite for file index chunk creation"""

    def test_create_index_with_single_file(self):
        """Test that single file is properly formatted in index"""
        files = ["file1.txt"]

        result = create_file_index_chunk(files)

        assert isinstance(result, list)
        assert len(result) >= 1
        assert isinstance(result[0], Document)
        assert "file1.txt" in result[0].page_content

    def test_create_index_with_multiple_files(self):
        """Test that all files appear in the generated index chunks"""
        files = ["file1.txt", "file2.pdf", "file3.docx"]

        result = create_file_index_chunk(files)

        assert len(result) >= 1

        all_content = " ".join([doc.page_content for doc in result])
        for file in files:
            assert file in all_content

    def test_create_index_includes_header(self):
        """Test that index contains descriptive header text"""
        files = ["test.txt"]

        result = create_file_index_chunk(files)

        assert "indexed" in result[0].page_content.lower()

    def test_create_index_metadata_correct(self):
        """Test that index chunks have proper metadata attribution"""
        files = ["file1.txt", "file2.txt"]

        result = create_file_index_chunk(files)

        for doc in result:
            assert doc.metadata["source"] == "indexing files"
            assert "chunk" in doc.metadata

    def test_create_index_empty_file_list(self):
        """Test that empty file list is handled without errors"""
        files = []

        result = create_file_index_chunk(files)

        assert isinstance(result, list)

    def test_create_index_many_files(self):
        """Test that large file lists are chunked appropriately"""
        files = [f"file{i}.txt" for i in range(100)]

        result = create_file_index_chunk(files)

        assert len(result) >= 1

        all_content = " ".join([doc.page_content for doc in result])
        assert "file0.txt" in all_content
        assert "file99.txt" in all_content


def test_chunk_text_realistic_document():
    """Test chunking multi-section document with realistic structure"""
    text = """
    Introduction

    This is a sample document that contains multiple paragraphs.
    It simulates real content that would be chunked for RAG.

    Section 1: Background

    The background section provides context about the topic.
    This helps the reader understand the motivation for the work.

    Section 2: Methods

    We describe our methodology here.
    Multiple steps are involved in the process.

    Conclusion

    This concludes our document.
    """

    result = chunk_text(text, "sample.txt")

    assert isinstance(result, list)
    assert all(isinstance(doc, Document) for doc in result)
    assert all("[Source: sample.txt]" in doc.page_content for doc in result)

    for i, doc in enumerate(result):
        assert doc.metadata["source"] == "sample.txt"
        assert doc.metadata["chunk"] == i
