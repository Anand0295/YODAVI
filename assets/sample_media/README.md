# 📁 Sample Media Collection

This directory contains sample images and videos for demonstrating AI Vision Pro's object detection capabilities across different vision types.

## 📂 Directory Structure

```
sample_media/
├── images/
│   ├── normal/          # Standard RGB images
│   ├── thermal/         # Thermal-style images
│   └── night_vision/    # Night vision-style images
└── videos/
    ├── normal/          # Standard video footage
    ├── thermal/         # Thermal video demonstrations
    └── night_vision/    # Night vision video demonstrations
```

## 🖼️ Image Samples

### Normal Vision (RGB)
- **sample_1.jpg** - Person detection scenario
- **sample_2.jpg** - Vehicle detection scene
- **sample_3.jpg** - Street scene with multiple objects
- **sample_4.jpg** - Office environment
- **sample_5.jpg** - Kitchen/indoor scene

### Thermal Vision
- **thermal_sample_*.jpg** - Heat signature style images
- Simulated thermal imaging with color mapping
- Enhanced for object detection in temperature-based scenarios

### Night Vision
- **night_sample_*.jpg** - Low-light enhanced images
- Green-tinted night vision effect
- Optimized for low-light object detection

## 🎥 Video Samples

### Demo Videos (5 seconds each)
- **normal_demo.mp4** - Moving object in standard lighting
- **thermal_demo.mp4** - Thermal-style moving object detection
- **night_vision_demo.mp4** - Night vision object tracking

## 🎯 Usage Examples

### Testing Image Upload
```bash
# Test with normal image
curl -X POST -F "file=@sample_media/images/normal/sample_1.jpg" http://localhost:3000/upload_file

# Test with thermal image
curl -X POST -F "file=@sample_media/images/thermal/thermal_sample_1.jpg" http://localhost:3000/upload_file
```

### Command Line Detection
```bash
# Detect objects in normal image
python yodavi.py --source sample_media/images/normal/sample_1.jpg

# Process thermal image
python yodavi.py --source sample_media/images/thermal/thermal_sample_1.jpg

# Analyze night vision image
python yodavi.py --source sample_media/images/night_vision/night_sample_1.jpg
```

## 📊 Expected Detection Results

### Normal Images
- **People**: High accuracy (85-95%)
- **Vehicles**: Excellent detection (90-98%)
- **Common Objects**: Good performance (80-90%)

### Thermal Images
- **Heat Sources**: Enhanced detection of warm objects
- **People**: Excellent thermal signature detection
- **Vehicles**: Good detection of engine heat

### Night Vision Images
- **Low Light Objects**: Improved visibility
- **Enhanced Contrast**: Better edge detection
- **Reduced Noise**: Cleaner object boundaries

## 🔧 Customization

### Adding Your Own Samples
1. Place images in appropriate subdirectories
2. Supported formats: JPG, PNG, BMP
3. Recommended resolution: 640x480 or higher
4. File size limit: 10MB per file

### Creating Custom Thermal Images
```python
import cv2
import numpy as np

# Load normal image
img = cv2.imread('normal_image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thermal colormap
thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
cv2.imwrite('thermal_image.jpg', thermal)
```

### Creating Night Vision Effect
```python
import cv2
import numpy as np

# Load normal image
img = cv2.imread('normal_image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create night vision effect
night_vision = np.zeros_like(img)
night_vision[:, :, 1] = gray  # Green channel only
cv2.imwrite('night_vision_image.jpg', night_vision)
```

## 📈 Performance Testing

### Batch Processing
```bash
# Process all normal images
for img in sample_media/images/normal/*.jpg; do
    python yodavi.py --source "$img" --report
done

# Process all thermal images
for img in sample_media/images/thermal/*.jpg; do
    python yodavi.py --source "$img" --report
done
```

### Accuracy Comparison
Test detection accuracy across different vision types:
1. Run detection on all sample types
2. Compare confidence scores
3. Analyze detection consistency
4. Document performance differences

## 🎨 Visual Examples

### Detection Overlays
- **Bounding Boxes**: Color-coded by object type
- **Confidence Scores**: Percentage accuracy display
- **Labels**: Clear object identification
- **Timestamps**: Detection timing information

### Color Schemes
- **Normal**: Standard RGB colors
- **Thermal**: Red-yellow heat mapping
- **Night Vision**: Green monochrome enhancement

## 📝 Notes

- All sample images are royalty-free from Unsplash
- Thermal and night vision effects are simulated
- Videos are synthetically generated for demonstration
- Actual performance may vary with real thermal/night vision equipment

---

**Ready to test?** Upload these samples through the web interface or use the command line tools to see AI Vision Pro in action!