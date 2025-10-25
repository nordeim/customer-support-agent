# backend/app/vector_store/chroma_client.py
import chromadb
from typing import List, Dict, Any, Optional
from ..core.logging import logger

class ChromaClient:
    """Client for interacting with Chroma vector database"""
    
    def __init__(self, persist_directory: str, collection_name: str = "knowledge_base"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Connected to existing Chroma collection: {collection_name}")
        except Exception:
            self.collection = self.client.create_collection(name=collection_name)
            logger.info(f"Created new Chroma collection: {collection_name}")
    
    def add(
        self,
        documents: List[str],
        embeddings: Optional[List[List[float]]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Add documents to the collection"""
        try:
            result = self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(
                f"Added {len(documents)} documents to Chroma collection",
                extra={"tool_name": "chroma_client", "count": len(documents)}
            )
            
            return result
        except Exception as e:
            logger.error(
                f"Failed to add documents to Chroma: {str(e)}",
                extra={"tool_name": "chroma_client"}
            )
            raise
    
    def query(
        self,
        query_embeddings: Optional[List[List[float]]] = None,
        query_texts: Optional[List[str]] = None,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query the collection"""
        try:
            result = self.collection.query(
                query_embeddings=query_embeddings,
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                where_document=where_document
            )
            
            logger.info(
                f"Queried Chroma collection, returned {len(result['ids'][0])} results",
                extra={"tool_name": "chroma_client", "result_count": len(result['ids'][0])}
            )
            
            return result
        except Exception as e:
            logger.error(
                f"Failed to query Chroma: {str(e)}",
                extra={"tool_name": "chroma_client"}
            )
            raise
    
    def get(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get documents from the collection"""
        try:
            result = self.collection.get(
                ids=ids,
                where=where,
                limit=limit
            )
            
            logger.info(
                f"Retrieved {len(result['ids'])} documents from Chroma",
                extra={"tool_name": "chroma_client", "count": len(result['ids'])}
            )
            
            return result
        except Exception as e:
            logger.error(
                f"Failed to get documents from Chroma: {str(e)}",
                extra={"tool_name": "chroma_client"}
            )
            raise
