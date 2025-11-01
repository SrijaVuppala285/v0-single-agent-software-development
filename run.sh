#!/bin/bash

set -e

echo "🚀 Starting SASDS (Single Agent Software Development System)"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your GEMINI_API_KEY and DATABASE_URL"
    echo "   Then run this script again."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️  Initializing database..."
python3 -c "from database_models import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Database initialized')"

echo ""
echo "✅ All setup complete!"
echo ""
echo "🌐 Starting Streamlit app..."
echo "📍 App will be available at: http://localhost:8501"
echo ""

# Run the Streamlit app
streamlit run app.py
