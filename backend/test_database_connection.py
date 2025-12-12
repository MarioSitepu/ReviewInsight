"""
Test database connection script
Run this before deploying to PythonAnywhere to verify DATABASE_URL is correct
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection using DATABASE_URL"""
    
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    print()
    
    # Get DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("[ERROR] DATABASE_URL not found in environment variables")
        print()
        print("[INFO] Solution:")
        print("1. Create .env file in backend directory")
        print("2. Add DATABASE_URL=your_connection_string")
        print()
        print("Example for Neon:")
        print("DATABASE_URL=postgresql://user:pass@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require")
        print()
        print("Example for local PostgreSQL:")
        print("DATABASE_URL=postgresql://postgres:postgres@localhost:5432/review_analyzer")
        return False
    
    print("[OK] DATABASE_URL found")
    print(f"    Connection string: {database_url[:50]}...")  # Show first 50 chars only
    print()
    
    # Check if it's a valid PostgreSQL URL
    if not database_url.startswith('postgresql://'):
        print("[WARNING] DATABASE_URL doesn't start with 'postgresql://'")
        print("          Make sure you're using PostgreSQL connection string")
        print()
    
    # Check for SSL mode (required for Neon and most cloud databases)
    if 'sslmode=require' not in database_url and 'neon.tech' in database_url:
        print("[WARNING] Neon database should include ?sslmode=require")
        print("          Example: ...neon.tech/dbname?sslmode=require")
        print()
    
    # Try to import SQLAlchemy and test connection
    try:
        print("[INFO] Testing SQLAlchemy import...")
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        print("[OK] SQLAlchemy imported successfully")
        print()
    except ImportError as e:
        print(f"[ERROR] Cannot import SQLAlchemy: {e}")
        print("        Install with: pip install flask-sqlalchemy psycopg2-binary")
        return False
    
    # Create Flask app and test connection
    try:
        print("[INFO] Testing database connection...")
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        # Test connection
        with app.app_context():
            # Try to connect
            db.engine.connect()
            print("[OK] Database connection successful!")
            print()
            
            # Check if tables exist
            print("[INFO] Checking database tables...")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"[OK] Found {len(tables)} table(s):")
                for table in tables:
                    print(f"     - {table}")
            else:
                print("[INFO] No tables found (this is OK if first time setup)")
                print("       Tables will be created automatically on first run")
            
            print()
            
            # Test creating tables
            print("[INFO] Testing table creation...")
            try:
                # Import Review model
                from app import Review
                db.create_all()
                print("[OK] Tables can be created successfully")
            except Exception as e:
                print(f"[WARNING] Table creation test: {str(e)}")
                print("          This might be OK if tables already exist")
            
            print()
            
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Database connection failed")
        print(f"        Error: {error_msg}")
        print()
        
        # Provide helpful error messages
        if "password authentication failed" in error_msg.lower():
            print("[TIP] Solution: Check username and password in DATABASE_URL")
        elif "could not connect" in error_msg.lower() or "connection refused" in error_msg.lower():
            print("[TIP] Solution: Check host and port in DATABASE_URL")
            print("       Make sure database server is running and accessible")
        elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("[TIP] Solution: Database name doesn't exist")
            print("       Create database first or check database name in DATABASE_URL")
        elif "ssl" in error_msg.lower() or "sslmode" in error_msg.lower():
            print("[TIP] Solution: Add ?sslmode=require to connection string")
            print("       Example: ...neon.tech/dbname?sslmode=require")
        elif "psycopg2" in error_msg.lower() or "psycopg" in error_msg.lower():
            print("[TIP] Solution: Install psycopg2-binary")
            print("       Run: pip install psycopg2-binary")
        else:
            print("[TIP] Check your DATABASE_URL format:")
            print("       postgresql://username:password@host:port/database?sslmode=require")
        
        return False
    
    print("=" * 60)
    print("[SUCCESS] All tests passed! Database is ready for deployment.")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_database_connection()
    sys.exit(0 if success else 1)

