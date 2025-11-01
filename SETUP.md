# 🔧 Detailed Setup Guide for SASDS

Complete step-by-step instructions for setting up SASDS from GitHub.

## Quick Start (5 minutes)

\`\`\`bash
# 1. Clone repository
git clone https://github.com/yourusername/sasds.git
cd sasds

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 5. Run application
chmod +x run.sh
./run.sh
\`\`\`

## Detailed Setup Steps

### 1. System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.10 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 500MB for code and database
- **Internet**: Required for API calls

### 2. Install Python

**Ubuntu/Debian:**
\`\`\`bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
\`\`\`

**macOS:**
\`\`\`bash
brew install python3
\`\`\`

**Windows:**
- Download from https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation

### 3. Clone Repository

\`\`\`bash
# Using HTTPS (no SSH key needed)
git clone https://github.com/yourusername/sasds.git
cd sasds

# Using SSH (if you have SSH key configured)
git clone git@github.com:yourusername/sasds.git
cd sasds
\`\`\`

### 4. Create Virtual Environment

**Linux/macOS:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

**Windows (Command Prompt):**
\`\`\`cmd
python -m venv venv
venv\Scripts\activate
\`\`\`

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
