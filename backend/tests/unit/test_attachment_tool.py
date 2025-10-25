# backend/tests/unit/test_attachment_tool.py
import pytest
from unittest.mock import Mock, patch, mock_open
from app.tools.attachment_tool import AttachmentTool

@pytest.fixture
def attachment_tool():
    return AttachmentTool()

@pytest.fixture
def mock_db():
    with patch('app.tools.attachment_tool.get_db') as mock_get_db:
        mock_session = Mock()
        mock_get_db.return_value.__next__.return_value = mock_session
        yield mock_session

def test_process_attachment_success(attachment_tool, mock_db):
    # Arrange
    parameters = {
        "action": "process_attachment",
        "session_id": "test-session",
        "file_path": "/tmp/test.pdf",
        "filename": "test.pdf",
        "content_type": "application/pdf"
    }
    
    # Mock markitdown
    with patch('app.tools.attachment_tool.markitdown') as mock_markitdown:
        mock_markitdown.convert.return_value = "Extracted text from PDF"
        
        # Act
        result = attachment_tool.execute(parameters)
        
        # Assert
        assert result["success"] is True
        assert "attachment_id" in result
        assert result["processed_text"] == "Extracted text from PDF"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

def test_get_attachment_text_success(attachment_tool, mock_db):
    # Arrange
    from app.db.models import Attachment
    parameters = {
        "action": "get_attachment_text",
        "attachment_id": "test-attachment-id"
    }
    
    # Mock database query
    mock_attachment = Mock(spec=Attachment)
    mock_attachment.id = "test-attachment-id"
    mock_attachment.filename = "test.pdf"
    mock_attachment.processed_text = "Extracted text from PDF"
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_attachment
    
    # Act
    result = attachment_tool.execute(parameters)
    
    # Assert
    assert result["attachment_id"] == "test-attachment-id"
    assert result["filename"] == "test.pdf"
    assert result["processed_text"] == "Extracted text from PDF"

def test_unknown_action(attachment_tool):
    # Arrange
    parameters = {
        "action": "unknown",
        "attachment_id": "test-attachment-id"
    }
    
    # Act
    result = attachment_tool.execute(parameters)
    
    # Assert
    assert "error" in result
    assert "Unknown action" in result["error"]
