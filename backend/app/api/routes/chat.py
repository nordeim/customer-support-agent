# backend/app/api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
import json

from ...db.database import get_db
from ...agents.chat_agent import ChatAgent
from ...core.logging import logger
from ...core.config import settings
from ...db.models import Session as DBSession
from ..dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize the chat agent
chat_agent = ChatAgent()

@router.post("/sessions")
async def create_session(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Create session in database
        db_session = DBSession(id=session_id, user_id=user_id)
        db.add(db_session)
        db.commit()
        
        # Create thread in Agent Framework
        thread_id = chat_agent.create_thread(session_id, user_id)
        
        logger.info(
            f"Created new chat session {session_id}",
            extra={"session_id": session_id, "user_id": user_id}
        )
        
        return {
            "session_id": session_id,
            "thread_id": thread_id,
            "message": "Session created successfully"
        }
    except Exception as e:
        logger.error(
            f"Failed to create session: {str(e)}",
            extra={"user_id": user_id}
        )
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: str,
    message: str = Form(...),
    attachments: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    """Send a message to the chat agent"""
    try:
        # Check if session exists
        db_session = db.query(DBSession).filter(DBSession.id == session_id).first()
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Process attachments if any
        processed_attachments = []
        for attachment in attachments:
            # Generate unique filename
            file_extension = os.path.splitext(attachment.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.upload_dir, unique_filename)
            
            # Save file
            os.makedirs(settings.upload_dir, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await attachment.read())
            
            # Add to processed attachments
            processed_attachments.append({
                "filename": attachment.filename,
                "file_path": file_path,
                "content_type": attachment.content_type
            })
        
        # Send message to agent
        response = chat_agent.send_message(
            session_id=session_id,
            message=message,
            attachments=processed_attachments
        )
        
        logger.info(
            f"Processed message for session {session_id}",
            extra={"session_id": session_id, "message_length": len(message)}
        )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to process message for session {session_id}: {str(e)}",
            extra={"session_id": session_id}
        )
        raise HTTPException(status_code=500, detail="Failed to process message")

@router.get("/sessions/{session_id}/history")
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    try:
        # Check if session exists
        db_session = db.query(DBSession).filter(DBSession.id == session_id).first()
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get messages from database
        from ...db.models import Message
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
        
        # Format messages
        history = [
            {
                "id": msg.id,
                "content": msg.content,
                "role": msg.role,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
        
        return {"session_id": session_id, "messages": history}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to get chat history for session {session_id}: {str(e)}",
            extra={"session_id": session_id}
        )
        raise HTTPException(status_code=500, detail="Failed to get chat history")
