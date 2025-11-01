import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class ProjectStorage:
    """Manages project storage and retrieval"""
    
    def __init__(self, db_path: str = "projects.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    requirement TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    version INTEGER DEFAULT 1
                )
            ''')
            
            # Code versions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS code_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    code TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id)
                )
            ''')
            
            # Test results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    passed INTEGER,
                    failed INTEGER,
                    log TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id)
                )
            ''')
            
            # Review reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    report TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id)
                )
            ''')
            
            conn.commit()
    
    def save_project(self, title: str, requirement: str, code: str) -> int:
        """Save a new project"""
        
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO projects (title, requirement, created_at, updated_at, version)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, requirement, now, now, 1))
            
            project_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO code_versions (project_id, code, version, created_at)
                VALUES (?, ?, ?, ?)
            ''', (project_id, code, 1, now))
            
            conn.commit()
            return project_id
    
    def get_recent_projects(self, limit: int = 10) -> List[Dict]:
        """Get recent projects"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, requirement, created_at, version
                FROM projects
                ORDER BY updated_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                projects.append({
                    "id": row[0],
                    "title": row[1],
                    "requirement": row[2][:100],
                    "created_at": row[3],
                    "version": row[4]
                })
            
            return projects
    
    def save_code_version(self, project_id: int, code: str, version: int):
        """Save a code version"""
        
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO code_versions (project_id, code, version, created_at)
                VALUES (?, ?, ?, ?)
            ''', (project_id, code, version, now))
            
            # Update project version
            cursor.execute('''
                UPDATE projects SET version = ?, updated_at = ?
                WHERE id = ?
            ''', (version, now, project_id))
            
            conn.commit()
    
    def save_test_results(self, project_id: int, passed: int, failed: int, log: str):
        """Save test results"""
        
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO test_results (project_id, passed, failed, log, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (project_id, passed, failed, log, now))
            
            conn.commit()
    
    def save_review_report(self, project_id: int, report: str):
        """Save review report"""
        
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO review_reports (project_id, report, created_at)
                VALUES (?, ?, ?)
            ''', (project_id, report, now))
            
            conn.commit()
