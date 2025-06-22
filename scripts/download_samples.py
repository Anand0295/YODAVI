#!/usr/bin/env python3
"""
Download sample images and videos for AI Vision Pro demonstration
"""

import os
import requests
from urllib.parse import urlparse
import cv2
import numpy as np

def download_file(url, filepath):
    """Download file from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return False

def create_synthetic_thermal(input_path, output_path):
    """Create synthetic thermal-style image"""
    img = cv2.imread(input_path)
    if img is None:
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thermal colormap
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    # Add some noise for realism
    noise = np.random.randint(0, 50, thermal.shape, dtype=np.uint8)
    thermal = cv2.add(thermal, noise)
    
    cv2.imwrite(output_path, thermal)
    return True

def create_synthetic_night_vision(input_path, output_path):
    """Create synthetic night vision style image"""
    img = cv2.imread(input_path)
    if img is None:
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply green tint for night vision effect
    night_vision = np.zeros_like(img)
    night_vision[:, :, 1] = gray  # Green channel
    
    # Add some grain
    grain = np.random.randint(0, 30, night_vision.shape, dtype=np.uint8)
    night_vision = cv2.add(night_vision, grain)
    
    cv2.imwrite(output_path, night_vision)
    return True

def main():
    print("🚀 Downloading sample media for AI Vision Pro...")
    
    # Sample URLs for different types of images
    sample_urls = {
        'normal': [
            'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=800',  # Person
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',  # Cars
            'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800',  # Street scene
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',  # Office
            'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800',   # Kitchen
        ]
    }
    
    base_dir = '../assets/sample_media'
    
    # Download normal images
    print("\n📸 Downloading normal images...")
    for i, url in enumerate(sample_urls['normal']):
        filename = f"sample_{i+1}.jpg"
        filepath = os.path.join(base_dir, 'images', 'normal', filename)
        download_file(url, filepath)
    
    # Create thermal and night vision variants
    print("\n🔥 Creating thermal images...")
    normal_dir = os.path.join(base_dir, 'images', 'normal')
    thermal_dir = os.path.join(base_dir, 'images', 'thermal')
    night_dir = os.path.join(base_dir, 'images', 'night_vision')
    
    os.makedirs(thermal_dir, exist_ok=True)
    os.makedirs(night_dir, exist_ok=True)
    
    for filename in os.listdir(normal_dir):
        if filename.endswith('.jpg'):
            input_path = os.path.join(normal_dir, filename)
            
            # Create thermal version
            thermal_path = os.path.join(thermal_dir, f"thermal_{filename}")
            if create_synthetic_thermal(input_path, thermal_path):
                print(f"✅ Created thermal: {filename}")
            
            # Create night vision version
            night_path = os.path.join(night_dir, f"night_{filename}")
            if create_synthetic_night_vision(input_path, night_path):
                print(f"✅ Created night vision: {filename}")
    
    # Create sample videos (simple ones using OpenCV)
    print("\n🎥 Creating sample videos...")
    create_sample_videos()
    
    print("\n🎉 Sample media download complete!")
    print(f"📁 Files saved in: {os.path.abspath(base_dir)}")

def create_sample_videos():
    """Create simple sample videos for demonstration"""
    video_dir = 'sample_media/videos'
    
    # Create a simple moving object video
    for vision_type in ['normal', 'thermal', 'night_vision']:
        output_path = os.path.join(video_dir, vision_type, f'{vision_type}_demo.mp4')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Video properties
        width, height = 640, 480
        fps = 30
        duration = 5  # seconds
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for frame_num in range(fps * duration):
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add moving rectangle (simulating object)
            x = int((frame_num / (fps * duration)) * (width - 100))
            y = height // 2 - 25
            
            if vision_type == 'normal':
                color = (0, 255, 0)  # Green
                frame[:] = (50, 50, 50)  # Dark background
            elif vision_type == 'thermal':
                color = (0, 0, 255)  # Red
                frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
            else:  # night_vision
                color = (0, 255, 0)  # Green
                frame[:] = (0, 20, 0)  # Dark green background
            
            cv2.rectangle(frame, (x, y), (x + 100, y + 50), color, -1)
            cv2.putText(frame, f'{vision_type.upper()} DEMO', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            out.write(frame)
        
        out.release()
        print(f"✅ Created video: {vision_type}_demo.mp4")

if __name__ == "__main__":
    main()