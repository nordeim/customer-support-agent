# backend/tests/integration/test_rag_flow.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)

def test_rag_search():
    # Mock the RAG tool
    with patch('app.tools.rag_tool.ChromaClient') as mock_chroma, \
         patch('app.tools.rag_tool.EmbeddingModel') as mock_embedding:
        
        # Setup mocks
        mock_chroma_instance = Mock()
        mock_chroma.return_value = mock_chroma_instance
        
        mock_embedding_instance = Mock()
        mock_embedding.return_value = mock_embedding_instance
        
        # Mock query response
        mock_chroma_instance.query.return_value = {
            "documents": [["Document about password reset"]],
            "ids": [["doc1"]],
            "metadatas": [[{"source": "kb1"}]],
            "distances": [[0.1]]
        }
        
        # Mock embedding
        mock_embedding_instance.embed_query.return_value = [0.1, 0.2, 0.3]
        
        # Import and use the RAG tool directly
        from app.tools.rag_tool import RAGTool
        rag_tool = RAGTool()
        
        # Act
        result = rag_tool.execute({
            "action": "search",
            "query": "How do I reset my password?",
            "session_id": "test-session",
            "n_results": 3
        })
        
        # Assert
        assert "documents" in result
        assert len(result["documents"]) == 1
        assert result["documents"][0]["content"] == "Document about password reset"
        assert result["documents"][0]["metadata"]["source"] == "kb1"
