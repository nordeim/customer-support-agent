# backend/tests/unit/test_memory_tool.py
import pytest
from unittest.mock import Mock, patch
from app.tools.memory_tool import MemoryTool

@pytest.fixture
def memory_tool():
    return MemoryTool()

@pytest.fixture
def mock_db():
    with patch('app.tools.memory_tool.get_db') as mock_get_db:
        mock_session = Mock()
        mock_get_db.return_value.__next__.return_value = mock_session
        yield mock_session

def test_store_memory_success(memory_tool, mock_db):
    # Arrange
    parameters = {
        "action": "store",
        "session_id": "test-session",
        "key": "user_preference",
        "value": "dark_mode"
    }
    
    # Act
    result = memory_tool.execute(parameters)
    
    # Assert
    assert result["success"] is True
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_retrieve_memory_success(memory_tool, mock_db):
    # Arrange
    from app.db.models import MemoryEntry
    parameters = {
        "action": "retrieve",
        "session_id": "test-session",
        "key": "user_preference"
    }
    
    # Mock database query
    mock_entry = Mock(spec=MemoryEntry)
    mock_entry.key = "user_preference"
    mock_entry.value = "dark_mode"
    mock_entry.timestamp = Mock()
    mock_entry.timestamp.isoformat.return_value = "2023-01-01T00:00:00"
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_entry]
    
    # Act
    result = memory_tool.execute(parameters)
    
    # Assert
    assert "entries" in result
    assert len(result["entries"]) == 1
    assert result["entries"][0]["key"] == "user_preference"
    assert result["entries"][0]["value"] == "dark_mode"

def test_unknown_action(memory_tool):
    # Arrange
    parameters = {
        "action": "unknown",
        "session_id": "test-session"
    }
    
    # Act
    result = memory_tool.execute(parameters)
    
    # Assert
    assert "error" in result
    assert "Unknown action" in result["error"]
