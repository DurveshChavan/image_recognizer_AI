/**
 * YOLOv8 Object Detection Web Application
 * Main JavaScript file for handling UI interactions and API calls
 */

class ObjectDetectionApp {
    constructor() {
        // DOM elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.loading = document.getElementById('loading');
        this.resultsContent = document.getElementById('resultsContent');
        
        // Initialize the application
        this.setupEventListeners();
        this.performHealthCheck();
    }

    /**
     * Set up all event listeners for the application
     */
    setupEventListeners() {
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // Drag and drop events
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // Upload button
        this.uploadBtn.addEventListener('click', () => {
            this.processImage();
        });
    }

    /**
     * Handle file selection
     * @param {File} file - The selected file
     */
    handleFileSelect(file) {
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            this.showError('Please select a valid image file.');
            return;
        }

        // Update UI
        this.uploadBtn.disabled = false;
        this.uploadBtn.innerHTML = '<i class="fas fa-magic"></i> Detect Objects';
        
        // Show preview
        this.showImagePreview(file);
    }

    /**
     * Show image preview before processing
     * @param {File} file - The image file to preview
     */
    showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.resultsContent.innerHTML = `
                <div class="image-container">
                    <img src="${e.target.result}" alt="Preview" class="image-display">
                </div>
                <div class="upload-hint">
                    Click "Detect Objects" to analyze this image
                </div>
            `;
        };
        reader.readAsDataURL(file);
    }

    /**
     * Process the uploaded image with YOLOv8
     */
    async processImage() {
        const file = this.fileInput.files[0];
        if (!file) return;

        // Show loading state
        this.showLoading(true);

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error || 'Processing failed');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display detection results
     * @param {Object} result - The API response with detection results
     */
    showResults(result) {
        const detections = result.detections;
        const summary = result.summary;

        let detectionsHtml = '';
        if (detections.length > 0) {
            detectionsHtml = `
                <div class="detections-list">
                    <h4><i class="fas fa-list"></i> Detected Objects (${detections.length})</h4>
                    ${detections.map(detection => `
                        <div class="detection-item">
                            <span class="detection-label">${detection.label}</span>
                            <span class="detection-confidence">${(detection.confidence * 100).toFixed(1)}%</span>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            detectionsHtml = `
                <div class="success-message">
                    <i class="fas fa-info-circle"></i>
                    No objects detected in this image. Try a different image or lower the confidence threshold.
                </div>
            `;
        }

        this.resultsContent.innerHTML = `
            <div class="tabs">
                <button class="tab active" onclick="app.switchTab('original')">Original</button>
                <button class="tab" onclick="app.switchTab('annotated')">Annotated</button>
            </div>
            
            <div class="tab-content active" id="original">
                <div class="image-container">
                    <img src="data:image/jpeg;base64,${result.original_image}" alt="Original" class="image-display">
                </div>
            </div>
            
            <div class="tab-content" id="annotated">
                <div class="image-container">
                    <img src="data:image/jpeg;base64,${result.annotated_image}" alt="Annotated" class="image-display">
                </div>
            </div>

            <div class="summary-stats">
                <div class="stat-card">
                    <div class="stat-number">${summary.total_objects}</div>
                    <div class="stat-label">Objects Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${summary.image_size}</div>
                    <div class="stat-label">Image Size</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${summary.processing_time}</div>
                    <div class="stat-label">Processing Time</div>
                </div>
            </div>

            ${detectionsHtml}
        `;
    }

    /**
     * Switch between original and annotated image tabs
     * @param {string} tabName - The tab to switch to
     */
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');
    }

    /**
     * Show or hide loading state
     * @param {boolean} show - Whether to show or hide loading
     */
    showLoading(show) {
        if (show) {
            this.loading.style.display = 'block';
            this.uploadBtn.disabled = true;
            this.uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        } else {
            this.loading.style.display = 'none';
            this.uploadBtn.disabled = false;
            this.uploadBtn.innerHTML = '<i class="fas fa-magic"></i> Detect Objects';
        }
    }

    /**
     * Display error message
     * @param {string} message - Error message to display
     */
    showError(message) {
        this.resultsContent.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                ${message}
            </div>
        `;
    }

    /**
     * Perform health check on application startup
     */
    async performHealthCheck() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (!data.yolo_initialized) {
                this.showError('YOLO model is not initialized. Please check the backend.');
            }
        } catch (error) {
            console.error('Health check failed:', error);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ObjectDetectionApp();
});
