#!/usr/bin/env python3
"""
AI Vision Pro - Main Application Runner
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web_app import app, socketio

def main():
    """Main entry point for the application"""
    print("AI Vision Pro - Object Detection Platform")
    print("=========================================")
    print("🚀 Starting server on http://localhost:3000")
    print("📊 Professional web interface ready")
    socketio.run(app, debug=False, host='0.0.0.0', port=3000, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()