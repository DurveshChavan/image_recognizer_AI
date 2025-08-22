#!/usr/bin/env python3
"""
YOLOv10 C++ Enhancement Build Script
Builds C++ components for enhanced performance with fallback to Python-only mode.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking C++ build dependencies...")
    
    # Map package names to their import names
    package_imports = {
        'pybind11': 'pybind11',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Please install them with: pip install pybind11 numpy")
        return False
    
    print("✅ All C++ build dependencies are installed")
    return True

def install_dependencies():
    """Install missing dependencies."""
    print("\n📦 Installing missing dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pybind11', 'numpy'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def detect_compilers():
    """Detect available C++ compilers."""
    print("\n🔍 Detecting C++ compilers...")
    
    compilers = []
    
    # Check for MSVC (Visual Studio)
    try:
        result = subprocess.run(['cl'], capture_output=True, text=True)
        if result.returncode != 1:  # cl exists but might not be in PATH
            compilers.append(('MSVC', 'cl'))
            print("  ✅ MSVC (Visual Studio) found")
    except:
        pass
    
    # Check for TDM-GCC
    tdm_gcc_paths = [
        'C:/TDM-GCC-32/bin/g++.exe',
        'C:/TDM-GCC-64/bin/g++.exe',
        'C:/TDM-GCC/bin/g++.exe'
    ]
    
    for path in tdm_gcc_paths:
        if os.path.exists(path):
            compilers.append(('TDM-GCC', path))
            print(f"  ✅ TDM-GCC found: {path}")
            break
    
    # Check for MinGW
    mingw_paths = [
        'C:/MinGW/bin/g++.exe',
        'C:/msys64/mingw64/bin/g++.exe',
        'C:/msys64/ucrt64/bin/g++.exe'
    ]
    
    for path in mingw_paths:
        if os.path.exists(path):
            compilers.append(('MinGW', path))
            print(f"  ✅ MinGW found: {path}")
            break
    
    # Check for GCC in PATH
    try:
        result = subprocess.run(['g++', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            compilers.append(('GCC', 'g++'))
            print("  ✅ GCC found in PATH")
    except:
        pass
    
    # Check for Clang
    try:
        result = subprocess.run(['clang++', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            compilers.append(('Clang', 'clang++'))
            print("  ✅ Clang found in PATH")
    except:
        pass
    
    if not compilers:
        print("  ❌ No C++ compilers found")
        print("     Please install one of:")
        print("     • Visual Studio Build Tools")
        print("     • TDM-GCC: https://jmeubank.github.io/tdm-gcc/")
        print("     • MinGW: https://www.mingw-w64.org/")
        print("     • MSYS2: https://www.msys2.org/")
        return None
    
    # Prefer MSYS2/MinGW on Windows (better Python library support)
    for name, path in compilers:
        if 'MinGW' in name or 'msys64' in path:
            print(f"  🎯 Selected: {name} ({path})")
            return name, path
    
    # Fallback to TDM-GCC
    for name, path in compilers:
        if 'TDM-GCC' in name:
            print(f"  🎯 Selected: {name} ({path})")
            return name, path
    
    # Fallback to first available
    name, path = compilers[0]
    print(f"  🎯 Selected: {name} ({path})")
    return name, path

def setup_msvc_environment():
    """Set up MSVC environment if available."""
    print("\n🔧 Setting up MSVC environment...")
    
    # Common Visual Studio paths
    vs_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    ]
    
    for path in vs_paths:
        if os.path.exists(path):
            print(f"  ✅ Found Visual Studio: {path}")
            return path
    
    print("  ❌ Visual Studio not found")
    return None

def build_with_msvc():
    """Build using MSVC."""
    print("\n🔨 Building with MSVC...")
    
    vcvars_path = setup_msvc_environment()
    if not vcvars_path:
        return False
    
    try:
        # Set up environment
        cmd = f'"{vcvars_path}" && cd /d "{os.getcwd()}" && python build_cpp_fixed.py'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MSVC build successful")
            return True
        else:
            print(f"❌ MSVC build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ MSVC build error: {e}")
        return False

def build_with_gcc(compiler_path):
    """Build using GCC-based compiler."""
    print(f"\n🔨 Building with {compiler_path}...")
    
    try:
        # Change to cpp directory and use Makefile
        cpp_dir = Path("cpp")
        if not cpp_dir.exists():
            print("❌ cpp directory not found")
            return False
        
        # Change to cpp directory
        os.chdir(cpp_dir)
        
        # Clean previous build
        print("🧹 Cleaning previous build...")
        subprocess.run(['C:/msys64/ucrt64/bin/mingw32-make.exe', 'clean'], 
                      capture_output=True, text=True)
        
        # Try building with setup.py first
        print("🔨 Trying setup.py build...")
        result = subprocess.run([sys.executable, 'setup_simple.py', 'build_ext', '--inplace'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️  setup.py failed, trying Makefile...")
            # Build using Makefile
            print("🔨 Building with Makefile...")
            result = subprocess.run(['C:/msys64/ucrt64/bin/mingw32-make.exe', 'all'], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ C++ components built successfully")
            
            # Install module to project root
            print("📦 Installing Python module...")
            subprocess.run(['C:/msys64/ucrt64/bin/mingw32-make.exe', 'install'], 
                          capture_output=True, text=True)
            
            # Change back to project root
            os.chdir('..')
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            os.chdir('..')
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build C++ components: {e}")
        os.chdir('..')
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        os.chdir('..')
        return False

def create_fallback_module():
    """Create Python fallback module if C++ build fails."""
    print("\n📝 Creating Python fallback module...")
    
    fallback_code = '''"""
YOLOv10 C++ Enhancement Module - Python Fallback
This module provides Python implementations when C++ compilation fails.
"""

import time
import numpy as np
from typing import Dict, Any, Optional

class ImageProcessor:
    """Python fallback implementation of ImageProcessor."""
    
    def __init__(self):
        self.performance_stats = {
            'total_processed': 0,
            'total_time': 0.0,
            'cpp_available': False,
            'fallback_mode': True
        }
    
    def preprocess_image(self, image_path: str, target_size: tuple = (640, 640)) -> Dict[str, Any]:
        """Preprocess image for YOLO inference (Python fallback)."""
        start_time = time.time()
        
        try:
            import cv2
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Resize image
            resized = cv2.resize(image, target_size)
            
            # Convert to RGB
            rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            
            # Normalize
            normalized = rgb_image.astype(np.float32) / 255.0
            
            # Update stats
            processing_time = time.time() - start_time
            self.performance_stats['total_processed'] += 1
            self.performance_stats['total_time'] += processing_time
            
            return {
                'success': True,
                'image': normalized,
                'original_size': image.shape[:2],
                'target_size': target_size,
                'processing_time': processing_time,
                'cpp_used': False
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'cpp_used': False
            }
    
    def get_image_statistics(self, image_path: str) -> Dict[str, Any]:
        """Get image statistics (Python fallback)."""
        try:
            import cv2
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not load image'}
            
            stats = {
                'width': image.shape[1],
                'height': image.shape[0],
                'channels': image.shape[2] if len(image.shape) > 2 else 1,
                'dtype': str(image.dtype),
                'mean': np.mean(image),
                'std': np.std(image),
                'min': np.min(image),
                'max': np.max(image)
            }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}

# Module-level functions
def get_version():
    """Get module version."""
    return "YOLOv10 C++ Enhancement Module v1.0.0 (Python Fallback)"

def test_compilation():
    """Test if module is working."""
    print("Python fallback module is working!")
    return True

def create_test_image(rows: int, cols: int):
    """Create a test image."""
    return np.random.rand(rows, cols).astype(np.float32)

def print_matrix_info(matrix):
    """Print matrix information."""
    print(f"Matrix: {matrix.shape}")
    print(f"Type: {matrix.dtype}")
    print(f"Min: {np.min(matrix)}")
    print(f"Max: {np.max(matrix)}")
    print(f"Mean: {np.mean(matrix)}")

# Create fallback classes for OpenCV types
class Size:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
    
    def get_width(self): return self.width
    def get_height(self): return self.height
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Scalar:
    def __init__(self, v0: float = 0.0, v1: float = 0.0, v2: float = 0.0, v3: float = 0.0):
        self.val = [v0, v1, v2, v3]
    
    def get_val(self, i: int): return self.val[i] if 0 <= i < 4 else 0.0
    def set_val(self, i: int, v: float):
        if 0 <= i < 4:
            self.val[i] = v

class Mat:
    def __init__(self, rows: int = 0, cols: int = 0):
        self.rows = rows
        self.cols = cols
        self.data = np.zeros((rows, cols), dtype=np.float32) if rows > 0 and cols > 0 else None
    
    def get_rows(self): return self.rows
    def get_cols(self): return self.cols
    
    def at(self, i: int, j: int):
        if self.data is not None and 0 <= i < self.rows and 0 <= j < self.cols:
            return self.data[i, j]
        return 0.0
    
    def set_at(self, i: int, j: int, value: float):
        if self.data is not None and 0 <= i < self.rows and 0 <= j < self.cols:
            self.data[i, j] = value
'''
    
    try:
        with open('yolov10_cpp_module.py', 'w', encoding='utf-8') as f:
            f.write(fallback_code)
        
        print("✅ Python fallback module created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create fallback module: {e}")
        return False

def verify_build():
    """Verify that the build was successful."""
    print("\n🔍 Verifying build...")
    
    # Check for C++ module
    if os.path.exists('yolov10_cpp_module.so'):
        print("  ✅ C++ module (.so) found")
        return True
    elif os.path.exists('yolov10_cpp_module.pyd'):
        print("  ✅ C++ module (.pyd) found")
        return True
    elif os.path.exists('yolov10_cpp_module.py'):
        print("  ✅ Python fallback module found")
        return True
    else:
        print("  ❌ No module found")
        return False

def test_module():
    """Test the built module."""
    print("\n🧪 Testing module...")
    
    try:
        import yolov10_cpp_module
        
        # Test basic functionality
        processor = yolov10_cpp_module.ImageProcessor()
        print("  ✅ ImageProcessor created successfully")
        
        # Test version
        version = yolov10_cpp_module.get_version()
        print(f"  ✅ Version: {version}")
        
        # Test compilation
        result = yolov10_cpp_module.test_compilation()
        print(f"  ✅ Compilation test: {result}")
        
        print("✅ Module test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Module test failed: {e}")
        return False

def main():
    """Main build function."""
    print("🚀 YOLOv10 C++ Enhancement Build")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return False
    
    # Detect compilers
    compiler_info = detect_compilers()
    if not compiler_info:
        print("\n⚠️  No C++ compilers found. Creating Python fallback...")
        if create_fallback_module():
            print("✅ Python fallback created successfully")
            if verify_build() and test_module():
                print("🎉 Build completed with Python fallback!")
                return True
        return False
    
    compiler_name, compiler_path = compiler_info
    
    # Build based on compiler
    build_success = False
    
    if 'MSVC' in compiler_name:
        build_success = build_with_msvc()
    else:
        build_success = build_with_gcc(compiler_path)
    
    # If C++ build failed, create fallback
    if not build_success:
        print("\n⚠️  C++ build failed. Creating Python fallback...")
        if create_fallback_module():
            print("✅ Python fallback created successfully")
        else:
            print("❌ Failed to create Python fallback")
            return False
    
    # Verify and test
    if verify_build() and test_module():
        print("\n🎉 Build completed successfully!")
        
        # Show final status
        if os.path.exists('yolov10_cpp_module.so') or os.path.exists('yolov10_cpp_module.pyd'):
            print("✅ C++ enhancements are available!")
        else:
            print("✅ Python fallback is working!")
        
        return True
    else:
        print("❌ Build verification failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
