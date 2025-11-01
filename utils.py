"""
Utility functions for SASDS
"""

import os
from pathlib import Path
from typing import Optional
import json

def read_file_content(file_path: str) -> Optional[str]:
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_file(file_path: str, content: str) -> bool:
    """Save content to a file"""
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def extract_json(text: str) -> Optional[dict]:
    """Extract JSON from text"""
    try:
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = text[start_idx:end_idx]
            return json.loads(json_str)
    except:
        pass
    return None

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def sanitize_code(code: str) -> str:
    """Sanitize generated code"""
    # Remove markdown code blocks if present
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1])
    
    # Remove common prefixes
    for prefix in ["python", "py", "Python"]:
        if code.startswith(prefix):
            code = code[len(prefix):].lstrip()
    
    return code.strip()

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"
