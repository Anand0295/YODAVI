#!/usr/bin/env python3
"""
Create animated GIF demonstrations of AI Vision Pro features
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
from PIL import Image, ImageDraw, ImageFont

def create_upload_demo_gif():
    """Create animated GIF showing file upload process"""
    frames = []
    
    # Create base GUI frame
    width, height = 800, 600
    
    # Frame 1: Initial state
    frame1 = create_base_gui_frame(width, height)
    add_text(frame1, "Drag & drop image here", (width//2 - 100, height//2), (128, 128, 128))
    frames.extend([frame1] * 30)  # Hold for 1 second
    
    # Frame 2: Drag indication
    frame2 = create_base_gui_frame(width, height)
    add_text(frame2, "Dragging image...", (width//2 - 80, height//2), (79, 70, 229))
    cv2.rectangle(frame2, (width//2 - 150, height//2 - 50), (width//2 + 150, height//2 + 50), (79, 70, 229), 2)
    frames.extend([frame2] * 20)
    
    # Frame 3: Processing
    frame3 = create_base_gui_frame(width, height)
    add_text(frame3, "Processing image...", (width//2 - 90, height//2), (245, 158, 11))
    frames.extend([frame3] * 20)
    
    # Frame 4: Results
    frame4 = create_base_gui_frame(width, height)
    add_text(frame4, "Detection Complete!", (width//2 - 100, height//2 - 50), (16, 185, 129))
    add_text(frame4, "Found 3 objects", (width//2 - 70, height//2), (55, 65, 81))
    add_text(frame4, "• Person (92%)", (width//2 - 60, height//2 + 30), (55, 65, 81))
    add_text(frame4, "• Car (88%)", (width//2 - 60, height//2 + 50), (55, 65, 81))
    frames.extend([frame4] * 40)
    
    # Save as GIF
    save_frames_as_gif(frames, '../docs/images/upload-demo.gif', fps=30)
    print("✅ Created upload demo GIF")

def create_detection_demo_gif():
    """Create animated GIF showing live detection process"""
    frames = []
    width, height = 800, 600
    
    # Simulate detection sequence
    objects = [
        {"name": "person", "conf": 0.92, "pos": (200, 150)},
        {"name": "car", "conf": 0.88, "pos": (400, 300)},
        {"name": "bicycle", "conf": 0.75, "pos": (150, 400)}
    ]
    
    for i in range(60):  # 2 seconds at 30fps
        frame = create_base_gui_frame(width, height)
        
        # Add detection boxes progressively
        num_objects = min(len(objects), (i // 20) + 1)
        
        for j in range(num_objects):
            obj = objects[j]
            x, y = obj["pos"]
            
            # Draw bounding box
            cv2.rectangle(frame, (x-50, y-30), (x+50, y+30), (79, 70, 229), 2)
            
            # Draw label
            label = f"{obj['name']} {obj['conf']:.2f}"
            cv2.rectangle(frame, (x-50, y-45), (x+50, y-30), (79, 70, 229), -1)
            add_text(frame, label, (x-40, y-35), (255, 255, 255))
        
        # Add FPS counter
        add_text(frame, f"FPS: {28 + (i % 5)}", (20, 30), (16, 185, 129))
        
        frames.append(frame)
    
    save_frames_as_gif(frames, '../docs/images/live-detection.gif', fps=30)
    print("✅ Created live detection GIF")

def create_base_gui_frame(width, height):
    """Create base GUI frame"""
    frame = np.ones((height, width, 3), dtype=np.uint8) * 245
    
    # Add navbar
    cv2.rectangle(frame, (0, 0), (width, 50), (255, 255, 255), -1)
    add_text(frame, "AI Vision Pro", (20, 30), (79, 70, 229))
    
    # Add sidebar
    cv2.rectangle(frame, (0, 50), (200, height), (255, 255, 255), -1)
    
    return frame

def add_text(frame, text, pos, color):
    """Add text to frame"""
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def save_frames_as_gif(frames, output_path, fps=30):
    """Save frames as animated GIF"""
    # Convert OpenCV frames to PIL Images
    pil_frames = []
    for frame in frames:
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(rgb_frame)
        pil_frames.append(pil_frame)
    
    # Save as GIF
    pil_frames[0].save(
        output_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=1000//fps,
        loop=0
    )

def main():
    """Create all demo GIFs"""
    print("🎬 Creating animated GIF demonstrations...")
    
    os.makedirs('../docs/images', exist_ok=True)
    
    create_upload_demo_gif()
    create_detection_demo_gif()
    
    print("\n🎉 All demo GIFs created successfully!")

if __name__ == "__main__":
    main()