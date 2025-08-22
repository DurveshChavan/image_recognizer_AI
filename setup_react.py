#!/usr/bin/env python3
"""
Setup script for React Frontend
This script installs React dependencies and builds the frontend.
"""

import os
import sys
import subprocess
import platform

def run_command(command, shell=True, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_node_npm():
    """Check if Node.js and npm are installed."""
    print("🔍 Checking Node.js and npm...")
    
    # Check Node.js
    success, stdout, stderr = run_command("node --version")
    if not success:
        print("❌ Node.js is not installed. Please install Node.js from https://nodejs.org/")
        print("   Download the LTS version for Windows.")
        return False
    
    node_version = stdout.strip()
    print(f"✅ Node.js: {node_version}")
    
    # Check npm
    success, stdout, stderr = run_command("npm --version")
    if not success:
        print("❌ npm is not installed. Please install npm.")
        return False
    
    npm_version = stdout.strip()
    print(f"✅ npm: {npm_version}")
    
    return True

def install_react_dependencies():
    """Install React dependencies."""
    print("\n📦 Installing React dependencies...")
    
    web_dir = os.path.join(os.getcwd(), 'web')
    
    # Check if package.json exists
    if not os.path.exists(os.path.join(web_dir, 'package.json')):
        print("❌ package.json not found in web directory")
        return False
    
    # Install dependencies
    print("Installing npm packages (this may take a few minutes)...")
    success, stdout, stderr = run_command("npm install", cwd=web_dir)
    
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        print("Try running manually: cd web && npm install")
        return False
    
    print("✅ React dependencies installed successfully!")
    return True

def build_react_app():
    """Build the React app for production."""
    print("\n🔨 Building React app...")
    
    web_dir = os.path.join(os.getcwd(), 'web')
    
    # Build the app
    print("Building React app for production...")
    success, stdout, stderr = run_command("npm run build", cwd=web_dir)
    
    if not success:
        print(f"❌ Failed to build React app: {stderr}")
        print("Try running manually: cd web && npm run build")
        return False
    
    print("✅ React app built successfully!")
    return True

def verify_setup():
    """Verify that the setup was successful."""
    print("\n🔍 Verifying setup...")
    
    web_dir = os.path.join(os.getcwd(), 'web')
    
    # Check for node_modules
    if not os.path.exists(os.path.join(web_dir, 'node_modules')):
        print("❌ node_modules not found")
        return False
    
    # Check for build directory
    if not os.path.exists(os.path.join(web_dir, 'build')):
        print("❌ build directory not found")
        return False
    
    # Check for build files
    build_files = ['index.html', 'static/js', 'static/css']
    for file in build_files:
        if not os.path.exists(os.path.join(web_dir, 'build', file)):
            print(f"❌ {file} not found in build directory")
            return False
    
    print("✅ Setup verification successful!")
    return True

def main():
    """Main setup function."""
    print("🚀 YOLOv10 React Frontend Setup")
    print("=" * 50)
    
    # Check Node.js and npm
    if not check_node_npm():
        print("\n❌ Please install Node.js and npm first.")
        print("Download from: https://nodejs.org/")
        sys.exit(1)
    
    # Install React dependencies
    if not install_react_dependencies():
        print("\n❌ Failed to install React dependencies.")
        sys.exit(1)
    
    # Build React app
    if not build_react_app():
        print("\n❌ Failed to build React app.")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("\n❌ Setup verification failed.")
        sys.exit(1)
    
    print("\n🎉 React frontend setup completed successfully!")
    print("=" * 50)
    print("The React app has been built and is ready to be served by Flask.")
    print("\nTo start the application:")
    print("  python start.py")
    print("\nThe application will be available at: http://localhost:5000")
    print("\nFor development (optional):")
    print("  cd web")
    print("  npm start")
    print("\nThis will start the React development server on http://localhost:3000")

if __name__ == "__main__":
    main()
