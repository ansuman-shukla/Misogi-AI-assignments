#!/bin/bash

# Setup script for Multimodal QA Agent
echo "🚀 Setting up Multimodal QA Agent..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment (Linux/Mac)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
# Activate virtual environment (Windows Git Bash)
elif [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
fi

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file and add your GOOGLE_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p screenshots
mkdir -p test_images

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GOOGLE_API_KEY"
echo "2. Run the app: streamlit run app.py"
echo "3. Or run tests: python test_agent.py"
