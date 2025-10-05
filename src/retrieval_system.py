def query_documents(collection, query_text, n_results=5):
    """
    Query the vector database for relevant document chunks.

    Args:
        collection: ChromaDB collection
        query_text (str): The user's question
        n_results (int): Number of results to return (default: 5)

    Returns:
        dict: Query results with documents, metadatas, and distances
    """
    results = collection.query(query_texts=[query_text], n_results=n_results)
    return results


if __name__ == "__main__":
    import chromadb

    chroma_client = chromadb.PersistentClient(path="./vectordb")
    collection = chroma_client.get_or_create_collection(name="my_documents")

    results = query_documents(
        collection=collection, query_text="docx files", n_results=1
    )

    for i, query_results in enumerate(results["documents"]):
        print("\n".join(query_results))
        print("\n--- Metadata ---")
        print(results["metadatas"][i])
