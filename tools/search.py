"""
Offline RAG tools for the Research Agent.
Indexes local documents using ChromaDB and Ollama embeddings.
"""
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_search_tool():
    """Create a local vector store retriever tool from PDFs in data/."""
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Load documents
    loader = PyPDFDirectoryLoader(data_dir)
    docs = loader.load()
    
    if not docs:
        # If no docs, create a dummy document so it doesn't crash
        docs = [Document(page_content="No local documents uploaded yet in the data/ folder.", metadata={"source": "system"})]
        
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Embeddings using Ollama natively
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    return retriever