"""
CLI application for document-based question answering using RAG (Retrieval-Augmented Generation).
Scans a directory for documents, indexes them in a vector store, and enables conversational Q&A.
"""

import os
import time
import sys

from document_loader import load_txt, load_pdf, load_docx, load_odt
from scan_folders import scan_folders
from vector_store import (
    chunk_text,
    create_collection,
    add_chunks,
    create_file_index_chunk,
)
from response_generator import set_llm, generate_answer, set_history
from retrieval_system import query_documents

# Map file extensions to loader functions
loaders = {".txt": load_txt, ".pdf": load_pdf, ".docx": load_docx, ".odt": load_odt}

# Get directory from user input with validation
directory = input("Enter directory to scan (default: data): ").strip()
if not directory:
    directory = "data"
    print(f"Default directory used: '{directory}'")
elif not os.path.isdir(directory):
    print(f"Directory '{directory}' not found. Using default directory 'data' instead.")
    directory = "data"
else:
    print(f"Directory used: '{directory}'")

# Scan directory for supported documents
files = scan_folders(directory)
if not files:
    print("No documents found to index. Exiting.")
    sys.exit(0)

# Create directory-specific vector database collection
try:
    collection = create_collection(directory)
except Exception:
    print("Error setting up the document storage system.")
    sys.exit(1)

# Load and index each document into the vector store
for file in files:
    name, extension = os.path.splitext(file)
    try:
        fn = loaders[extension]
        content = fn(file)
    except KeyError:
        # Skip unsupported file types
        content = ""
        print(f"File {file} not supported. Skipping.")

    chunks = chunk_text(content, file)
    if chunks:
        try:
            collection = add_chunks(chunks, collection)
        except Exception:
            # skip problematic files and continue indexing others
            print(f"Error processing file {file}. Skipping.")
            continue

# Create and add file index chunk (provides LLM with list of available documents)
file_index = create_file_index_chunk(files)
try:
    collection = add_chunks(file_index, collection)
except Exception:
    print("Warning: Could not index file names. You can still search document content.")

# Display indexing completion timestamp
print(time.strftime("%b %d, %Y %H:%M:%S"))

# Initialize LLM and conversation history
llm = set_llm()
history = []


# Main chat loop: handle user queries with RAG-based responses
while True:
    user_input = input("Type a question or exit for exit the program: ")

    if user_input.lower() == "exit":
        break

    # Retrieve relevant document chunks via semantic search
    try:
        related_chunks = query_documents(collection=collection, query_text=user_input)
    except Exception:
        # allow user to retry query
        print("Error searching documents. Please try again.")
        continue

    # Generate LLM response using retrieved context and conversation history
    answer = generate_answer(llm, user_input, related_chunks, history)
    print(answer)

    # Append to conversation history for context continuity
    history = set_history(history=history, query=user_input, answer=answer)
