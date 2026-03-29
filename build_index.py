from ingestion.ingest import load_catalog, chunk_documents
from rag.vectorstore import build_vectorstore

docs = load_catalog("data/sources.json")
chunks = chunk_documents(docs)

build_vectorstore(chunks)

print("Vector DB created successfully")