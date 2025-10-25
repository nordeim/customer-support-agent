# backend/app/tools/memory_tool.py
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import MemoryEntry, Session
from ..core.logging import logger

class MemoryTool:
    """Tool for storing and retrieving conversation memory"""
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the memory tool based on parameters"""
        action = parameters.get("action")
        session_id = parameters.get("session_id")
        
        if action == "store":
            return self._store_memory(session_id, parameters)
        elif action == "retrieve":
            return self._retrieve_memory(session_id, parameters)
        elif action == "store_thread_mapping":
            return self._store_thread_mapping(session_id, parameters)
        elif action == "get_thread_id":
            return self._get_thread_id(session_id)
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _store_memory(self, session_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Store a memory entry"""
        key = parameters.get("key")
        value = parameters.get("value")
        
        if not key or not value:
            return {"error": "Both key and value are required"}
        
        try:
            db = next(get_db())
            memory_entry = MemoryEntry(
                session_id=session_id,
                key=key,
                value=value
            )
            db.add(memory_entry)
            db.commit()
            
            logger.info(
                f"Stored memory entry for session {session_id}",
                extra={"session_id": session_id, "tool_name": "memory_tool", "key": key}
            )
            
            return {"success": True, "message": "Memory stored successfully"}
        except Exception as e:
            logger.error(
                f"Failed to store memory for session {session_id}: {str(e)}",
                extra={"session_id": session_id, "tool_name": "memory_tool"}
            )
            return {"error": f"Failed to store memory: {str(e)}"}
        finally:
            db.close()
    
    def _retrieve_memory(self, session_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve memory entries"""
        key = parameters.get("key")
        
        try:
            db = next(get_db())
            query = db.query(MemoryEntry).filter(MemoryEntry.session_id == session_id)
            
            if key:
                query = query.filter(MemoryEntry.key == key)
            
            memory_entries = query.all()
            
            result = {
                "entries": [
                    {"key": entry.key, "value": entry.value, "timestamp": entry.timestamp.isoformat()}
                    for entry in memory_entries
                ]
            }
            
            logger.info(
                f"Retrieved {len(memory_entries)} memory entries for session {session_id}",
                extra={"session_id": session_id, "tool_name": "memory_tool"}
            )
            
            return result
        except Exception as e:
            logger.error(
                f"Failed to retrieve memory for session {session_id}: {str(e)}",
                extra={"session_id": session_id, "tool_name": "memory_tool"}
            )
            return {"error": f"Failed to retrieve memory: {str(e)}"}
        finally:
            db.close()
    
    def _store_thread_mapping(self, session_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Store mapping between session ID and thread ID"""
        thread_id = parameters.get("thread_id")
        user_id = parameters.get("user_id")
        
        if not thread_id:
            return {"error": "Thread ID is required"}
        
        try:
            db = next(get_db())
            
            # Check if session exists
            session_obj = db.query(Session).filter(Session.id == session_id).first()
            
            if not session_obj:
                # Create new session
                session_obj = Session(
                    id=session_id,
                    user_id=user_id
                )
                db.add(session_obj)
            
            # Store thread mapping as a memory entry
            memory_entry = MemoryEntry(
                session_id=session_id,
                key="thread_id",
                value=thread_id
            )
            db.add(memory_entry)
            db.commit()
            
            logger.info(
                f"Stored thread mapping for session {session_id}",
                extra={"session_id": session_id, "tool_name": "memory_tool", "thread_id": thread_id}
            )
            
            return {"success": True, "message": "Thread mapping stored successfully"}
        except Exception as e:
            logger.error(
                f"Failed to store thread mapping for session {session_id}: {str(e)}",
                extra={"session_id": session_id, "tool_name": "memory_tool"}
            )
            return {"error": f"Failed to store thread mapping: {str(e)}"}
        finally:
            db.close()
    
    def _get_thread_id(self, session_id: str) -> Optional[str]:
        """Get thread ID for a session"""
        try:
            db = next(get_db())
            memory_entry = db.query(MemoryEntry).filter(
                MemoryEntry.session_id == session_id,
                MemoryEntry.key == "thread_id"
            ).first()
            
            if memory_entry:
                return memory_entry.value
            return None
        except Exception as e:
            logger.error(
                f"Failed to get thread ID for session {session_id}: {str(e)}",
                extra={"session_id": session_id, "tool_name": "memory_tool"}
            )
            return None
        finally:
            db.close()
    
    # Convenience methods for the ChatAgent class
    def store_thread_mapping(self, session_id: str, thread_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Store mapping between session ID and thread ID"""
        return self._store_thread_mapping(session_id, {"thread_id": thread_id, "user_id": user_id})
    
    def get_thread_id(self, session_id: str) -> Optional[str]:
        """Get thread ID for a session"""
        return self._get_thread_id(session_id)
