import streamlit as st
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import and run the main app
import app

# Run the main function from app.py
if __name__ == "__main__":
    app.main()