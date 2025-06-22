import cv2
import os
import argparse
import json
import sqlite3
import time
from datetime import datetime
from collections import deque
import numpy as np
from ultralytics import YOLO

class SmartDetectionSystem:
    def __init__(self, model_path='yolo11n.pt'):
        self.model = YOLO(model_path)
        self.detection_history = deque(maxlen=100)
        self.db = self.init_database()
        self.class_names = self.model.names
        
        # Fine-tuned confidence thresholds for better accuracy
        self.confidence_thresholds = {
            'person': 0.6,
            'car': 0.7, 'truck': 0.7, 'bus': 0.7, 'motorcycle': 0.6,
            'knife': 0.4, 'scissors': 0.5  # Lower for weapons due to rarity
        }

    def get_adaptive_confidence(self, class_name):
        """Get adaptive confidence threshold based on class type"""
        return self.confidence_thresholds.get(class_name, 0.5)

    def init_database(self):
        conn = sqlite3.connect('detections.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                class_name TEXT,
                confidence REAL,
                bbox TEXT,
                image_path TEXT
            )
        ''')
        
        conn.commit()
        return conn

    def detect_objects(self, frame, conf_threshold=0.5):
        """Enhanced detection with adaptive confidence and NMS"""
        results = self.model(frame, conf=conf_threshold, iou=0.4)
        detections = []
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.class_names[class_id]
                    confidence = float(box.conf[0])
                    
                    # Apply adaptive confidence threshold
                    adaptive_conf = self.get_adaptive_confidence(class_name)
                    
                    if confidence >= adaptive_conf:
                        detection = {
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': box.xyxy[0].cpu().numpy().tolist(),
                            'timestamp': datetime.now().strftime('%H:%M:%S')
                        }
                        detections.append(detection)
        
        return detections

    def store_detection(self, detection, image_path='webcam'):
        """Store detection in database"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO detections (class_name, confidence, bbox, image_path)
            VALUES (?, ?, ?, ?)
        ''', (detection['class'], detection['confidence'], 
             json.dumps(detection['bbox']), image_path))
        self.db.commit()
    
    def calculate_accuracy_metrics(self):
        """Calculate detection accuracy metrics for academic analysis"""
        cursor = self.db.cursor()
        cursor.execute('SELECT class_name, confidence FROM detections')
        data = cursor.fetchall()
        
        if not data:
            return {}
        
        class_stats = {}
        for class_name, confidence in data:
            if class_name not in class_stats:
                class_stats[class_name] = []
            class_stats[class_name].append(confidence)
        
        metrics = {}
        for class_name, confidences in class_stats.items():
            metrics[class_name] = {
                'count': len(confidences),
                'avg_confidence': sum(confidences) / len(confidences),
                'max_confidence': max(confidences),
                'min_confidence': min(confidences)
            }
        
        return metrics

    def process_image(self, image_path, output_path=None):
        """Process single image with enhanced accuracy"""
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error: Could not load image {image_path}")
            return []
        
        detections = self.detect_objects(frame)
        
        # Store detections
        for detection in detections:
            self.store_detection(detection, image_path)
        
        # Annotate frame
        annotated_frame = self.draw_detections(frame, detections)
        
        if output_path:
            cv2.imwrite(output_path, annotated_frame)
            print(f"Results saved to {output_path}")
        else:
            cv2.imshow('Smart Detection - Image', annotated_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return detections

    def process_video(self, video_path, output_path=None):
        """Process video with optimized frame sampling"""
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        all_detections = []
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every 3rd frame for better accuracy vs performance balance
            if frame_count % 3 == 0:
                detections = self.detect_objects(frame)
                all_detections.extend(detections)
                annotated_frame = self.draw_detections(frame, detections)
            else:
                annotated_frame = frame
            
            if output_path:
                out.write(annotated_frame)
            else:
                cv2.imshow('Smart Detection - Video', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        print(f"Processed {frame_count} frames, found {len(all_detections)} detections")
        return all_detections

    def process_webcam(self):
        """Real-time webcam detection with performance monitoring"""
        cap = cv2.VideoCapture(0)
        frame_count = 0
        fps_counter = deque(maxlen=30)
        
        print("Starting webcam detection. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from webcam")
                break
            
            frame_count += 1
            start_time = time.time()
            
            detections = self.detect_objects(frame)
            
            # Store detections
            for detection in detections:
                self.store_detection(detection, 'webcam')
                self.detection_history.append(detection)
            
            # Draw detections
            annotated_frame = self.draw_detections(frame, detections)
            
            # Calculate and display FPS
            processing_time = time.time() - start_time
            fps = 1.0 / processing_time if processing_time > 0 else 0
            fps_counter.append(fps)
            avg_fps = sum(fps_counter) / len(fps_counter)
            
            # Add performance info
            cv2.putText(annotated_frame, f"FPS: {avg_fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Detections: {len(detections)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Smart Detection System - Live', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"Session ended. Processed {frame_count} frames.")

    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        annotated = frame.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            
            # Color coding based on object type
            if 'weapon' in detection['class'].lower() or 'knife' in detection['class'].lower():
                color = (0, 0, 255)  # Red for weapons
            elif 'person' in detection['class'].lower():
                color = (255, 0, 0)  # Blue for persons
            else:
                color = (0, 255, 0)  # Green for vehicles/others
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Draw label with confidence
            label = f"{detection['class']} {detection['confidence']:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            
            # Background for text
            cv2.rectangle(annotated, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            
            # Text
            cv2.putText(annotated, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return annotated
    
    def generate_report(self):
        """Generate academic analysis report"""
        metrics = self.calculate_accuracy_metrics()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_detections': sum(m['count'] for m in metrics.values()),
            'class_statistics': metrics,
            'recent_detections': list(self.detection_history)[-10:]
        }
        
        with open('detection_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n=== Detection Report ===")
        print(f"Total detections: {report['total_detections']}")
        for class_name, stats in metrics.items():
            print(f"{class_name}: {stats['count']} detections, "
                  f"avg confidence: {stats['avg_confidence']:.3f}")
        
        return report

    def close(self):
        """Clean up resources"""
        self.db.close()

def main():
    parser = argparse.ArgumentParser(description='Smart Object Detection System - MIT Student Project')
    parser.add_argument('--source', type=str, default='webcam', 
                       help='Source: webcam, image path, or video path')
    parser.add_argument('--model', type=str, default='yolo11n.pt',
                       help='YOLO model path')
    parser.add_argument('--output', type=str, default=None,
                       help='Output path for processed media')
    parser.add_argument('--report', action='store_true',
                       help='Generate accuracy analysis report')
    
    args = parser.parse_args()
    
    # Initialize detection system
    detector = SmartDetectionSystem(args.model)
    
    try:
        print("Smart Detection System - MIT Computer Vision Project")
        print("=====================================================")
        
        if args.source == 'webcam':
            detector.process_webcam()
        elif os.path.isfile(args.source):
            if args.source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                detections = detector.process_image(args.source, args.output)
                print(f"Found {len(detections)} objects in image")
            else:
                detections = detector.process_video(args.source, args.output)
                print(f"Processed video with {len(detections)} total detections")
        else:
            print(f"Error: Invalid source '{args.source}'")
            return
        
        if args.report:
            detector.generate_report()
    
    except KeyboardInterrupt:
        print("\nDetection stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        detector.close()
        print("System shutdown complete")

if __name__ == '__main__':
    main()