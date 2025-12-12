"""
Setup script for PythonAnywhere deployment
Run this on PythonAnywhere console after uploading files
"""

import os
import subprocess
import sys

def setup_pythonanywhere():
    """Setup ReviewInsight backend on PythonAnywhere"""
    
    print("🚀 Setting up ReviewInsight backend on PythonAnywhere...")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    # Check .env file
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("Create .env file with:")
        print("  DATABASE_URL=your_database_url")
        print("  GEMINI_API_KEY=your_gemini_api_key")
        print("  FLASK_ENV=production")
        return False
    else:
        print("✓ .env file found")
    
    # Create database tables
    print("\n🗄️  Creating database tables...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✓ Database tables created")
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("   Make sure DATABASE_URL is correct in .env")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Update your Web app WSGI file to point to app:app")
    print("2. Set up static files mapping (if needed)")
    print("3. Reload your web app")
    print("4. Update CORS settings in app.py if needed")
    
    return True

if __name__ == '__main__':
    setup_pythonanywhere()

