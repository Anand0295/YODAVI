from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import base64
import json
import sqlite3
from datetime import datetime
from ultralytics import YOLO
import threading
import os
import time
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mit_photobooth_detection_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

class PhotoBoothDetector:
    def __init__(self):
        self.model = YOLO('yolo11n.pt')
        self.detection_log = deque(maxlen=50)
        self.is_running = False
        self.cap = None
        self.db = self.init_database()
        self.class_names = self.model.names
        
        # Optimized for performance
        self.confidence_thresholds = {
            'person': 0.7,
            'car': 0.8,
            'knife': 0.5
        }
        
        self.stats = {
            'total_detections': 0,
            'session_start': datetime.now()
        }

    def init_database(self):
        conn = sqlite3.connect('photobooth_detections.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                class_name TEXT,
                confidence REAL,
                source TEXT
            )
        ''')
        
        conn.commit()
        return conn

    def detect_objects(self, frame):
        """Lightweight object detection optimized for real-time"""
        results = self.model(frame, conf=0.5, iou=0.4, verbose=False)
        detections = []
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.class_names[class_id]
                    confidence = float(box.conf[0])
                    
                    # Apply confidence threshold
                    threshold = self.confidence_thresholds.get(class_name, 0.6)
                    
                    if confidence >= threshold:
                        detection = {
                            'class': class_name,
                            'confidence': round(confidence, 3),
                            'bbox': box.xyxy[0].cpu().numpy().tolist(),
                            'timestamp': datetime.now().strftime('%H:%M:%S')
                        }
                        detections.append(detection)
        
        return detections

    def draw_detections(self, frame, detections):
        """Draw PhotoBooth-style overlays"""
        annotated = frame.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            class_name = detection['class']
            confidence = detection['confidence']
            
            # PhotoBooth-style colors (softer, more aesthetic)
            if 'person' in class_name.lower():
                color = (255, 200, 100)  # Light blue
            elif any(vehicle in class_name.lower() for vehicle in ['car', 'truck', 'bus']):
                color = (100, 255, 200)  # Light green
            else:
                color = (200, 100, 255)  # Light purple
            
            # Rounded rectangle effect
            thickness = 3
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
            
            # Modern label style
            label = f"{class_name} {confidence:.2f}"
            font_scale = 0.6
            font_thickness = 2
            
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            
            # Draw rounded background
            cv2.rectangle(annotated, 
                         (x1, y1 - text_height - 15), 
                         (x1 + text_width + 10, y1), 
                         color, -1)
            
            # Add text
            cv2.putText(annotated, label, (x1 + 5, y1 - 8), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
        
        return annotated

    def store_detections(self, detections, source='webcam'):
        """Store detections efficiently"""
        if not detections:
            return
            
        cursor = self.db.cursor()
        for detection in detections:
            cursor.execute('''
                INSERT INTO detections (class_name, confidence, source)
                VALUES (?, ?, ?)
            ''', (detection['class'], detection['confidence'], source))
        
        self.db.commit()
        self.stats['total_detections'] += len(detections)

    def get_statistics(self):
        """Get lightweight statistics"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT class_name, COUNT(*) as count, AVG(confidence) as avg_conf
            FROM detections 
            WHERE timestamp > datetime('now', '-10 minutes')
            GROUP BY class_name
            ORDER BY count DESC
            LIMIT 5
        ''')
        
        class_stats = {}
        for row in cursor.fetchall():
            class_stats[row[0]] = {
                'count': row[1],
                'avg_confidence': round(row[2], 3)
            }
        
        return {
            'class_statistics': class_stats,
            'total_detections': self.stats['total_detections'],
            'session_duration': str(datetime.now() - self.stats['session_start']).split('.')[0]
        }

    def start_webcam(self):
        """Start PhotoBooth-style webcam with optimized performance"""
        self.cap = cv2.VideoCapture(0)
        
        # Optimize camera settings for performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_running = True
        frame_count = 0
        
        print("PhotoBooth detection started...")
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading from webcam")
                break
            
            frame_count += 1
            
            # Process every 4th frame for optimal performance
            if frame_count % 4 == 0:
                # Flip frame for PhotoBooth mirror effect
                frame = cv2.flip(frame, 1)
                
                detections = self.detect_objects(frame)
                
                if detections:
                    self.store_detections(detections)
                    self.detection_log.extend(detections)
                
                annotated_frame = self.draw_detections(frame, detections)
                
                # Add PhotoBooth-style frame counter
                cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Convert to base64 with optimized quality
                _, buffer = cv2.imencode('.jpg', annotated_frame, 
                                       [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Emit to clients
                socketio.emit('video_frame', {
                    'frame': frame_base64,
                    'detections': detections,
                    'stats': self.get_statistics(),
                    'frame_count': frame_count
                })
            
            time.sleep(0.03)  # ~30 FPS
        
        if self.cap:
            self.cap.release()
            print("PhotoBooth stopped")

    def stop_webcam(self):
        """Stop webcam detection"""
        self.is_running = False
        if self.cap:
            self.cap.release()

detector = PhotoBoothDetector()

@app.route('/')
def index():
    return render_template('photobooth.html')

@app.route('/start_webcam', methods=['POST'])
def start_webcam():
    if not detector.is_running:
        thread = threading.Thread(target=detector.start_webcam)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already_running'})

@app.route('/stop_webcam', methods=['POST'])
def stop_webcam():
    detector.stop_webcam()
    return jsonify({'status': 'stopped'})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    # Save and process file
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)
    
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        frame = cv2.imread(filepath)
        if frame is not None:
            detections = detector.detect_objects(frame)
            
            if detections:
                detector.store_detections(detections, filename)
            
            annotated_frame = detector.draw_detections(frame, detections)
            
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                'frame': frame_base64,
                'detections': detections,
                'count': len(detections)
            })
    
    return jsonify({'error': 'Unsupported file type'})

@app.route('/statistics')
def statistics():
    return jsonify(detector.get_statistics())

@app.route('/get_logs')
def get_logs():
    recent_logs = list(detector.detection_log)[-20:]
    return jsonify(recent_logs)

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    cursor = detector.db.cursor()
    cursor.execute('DELETE FROM detections')
    detector.db.commit()
    detector.stats['total_detections'] = 0
    detector.detection_log.clear()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    print("AI Vision Pro - Object Detection Platform")
    print("=========================================")
    print("🚀 Starting server on http://localhost:3000")
    print("📊 Professional web interface ready")
    socketio.run(app, debug=False, host='0.0.0.0', port=3000, allow_unsafe_werkzeug=True)