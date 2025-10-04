import os

from document_loader import load_txt, load_pdf, load_docx, load_odt
from scan_folders import scan_folders

loaders = {".txt": load_txt, ".pdf": load_pdf, ".docx": load_docx, ".odt": load_odt}

files = scan_folders()

for file in files:
    name, extension = os.path.splitext(file)
    fn = loaders[extension]
    print(f"\n--- {file} ---")
    print(fn(file))
