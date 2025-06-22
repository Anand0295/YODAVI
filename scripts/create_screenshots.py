#!/usr/bin/env python3
"""
Create screenshots of AI Vision Pro GUI with object detection results
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
import base64
from PIL import Image, ImageDraw, ImageFont
import json

def create_gui_mockup_with_detection(image_path, output_path, vision_type="normal"):
    """Create a GUI mockup screenshot with detection results"""
    
    # Load YOLO model
    model = YOLO('yolo11n.pt')
    
    # Load and process image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return False
    
    # Run detection
    results = model(img, conf=0.5, verbose=False)
    
    # Draw detections
    annotated_img = img.copy()
    detections = []
    
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                
                # Get class info
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                
                # Store detection info
                detections.append({
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })
                
                # Choose color based on vision type
                if vision_type == "thermal":
                    color = (0, 0, 255)  # Red for thermal
                elif vision_type == "night_vision":
                    color = (0, 255, 0)  # Green for night vision
                else:
                    color = (255, 100, 100)  # Light blue for normal
                
                # Draw bounding box
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} {confidence:.2f}"
                font_scale = 0.6
                thickness = 2
                
                # Get text size
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                
                # Draw label background
                cv2.rectangle(annotated_img, 
                             (x1, y1 - text_height - 10), 
                             (x1 + text_width + 10, y1), 
                             color, -1)
                
                # Draw text
                cv2.putText(annotated_img, label, (x1 + 5, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
    
    # Create GUI mockup
    create_full_gui_screenshot(annotated_img, detections, output_path, vision_type)
    
    return True

def create_full_gui_screenshot(detection_img, detections, output_path, vision_type):
    """Create a full GUI screenshot with sidebar and main content"""
    
    # Resize detection image to fit in main area
    detection_img = cv2.resize(detection_img, (800, 600))
    
    # Create full GUI canvas (1200x800)
    gui_width, gui_height = 1200, 800
    gui_img = np.ones((gui_height, gui_width, 3), dtype=np.uint8) * 245  # Light gray background
    
    # Create navbar (top bar)
    navbar_height = 60
    gui_img[0:navbar_height, :] = [255, 255, 255]  # White navbar
    
    # Add navbar text
    cv2.putText(gui_img, "AI Vision Pro", (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (79, 70, 229), 2)
    cv2.putText(gui_img, "Dashboard", (400, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (107, 114, 128), 2)
    cv2.putText(gui_img, "Analytics", (520, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (107, 114, 128), 2)
    
    # Create sidebar (left panel)
    sidebar_width = 300
    sidebar_start = navbar_height + 20
    sidebar_height = gui_height - sidebar_start - 20
    
    # Sidebar background
    gui_img[sidebar_start:sidebar_start+sidebar_height, 20:20+sidebar_width] = [255, 255, 255]
    
    # Add sidebar content
    y_pos = sidebar_start + 30
    
    # Live Detection section
    cv2.putText(gui_img, "Live Detection", (40, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 65, 81), 2)
    y_pos += 40
    
    # Start button
    cv2.rectangle(gui_img, (40, y_pos), (280, y_pos + 35), (79, 70, 229), -1)
    cv2.putText(gui_img, "Start Detection", (60, y_pos + 22), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y_pos += 60
    
    # Upload section
    cv2.putText(gui_img, "Upload Image", (40, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 65, 81), 2)
    y_pos += 40
    
    # Upload area
    cv2.rectangle(gui_img, (40, y_pos), (280, y_pos + 80), (229, 231, 235), 2)
    cv2.putText(gui_img, "Drag & drop or click", (60, y_pos + 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (107, 114, 128), 1)
    cv2.putText(gui_img, "to upload", (110, y_pos + 55), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (107, 114, 128), 1)
    y_pos += 100
    
    # Stats section
    cv2.putText(gui_img, "Live Stats", (40, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 65, 81), 2)
    y_pos += 40
    
    # Stats cards
    stats = [
        ("Objects Detected", str(len(detections))),
        ("Session Time", "00:02:15"),
        ("FPS", "28")
    ]
    
    for i, (label, value) in enumerate(stats):
        card_y = y_pos + i * 60
        cv2.rectangle(gui_img, (40, card_y), (280, card_y + 50), (248, 250, 252), -1)
        cv2.putText(gui_img, value, (50, card_y + 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 41, 59), 2)
        cv2.putText(gui_img, label, (50, card_y + 42), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 116, 139), 1)
    
    # Main content area
    main_x = sidebar_width + 40
    main_y = sidebar_start
    main_width = gui_width - main_x - 20
    main_height = 400
    
    # Main content background
    gui_img[main_y:main_y+main_height, main_x:main_x+main_width] = [255, 255, 255]
    
    # Add title
    title = f"Real-time Object Detection - {vision_type.replace('_', ' ').title()}"
    cv2.putText(gui_img, title, (main_x + 20, main_y + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (31, 41, 55), 2)
    
    # Place detection image
    img_y = main_y + 50
    img_height = min(detection_img.shape[0], main_height - 70)
    img_width = min(detection_img.shape[1], main_width - 40)
    
    # Resize if needed
    if detection_img.shape[0] > img_height or detection_img.shape[1] > img_width:
        detection_img = cv2.resize(detection_img, (img_width, img_height))
    
    # Place the detection image
    gui_img[img_y:img_y+detection_img.shape[0], 
            main_x+20:main_x+20+detection_img.shape[1]] = detection_img
    
    # Analytics section (bottom)
    analytics_y = main_y + main_height + 20
    analytics_height = gui_height - analytics_y - 20
    
    # Recent detections panel
    panel_width = (main_width - 30) // 2
    cv2.rectangle(gui_img, (main_x, analytics_y), 
                  (main_x + panel_width, analytics_y + analytics_height), [255, 255, 255], -1)
    
    cv2.putText(gui_img, "Recent Detections", (main_x + 20, analytics_y + 25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 65, 81), 2)
    
    # List recent detections
    for i, detection in enumerate(detections[:5]):
        det_y = analytics_y + 50 + i * 25
        cv2.putText(gui_img, f"{detection['class']}", (main_x + 20, det_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (55, 65, 81), 1)
        cv2.putText(gui_img, f"{detection['confidence']:.1%}", (main_x + 150, det_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (107, 114, 128), 1)
    
    # Object distribution panel
    chart_x = main_x + panel_width + 20
    cv2.rectangle(gui_img, (chart_x, analytics_y), 
                  (chart_x + panel_width, analytics_y + analytics_height), [255, 255, 255], -1)
    
    cv2.putText(gui_img, "Object Distribution", (chart_x + 20, analytics_y + 25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 65, 81), 2)
    
    # Simple pie chart representation
    if detections:
        class_counts = {}
        for det in detections:
            class_counts[det['class']] = class_counts.get(det['class'], 0) + 1
        
        # Draw simple bars
        colors = [(79, 70, 229), (16, 185, 129), (245, 158, 11), (239, 68, 68)]
        y_offset = analytics_y + 50
        
        for i, (class_name, count) in enumerate(class_counts.items()):
            color = colors[i % len(colors)]
            bar_width = int((count / len(detections)) * 150)
            
            cv2.rectangle(gui_img, (chart_x + 20, y_offset), 
                         (chart_x + 20 + bar_width, y_offset + 20), color, -1)
            cv2.putText(gui_img, f"{class_name} ({count})", (chart_x + 20, y_offset + 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (55, 65, 81), 1)
            y_offset += 45
    
    # Save the screenshot
    cv2.imwrite(output_path, gui_img)
    print(f"✅ Created GUI screenshot: {output_path}")
    
    return True

def main():
    """Create screenshots for all sample images"""
    print("📸 Creating GUI screenshots with object detection...")
    
    # Ensure output directory exists
    os.makedirs('../docs/images', exist_ok=True)
    
    # Sample images to process
    samples = [
        ('../assets/sample_media/images/normal/sample_1.jpg', '../docs/images/dashboard-normal.png', 'normal'),
        ('../assets/sample_media/images/normal/sample_2.jpg', '../docs/images/detection-cars.png', 'normal'),
        ('../assets/sample_media/images/thermal/thermal_sample_1.jpg', '../docs/images/thermal-detection.png', 'thermal'),
        ('../assets/sample_media/images/night_vision/night_sample_1.jpg', '../docs/images/night-vision-detection.png', 'night_vision'),
    ]
    
    success_count = 0
    for input_path, output_path, vision_type in samples:
        if os.path.exists(input_path):
            if create_gui_mockup_with_detection(input_path, output_path, vision_type):
                success_count += 1
        else:
            print(f"❌ Sample not found: {input_path}")
    
    print(f"\n🎉 Created {success_count} GUI screenshots!")
    print("📁 Screenshots saved in docs/images/")

if __name__ == "__main__":
    main()