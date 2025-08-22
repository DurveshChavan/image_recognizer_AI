#!/usr/bin/env python3
"""
YOLOv10 Web Application Startup Script
Simple and clean startup script for the object detection web app.
"""

import os
import sys
import webbrowser
import time

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        'flask': 'flask',
        'flask-cors': 'flask_cors',
        'werkzeug': 'werkzeug',
        'opencv-python': 'cv2',
        'Pillow': 'PIL',
        'pyyaml': 'yaml',
        'ultralytics': 'ultralytics'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are available!")
    return True

def check_react_setup():
    """Check React frontend setup."""
    print("\n⚛️  Checking React frontend...")
    
    # Check if package.json exists
    package_json_path = 'web/package.json'
    if not os.path.exists(package_json_path):
        print(f"  ❌ {package_json_path} (missing)")
        print("  React frontend not set up. Please run: python setup_react.py")
        return False
    
    # Check if node_modules exists
    node_modules_path = 'web/node_modules'
    if not os.path.exists(node_modules_path):
        print(f"  ⚠️  {node_modules_path} (missing)")
        print("  React dependencies not installed. Please run: python setup_react.py")
        return False
    
    # Check if build exists
    build_path = 'web/build'
    if not os.path.exists(build_path):
        print(f"  ⚠️  {build_path} (missing)")
        print("  React app not built. Please run: python setup_react.py")
        return False
    
    print("  ✅ React frontend ready!")
    return True

def check_files():
    """Check if required files exist."""
    print("\n📁 Checking required files...")
    
    required_files = [
        'web/app.py',
        'YOLOv10/config.yaml'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    # Check for YOLOv10 model
    model_path = 'yolov10n.pt'
    if os.path.exists(model_path):
        print(f"  ✅ {model_path}")
    else:
        print(f"  ❌ {model_path} (missing)")
        missing_files.append(model_path)
    
    # Check for React build (optional - will fallback to development mode)
    react_build_path = 'web/build'
    if os.path.exists(react_build_path):
        print(f"  ✅ {react_build_path} (React build found)")
    else:
        print(f"  ⚠️  {react_build_path} (React build not found - will use development mode)")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        
        # Check if only the model is missing
        if len(missing_files) == 1 and 'yolov10n.pt' in missing_files[0]:
            print("\n📥 Attempting to download YOLOv10 model...")
            if download_model():
                print("✅ Model downloaded successfully!")
                return True
            else:
                print("❌ Failed to download model. Please run: python download_model.py")
                return False
        
        return False
    
    print("✅ All required files are present!")
    return True

def download_model():
    """Download YOLOv10 model if missing."""
    try:
        from ultralytics import YOLO
        
        print("📥 Downloading YOLOv10 nano model...")
        print("This may take a few minutes depending on your internet connection.")
        
        # Download the model
        model = YOLO('yolov10n.pt')
        
        # Save it to the root directory
        model.export(format="torchscript", file="yolov10n.pt")
        
        print("✅ YOLOv10 model downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading YOLOv10 model: {e}")
        return False

def main():
    """Main startup function."""
    print("🚀 YOLOv10 Web Application")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start application due to missing dependencies.")
        return False
    
    # Check files
    if not check_files():
        print("\n❌ Cannot start application due to missing files.")
        return False
    
    # Check React setup (optional but recommended)
    react_ready = check_react_setup()
    if not react_ready:
        print("\n⚠️  React frontend not ready. The app will work with basic functionality.")
        print("💡 For the full experience, run: python setup_react.py")
        print("   Or manually: cd web && npm install && npm run build")
    
    print("\n✅ All checks passed!")
    print("\n🌐 Starting web application...")
    print("📱 The application will be available at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Wait a moment for user to read
    time.sleep(2)
    
    # Try to open browser automatically
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opening browser automatically...")
    except:
        print("📱 Please open your browser and go to: http://localhost:5000")
    
    # Start the Flask application
    try:
        # Add web directory to Python path
        sys.path.insert(0, os.path.join(os.getcwd(), 'web'))
        # Add YOLOv10 directory to Python path
        sys.path.insert(0, os.path.join(os.getcwd(), 'YOLOv10'))
        
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
