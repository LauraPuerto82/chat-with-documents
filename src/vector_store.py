import chromadb
import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from utils import sanitize_filename


def chunk_text(text, file):
    """
    Split text into smaller chunks with metadata for vector storage.

    Args:
        text (str): The text content to be split into chunks.
        file (str): The source file path to be stored in metadata.

    Returns:
        list[Document]: List of Document objects containing chunked text with metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_text(text)

    docs = [
        Document(
            page_content=f"[Source: {file}]\n\n{content}",
            metadata={"source": file, "chunk": index},
        )
        for index, content in enumerate(chunks)
    ]

    return docs


def create_collection(path):
    """
    Create or retrieve a ChromaDB collection for document storage.

    Returns:
        chromadb.Collection: The ChromaDB collection named after the sanitized path.
    """
    name = sanitize_filename(path)
    chroma_client = chromadb.PersistentClient(path="./vectordb")
    collection = chroma_client.get_or_create_collection(name=name)
    return collection


def add_chunks(chunks, collection):
    """
    Add document chunks to a ChromaDB collection.

    Args:
        chunks (list[Document]): List of Document objects to add to the collection.
        collection (chromadb.Collection): The ChromaDB collection to add chunks to.

    Returns:
        chromadb.Collection: The updated collection with new chunks.
    """
    collection.upsert(
        documents=[doc.page_content for doc in chunks],
        # Generate deterministic IDs using MD5 hash of source+index
        # This ensures same document chunks get same ID, preventing duplicates on re-indexing
        ids=[
            hashlib.md5(f"{doc.metadata['source']}-{i}".encode()).hexdigest()
            for i, doc in enumerate(chunks)
        ],
        metadatas=[doc.metadata for doc in chunks],
    )

    return collection


def create_file_index_chunk(files):
    """
    Create document chunks from a list of indexed file paths.

    Args:
        files (list[str]): List of file paths that were indexed.

    Returns:
        list[Document]: List of Document objects containing file index information.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )

    text = "The following files were indexed:\n" + "\n".join(files)
    chunks = splitter.split_text(text)

    docs = [
        Document(page_content=c, metadata={"source": "indexing files", "chunk": i})
        for i, c in enumerate(chunks)
    ]

    return docs
