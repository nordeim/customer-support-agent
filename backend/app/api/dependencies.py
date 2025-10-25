# backend/app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import re

from .core.security import verify_token, sanitize_input
from .core.config import settings
from .db.database import get_db

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get the current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    # Extract user information
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    return {
        "user_id": user_id,
        "exp": payload.get("exp"),
        "iat": payload.get("iat")
    }

async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Get the current user from JWT token (optional)"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        return {
            "user_id": user_id,
            "exp": payload.get("exp"),
            "iat": payload.get("iat")
        }
    except Exception:
        return None

def validate_message_content(message: str) -> str:
    """Validate and sanitize message content"""
    if not message or not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty"
        )
    
    # Sanitize input
    sanitized_message = sanitize_input(message)
    
    if not sanitized_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message content"
        )
    
    # Check length
    if len(sanitized_message) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content too long (max 10000 characters)"
        )
    
    return sanitized_message

def validate_session_id(session_id: str) -> str:
    """Validate session ID format"""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID is required"
        )
    
    # Check if session ID matches UUID format
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )
    
    return session_id

def validate_attachment_file(filename: str, content_type: str, file_size: int) -> dict:
    """Validate attachment file"""
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    # Check file size (max 10MB)
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 10MB)"
        )
    
    # Check file extension
    allowed_extensions = {
        '.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif'
    }
    file_extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not allowed"
        )
    
    # Check content type
    allowed_content_types = {
        'text/plain',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
        'image/gif'
    }
    
    if content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content type {content_type} not allowed"
        )
    
    return {
        "filename": sanitize_input(filename),
        "content_type": content_type,
        "file_size": file_size,
        "file_extension": file_extension
    }
