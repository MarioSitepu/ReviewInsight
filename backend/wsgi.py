"""
WSGI entry point for PythonAnywhere
This file should be referenced in your PythonAnywhere Web app configuration
"""

import sys
import os

# Add the current directory to Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Import the Flask app
from app import app

# For PythonAnywhere, you might need to set the application variable
application = app

if __name__ == "__main__":
    app.run()

