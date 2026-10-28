# api/index.py - Vercel Serverless Entrypoint for HemePath
import os
import sys

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# Expose app for Vercel WSGI
app = app
