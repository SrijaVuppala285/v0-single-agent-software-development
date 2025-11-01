"""
Configuration module for SASDS
Handles environment variables and settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directories
ROOT_DIR = Path(__file__).parent
MODULES_DIR = ROOT_DIR / "modules"

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", str(ROOT_DIR / "projects.db"))

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "SASDS - AI Software Development",
    "page_icon": "🚀",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Application Configuration
APP_CONFIG = {
    "max_file_size_mb": 10,
    "supported_formats": ["txt", "pdf", "docx", "csv", "json", "py"],
    "timeout_seconds": 30,
    "max_code_length": 10000
}

# Default Prompts
REQUIREMENT_PROMPT = """
Analyze the following software requirement and break it down into:
1. Functional Tasks (what needs to be done)
2. Required Python Libraries
3. Input/Output specifications
4. Any constraints or considerations

Respond in JSON format with keys: tasks, libraries, input_output, constraints
"""

CODE_GENERATION_PROMPT = """
Generate production-ready Python code with:
1. Clean, modular, well-commented code
2. Error handling and input validation
3. Functions to organize code
4. Docstrings for all functions
5. Testable structure
6. A main() function

Generate only the Python code, no explanations.
"""

REVIEW_PROMPT = """
Review this Python code and provide:
1. Code quality assessment
2. Performance improvements
3. Bug fixes if needed
4. Best practices recommendations
5. Security considerations

Then generate an improved version of the code.
"""
