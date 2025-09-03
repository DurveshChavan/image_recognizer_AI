# 🚀 YOLOv10 Object Detection Web App

A modern full-stack web application for AI-powered object detection using YOLOv10, featuring a beautiful React frontend and Flask backend.

## ✨ Features

- **YOLOv10 Object Detection** - State-of-the-art AI model for real-time object detection
- **Modern React Frontend** - Beautiful glassmorphism UI with drag & drop upload
- **Multiple Image Formats** - Supports JPG, PNG, GIF, BMP, TIFF
- **Real-time Processing** - Live status updates and progress indicators
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Performance Analytics** - Detailed processing metrics and statistics

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **React Dropzone** - Drag & drop file uploads

### Backend
- **Vercel Serverless Functions** - Node.js API endpoints
- **Formidable.js** - File upload handling
- **Mock YOLO Detection** - Demo object detection (replaceable with real ML service)

### Local Development
- **Flask** - Python web framework (for local development only)
- **YOLOv10** - Latest YOLO model for object detection
- **OpenCV** - Image processing and visualization
- **Ultralytics** - YOLO model management

## 🚀 Quick Start

### Option 1: Vercel Deployment (Recommended)
For production deployment on Vercel:

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy to Vercel**
```bash
# Windows
deploy-vercel.bat

# PowerShell
./deploy-vercel.ps1

# Or manually:
vercel --prod
```

3. **Your app will be available at**: `https://your-domain.vercel.app`

### Option 2: Local Development
For local development and testing:

#### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DurveshChavan/image_recognizer_AI.git
cd image_recognizer_AI
```

2. **Set up Python environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

3. **Set up React frontend**
```bash
# Automatic setup (recommended)
python setup_react.py

# Or manual setup:
cd web
npm install
npm run build
cd ..
```

4. **Start the application**
```bash
python start.py
```

The application will be available at: **http://localhost:5000**

## 📁 Project Structure

```
cv/
├── web/                          # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── App.js                # Main app component
│   │   └── index.js              # React entry point
│   ├── public/                   # Static assets
│   ├── build/                    # Production build
│   └── app.py                    # Flask backend
├── YOLOv10/                      # YOLO model files
│   ├── config.yaml               # Model configuration
│   ├── yolov10_service.py        # YOLO service
│   └── cvat_integration.py       # CVAT integration
├── uploads/                      # Uploaded images
├── yolov10n.pt                   # YOLOv10 model file
├── requirements.txt              # Python dependencies
├── start.py                      # Main startup script
└── setup_react.py                # React setup script
```

## 🎯 Usage

1. **Upload Image** - Drag & drop or click to upload an image
2. **Processing** - Watch real-time processing status
3. **View Results** - See detected objects with confidence scores
4. **Toggle Views** - Switch between original and annotated images
5. **Analyze Stats** - Review performance metrics

## 🚀 Deployment

### Vercel Deployment (Production)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

For detailed deployment instructions, see [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)

### Local Development

#### Frontend Development
```bash
cd web
npm start
```
This starts the React development server on http://localhost:3000

#### Backend Development
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run Flask app directly
cd web
python app.py
```

### Building for Production
```bash
cd web
npm run build
```

## 🎨 Customization

### Styling
- Modify `web/tailwind.config.js` for theme changes
- Update `web/src/index.css` for global styles

### Model Configuration
- Adjust settings in `YOLOv10/config.yaml`
- Change confidence thresholds and device settings

## 🔍 Troubleshooting

### Common Issues

**React build not found:**
```bash
cd web
npm install
npm run build
```

**YOLO model missing:**
```bash
python start.py  # Will auto-download if missing
```

**Node.js not found:**
Download and install from https://nodejs.org/

**Python dependencies missing:**
```bash
pip install -r requirements.txt
```

## 📊 Performance

- **Processing Speed**: ~1-2 seconds per image (CPU)
- **Model Size**: YOLOv10 Nano (~6MB)
- **Supported Objects**: 80+ COCO classes
- **Accuracy**: High precision with configurable confidence thresholds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv10 implementation
- **React Team** - Frontend framework
- **Tailwind CSS** - Styling framework
- **Flask** - Backend framework

---

**Made with ❤️ using YOLOv10 and React**
