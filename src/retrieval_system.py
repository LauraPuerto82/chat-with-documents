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
