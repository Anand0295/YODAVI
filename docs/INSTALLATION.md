# 🛠️ Installation Guide - AI Vision Pro

This comprehensive guide will walk you through installing and setting up AI Vision Pro on your system.

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 2GB available memory
- **Storage**: 1GB free disk space
- **Camera**: Any USB webcam or built-in camera
- **Internet**: Required for initial model download

### Recommended Specifications
- **CPU**: Quad-core processor 2.5GHz+
- **RAM**: 4GB+ available memory
- **Storage**: 2GB+ free disk space
- **Camera**: 720p or higher resolution
- **GPU**: Optional, but improves performance

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone and setup in one command
curl -sSL https://raw.githubusercontent.com/your-username/ai-vision-pro/main/install.sh | bash
```

### Option 2: Manual Installation

#### Step 1: Install Python
**Windows:**
1. Download Python from [python.org](https://python.org)
2. Run installer and check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/your-username/ai-vision-pro.git
cd ai-vision-pro
```

#### Step 3: Create Virtual Environment
```bash
# Create virtual environment
python -m venv ai-vision-env

# Activate virtual environment
# Windows:
ai-vision-env\Scripts\activate
# macOS/Linux:
source ai-vision-env/bin/activate
```

#### Step 4: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 5: Verify Installation
```bash
python -c "import cv2, ultralytics, flask; print('All dependencies installed successfully!')"
```

## 🔧 Platform-Specific Setup

### Windows Setup

#### Install Visual C++ Build Tools
Some packages require compilation:
1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Install with C++ build tools

#### Camera Permissions
1. Go to **Settings > Privacy > Camera**
2. Enable camera access for desktop apps

### macOS Setup

#### Install Xcode Command Line Tools
```bash
xcode-select --install
```

#### Camera Permissions
1. **System Preferences > Security & Privacy > Camera**
2. Allow Terminal or your IDE to access camera

### Linux Setup

#### Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt install python3-dev python3-pip libopencv-dev

# CentOS/RHEL
sudo yum install python3-devel python3-pip opencv-devel

# Arch Linux
sudo pacman -S python python-pip opencv
```

#### Camera Setup
```bash
# Check camera devices
ls /dev/video*

# Install v4l-utils for camera management
sudo apt install v4l-utils
```

## 🐳 Docker Installation

### Using Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'
services:
  ai-vision-pro:
    build: .
    ports:
      - "3000:3000"
    devices:
      - /dev/video0:/dev/video0  # Linux camera access
    volumes:
      - ./uploads:/app/uploads
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
```

```bash
# Run with Docker Compose
docker-compose up -d
```

### Manual Docker Build

```bash
# Build image
docker build -t ai-vision-pro .

# Run container
docker run -p 3000:3000 --device=/dev/video0 ai-vision-pro
```

## ☁️ Cloud Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: python web_app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### AWS EC2 Deployment

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip git

# Clone and setup
git clone https://github.com/your-username/ai-vision-pro.git
cd ai-vision-pro
pip3 install -r requirements.txt

# Run with screen
screen -S ai-vision
python3 web_app.py
```

## 🔍 Troubleshooting

### Common Installation Issues

#### Issue: "No module named cv2"
```bash
# Solution
pip uninstall opencv-python
pip install opencv-python-headless
```

#### Issue: "YOLO model download fails"
```bash
# Manual download
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11n.pt
# Place in project root directory
```

#### Issue: "Permission denied" on camera
```bash
# Linux: Add user to video group
sudo usermod -a -G video $USER
# Logout and login again
```

#### Issue: "Port already in use"
```bash
# Find process using port
lsof -i :3000
# Kill process
kill -9 <PID>
# Or change port in web_app.py
```

### Performance Optimization

#### GPU Acceleration (Optional)
```bash
# Install CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### Memory Optimization
```python
# In web_app.py, adjust these settings:
DETECTION_HISTORY_LIMIT = 25  # Reduce from 50
FRAME_SKIP_RATE = 6  # Increase from 4
```

## 🧪 Development Setup

### IDE Configuration

#### VS Code Setup
```json
// .vscode/settings.json
{
    "python.defaultInterpreter": "./ai-vision-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

#### PyCharm Setup
1. **File > Settings > Project > Python Interpreter**
2. Select virtual environment: `ai-vision-env/bin/python`

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📊 Verification Tests

### System Test Script
```python
# test_installation.py
import sys
import cv2
import ultralytics
import flask
import flask_socketio

def test_installation():
    print("Testing AI Vision Pro Installation...")
    
    # Test Python version
    assert sys.version_info >= (3, 8), "Python 3.8+ required"
    print("✅ Python version OK")
    
    # Test camera access
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Camera not accessible"
    cap.release()
    print("✅ Camera access OK")
    
    # Test YOLO model
    from ultralytics import YOLO
    model = YOLO('yolo11n.pt')
    print("✅ YOLO model loaded")
    
    print("🎉 Installation verified successfully!")

if __name__ == "__main__":
    test_installation()
```

```bash
# Run verification
python test_installation.py
```

## 🔄 Updates and Maintenance

### Updating AI Vision Pro
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
```

### Backup Configuration
```bash
# Backup database
cp photobooth_detections.db backup_$(date +%Y%m%d).db

# Backup uploads
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

## 📞 Getting Help

If you encounter issues during installation:

1. **Check System Requirements**: Ensure your system meets minimum requirements
2. **Review Error Messages**: Most errors provide helpful information
3. **Search Issues**: Check [GitHub Issues](https://github.com/your-username/ai-vision-pro/issues)
4. **Create New Issue**: Provide system info and error logs
5. **Community Support**: Join our [Discord](https://discord.gg/ai-vision-pro)

### System Information Script
```bash
# Generate system info for support
python -c "
import platform, sys, cv2, ultralytics
print(f'OS: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'OpenCV: {cv2.__version__}')
print(f'Ultralytics: {ultralytics.__version__}')
"
```

---

**Next Steps**: After successful installation, check out the [Usage Guide](USAGE.md) to start detecting objects!