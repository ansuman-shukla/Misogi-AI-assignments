@echo off
REM Setup script for Multimodal QA Agent (Windows)
echo 🚀 Setting up Multimodal QA Agent...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔑 Creating .env file...
    copy .env.example .env
    echo Please edit .env file and add your GOOGLE_API_KEY
) else (
    echo ✅ .env file already exists
)

REM Create directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist screenshots mkdir screenshots
if not exist test_images mkdir test_images

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your GOOGLE_API_KEY
echo 2. Run the app: streamlit run app.py
echo 3. Or run tests: python test_agent.py

pause
