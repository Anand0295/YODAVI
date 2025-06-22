#!/usr/bin/env python3
"""
Configuration settings for AI Vision Pro
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Application settings
APP_NAME = "AI Vision Pro"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 3000))
SECRET_KEY = os.getenv("SECRET_KEY", "ai_vision_pro_2024")

# Detection settings
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolo11n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", 0.4))

# Camera settings
CAMERA_WIDTH = int(os.getenv("CAMERA_WIDTH", 640))
CAMERA_HEIGHT = int(os.getenv("CAMERA_HEIGHT", 480))
CAMERA_FPS = int(os.getenv("CAMERA_FPS", 30))

# Performance settings
FRAME_SKIP_RATE = int(os.getenv("FRAME_SKIP_RATE", 4))
MAX_DETECTION_HISTORY = int(os.getenv("MAX_DETECTION_HISTORY", 50))
JPEG_QUALITY = int(os.getenv("JPEG_QUALITY", 80))

# Database settings
DATABASE_PATH = os.getenv("DATABASE_PATH", "ai_vision_detections.db")

# File upload settings
UPLOAD_FOLDER = BASE_DIR / "uploads"
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}

# Paths
STATIC_FOLDER = BASE_DIR / "assets" / "static"
TEMPLATE_FOLDER = BASE_DIR / "assets" / "templates"
SAMPLE_MEDIA_FOLDER = BASE_DIR / "assets" / "sample_media"

# Class-specific confidence thresholds
CONFIDENCE_THRESHOLDS = {
    'person': 0.7,
    'car': 0.8,
    'truck': 0.8,
    'bus': 0.8,
    'motorcycle': 0.7,
    'bicycle': 0.6,
    'knife': 0.5,
    'gun': 0.5,
    'default': 0.6
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'ai_vision_pro.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}