#!/usr/bin/env python3
"""
React Frontend Setup Script for YOLOv10 Object Detection App

This script sets up the React frontend for both local development and Render deployment.
It handles dependency installation, building, and verification.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🚀 YOLOv10 React Frontend Setup")
    print("=" * 50)
    print()

def check_prerequisites():
    """Check if Node.js and npm are available."""
    print("🔍 Checking prerequisites...")
    
    try:
        # Check Node.js
        node_version = subprocess.check_output(['node', '--version'], 
                                             stderr=subprocess.STDOUT, 
                                             text=True).strip()
        print(f"✅ Node.js: {node_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js not found!")
        print("   Please install Node.js from: https://nodejs.org/")
        print("   Required version: 16.0.0 or higher")
        return False
    
    try:
        # Check npm
        npm_version = subprocess.check_output(['npm', '--version'], 
                                            stderr=subprocess.STDOUT, 
                                            text=True).strip()
        print(f"✅ npm: {npm_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found!")
        print("   Please install npm (usually comes with Node.js)")
        return False
    
    print()
    return True

def install_dependencies():
    """Install React dependencies."""
    print("📦 Installing React dependencies...")
    
    web_dir = Path("web")
    if not web_dir.exists():
        print("❌ 'web' directory not found!")
        print("   Please run this script from the project root directory")
        return False
    
    try:
        # Change to web directory
        os.chdir(web_dir)
        
        # Install dependencies
        print("   Installing packages (this may take a few minutes)...")
        result = subprocess.run(['npm', 'install'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        print("✅ Dependencies installed successfully!")
        print()
        
        # Go back to root
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def build_react_app():
    """Build React app for production."""
    print("🔨 Building React app for production...")
    
    try:
        # Change to web directory
        os.chdir("web")
        
        # Build the app
        print("   Building production bundle...")
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        print("✅ React app built successfully!")
        print()
        
        # Go back to root
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build React app: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_build():
    """Verify that the build was created successfully."""
    print("🔍 Verifying build...")
    
    build_dir = Path("web/build")
    required_files = [
        "index.html",
        "static/js/main.js",
        "static/css/main.css"
    ]
    
    if not build_dir.exists():
        print("❌ Build directory not found!")
        return False
    
    missing_files = []
    for file_path in required_files:
        if not (build_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing build files: {', '.join(missing_files)}")
        return False
    
    print("✅ Build verification successful!")
    print(f"   Build directory: {build_dir.absolute()}")
    print()
    return True

def cleanup_old_builds():
    """Clean up old build files if they exist."""
    print("🧹 Cleaning up old builds...")
    
    build_dir = Path("web/build")
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
            print("✅ Old build files cleaned up")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean old build: {e}")
    else:
        print("   No old build files found")
    
    print()

def print_success():
    """Print success message."""
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print()
    print("🚀 Your React frontend is ready!")
    print()
    print("📱 Next steps:")
    print("   1. Run 'python start.py' to start your app")
    print("   2. Open http://localhost:5000 in your browser")
    print("   3. Upload an image to test YOLOv10 detection")
    print()
    print("🌐 For Render deployment:")
    print("   - Your app will auto-deploy when you push to GitHub")
    print("   - No additional setup needed!")
    print()
    print("💡 Tips:")
    print("   - For development: cd web && npm start")
    print("   - For production: cd web && npm run build")
    print("   - Build files are automatically included in deployment")

def print_failure():
    """Print failure message."""
    print("❌ Setup failed!")
    print("=" * 50)
    print()
    print("🔧 Troubleshooting:")
    print("   1. Make sure you're in the project root directory")
    print("   2. Ensure Node.js 16+ is installed")
    print("   3. Check your internet connection")
    print("   4. Try running 'npm cache clean --force' in the web directory")
    print()
    print("📞 If problems persist:")
    print("   - Check the error messages above")
    print("   - Ensure all prerequisites are met")
    print("   - Try running the setup again")

def main():
    """Main setup function."""
    print_header()
    
    # Check prerequisites
    if not check_prerequisites():
        print_failure()
        return False
    
    # Clean up old builds
    cleanup_old_builds()
    
    # Install dependencies
    if not install_dependencies():
        print_failure()
        return False
    
    # Build React app
    if not build_react_app():
        print_failure()
        return False
    
    # Verify build
    if not verify_build():
        print_failure()
        return False
    
    # Success!
    print_success()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
