#!/bin/bash

echo "Setting up backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy backend/env_example.txt to backend/.env"
echo "2. Edit backend/.env with your database URL and Gemini API key"
echo "3. Make sure PostgreSQL is running and database 'review_analyzer' exists"
echo "4. Run: python app.py"
echo ""


