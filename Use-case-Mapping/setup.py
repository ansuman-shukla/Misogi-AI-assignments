#!/usr/bin/env python3
"""
Setup script for the Model Comparison Tool.
Run this to install dependencies and set up the environment.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8 or higher required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_venv():
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  Warning: Not running in virtual environment")
        print("   It's recommended to use a virtual environment")
        response = input("   Continue anyway? (y/n): ").lower()
        return response.startswith('y')
    print("✅ Running in virtual environment")
    return True


def install_dependencies():
    """Install required dependencies."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    )


def setup_env_file():
    """Set up environment file."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("   Overwrite? (y/n): ").lower()
        if not response.startswith('y'):
            print("✅ Keeping existing .env file")
            return True
    
    try:
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def create_config_dir():
    """Create config directory if needed."""
    config_dir = Path("config")
    if not config_dir.exists():
        try:
            config_dir.mkdir()
            print("✅ Created config directory")
        except Exception as e:
            print(f"❌ Failed to create config directory: {e}")
            return False
    return True


def test_installation():
    """Test if installation works."""
    print("🧪 Testing installation...")
    
    # Test basic imports
    try:
        sys.path.insert(0, str(Path.cwd() / "src"))
        from models.model_config import load_config
        from utils.logger import setup_logger
        print("✅ Core modules import successfully")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    # Test config loading
    try:
        config = load_config()
        print("✅ Configuration loads successfully")
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🚀 Model Comparison Tool Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check virtual environment
    if not check_venv():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        return 1
    
    # Set up environment file
    if not setup_env_file():
        print("❌ Setup failed during environment setup")
        return 1
    
    # Create config directory
    if not create_config_dir():
        print("❌ Setup failed during config setup")
        return 1
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python main.py --help")
    print("3. Try: python demo.py")
    print("4. Or start with: python main.py --interactive")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
