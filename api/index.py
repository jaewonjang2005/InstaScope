import sys
import os

# Add backend to path for Vercel serverless execution
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.main import app
