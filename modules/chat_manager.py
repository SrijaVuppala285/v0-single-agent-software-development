from datetime import datetime
from typing import List, Dict
from database_models import SessionLocal, ChatSession, ChatMessage

class ChatManager:
    """Manages chat sessions and message history"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def create_session(self, title: str = "New Chat") -> int:
        """Create a new chat session"""
        session = ChatSession(title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session.id
    
    def add_message(self, session_id: int, role: str, content: str):
        """Add a message to a chat session"""
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
        return message.id
    
    def get_session_messages(self, session_id: int) -> List[Dict]:
        """Get all messages in a session"""
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            return []
        
        messages = []
        for msg in session.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            })
        return messages
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all chat sessions (for sidebar)"""
        sessions = self.db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
        
        result = []
        for session in sessions:
            result.append({
                "id": session.id,
                "title": session.title,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
                "message_count": len(session.messages)
            })
        return result
    
    def update_session_title(self, session_id: int, title: str):
        """Update session title"""
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.title = title
            self.db.commit()
    
    def delete_session(self, session_id: int):
        """Delete a chat session"""
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            self.db.delete(session)
            self.db.commit()
    
    def __del__(self):
        self.db.close()
