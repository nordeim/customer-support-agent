# backend/scripts/populate_kb.py
import os
import argparse
from app.vector_store.chroma_client import ChromaClient
from app.vector_store.embeddings import EmbeddingModel
from app.core.config import settings
from app.core.logging import logger, setup_logging

def populate_knowledge_base(documents_dir: str):
    """Populate the knowledge base with documents from a directory"""
    # Setup logging
    setup_logging()
    
    # Initialize components
    chroma_client = ChromaClient(
        persist_directory=settings.chroma_persist_directory
    )
    embedding_model = EmbeddingModel(
        model_name=settings.embedding_model_name
    )
    
    # Get all text files in the directory
    documents = []
    metadatas = []
    ids = []
    
    for filename in os.listdir(documents_dir):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(documents_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            documents.append(content)
            metadatas.append({"source": filename})
            ids.append(filename.replace(".", "_"))
    
    if not documents:
        logger.warning("No documents found in the specified directory")
        return
    
    # Generate embeddings
    logger.info(f"Generating embeddings for {len(documents)} documents")
    embeddings = embedding_model.embed_documents(documents)
    
    # Add to Chroma
    logger.info("Adding documents to Chroma")
    chroma_client.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    logger.info(f"Successfully added {len(documents)} documents to the knowledge base")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate the knowledge base with documents")
    parser.add_argument("--documents-dir", required=True, help="Directory containing documents to add")
    args = parser.parse_args()
    
    populate_knowledge_base(args.documents_dir)
