# backend/tests/unit/test_rag_tool.py
import pytest
from unittest.mock import Mock, patch
from app.tools.rag_tool import RAGTool

@pytest.fixture
def rag_tool():
    with patch('app.tools.rag_tool.ChromaClient'), \
         patch('app.tools.rag_tool.EmbeddingModel'):
        return RAGTool()

def test_search_success(rag_tool):
    # Arrange
    parameters = {
        "action": "search",
        "query": "How do I reset my password?",
        "session_id": "test-session",
        "n_results": 3
    }
    
    # Mock Chroma client response
    mock_results = {
        "documents": [["Document 1 content", "Document 2 content"]],
        "ids": [["doc1", "doc2"]],
        "metadatas": [[{"source": "kb1"}, {"source": "kb2"}]],
        "distances": [[0.1, 0.2]]
    }
    
    rag_tool.chroma_client.query.return_value = mock_results
    
    # Mock embedding model
    rag_tool.embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]
    
    # Act
    result = rag_tool.execute(parameters)
    
    # Assert
    assert "documents" in result
    assert len(result["documents"]) == 2
    assert result["documents"][0]["id"] == "doc1"
    assert result["documents"][0]["content"] == "Document 1 content"
    assert result["documents"][0]["metadata"]["source"] == "kb1"
    assert result["documents"][0]["distance"] == 0.1

def test_add_document_success(rag_tool):
    # Arrange
    parameters = {
        "action": "add_document",
        "content": "This is a test document",
        "metadata": {"source": "test"},
        "document_id": "test-doc"
    }
    
    # Mock embedding model
    rag_tool.embedding_model.embed_document.return_value = [0.1, 0.2, 0.3]
    
    # Act
    result = rag_tool.execute(parameters)
    
    # Assert
    assert result["success"] is True
    rag_tool.chroma_client.add.assert_called_once()

def test_unknown_action(rag_tool):
    # Arrange
    parameters = {
        "action": "unknown",
        "query": "test query"
    }
    
    # Act
    result = rag_tool.execute(parameters)
    
    # Assert
    assert "error" in result
    assert "Unknown action" in result["error"]
