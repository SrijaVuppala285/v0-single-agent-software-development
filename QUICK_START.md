# ⚡ Quick Start (5 minutes)

For experienced developers who want to get started fast.

## TL;DR

\`\`\`bash
# Clone
git clone https://github.com/yourusername/sasds.git
cd sasds

# Setup
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install & Config
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY from https://aistudio.google.com/app/apikeys

# Run
python -m streamlit run app.py
\`\`\`

**App at:** http://localhost:8501

## What's Included

| Feature | Status |
|---------|--------|
| Chat History | ✅ PostgreSQL/SQLite |
| AI Analysis | ✅ Gemini API |
| Code Generation | ✅ LLM-powered |
| Testing | ✅ Pytest automated |
| File Upload | ✅ Document support |
| Code Review | ✅ Auto-refinement |

## Environment Setup

### Get API Key (Required)

1. Visit: https://aistudio.google.com/app/apikeys
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=...`

### Database (Optional)

- **Default:** SQLite (no setup)
- **Cloud:** Neon.tech (free tier)
- **Local:** PostgreSQL

## Usage

1. Click "➕ New Chat"
2. Describe requirement
3. Click "🔍 Analyze"
4. Click "⚙ Generate Code"
5. Click "🧪 Run Tests"
6. Click "🔁 Review"
7. Download results

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `python: command not found` | Install Python 3.10+ |
| `ModuleNotFoundError` | Activate venv, reinstall deps |
| `GEMINI_API_KEY not recognized` | Add key to .env, restart app |
| `Port 8501 in use` | `streamlit run app.py --server.port 8502` |

## Documentation

- **Full Guide:** README.md
- **Detailed Setup:** SETUP.md
- **Windows Users:** WINDOWS_SETUP.md
- **GitHub Setup:** GITHUB_SETUP.md

---

**Ready? Let's build! 🚀**
