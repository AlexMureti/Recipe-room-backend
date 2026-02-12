#!/bin/bash
# Development startup script for Recipe Room Backend
# This script ensures the correct environment variables are used from .env file

# Unset any system-level DATABASE_URL that might interfere
unset DATABASE_URL

# Activate virtual environment
source venv/bin/activate

# Load environment from .env file and start app
python app.py
