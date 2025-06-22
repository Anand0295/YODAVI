# 📖 Usage Guide - AI Vision Pro

Complete guide to using AI Vision Pro for object detection and analysis.

## 🚀 Getting Started

### Starting the Application

1. **Navigate to project directory**:
   ```bash
   cd ai-vision-pro
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   ai-vision-env\Scripts\activate
   
   # macOS/Linux
   source ai-vision-env/bin/activate
   ```

3. **Start the server**:
   ```bash
   python web_app.py
   ```

4. **Open web interface**:
   Navigate to `http://localhost:3000` in your browser

## 🖥️ Interface Overview

### Navigation Bar
- **AI Vision Pro**: Brand logo and home link
- **Dashboard**: Main detection interface (active)
- **Analytics**: Detailed statistics view
- **Settings**: Configuration options

### Sidebar Controls
- **Live Detection**: Start/stop webcam detection
- **Upload Image**: Drag & drop or browse files
- **Live Stats**: Real-time metrics display

### Main Content Area
- **Video Feed**: Live camera or uploaded image display
- **Status Indicator**: Connection and detection status
- **Analytics Section**: Charts and detection history

## 🎥 Live Detection

### Starting Live Detection

1. **Click "Start Detection"** in the sidebar
2. **Allow camera permissions** when prompted by browser
3. **Position yourself** in front of the camera
4. **Watch real-time detection** with bounding boxes

### Detection Features

#### Object Recognition
- **80+ Object Classes**: People, vehicles, animals, everyday objects
- **Confidence Scores**: Percentage accuracy for each detection
- **Bounding Boxes**: Colored rectangles around detected objects
- **Real-time Labels**: Object names with confidence percentages

#### Performance Metrics
- **FPS Counter**: Frames processed per second
- **Session Timer**: Duration of current detection session
- **Object Counter**: Total objects detected in session

### Stopping Detection

1. **Click "Stop"** button in sidebar
2. **Detection feed stops** immediately
3. **Statistics preserved** for analysis
4. **Camera released** for other applications

## 📁 Image Upload & Analysis

### Supported Formats
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **BMP** (.bmp)
- **Maximum size**: 10MB per file

### Upload Methods

#### Drag & Drop
1. **Drag image file** from your computer
2. **Drop onto upload area** in sidebar
3. **Processing starts** automatically
4. **Results display** in main area

#### Browse & Select
1. **Click upload area** in sidebar
2. **Browse files** in dialog
3. **Select image** to analyze
4. **Upload and process** automatically

### Analysis Results
- **Detected Objects**: List with confidence scores
- **Bounding Boxes**: Visual markers on image
- **Statistics**: Object counts and distribution
- **Download Option**: Save processed image

## 📊 Analytics & Statistics

### Live Statistics Panel

#### Session Metrics
- **Objects Detected**: Total count for current session
- **Session Time**: Duration since detection started
- **FPS**: Current processing frame rate

#### Recent Detections
- **Last 5 Objects**: Most recently detected items
- **Confidence Scores**: Accuracy percentage for each
- **Timestamps**: When each object was detected

### Object Distribution Chart
- **Pie Chart**: Visual breakdown of detected object types
- **Interactive**: Hover for detailed information
- **Real-time Updates**: Changes as new objects detected
- **Color Coded**: Different colors for each object class

### Detection History
- **Comprehensive Log**: All detections with timestamps
- **Searchable**: Filter by object type or time
- **Exportable**: Download as CSV or JSON
- **Persistent**: Stored in SQLite database

## 🎯 Advanced Features

### Frame Capture

#### During Live Detection
1. **Click "Capture"** button while detection is running
2. **Current frame saved** with all bounding boxes
3. **Automatic download** to your computer
4. **Filename includes** timestamp for organization

#### Capture Settings
- **Format**: JPEG with detection overlays
- **Quality**: High resolution (original camera quality)
- **Annotations**: All detected objects with labels
- **Metadata**: Timestamp and detection count

### Data Management

#### Clear Detection Data
1. **Click "Clear Data"** button
2. **Confirm deletion** in popup dialog
3. **All statistics reset** to zero
4. **Database cleared** of detection history
5. **Charts and lists** updated immediately

#### Export Options
- **Detection Log**: CSV file with all detections
- **Statistics Report**: JSON with session summary
- **Captured Images**: ZIP file of all captures
- **Database Backup**: SQLite file download

## ⚙️ Configuration Options

### Detection Settings

#### Confidence Thresholds
Adjust minimum confidence for different object types:
```python
# In web_app.py
confidence_thresholds = {
    'person': 0.7,      # 70% confidence for people
    'car': 0.8,         # 80% confidence for vehicles
    'knife': 0.5,       # 50% confidence for knives
    'default': 0.6      # 60% for all other objects
}
```

#### Performance Tuning
```python
# Frame processing settings
FRAME_SKIP_RATE = 4     # Process every 4th frame
JPEG_QUALITY = 80       # Compression quality (1-100)
MAX_DETECTIONS = 50     # Maximum stored detections
```

### Camera Settings

#### Resolution Options
```python
# Camera configuration
FRAME_WIDTH = 640       # Pixels width
FRAME_HEIGHT = 480      # Pixels height
TARGET_FPS = 30         # Frames per second
```

#### Video Effects
- **Mirror Mode**: Flip camera horizontally (default: enabled)
- **Brightness**: Adjust camera brightness
- **Contrast**: Modify image contrast
- **Saturation**: Change color saturation

## 🔧 Troubleshooting

### Common Issues

#### Camera Not Working
**Symptoms**: Black screen, "Camera not accessible" error
**Solutions**:
1. Check camera permissions in browser settings
2. Ensure no other applications are using camera
3. Try different browser (Chrome recommended)
4. Restart browser and try again

#### Slow Performance
**Symptoms**: Low FPS, laggy interface
**Solutions**:
1. Close other applications to free memory
2. Reduce camera resolution in settings
3. Increase frame skip rate
4. Use Chrome for better performance

#### Detection Accuracy Issues
**Symptoms**: Objects not detected or false positives
**Solutions**:
1. Ensure good lighting conditions
2. Position objects clearly in frame
3. Adjust confidence thresholds
4. Try different camera angles

#### Upload Failures
**Symptoms**: Images won't upload or process
**Solutions**:
1. Check file format (JPG, PNG, BMP only)
2. Ensure file size under 10MB
3. Try different image
4. Check internet connection

### Browser Compatibility

#### Recommended Browsers
- **Chrome 90+**: Best performance and compatibility
- **Firefox 88+**: Good performance, some features limited
- **Safari 14+**: Works well on macOS
- **Edge 90+**: Good alternative on Windows

#### Required Features
- **WebRTC**: For camera access
- **WebSocket**: For real-time communication
- **Canvas API**: For image processing
- **File API**: For drag & drop uploads

## 📱 Mobile Usage

### Mobile Interface
- **Responsive Design**: Adapts to phone/tablet screens
- **Touch Optimized**: Large buttons and touch targets
- **Swipe Navigation**: Easy switching between sections
- **Portrait/Landscape**: Works in both orientations

### Mobile Limitations
- **Camera Access**: May require HTTPS in some browsers
- **Performance**: Slower processing on mobile devices
- **Battery Usage**: Intensive processing drains battery
- **File Upload**: Limited by mobile browser capabilities

## 🎓 Best Practices

### For Best Detection Results
1. **Good Lighting**: Ensure adequate, even lighting
2. **Clear Background**: Avoid cluttered backgrounds
3. **Object Size**: Objects should be clearly visible
4. **Stable Camera**: Minimize camera shake
5. **Multiple Angles**: Try different viewpoints

### For Optimal Performance
1. **Close Unused Tabs**: Free up browser memory
2. **Stable Internet**: Ensure good connection
3. **Regular Clearing**: Clear detection data periodically
4. **Browser Updates**: Keep browser up to date
5. **System Resources**: Ensure adequate RAM available

### For Data Management
1. **Regular Backups**: Export detection data regularly
2. **Organized Captures**: Use descriptive filenames
3. **Storage Monitoring**: Check available disk space
4. **Privacy Awareness**: Be mindful of captured content
5. **Data Retention**: Clear old data when not needed

## 📞 Support & Help

### Getting Help
- **Documentation**: Check this guide and README
- **Video Tutorials**: Available on project website
- **Community Forum**: Join discussions with other users
- **GitHub Issues**: Report bugs and request features
- **Email Support**: Contact development team

### Keyboard Shortcuts
- **Space**: Start/stop detection
- **C**: Capture current frame
- **U**: Open file upload dialog
- **Esc**: Close any open dialogs
- **R**: Refresh/reset interface

---

**Ready to start detecting?** Launch the application and begin exploring the world of AI-powered object detection!