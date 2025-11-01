# Single Agent Software Development System (SASDS)

An intelligent, autonomous software development environment powered by AI and Natural Language Understanding. Build, test, and refine software automatically using Google Gemini AI with persistent chat history and advanced LLM workflows.

## ✨ Features

- **💬 Chat History Interface** - ChatGPT-like conversation sidebar with persistent message storage
- **📁 File Management** - Upload and store requirement documents with automatic organization
- **🤖 Natural Language Requirements** - Input requirements as text or upload documents (PDF, DOCX, TXT, CSV, JSON, PY)
- **🔍 Automated Analysis** - AI breaks down requirements into actionable tasks using LangChain
- **⚙️ Code Generation** - Generates production-ready Python code with proper structure
- **🧪 Automated Testing** - Creates and runs pytest test cases automatically
- **🔄 Self-Refinement** - AI reviews code and suggests improvements based on test results
- **💾 Project Memory** - PostgreSQL/SQLite database stores all project history, chats, and files
- **📥 Download Ready** - Export generated code, tests, and reports as files

## 🧠 Architecture

\`\`\`
User Input (Text/File)
    ↓
Chat Interface & History Storage (PostgreSQL/SQLite)
    ↓
LangChain + Requirement Analyzer (Gemini AI)
    ↓
Task Extraction & Code Generation
    ↓
Automated Testing (Pytest)
    ↓
Code Review & Refinement Loop
    ↓
Output & Download
    ↓
Database Storage (Chat, Projects, Files)
\`\`\`

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini AI API (Free Tier) |
| **Language** | Python 3.10+ |
| **LLM Framework** | LangChain |
| **Database** | PostgreSQL / SQLite |
| **Testing** | Pytest |
| **Database ORM** | SQLAlchemy |
| **Libraries** | Pandas, Matplotlib, google-generativeai |

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git (for cloning repository)
- PostgreSQL (optional - SQLite works by default)

### Quick Start (5 minutes)

\`\`\`bash
# Clone repository
git clone https://github.com/yourusername/sasds.git
cd sasds

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
# Edit .env and add GEMINI_API_KEY from https://aistudio.google.com/app/apikeys

# Run application
streamlit run app.py
\`\`\`

The app will open at **http://localhost:8501**

### Detailed Setup

For step-by-step instructions, see:
- **QUICK_START.md** - 5-minute setup
- **SETUP.md** - Detailed setup guide
- **GITHUB_SETUP.md** - Complete GitHub to running guide
- **WINDOWS_SETUP.md** - Windows-specific instructions

## 🚀 Running the Application

### Using the run script
\`\`\`bash
chmod +x run.sh
./run.sh
\`\`\`

### Manual run
\`\`\`bash
streamlit run app.py
\`\`\`

The app will open at `http://localhost:8501`

## 🔑 API Key Setup

### Getting Your Free Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Sign in with your Google account (create one if needed)
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file:
   \`\`\`
   GEMINI_API_KEY=your_key_here
   \`\`\`

**Note**: Google provides free tier API access with generous limits for testing and development.

## 🗄️ Database Configuration

### Option 1: SQLite (Default - No Setup)
- Built-in, no configuration needed
- Database file: `sasds.db` (auto-created)
- Perfect for development

### Option 2: PostgreSQL (Production)

**Using Neon.tech (Free Cloud):**
1. Sign up at https://neon.tech (free tier)
2. Create project
3. Copy connection string
4. Add to `.env`: `DATABASE_URL=postgresql://user:password@host/database`

**Using Local PostgreSQL:**
\`\`\`bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE sasds_db;"

# Update .env
DATABASE_URL=postgresql://postgres@localhost:5432/sasds_db
\`\`\`

## 💬 How It Works

### Workflow

1. **Create Chat Session**
   - Click "➕ New Chat" to start conversation
   - All messages automatically saved to database

2. **Input Requirements**
   - Type requirements in natural language
   - Or upload requirement documents (PDF, DOCX, TXT, CSV, JSON, PY)
   - Files stored with project for reference

3. **Analysis**
   - LangChain + Gemini AI analyzes requirements
   - System extracts tasks, libraries, and constraints
   - Chat history updated with analysis results

4. **Code Generation**
   - AI generates production-ready Python code
   - Code includes error handling, docstrings, and proper structure
   - Displayed in syntax-highlighted editor

5. **Testing**
   - System auto-generates pytest test cases
   - Runs tests and captures results
   - Shows pass/fail metrics

6. **Review & Refinement**
   - AI reviews code quality and performance
   - Suggests improvements and fixes
   - Can iterate until all tests pass

7. **Save & Download**
   - Export final code, tests, and reports
   - Project history saved in database
   - View and reopen old projects anytime
   - Access full chat history

## 📝 Example Usage

**Input:**
\`\`\`
Build a program that reads a CSV of employee details and prints names of employees earning above 50,000
\`\`\`

**System Output:**
- Tasks: Read CSV file, Filter employees, Display filtered output
- Generated code with proper structure
- Automated tests validating the code
- Review suggestions for optimization
- Download complete project package

## 📁 Project Structure

\`\`\`
sasds/
├── app.py                           # Main Streamlit application
├── database_models.py               # SQLAlchemy database models
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
│
├── run.sh                           # Run script
├── quick-start.sh                   # Quick setup script
├── verify-setup.sh                  # Verification script
│
├── README.md                        # This file
├── SETUP.md                         # Detailed setup guide
├── GITHUB_SETUP.md                  # GitHub to running guide
├── WINDOWS_SETUP.md                 # Windows setup
├── QUICK_START.md                   # Quick start guide
├── DEPLOYMENT.md                    # Deployment guide
├── TROUBLESHOOTING.md               # Troubleshooting
├── INSTALLATION_SUMMARY.md          # Installation overview
│
├── modules/
│   ├── __init__.py
│   ├── requirement_analyzer.py      # Analyzes requirements
│   ├── code_generator.py            # Generates Python code
│   ├── test_runner.py               # Runs pytest tests
│   ├── reviewer.py                  # Reviews & refines code
│   ├── storage.py                   # Project storage
│   ├── chat_manager.py              # Chat history management
│   ├── file_manager.py              # File upload & storage
│   └── langchain_integration.py     # LangChain workflows
│
├── uploads/                         # Uploaded files (auto-created)
└── sasds.db                         # SQLite database (auto-created)
\`\`\`

## 🚢 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from GitHub repository
4. Set `GEMINI_API_KEY` in Secrets section
5. (Optional) Set `DATABASE_URL` for PostgreSQL

See **DEPLOYMENT.md** for detailed instructions.

### Deploy to Render (Free)

1. Create account at [Render.com](https://render.com)
2. Create new Web Service from GitHub repo
3. Set environment variables
4. Deploy

### Deploy to Railway (Free Credit)

1. Go to [Railway.app](https://railway.app)
2. Create project from GitHub
3. Add PostgreSQL plugin
4. Deploy

See **DEPLOYMENT.md** for all options.

## 📊 Free Tier Resources

| Resource | Free Tier |
|----------|-----------|
| Gemini API | 60 requests/minute, daily quotas |
| Neon PostgreSQL | 3 projects, 3GB storage |
| Streamlit Cloud | Free hosting (community) |
| Railway | $5 credit/month |
| SQLite | Unlimited local storage |

## ❓ Troubleshooting

### "API key not found" error
- Ensure `.env` file is in the root directory
- Check format: `GEMINI_API_KEY=your_key_here` (no quotes)
- Restart app after editing .env

### Database connection error
- For SQLite: Leave `DATABASE_URL` empty
- For PostgreSQL: Verify connection string format
- Test connection: `python3 -c "from database_models import SessionLocal; db = SessionLocal()"`

### Chat history not saving
- Verify database is initialized
- Check `.env` DATABASE_URL is correct
- Ensure uploads directory exists and is writable

### Port 8501 already in use
\`\`\`bash
streamlit run app.py --server.port 8502
\`\`\`

See **TROUBLESHOOTING.md** for comprehensive solutions.

## 🔄 Self-Refinement Loop

The system can automatically improve code:

1. Generate initial code
2. Run tests
3. If tests fail → Review & identify issues
4. Generate improved code
5. Run tests again
6. Repeat until all tests pass (max iterations: 3)

## 📚 Documentation

- **README.md** (this file) - Project overview
- **SETUP.md** - Detailed setup instructions
- **GITHUB_SETUP.md** - Complete GitHub to running guide
- **WINDOWS_SETUP.md** - Windows-specific setup
- **QUICK_START.md** - 5-minute quick start
- **DEPLOYMENT.md** - Cloud deployment options
- **TROUBLESHOOTING.md** - Problem solving guide
- **INSTALLATION_SUMMARY.md** - Installation overview

## 🚀 Next Steps

After installation:

1. ✅ Verify setup: `bash verify-setup.sh`
2. 📝 Create first chat session
3. 🔍 Analyze a sample requirement
4. ⚙️ Generate code
5. 🧪 Run tests
6. 💬 Check chat history persists
7. 📦 Download project files

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push branch: `git push origin feature/YourFeature`
5. Submit pull request

## 📄 License

This project is open source and free to use.

## 💬 Support & Issues

- **Installation Help:** See SETUP.md or GITHUB_SETUP.md
- **Troubleshooting:** See TROUBLESHOOTING.md
- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check all .md files in repository

## 🌟 Features Roadmap

- [ ] Support for multiple programming languages (JavaScript, Java, Go)
- [ ] Advanced code metrics and analytics
- [ ] Team collaboration features
- [ ] Custom AI model support
- [ ] API endpoints for integration
- [ ] Mobile app support
- [ ] Real-time code collaboration

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - UI Framework
- [Google Gemini AI](https://ai.google.dev/) - AI Model
- [LangChain](https://python.langchain.com/) - LLM Framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pytest](https://pytest.org/) - Testing Framework
- [Python](https://python.org/) - Programming Language

---

**Made with ❤️ for developers who want to code smarter, not harder.**

**Start building with SASDS today! 🚀**
