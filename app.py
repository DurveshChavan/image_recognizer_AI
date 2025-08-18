#!/usr/bin/env python3
"""
YOLOv8 Object Detection Web Application
A clean, organized Flask web application for AI-powered object detection.
"""

import os
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2

from cvat_integration import CVATIntegration

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
CORS(app)

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global CVAT integration instance
cvat_integration = None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def initialize_yolo():
    """Initialize YOLO model."""
    global cvat_integration
    if cvat_integration is None:
        try:
            cvat_integration = CVATIntegration('config.yaml')
            cvat_integration.initialize_yolo_service()
            print("✅ YOLO model initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing YOLO model: {e}")
            return False
    return True

def encode_image_to_base64(image_path):
    """Encode image to base64 for frontend display."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def draw_detections_on_image(image_path, detections):
    """Draw bounding boxes on image and return base64 encoded result."""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Draw detections
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            label = detection['label']
            confidence = detection['confidence']
            
            # Convert coordinates to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label_text = f"{label}: {confidence:.2f}"
            cv2.putText(image, label_text, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        return img_base64
        
    except Exception as e:
        print(f"Error drawing detections: {e}")
        return None

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process with YOLOv8."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Initialize YOLO if not already done
            if not initialize_yolo():
                return jsonify({'error': 'Failed to initialize YOLO model'}), 500
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process image with YOLOv8
            print(f"Processing image: {filepath}")
            cvat_data = cvat_integration.predict_and_convert(filepath)
            
            # Extract detection results
            annotation = cvat_data['annotations'][0]
            detections = []
            
            for shape in annotation['shapes']:
                points = shape['points']
                if len(points) >= 2:
                    x1, y1 = points[0]
                    x2, y2 = points[1]
                    confidence = shape['attributes'][0]['value']
                    
                    detections.append({
                        'label': shape['label'],
                        'bbox': [x1, y1, x2, y2],
                        'confidence': float(confidence)
                    })
            
            # Draw detections on image
            annotated_image = draw_detections_on_image(filepath, detections)
            
            # Prepare response
            response = {
                'success': True,
                'filename': filename,
                'original_image': encode_image_to_base64(filepath),
                'annotated_image': annotated_image,
                'detections': detections,
                'summary': {
                    'total_objects': len(detections),
                    'image_size': f"{annotation['width']}x{annotation['height']}",
                    'processing_time': '~1-2 seconds'
                }
            }
            
            return jsonify(response)
        
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'yolo_initialized': cvat_integration is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("🚀 Starting YOLOv8 Web Application...")
    print("=" * 50)
    
    # Initialize YOLO model on startup
    if initialize_yolo():
        print("✅ Backend ready!")
        print("🌐 Starting web server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize backend")
