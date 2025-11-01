#!/bin/bash

set -e

echo "🚀 SASDS Quick Start"
echo ""

# Step 1: Check if venv exists
if [ ! -d "venv" ]; then
    echo "📌 Creating virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate venv
echo "📌 Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "📌 Upgrading pip..."
pip install --upgrade pip > /dev/null

# Step 4: Install requirements
echo "📌 Installing dependencies..."
pip install -r requirements.txt > /dev/null

# Step 5: Check .env
if [ ! -f .env ]; then
    echo "📌 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please add your GEMINI_API_KEY to .env file"
    echo "   1. Get key from: https://aistudio.google.com/app/apikeys"
    echo "   2. Edit .env file and add your key"
    echo "   3. Run this script again"
    echo ""
    exit 1
fi

# Step 6: Initialize database
echo "📌 Initializing database..."
python3 -c "from database_models import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null || true

# Step 7: Start app
echo ""
echo "✅ Setup complete!"
echo "🌐 Starting SASDS at http://localhost:8501"
echo ""
echo "💡 Tip: Press Ctrl+C to stop the app"
echo ""

streamlit run app.py
