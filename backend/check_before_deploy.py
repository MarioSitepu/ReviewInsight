"""
Pre-deployment checklist for PythonAnywhere
Run this script before uploading to PythonAnywhere
"""

import os
import sys
from pathlib import Path

def check_before_deploy():
    """Check all requirements before deploying to PythonAnywhere"""
    
    print("=" * 60)
    print("PythonAnywhere Pre-Deployment Checklist")
    print("=" * 60)
    print()
    
    checks_passed = 0
    checks_failed = 0
    
    # Check 1: .env file exists
    print("1. Checking .env file...")
    env_file = Path('.env')
    if env_file.exists():
        print("   [OK] .env file found")
        checks_passed += 1
        
        # Check if DATABASE_URL is set
        from dotenv import load_dotenv
        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            print("   [OK] DATABASE_URL is set")
            checks_passed += 1
        else:
            print("   [ERROR] DATABASE_URL not found in .env")
            checks_failed += 1
    else:
        print("   [ERROR] .env file not found")
        print("   [INFO] Create .env file with DATABASE_URL and API keys")
        checks_failed += 1
    
    print()
    
    # Check 2: Required files exist
    print("2. Checking required files...")
    required_files = [
        'app.py',
        'sentiment_analyzer.py',
        'key_points_extractor.py',
        'requirements.txt',
        'wsgi.py'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"   [OK] {file}")
            checks_passed += 1
        else:
            print(f"   [ERROR] {file} not found")
            missing_files.append(file)
            checks_failed += 1
    
    if missing_files:
        print(f"   Missing files: {', '.join(missing_files)}")
    
    print()
    
    # Check 3: Test database connection
    print("3. Testing database connection...")
    try:
        from test_database_connection import test_database_connection
        if test_database_connection():
            checks_passed += 1
        else:
            checks_failed += 1
    except Exception as e:
        print(f"   ❌ Cannot test database: {e}")
        checks_failed += 1
    
    print()
    
    # Check 4: Required Python packages
    print("4. Checking Python packages...")
    required_packages = [
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'psycopg2',
        'transformers',
        'google.generativeai',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'psycopg2':
                __import__('psycopg2')
            elif package == 'google.generativeai':
                __import__('google.generativeai')
            else:
                __import__(package)
            print(f"   [OK] {package}")
            checks_passed += 1
        except ImportError:
            print(f"   [ERROR] {package} not installed")
            missing_packages.append(package)
            checks_failed += 1
    
    if missing_packages:
        print(f"   Install with: pip install {' '.join(missing_packages)}")
    
    print()
    
    # Check 5: API Keys
    print("5. Checking API keys...")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_keys = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'HUGGINGFACE_API_KEY': os.getenv('HUGGINGFACE_API_KEY')
    }
    
    at_least_one = False
    for key_name, key_value in api_keys.items():
        if key_value:
            print(f"   [OK] {key_name} is set")
            at_least_one = True
        else:
            print(f"   [WARNING] {key_name} not set (optional)")
    
    if at_least_one:
        print("   [OK] At least one AI API key is configured")
        checks_passed += 1
    else:
        print("   [ERROR] No AI API keys found")
        print("   [INFO] Add at least GEMINI_API_KEY to .env")
        checks_failed += 1
    
    print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"[OK] Passed: {checks_passed}")
    print(f"[ERROR] Failed: {checks_failed}")
    print()
    
    if checks_failed == 0:
        print("[SUCCESS] All checks passed! Ready for deployment to PythonAnywhere.")
        print()
        print("[INFO] Next steps:")
        print("1. Upload all files to PythonAnywhere")
        print("2. Install dependencies: pip3.10 install --user -r requirements.txt")
        print("3. Configure Web app WSGI file to point to wsgi:application")
        print("4. Reload web app")
        return True
    else:
        print("[ERROR] Some checks failed. Please fix issues before deploying.")
        return False

if __name__ == '__main__':
    success = check_before_deploy()
    sys.exit(0 if success else 1)

