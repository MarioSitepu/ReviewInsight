"""
Helper script to create PostgreSQL database if it doesn't exist.
This works on all platforms and doesn't require createdb command.
"""
import psycopg2
from psycopg2 import sql
import sys

def create_database(dbname='review_analyzer', user='postgres', password='postgres', host='localhost', port=5432):
    """
    Create a PostgreSQL database if it doesn't exist.
    
    Args:
        dbname: Name of the database to create
        user: PostgreSQL username
        password: PostgreSQL password
        host: Database host
        port: Database port
    """
    # Connect to PostgreSQL server (not to the specific database)
    # Use default 'postgres' database
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to default database
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (dbname,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ Database '{dbname}' already exists!")
            return True
        else:
            # Create database
            print(f"Creating database '{dbname}'...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(dbname)
                )
            )
            print(f"✅ Database '{dbname}' created successfully!")
            return True
            
    except psycopg2.OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL server:")
        print(f"   {str(e)}")
        print("\nPossible issues:")
        print("1. PostgreSQL is not running")
        print("2. Wrong username/password")
        print("3. PostgreSQL is not installed")
        print("4. Wrong host/port")
        return False
    except Exception as e:
        print(f"❌ Error creating database: {str(e)}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == '__main__':
    import argparse
    import os
    from urllib.parse import urlparse
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Try to parse DATABASE_URL from .env if available
    db_url = os.getenv('DATABASE_URL', '')
    dbname = 'review_analyzer'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = 5432
    
    if db_url:
        try:
            parsed = urlparse(db_url)
            dbname = parsed.path.lstrip('/') if parsed.path else 'review_analyzer'
            user = parsed.username or 'postgres'
            password = parsed.password or 'postgres'
            host = parsed.hostname or 'localhost'
            port = parsed.port or 5432
        except Exception:
            pass  # Use defaults if parsing fails
    
    parser = argparse.ArgumentParser(description='Create PostgreSQL database')
    parser.add_argument('--dbname', default=dbname, help='Database name')
    parser.add_argument('--user', default=user, help='PostgreSQL username')
    parser.add_argument('--password', default=password, help='PostgreSQL password')
    parser.add_argument('--host', default=host, help='Database host')
    parser.add_argument('--port', type=int, default=port, help='Database port')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("PostgreSQL Database Creator")
    print("=" * 50)
    print(f"Database: {args.dbname}")
    print(f"Host: {args.host}:{args.port}")
    print(f"User: {args.user}")
    print("=" * 50)
    print()
    
    success = create_database(
        dbname=args.dbname,
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port
    )
    
    if success:
        print("\n✅ Setup complete! You can now run the Flask application.")
        sys.exit(0)
    else:
        print("\n❌ Database creation failed. Please check the error messages above.")
        sys.exit(1)

