import os
import time

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

# Map file extensions to their corresponding loader functions
loaders = {".txt": load_txt, ".pdf": load_pdf, ".docx": load_docx, ".odt": load_odt}

directory = input("Enter directory to scan (default: data): ").strip()
if not directory:
    directory = "data"
elif not os.path.isdir(directory):
    print(f"Directory '{directory}' not found. Using default 'data' instead.")
    directory = "data"

# Initialize: scan for documents and create vector database collection
files = scan_folders(directory)
collection = create_collection(directory)

# Process each document: load, chunk, and add to vector store
for file in files:
    name, extension = os.path.splitext(file)
    fn = loaders[extension]
    content = fn(file)

    chunks = chunk_text(content, file)
    if chunks:
        collection = add_chunks(chunks, collection)

# Add a special chunk listing all indexed files (helps LLM know what's available)
file_index = create_file_index_chunk(files)
collection = add_chunks(file_index, collection)

print(time.strftime("%b %d, %Y %H:%M:%S"))

# Set up the language model and initialize empty chat history
llm = set_llm()
history = []


# Main chat loop: retrieve relevant chunks, generate answers, and maintain conversation history
while True:
    user_input = input("Type a question or exit for exit the program: ")

    if user_input.lower() == "exit":
        break

    # Find relevant document chunks using semantic search
    related_chunks = query_documents(collection=collection, query_text=user_input)

    # Generate answer using LLM with context and history
    answer = generate_answer(llm, user_input, related_chunks, history)
    print(answer)

    # Update conversation history for context in future responses
    history = set_history(history=history, query=user_input, answer=answer)
