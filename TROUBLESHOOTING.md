# 🔧 Comprehensive Troubleshooting Guide

Solutions for common issues during setup and usage.

## Installation Issues

### Python Installation

**Error:** "python: command not found" or "Python not recognized"

**Solutions:**
1. Download from https://python.org
2. Reinstall with "Add Python to PATH" checked
3. Restart terminal after installation
4. Use `python3` instead of `python`

**Verify:**
\`\`\`bash
python --version
python3 --version
\`\`\`

### Virtual Environment

**Error:** "No module named venv"

**Solution:**
\`\`\`bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# macOS
brew install python3

# Windows - Reinstall Python
\`\`\`

**Error:** "venv not activated"

**Solution:**
\`\`\`bash
# Linux/macOS
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1
\`\`\`

Verify activation - `(venv)` should show in prompt.

### Dependency Installation

**Error:** "pip: command not found"

**Solution:**
\`\`\`bash
# Use Python to run pip
python -m pip install -r requirements.txt

# Or upgrade pip
python -m pip install --upgrade pip
\`\`\`

**Error:** "Failed to build wheel for X"

**Solution:**
\`\`\`bash
# Install with no cache
pip install -r requirements.txt --no-cache-dir

# Or install specific problematic packages
pip install package_name --no-binary :all:
\`\`\`

**Error:** "Permission denied" during pip install

**Solution:**
\`\`\`bash
# Use --user flag
pip install -r requirements.txt --user

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
\`\`\`

## Configuration Issues

### .env File

**Error:** ".env file not found"

**Solution:**
\`\`\`bash
cp .env.example .env
\`\`\`

**Error:** "GEMINI_API_KEY not recognized"

**Solutions:**
1. Verify .env file exists in project root
2. Check no spaces around `=`: `GEMINI_API_KEY=key` ✅ NOT `GEMINI_API_KEY = key`
3. No quotes needed: `GEMINI_API_KEY=AIza...` NOT `GEMINI_API_KEY="AIza..."`
4. Restart app after editing .env
5. Ensure key format is correct (starts with `AIza`)

**Test key:**
\`\`\`bash
python3 -c "import os; os.environ['GEMINI_API_KEY']='your_key'; import google.generativeai as genai; genai.configure(api_key='your_key'); print('✅ Valid')"
\`\`\`

### Getting Gemini API Key

**Error:** "Invalid API key"

**Solution:**
1. Go to https://aistudio.google.com/app/apikeys
2. Sign in with Google account
3. Click "Create API key"
4. Copy the full key (usually starts with `AIza`)
5. Add to .env with no modifications
6. Restart app

## Database Issues

### SQLite (Default)

**Error:** "database is locked"

**Solution:**
\`\`\`bash
# Delete old database file
rm sasds.db

# Or
del sasds.db  # Windows

# Restart app - database will be recreated
\`\`\`

**Error:** "no such table" or similar

**Solution:**
\`\`\`bash
# Reinitialize database
python3 -c "from database_models import Base, engine; Base.metadata.create_all(bind=engine)"
\`\`\`

### PostgreSQL Connection

**Error:** "could not connect to server"

**Solutions:**

1. **Verify connection string format:**
   \`\`\`
   ✅ postgresql://user:password@host:5432/database
   ❌ postgres://user:password@host:5432/database
   ❌ postgresql://user@host  (missing password)
   \`\`\`

2. **Test connection:**
   \`\`\`bash
   python3 -c "from database_models import SessionLocal; db = SessionLocal(); print('✅ Connected')"
   \`\`\`

3. **For Neon.tech:**
   - Connection string in Neon dashboard
   - Add `?sslmode=require` at end
   - Example: `postgresql://user:pass@ep-xxxxx.neon.tech/db?sslmode=require`

4. **For local PostgreSQL:**
   \`\`\`bash
   # Check if service is running
   # Linux
   sudo systemctl status postgresql
   
   # macOS
   brew services list
   
   # Windows - Check Services app
   \`\`\`

**Error:** "FATAL: role 'postgres' does not exist"

**Solution:**
\`\`\`bash
# Check actual database user
psql -U postgres -c "\du"

# Use correct user in .env
DATABASE_URL=postgresql://correct_user:password@localhost:5432/sasds_db
\`\`\`

## Runtime Issues

### Streamlit App

**Error:** "Port 8501 already in use"

**Solution:**
\`\`\`bash
# Option 1: Use different port
streamlit run app.py --server.port 8502

# Option 2: Kill process using 8501
# Linux/macOS
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
\`\`\`

**Error:** "ModuleNotFoundError: No module named 'X'"

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall requirements:
   \`\`\`bash
   pip install -r requirements.txt --force-reinstall
   \`\`\`

**Error:** "Connection refused" or "Address already in use"

**Solution:**
\`\`\`bash
# Wait 30 seconds
# Stop other Streamlit instances
# Use different port
streamlit run app.py --server.port 9000
\`\`\`

### Chat History

**Error:** "Chat history not saving"

**Solutions:**
1. Check database is initialized:
   \`\`\`bash
   python3 -c "from database_models import SessionLocal; SessionLocal()"
   \`\`\`

2. Verify DATABASE_URL is set correctly

3. For SQLite, check `sasds.db` file exists and is writable

4. Check file permissions:
   \`\`\`bash
   ls -la sasds.db  # Check readable/writable
   chmod 666 sasds.db  # If needed
   \`\`\`

### File Upload

**Error:** "uploads directory permission denied"

**Solution:**
\`\`\`bash
# Create uploads directory
mkdir uploads

# Set permissions
chmod 755 uploads

# Or Python will auto-create it
\`\`\`

**Error:** "File too large"

**Solution:**
- Default limit is usually 200MB
- Edit upload limits in Streamlit config if needed

## API Issues

### Gemini API

**Error:** "Error 429: Too many requests"

**Solution:**
- Free tier has rate limits
- Wait a few minutes
- Consider paid tier for production

**Error:** "API key not valid"

**Solutions:**
1. Verify key format (starts with `AIza`)
2. Check key is in .env correctly
3. Get new key from https://aistudio.google.com/app/apikeys
4. Ensure key hasn't been revoked

**Error:** "Invalid request format"

**Solution:**
- Check requirement text isn't too long
- Ensure text is valid UTF-8
- Try shorter test input

## Performance Issues

### Slow Code Generation

**Solutions:**
1. Clear chat history to reduce context
2. Use shorter requirements
3. Check internet connection
4. Try again - API may be busy

### Slow File Upload

**Solutions:**
1. Check file size (recommend < 5MB)
2. Verify upload_dir has space
3. Check internet speed
4. Try smaller file first

### Slow Database

**Solutions:**
\`\`\`bash
# For SQLite, if database grows large:
# 1. Archive old projects
# 2. Back up database
# 3. Delete old entries

# For PostgreSQL, create index:
# CREATE INDEX idx_chat_session ON chat_messages(session_id);
\`\`\`

## Windows-Specific Issues

**Error:** "Script disabled on system" (PowerShell)

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
