from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "data/faiss_index"

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(INDEX_PATH)
    return vs

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

def get_retriever(vs, k=6):
    return vs.as_retriever(search_kwargs={"k": k})
