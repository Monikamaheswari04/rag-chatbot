# loader.py
import os
import fitz  # PyMuPDF
from docx import Document

def load_documents(data_dir="data"):
    docs = []
    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)
        if file.endswith(".pdf"):
            pdf = fitz.open(path)
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                docs.append({
                    "content": page.get_text(),
                    "source": file,
                    "page": page_num + 1
                })
        elif file.endswith(".docx"):
            doc = Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
            docs.append({
                "content": text,
                "source": file,
                "page": 1
            })
    return docs

def chunk_documents(docs, chunk_size=500, overlap=100):
    chunks = []
    for doc in docs:
        text = doc["content"]
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append({
                "content": chunk,
                "source": doc["source"],
                "page": doc["page"]
            })
    return chunks
