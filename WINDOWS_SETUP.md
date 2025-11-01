# 🪟 Windows-Specific Setup Guide

Complete guide for setting up SASDS on Windows.

## Prerequisites

### 1. Install Python 3.10+

1. Go to https://www.python.org/downloads/windows/
2. Download "Windows installer (64-bit)" or (32-bit)
3. Run the installer
4. ⚠️ **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

**Verify installation:**
\`\`\`cmd
python --version
\`\`\`

Should show: `Python 3.10.x` or higher

### 2. Install Git

1. Go to https://git-scm.com/download/win
2. Download "64-bit Git for Windows Setup"
3. Run the installer
4. Click "Next" through options
5. Click "Install"

**Verify installation:**
\`\`\`cmd
git --version
\`\`\`

## Clone Repository

### Using Git Bash

1. **Open Git Bash**
   - Right-click on desktop → Git Bash Here
   - Or search "Git Bash" in Start Menu

2. **Clone repository:**
   \`\`\`bash
   git clone https://github.com/yourusername/sasds.git
   cd sasds
   \`\`\`

### Using Command Prompt

1. **Open Command Prompt** (Win + R, type `cmd`, press Enter)

2. **Navigate to your projects folder:**
   \`\`\`cmd
   cd C:\Users\YourUsername\Documents
   \`\`\`

3. **Clone repository:**
   \`\`\`cmd
   git clone https://github.com/yourusername/sasds.git
   cd sasds
   \`\`\`

## Setup Virtual Environment

### Using Command Prompt (Recommended)

\`\`\`cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) at the start of each line now
\`\`\`

### Using PowerShell

```powershell
# Create virtual environment
python -m venv venv

# Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate it
venv\Scripts\Activate.ps1

# You should see (venv) at the start of each line now
