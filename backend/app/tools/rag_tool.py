# backend/app/tools/rag_tool.py
from typing import Dict, Any, List
import hashlib
from ..vector_store.chroma_client import ChromaClient
from ..vector_store.embeddings import EmbeddingModel
from ..core.cache import cache_manager, cache_result
from ..core.logging import logger
from ..core.config import settings
from ..metrics import track_rag_metrics

class RAGTool:
    """Tool for Retrieval-Augmented Generation with caching"""
    
    def __init__(self):
        self.chroma_client = ChromaClient(
            persist_directory=settings.chroma_persist_directory
        )
        self.embedding_model = EmbeddingModel(
            model_name=settings.embedding_model_name
        )
    
    def _generate_cache_key(self, query: str, n_results: int) -> str:
        """Generate cache key for RAG query"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return f"rag_query:{query_hash}:{n_results}"
    
    @track_rag_metrics
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the RAG tool with caching"""
        action = parameters.get("action")
        
        if action == "search":
            return self._search_cached(parameters)
        elif action == "add_document":
            return self._add_document(parameters)
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _search_cached(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Search with caching"""
        query = parameters.get("query")
        n_results = parameters.get("n_results", 5)
        session_id = parameters.get("session_id")
        
        if not query:
            return {"error": "Query is required"}
        
        # Generate cache key
        cache_key = self._generate_cache_key(query, n_results)
        
        # Try to get from cache
        cached_result = cache_manager.get(cache_key)
        if cached_result:
            logger.info(
                f"RAG cache hit for query: {query[:50]}...",
                extra={"session_id": session_id, "tool_name": "rag_tool"}
            )
            return cached_result
        
        # Perform search
        result = self._search(parameters)
        
        # Cache result for 30 minutes
        cache_manager.set(cache_key, result, ttl=1800)
        
        return result
    
    def _search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform actual search"""
        query = parameters.get("query")
        n_results = parameters.get("n_results", 5)
        session_id = parameters.get("session_id")
        
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.embed_query(query)
            
            # Search in Chroma
            results = self.chroma_client.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            documents = []
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "id": results["ids"][0][i],
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
            
            logger.info(
                f"RAG search for session {session_id} returned {len(documents)} documents",
                extra={"session_id": session_id, "tool_name": "rag_tool", "query": query}
            )
            
            return {"documents": documents}
        except Exception as e:
            logger.error(
                f"RAG search failed for session {session_id}: {str(e)}",
                extra={"session_id": session_id, "tool_name": "rag_tool"}
            )
            return {"error": f"Search failed: {str(e)}"}
    
    def _add_document(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Add a document to the vector store"""
        content = parameters.get("content")
        metadata = parameters.get("metadata", {})
        document_id = parameters.get("document_id")
        
        if not content:
            return {"error": "Content is required"}
        
        try:
            # Generate embedding for the document
            embedding = self.embedding_model.embed_document(content)
            
            # Add to Chroma
            self.chroma_client.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[document_id] if document_id else None
            )
            
            # Clear relevant cache entries
            cache_manager.clear_pattern("rag_query:*")
            
            logger.info(
                f"Added document to vector store",
                extra={"tool_name": "rag_tool", "document_id": document_id}
            )
            
            return {"success": True, "message": "Document added successfully"}
        except Exception as e:
            logger.error(
                f"Failed to add document to vector store: {str(e)}",
                extra={"tool_name": "rag_tool"}
            )
            return {"error": f"Failed to add document: {str(e)}"}
