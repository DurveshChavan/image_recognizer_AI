#!/usr/bin/env python3
"""
Python wrapper for YOLOv10 Java Enhancement Module
Provides Python interface to Java image processing classes
"""

import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np

class JavaImageProcessor:
    """Python wrapper for Java ImageProcessor class."""
    
    def __init__(self):
        self.jar_path = Path("yolov10_java_module.jar")
        self.java_class = "yolov10.ImageProcessor"
        self._check_java_setup()
    
    def _check_java_setup(self):
        """Check if Java and JAR file are available."""
        if not self.jar_path.exists():
            raise FileNotFoundError(f"JAR file not found: {self.jar_path}")
        
        # Check Java installation
        try:
            subprocess.run(['java', '-version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("Java not found. Please install Java JDK.")
    
    def _run_java_method(self, method_name: str, *args) -> str:
        """Run a Java method and return the result."""
        cmd = [
            'java',
            '-cp', str(self.jar_path),
            self.java_class,
            method_name
        ] + [str(arg) for arg in args]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Java method execution failed: {e.stderr}")
    
    def get_version(self) -> str:
        """Get module version."""
        return self._run_java_method("getVersion")
    
    def test_compilation(self) -> bool:
        """Test if Java module is working."""
        result = self._run_java_method("testCompilation")
        return "successfully" in result.lower()
    
    def preprocess_image(self, image_path: str, target_width: int, target_height: int, normalize: bool = True) -> np.ndarray:
        """Preprocess an image for YOLO inference."""
        result = self._run_java_method("preprocessImage", image_path, target_width, target_height, normalize)
        
        # Parse result (assuming JSON format)
        try:
            data = json.loads(result)
            return np.array(data)
        except json.JSONDecodeError:
            raise RuntimeError(f"Failed to parse Java result: {result}")
    
    def get_image_statistics(self, image_path: str) -> Dict[str, float]:
        """Get image statistics."""
        result = self._run_java_method("getImageStatistics", image_path)
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise RuntimeError(f"Failed to parse image statistics: {result}")
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics."""
        result = self._run_java_method("getPerformanceStats")
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {}

# Create module-level functions for compatibility
def get_version() -> str:
    """Get module version."""
    processor = JavaImageProcessor()
    return processor.get_version()

def test_compilation() -> bool:
    """Test if Java module is working."""
    processor = JavaImageProcessor()
    return processor.test_compilation()

def create_test_image(rows: int, cols: int) -> np.ndarray:
    """Create a test image matrix."""
    return np.random.rand(rows, cols)

def print_matrix_info(matrix: np.ndarray):
    """Print matrix information."""
    print(f"Matrix: {matrix.shape}")
    if matrix.size > 0:
        print(f"First element: {matrix.flat[0]}")
        print(f"Last element: {matrix.flat[-1]}")

# Export main classes
__all__ = ['JavaImageProcessor', 'get_version', 'test_compilation', 'create_test_image', 'print_matrix_info']
