#!/usr/bin/env python3
"""
YOLOv8 Web Application Startup Script
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

def check_files():
    """Check if required files exist."""
    print("\n📁 Checking required files...")
    
    required_files = [
        'app.py',
        'templates/index.html',
        'config.yaml',
        'yolov8n.pt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present!")
    return True

def main():
    """Main startup function."""
    print("🚀 YOLOv8 Web Application")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start application due to missing dependencies.")
        return False
    
    # Check files
    if not check_files():
        print("\n❌ Cannot start application due to missing files.")
        return False
    
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
