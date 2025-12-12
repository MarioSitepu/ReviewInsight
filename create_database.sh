#!/bin/bash

echo "Creating PostgreSQL database..."
echo ""

cd backend

echo "Checking Python virtual environment..."
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing psycopg2 if needed..."
pip install psycopg2-binary python-dotenv --quiet

echo ""
echo "Running database creation script..."
echo ""
python create_database.py


