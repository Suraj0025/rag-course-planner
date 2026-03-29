import os, re, json
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF

CHUNK_SIZE    = 800   # tokens (~600 words) — large enough to capture full prereq rule
CHUNK_OVERLAP = 150   # 19% overlap — preserves sentences at boundaries

def load_html(path: str, metadata: Dict) -> List[Document]:
    with open(path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    # Remove nav/header/footer noise
    for tag in soup(['nav','header','footer','script','style']):
        tag.decompose()
    text = re.sub(r'\n{3,}', '\n\n', soup.get_text(separator='\n')).strip()
    return [Document(page_content=text, metadata=metadata)]

def load_pdf(path: str, metadata: Dict) -> List[Document]:
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        m = {**metadata, 'page': i+1}
        pages.append(Document(page_content=text, metadata=m))
    return pages

def load_text(path: str, metadata: Dict) -> List[Document]:
    text = Path(path).read_text(encoding='utf-8')
    return [Document(page_content=text, metadata=metadata)]

def load_catalog(catalog_json: str) -> List[Document]:
    """Load all sources described in data/sources.json"""
    sources = json.loads(Path(catalog_json).read_text())
    docs = []
    for src in sources:
        path = src['local_path']
        meta = {
            'source': src['url'],
            'doc_type': src['doc_type'],  # course | program | policy
            'title': src['title'],
            'accessed': src['accessed'],
        }
        ext = Path(path).suffix.lower()
        if ext in ('.html', '.htm'): docs += load_html(path, meta)
        elif ext == '.pdf':          docs += load_pdf(path, meta)
        else:                        docs += load_text(path, meta)
    return docs

def chunk_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=['\n\n','\n','. ','! ','? ',' '],
        length_function=lambda x: len(x.split())  # rough token count,
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = f"{chunk.metadata['doc_type']}_{i:04d}"
    return chunks

if __name__ == '__main__':
    docs   = load_catalog('data/sources.json')
    chunks = chunk_documents(docs)
    print(f'Loaded {len(docs)} docs → {len(chunks)} chunks')
