import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from database_models import SessionLocal, UploadedFile, Project

class FileManager:
    """Manages file uploads and storage"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.db = SessionLocal()
    
    def save_uploaded_file(self, project_id: int, file_content: bytes, filename: str) -> str:
        """Save uploaded file and return path"""
        
        # Create project-specific directory
        project_dir = self.upload_dir / f"project_{project_id}"
        project_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = project_dir / filename
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Record in database
        file_type = filename.split('.')[-1] if '.' in filename else 'unknown'
        uploaded_file = UploadedFile(
            project_id=project_id,
            filename=filename,
            file_path=str(file_path),
            file_type=file_type
        )
        self.db.add(uploaded_file)
        self.db.commit()
        
        return str(file_path)
    
    def get_project_files(self, project_id: int) -> list:
        """Get all files for a project"""
        files = self.db.query(UploadedFile).filter(
            UploadedFile.project_id == project_id
        ).all()
        
        result = []
        for file in files:
            result.append({
                "filename": file.filename,
                "file_type": file.file_type,
                "created_at": file.created_at.isoformat(),
                "file_path": file.file_path
            })
        return result
    
    def delete_project_files(self, project_id: int):
        """Delete all files for a project"""
        project_dir = self.upload_dir / f"project_{project_id}"
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        # Remove from database
        files = self.db.query(UploadedFile).filter(
            UploadedFile.project_id == project_id
        ).all()
        for file in files:
            self.db.delete(file)
        self.db.commit()
    
    def __del__(self):
        self.db.close()
