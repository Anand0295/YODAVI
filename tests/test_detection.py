#!/usr/bin/env python3
"""
Unit tests for object detection functionality
"""

import unittest
import sys
import os
import cv2
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from web_app import PhotoBoothDetector
except ImportError:
    # Fallback for different import paths
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.web_app import PhotoBoothDetector

class TestObjectDetection(unittest.TestCase):
    """Test cases for object detection"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = PhotoBoothDetector()
        
    def test_model_loading(self):
        """Test YOLO model loads correctly"""
        self.assertIsNotNone(self.detector.model)
        self.assertIsNotNone(self.detector.class_names)
        
    def test_detection_on_sample_image(self):
        """Test detection on a sample image"""
        # Create a simple test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Run detection
        detections = self.detector.detect_objects(test_image)
        
        # Should return a list (even if empty)
        self.assertIsInstance(detections, list)
        
    def test_confidence_thresholds(self):
        """Test confidence threshold settings"""
        self.assertIn('person', self.detector.confidence_thresholds)
        self.assertIn('car', self.detector.confidence_thresholds)
        
    def test_database_initialization(self):
        """Test database is properly initialized"""
        self.assertIsNotNone(self.detector.db)
        
        # Test table exists
        cursor = self.detector.db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='detections'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()