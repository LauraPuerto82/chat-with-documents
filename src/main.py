import os

from document_loader import load_txt, load_pdf, load_docx, load_odt
from scan_folders import scan_folders
from vector_store import chunk_text, create_collection, add_chunks

loaders = {".txt": load_txt, ".pdf": load_pdf, ".docx": load_docx, ".odt": load_odt}

files = scan_folders()
collection = create_collection()

for file in files:
    name, extension = os.path.splitext(file)
    fn = loaders[extension]
    content = fn(file)

    chunks = chunk_text(content, file)
    collection = add_chunks(chunks, collection)
