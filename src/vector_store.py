import chromadb
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document


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
        Document(page_content=c, metadata={"source": file, "chunk": i})
        for i, c in enumerate(chunks)
    ]

    return docs


def create_collection():
    """
    Create or retrieve a ChromaDB collection for document storage.

    Returns:
        chromadb.Collection: The ChromaDB collection named 'my_documents'.
    """
    chroma_client = chromadb.PersistentClient(path="./vectordb")
    collection = chroma_client.get_or_create_collection(name="my_documents")
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
        ids=[str(uuid.uuid4()) for _ in chunks],
        metadatas=[doc.metadata for doc in chunks],
    )

    return collection


if __name__ == "__main__":
    with open("tests/text.txt", "r") as file:
        text = file.read()

    chunks = chunk_text(text, "tests/text.txt")

    print(len(chunks), "chunks")
    for chunk in chunks:
        print(chunk)
        print()

    collection = create_collection()
    collection = add_chunks(chunks, collection)

    results = collection.peek(5)  # Shows first 5 items
    print("\nFirst few items in collection:")
    print(results)
