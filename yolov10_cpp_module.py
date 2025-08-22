"""
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
