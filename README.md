# 🎯 YOLOv8 Object Detection Web Application


A modern, clean web application for AI-powered object detection using YOLOv8. Upload images and get instant object detection results with bounding boxes and confidence scores.

## ✨ Features

- **🎨 Beautiful UI**: Modern, responsive design with drag-and-drop functionality
- **🤖 AI-Powered**: YOLOv8 object detection with 80+ COCO dataset classes
- **⚡ Real-time**: Fast processing with visual feedback
- **📱 Mobile-friendly**: Works perfectly on all devices
- **🔍 Visual Results**: Original vs annotated image comparison
- **📊 Statistics**: Detailed detection information and confidence scores

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python start.py
```

### 3. Open Your Browser
The application will automatically open at: **http://localhost:5000**

## 📁 Project Structure

```
cv/
├── app.py                   # Flask web application
├── start.py                 # Startup script
├── setup_github.py          # Universal GitHub upload automation script
├── config.yaml             # YOLOv8 configuration
├── yolov8n.pt             # Pre-trained YOLOv8 model
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git ignore rules
├── GITHUB_UPLOAD_GUIDE.md # Universal GitHub upload instructions
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   └── js/
│       └── app.js         # Frontend JavaScript
├── uploads/               # Temporary upload storage
├── cvat_integration.py    # CVAT format conversion
└── yolov8_service.py      # YOLOv8 model service
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **YOLOv8**: Object detection model
- **OpenCV**: Image processing
- **PyTorch**: Deep learning framework

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons

## 🎯 Usage

1. **Upload Image**: Drag & drop or click to browse
2. **Process**: Click "Detect Objects" to analyze
3. **View Results**: See original vs annotated images
4. **Explore**: Check detection list and statistics

## 🔧 Configuration

Edit `config.yaml` to customize detection settings:

```yaml
# Model settings
yolov8_model_path: "yolov8n.pt"
confidence_threshold: 0.5
iou_threshold: 0.45

# Output settings
output_format: "cvat"
```

## 📊 Supported Objects

The application can detect 80+ object classes including:
- **People**: person
- **Vehicles**: car, truck, bus, motorcycle, bicycle
- **Animals**: dog, cat, horse, bird, sheep, cow
- **Objects**: chair, table, laptop, phone, book
- **Food**: pizza, hot dog, apple, banana
- And many more...

## 🚀 Performance

- **YOLOv8n**: ~6ms inference time (CPU)
- **Total processing**: ~1-2 seconds per image
- **Real-time upload**: Instant preview

## 🛡️ Security

- File type validation
- Size limits (16MB max)
- Secure filename handling
- Input sanitization

## 📱 Mobile Experience

- Responsive design
- Touch-friendly interface
- Optimized for mobile networks
- Smooth animations

## 🔄 Development

### Running in Development Mode
```bash
python start.py
```

### Debug Features
- Hot reloading
- Detailed error messages
- Health check endpoint

## 🐛 Troubleshooting

### Common Issues

1. **Model not found**:
   ```bash
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

2. **Import errors**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Port already in use**:
   Change port in `app.py` or kill existing process

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- [OpenCV](https://opencv.org/) for image processing
- [Flask](https://flask.palletsprojects.com/) for web framework

---

**Happy detecting! 🎯**
