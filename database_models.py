import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# PostgreSQL connection string (uses environment variable)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./sasds.db"  # Fallback to SQLite if PostgreSQL not available
)

# Create engine
engine = create_engine(
    DATABASE_URL if "postgresql" in DATABASE_URL else "sqlite:///./sasds.db",
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatSession(Base):
    """Represents a chat session (similar to ChatGPT conversations)"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    project = relationship("Project", uselist=False, back_populates="chat_session")

class ChatMessage(Base):
    """Represents individual messages in a chat session"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), index=True)
    role = Column(String(50))  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")

class Project(Base):
    """Represents a software project"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True)
    title = Column(String(255), index=True)
    requirement = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    
    # Relationships
    chat_session = relationship("ChatSession", back_populates="project")
    code_versions = relationship("CodeVersion", back_populates="project", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="project", cascade="all, delete-orphan")
    review_reports = relationship("ReviewReport", back_populates="project", cascade="all, delete-orphan")
    uploaded_files = relationship("UploadedFile", back_populates="project", cascade="all, delete-orphan")

class CodeVersion(Base):
    """Stores different versions of generated code"""
    __tablename__ = "code_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    code = Column(Text)
    version = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="code_versions")

class TestResult(Base):
    """Stores test execution results"""
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    log = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="test_results")

class ReviewReport(Base):
    """Stores code review and refinement reports"""
    __tablename__ = "review_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    report = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="review_reports")

class UploadedFile(Base):
    """Stores information about uploaded requirement files"""
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    filename = Column(String(255))
    file_path = Column(String(500))
    file_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="uploaded_files")

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
