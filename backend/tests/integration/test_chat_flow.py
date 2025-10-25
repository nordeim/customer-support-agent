# backend/tests/integration/test_chat_flow.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)

def test_create_session():
    # Act
    response = client.post("/chat/sessions", json={"user_id": "test-user"})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "thread_id" in data
    assert data["message"] == "Session created successfully"

def test_send_message():
    # First create a session
    session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
    session_id = session_response.json()["session_id"]
    
    # Mock the chat agent
    with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
        mock_send.return_value = {
            "message": "This is a test response",
            "sources": [],
            "requires_escalation": False
        }
        
        # Act
        response = client.post(
            f"/chat/sessions/{session_id}/messages",
            data={"message": "Hello, I need help"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "This is a test response"
        assert data["sources"] == []
        assert data["requires_escalation"] is False

def test_get_chat_history():
    # First create a session
    session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
    session_id = session_response.json()["session_id"]
    
    # Act
    response = client.get(f"/chat/sessions/{session_id}/history")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "messages" in data

def test_session_not_found():
    # Act
    response = client.get("/chat/sessions/non-existent-session/history")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
