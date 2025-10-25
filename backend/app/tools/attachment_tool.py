# backend/app/tools/attachment_tool.py
from typing import Dict, Any, List, Optional
import os
import uuid
from markitdown import markitdown
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Attachment
from ..core.logging import logger
from ..core.config import settings

class AttachmentTool:
    """Tool for processing user attachments"""
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the attachment tool based on parameters"""
        action = parameters.get("action")
        
        if action == "process_attachment":
            return self._process_attachment(parameters)
        elif action == "get_attachment_text":
            return self._get_attachment_text(parameters)
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _process_attachment(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process an uploaded attachment"""
        session_id = parameters.get("session_id")
        file_path = parameters.get("file_path")
        filename = parameters.get("filename")
        content_type = parameters.get("content_type")
        
        if not all([session_id, file_path, filename, content_type]):
            return {"error": "Missing required parameters"}
        
        try:
            # Generate unique ID for the attachment
            attachment_id = str(uuid.uuid4())
            
            # Process the attachment with markitdown
            processed_text = markitdown.convert(file_path)
            
            # Store attachment info in database
            db = next(get_db())
            attachment = Attachment(
                id=attachment_id,
                session_id=session_id,
                filename=filename,
                content_type=content_type,
                file_path=file_path,
                processed_text=processed_text
            )
            db.add(attachment)
            db.commit()
            
            logger.info(
                f"Processed attachment {filename} for session {session_id}",
                extra={
                    "session_id": session_id,
                    "tool_name": "attachment_tool",
                    "attachment_id": attachment_id,
                    "filename": filename
                }
            )
            
            return {
                "success": True,
                "attachment_id": attachment_id,
                "processed_text": processed_text
            }
        except Exception as e:
            logger.error(
                f"Failed to process attachment {filename} for session {session_id}: {str(e)}",
                extra={
                    "session_id": session_id,
                    "tool_name": "attachment_tool",
                    "filename": filename
                }
            )
            return {"error": f"Failed to process attachment: {str(e)}"}
        finally:
            db.close()
    
    def _get_attachment_text(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get processed text for an attachment"""
        attachment_id = parameters.get("attachment_id")
        
        if not attachment_id:
            return {"error": "Attachment ID is required"}
        
        try:
            db = next(get_db())
            attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
            
            if not attachment:
                return {"error": "Attachment not found"}
            
            return {
                "attachment_id": attachment_id,
                "filename": attachment.filename,
                "processed_text": attachment.processed_text
            }
        except Exception as e:
            logger.error(
                f"Failed to get attachment text for {attachment_id}: {str(e)}",
                extra={"tool_name": "attachment_tool", "attachment_id": attachment_id}
            )
            return {"error": f"Failed to get attachment text: {str(e)}"}
        finally:
            db.close()
    
    # Convenience method for the ChatAgent class
    def process_attachment(self, session_id: str, attachment: Dict[str, Any]) -> Dict[str, Any]:
        """Process an attachment from the ChatAgent"""
        return self._process_attachment({
            "session_id": session_id,
            "file_path": attachment.get("file_path"),
            "filename": attachment.get("filename"),
            "content_type": attachment.get("content_type")
        })
