# backend/tests/unit/test_escalation_tool.py
import pytest
from app.tools.escalation_tool import EscalationTool

@pytest.fixture
def escalation_tool():
    return EscalationTool()

def test_escalation_success(escalation_tool):
    # Arrange
    parameters = {
        "session_id": "test-session",
        "reason": "Complex technical issue",
        "user_id": "test-user",
        "conversation_summary": "User is experiencing issues with..."
    }
    
    # Act
    result = escalation_tool.execute(parameters)
    
    # Assert
    assert result["success"] is True
    assert "ticket_id" in result
    assert "message" in result
    assert "estimated_wait_time" in result

def test_escalation_missing_parameters(escalation_tool):
    # Arrange
    parameters = {
        "session_id": "test-session"
        # Missing reason parameter
    }
    
    # Act
    result = escalation_tool.execute(parameters)
    
    # Assert
    assert "error" in result
    assert "Session ID and reason are required" in result["error"]
