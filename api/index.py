from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create Flask app
app = create_app('production')

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function handler"""
    return app(request, context)

# For local development
if __name__ == '__main__':
    app.run(debug=True) 