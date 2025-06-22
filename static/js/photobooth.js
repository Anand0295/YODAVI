// Professional Web Application JavaScript
class AIVisionPro {
    constructor() {
        this.socket = io();
        this.isRunning = false;
        this.sessionStartTime = null;
        this.detectionChart = null;
        this.frameCount = 0;
        this.lastFrameTime = Date.now();
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupSocketHandlers();
        this.initializeChart();
    }

    initializeElements() {
        this.elements = {
            startBtn: document.getElementById('start-btn'),
            stopBtn: document.getElementById('stop-btn'),
            captureBtn: document.getElementById('capture-btn'),
            clearBtn: document.getElementById('clear-logs-btn'),
            fileInput: document.getElementById('file-input'),
            uploadArea: document.getElementById('upload-area'),
            videoFeed: document.getElementById('video-feed'),
            placeholder: document.getElementById('placeholder'),
            statusText: document.getElementById('status-text'),
            statusDot: document.querySelector('.status-dot'),
            totalObjects: document.getElementById('total-objects'),
            sessionTime: document.getElementById('session-time'),
            fpsCounter: document.getElementById('fps-counter'),
            recentDetections: document.getElementById('recent-detections'),
            distributionChart: document.getElementById('distribution-chart')
        };
    }

    setupEventListeners() {
        // Control buttons
        this.elements.startBtn.addEventListener('click', () => this.startDetection());
        this.elements.stopBtn.addEventListener('click', () => this.stopDetection());
        this.elements.captureBtn.addEventListener('click', () => this.captureFrame());
        this.elements.clearBtn.addEventListener('click', () => this.clearData());

        // File upload
        this.elements.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        this.elements.uploadArea.addEventListener('click', () => this.elements.fileInput.click());
        
        // Drag and drop
        this.elements.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.elements.uploadArea.style.borderColor = '#4f46e5';
        });
        
        this.elements.uploadArea.addEventListener('dragleave', () => {
            this.elements.uploadArea.style.borderColor = '#d1d5db';
        });
        
        this.elements.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.elements.uploadArea.style.borderColor = '#d1d5db';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.uploadFile(files[0]);
            }
        });

        // Session timer
        setInterval(() => this.updateSessionTime(), 1000);
    }

    setupSocketHandlers() {
        this.socket.on('video_frame', (data) => {
            this.handleVideoFrame(data);
        });

        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.updateStatus('Connected', 'success');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.updateStatus('Disconnected', 'error');
        });
    }

    initializeChart() {
        const ctx = this.elements.distributionChart.getContext('2d');
        this.detectionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                        '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6b7280'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    async startDetection() {
        try {
            this.showLoading(this.elements.startBtn);
            const response = await fetch('/start_webcam', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'started' || data.status === 'already_running') {
                this.isRunning = true;
                this.sessionStartTime = new Date();
                this.updateControlStates();
                this.updateStatus('Detecting...', 'success');
                this.elements.placeholder.style.display = 'none';
                this.elements.videoFeed.style.display = 'block';
            }
        } catch (error) {
            console.error('Error starting detection:', error);
            this.updateStatus('Error starting detection', 'error');
        } finally {
            this.hideLoading(this.elements.startBtn);
        }
    }

    async stopDetection() {
        try {
            this.showLoading(this.elements.stopBtn);
            const response = await fetch('/stop_webcam', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'stopped') {
                this.isRunning = false;
                this.updateControlStates();
                this.updateStatus('Stopped', 'warning');
                this.elements.placeholder.style.display = 'flex';
                this.elements.videoFeed.style.display = 'none';
            }
        } catch (error) {
            console.error('Error stopping detection:', error);
        } finally {
            this.hideLoading(this.elements.stopBtn);
        }
    }

    captureFrame() {
        if (this.isRunning && this.elements.videoFeed.src) {
            // Create download link for current frame
            const link = document.createElement('a');
            link.download = `detection_${new Date().toISOString().slice(0, 19)}.jpg`;
            link.href = this.elements.videoFeed.src;
            link.click();
            
            this.showNotification('Frame captured successfully!', 'success');
        }
    }

    async clearData() {
        if (confirm('Are you sure you want to clear all detection data?')) {
            try {
                this.showLoading(this.elements.clearBtn);
                const response = await fetch('/clear_logs', { method: 'POST' });
                const data = await response.json();
                
                if (data.status === 'cleared') {
                    this.elements.totalObjects.textContent = '0';
                    this.elements.recentDetections.innerHTML = '<p class="text-gray-500">No recent detections</p>';
                    this.updateChart([]);
                    this.showNotification('Data cleared successfully!', 'success');
                }
            } catch (error) {
                console.error('Error clearing data:', error);
            } finally {
                this.hideLoading(this.elements.clearBtn);
            }
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            this.uploadFile(file);
        }
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            this.updateStatus('Processing image...', 'processing');
            const response = await fetch('/upload_file', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.frame) {
                this.elements.videoFeed.src = `data:image/jpeg;base64,${data.frame}`;
                this.elements.videoFeed.style.display = 'block';
                this.elements.placeholder.style.display = 'none';
                
                if (data.detections && data.detections.length > 0) {
                    this.updateRecentDetections(data.detections);
                    this.showNotification(`Found ${data.count} objects in image!`, 'success');
                } else {
                    this.showNotification('No objects detected in image', 'info');
                }
                
                this.updateStatus('Image processed', 'success');
            } else if (data.error) {
                this.showNotification(data.error, 'error');
                this.updateStatus('Error processing image', 'error');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            this.showNotification('Error uploading file', 'error');
            this.updateStatus('Upload failed', 'error');
        }
    }

    handleVideoFrame(data) {
        // Update video feed
        this.elements.videoFeed.src = `data:image/jpeg;base64,${data.frame}`;
        
        // Update FPS counter
        this.frameCount++;
        const now = Date.now();
        if (now - this.lastFrameTime >= 1000) {
            this.elements.fpsCounter.textContent = Math.round(this.frameCount * 1000 / (now - this.lastFrameTime));
            this.frameCount = 0;
            this.lastFrameTime = now;
        }
        
        // Update detections
        if (data.detections && data.detections.length > 0) {
            this.updateRecentDetections(data.detections);
        }
        
        // Update statistics
        if (data.stats) {
            this.updateStatistics(data.stats);
        }
    }

    updateRecentDetections(detections) {
        const container = this.elements.recentDetections;
        container.innerHTML = '';
        
        detections.slice(-5).reverse().forEach(detection => {
            const item = document.createElement('div');
            item.className = 'detection-item';
            item.innerHTML = `
                <span class="detection-class">${detection.class}</span>
                <span class="detection-confidence">${(detection.confidence * 100).toFixed(1)}%</span>
            `;
            container.appendChild(item);
        });
    }

    updateStatistics(stats) {
        if (stats.total_detections !== undefined) {
            this.elements.totalObjects.textContent = stats.total_detections;
        }
        
        if (stats.class_statistics) {
            this.updateChart(stats.class_statistics);
        }
    }

    updateChart(classStats) {
        const labels = Object.keys(classStats);
        const data = Object.values(classStats).map(stat => stat.count);
        
        this.detectionChart.data.labels = labels;
        this.detectionChart.data.datasets[0].data = data;
        this.detectionChart.update();
    }

    updateControlStates() {
        this.elements.startBtn.disabled = this.isRunning;
        this.elements.stopBtn.disabled = !this.isRunning;
        this.elements.captureBtn.disabled = !this.isRunning;
        
        if (this.isRunning) {
            this.elements.startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running';
            this.elements.stopBtn.innerHTML = '<i class="fas fa-stop"></i> Stop';
        } else {
            this.elements.startBtn.innerHTML = '<i class="fas fa-play"></i> Start Detection';
            this.elements.stopBtn.innerHTML = '<i class="fas fa-stop"></i> Stop';
        }
    }

    updateStatus(text, type = 'info') {
        this.elements.statusText.textContent = text;
        
        const dot = this.elements.statusDot;
        dot.className = 'status-dot';
        
        switch (type) {
            case 'success':
                dot.style.background = '#10b981';
                break;
            case 'error':
                dot.style.background = '#ef4444';
                break;
            case 'warning':
                dot.style.background = '#f59e0b';
                break;
            case 'processing':
                dot.style.background = '#6366f1';
                break;
            default:
                dot.style.background = '#6b7280';
        }
    }

    updateSessionTime() {
        if (this.sessionStartTime) {
            const elapsed = new Date() - this.sessionStartTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            
            this.elements.sessionTime.textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    showLoading(button) {
        button.disabled = true;
        const originalContent = button.innerHTML;
        button.innerHTML = '<div class="spinner"></div>';
        button.dataset.originalContent = originalContent;
    }

    hideLoading(button) {
        button.disabled = false;
        button.innerHTML = button.dataset.originalContent || button.innerHTML;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        switch (type) {
            case 'success':
                notification.style.background = '#10b981';
                break;
            case 'error':
                notification.style.background = '#ef4444';
                break;
            case 'warning':
                notification.style.background = '#f59e0b';
                break;
            default:
                notification.style.background = '#6366f1';
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiVisionPro = new AIVisionPro();
});