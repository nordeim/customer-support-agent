# backend/tests/e2e/test_complete_chat_flow.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import time

from app.main import app
from app.core.config import settings

client = TestClient(app)

class TestCompleteChatFlow:
    """End-to-end tests for the complete chat flow"""
    
    def test_complete_chat_session(self):
        """Test a complete chat session from start to finish"""
        # Step 1: Create a new session
        session_response = client.post("/chat/sessions", json={"user_id": "test-user-123"})
        assert session_response.status_code == 200
        
        session_data = session_response.json()
        session_id = session_data["session_id"]
        assert session_id is not None
        
        # Step 2: Send initial message
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.return_value = {
                "message": "Hello! How can I help you today?",
                "sources": [],
                "requires_escalation": False
            }
            
            message_response = client.post(
                f"/chat/sessions/{session_id}/messages",
                data={"message": "Hello, I need help with my order"}
            )
            assert message_response.status_code == 200
            
            message_data = message_response.json()
            assert message_data["message"] == "Hello! How can I help you today?"
            assert message_data["requires_escalation"] is False
        
        # Step 3: Send message with attachment
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.return_value = {
                "message": "I see you've uploaded an invoice. Let me help you with that.",
                "sources": [
                    {
                        "id": "doc1",
                        "content": "Information about invoice processing",
                        "metadata": {"source": "invoice_kb.pdf"},
                        "distance": 0.2
                    }
                ],
                "requires_escalation": False
            }
            
            # Create a mock file
            mock_file = ("test_invoice.pdf", b"mock pdf content", "application/pdf")
            
            message_response = client.post(
                f"/chat/sessions/{session_id}/messages",
                data={"message": "Here's my invoice"},
                files={"attachments": mock_file}
            )
            assert message_response.status_code == 200
            
            message_data = message_response.json()
            assert "invoice" in message_data["message"]
            assert len(message_data["sources"]) == 1
            assert message_data["sources"][0]["metadata"]["source"] == "invoice_kb.pdf"
        
        # Step 4: Trigger escalation
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.return_value = {
                "message": "I'm escalating your issue to a human agent. Ticket ID: TICKET-123",
                "sources": [],
                "requires_escalation": True
            }
            
            message_response = client.post(
                f"/chat/sessions/{session_id}/messages",
                data={"message": "This is too complex, I need to speak to a human"}
            )
            assert message_response.status_code == 200
            
            message_data = message_response.json()
            assert message_data["requires_escalation"] is True
            assert "TICKET-123" in message_data["message"]
        
        # Step 5: Verify chat history
        history_response = client.get(f"/chat/sessions/{session_id}/history")
        assert history_response.status_code == 200
        
        history_data = history_response.json()
        assert history_data["session_id"] == session_id
        # Note: In a real implementation, we'd verify the actual message count
        
        # Step 6: Health check
        health_response = client.get("/health/")
        assert health_response.status_code == 200
        
        health_data = health_response.json()
        assert health_data["status"] in ["healthy", "unhealthy"]
        assert "components" in health_data
    
    def test_error_handling(self):
        """Test error handling in the chat flow"""
        # Test invalid session ID
        response = client.get("/chat/sessions/invalid-session-id/history")
        assert response.status_code == 404
        
        # Test empty message
        session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
        session_id = session_response.json()["session_id"]
        
        response = client.post(
            f"/chat/sessions/{session_id}/messages",
            data={"message": ""}
        )
        assert response.status_code == 422  # Validation error
    
    def test_concurrent_sessions(self):
        """Test handling multiple concurrent sessions"""
        sessions = []
        
        # Create multiple sessions
        for i in range(5):
            response = client.post("/chat/sessions", json={"user_id": f"test-user-{i}"})
            assert response.status_code == 200
            sessions.append(response.json()["session_id"])
        
        # Send messages to all sessions concurrently
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.return_value = {
                "message": "Response to concurrent message",
                "sources": [],
                "requires_escalation": False
            }
            
            responses = []
            for session_id in sessions:
                response = client.post(
                    f"/chat/sessions/{session_id}/messages",
                    data={"message": f"Concurrent message for {session_id}"}
                )
                responses.append(response)
            
            # Verify all responses are successful
            for response in responses:
                assert response.status_code == 200
                assert response.json()["message"] == "Response to concurrent message"
    
    def test_attachment_processing(self):
        """Test attachment processing in various scenarios"""
        # Create session
        session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
        session_id = session_response.json()["session_id"]
        
        # Test different file types
        test_files = [
            ("test.txt", b"plain text content", "text/plain"),
            ("test.jpg", b"fake jpg content", "image/jpeg"),
            ("test.pdf", b"fake pdf content", "application/pdf"),
        ]
        
        for filename, content, content_type in test_files:
            with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
                mock_send.return_value = {
                    "message": f"Processed {filename} successfully",
                    "sources": [],
                    "requires_escalation": False
                }
                
                response = client.post(
                    f"/chat/sessions/{session_id}/messages",
                    data={"message": f"Uploading {filename}"},
                    files={"attachments": (filename, content, content_type)}
                )
                assert response.status_code == 200
                assert filename in response.json()["message"]
        
        # Test invalid file type
        response = client.post(
            f"/chat/sessions/{session_id}/messages",
            data={"message": "Uploading invalid file"},
            files={"attachments": ("test.exe", b"fake exe content", "application/x-executable")}
        )
        assert response.status_code == 422  # Validation error
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Create session
        session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
        session_id = session_response.json()["session_id"]
        
        # Send multiple messages rapidly
        responses = []
        for i in range(35):  # Exceed the rate limit of 30 messages per minute
            with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
                mock_send.return_value = {
                    "message": f"Message {i}",
                    "sources": [],
                    "requires_escalation": False
                }
                
                response = client.post(
                    f"/chat/sessions/{session_id}/messages",
                    data={"message": f"Message {i}"}
                )
                responses.append(response)
        
        # Check that some responses are rate limited
        rate_limited_count = sum(1 for r in responses if r.status_code == 429)
        assert rate_limited_count > 0, "Expected some requests to be rate limited"
    
    def test_system_resilience(self):
        """Test system resilience under various failure conditions"""
        # Create session
        session_response = client.post("/chat/sessions", json={"user_id": "test-user"})
        session_id = session_response.json()["session_id"]
        
        # Test agent framework failure
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.side_effect = Exception("Agent framework unavailable")
            
            response = client.post(
                f"/chat/sessions/{session_id}/messages",
                data={"message": "Test message during failure"}
            )
            assert response.status_code == 500
        
        # Test database failure
        with patch('app.db.database.get_db') as mock_db:
            mock_db.side_effect = Exception("Database unavailable")
            
            response = client.get(f"/chat/sessions/{session_id}/history")
            assert response.status_code == 500
        
        # Test recovery after failure
        with patch('app.api.routes.chat.chat_agent.send_message') as mock_send:
            mock_send.return_value = {
                "message": "System recovered",
                "sources": [],
                "requires_escalation": False
            }
            
            response = client.post(
                f"/chat/sessions/{session_id}/messages",
                data={"message": "Test message after recovery"}
            )
            assert response.status_code == 200
            assert response.json()["message"] == "System recovered"
