#!/usr/bin/env python3
"""
Simple setup script for YOLOv10 C++ Enhancement Module
"""

from setuptools import setup, Extension
import pybind11
import os

# Get the directory containing this file
cpp_dir = os.path.dirname(os.path.abspath(__file__))

# Define the extension module
ext_modules = [
    Extension(
        "yolov10_cpp_module",
        [
            os.path.join(cpp_dir, "src", "python_bindings.cpp"),
            os.path.join(cpp_dir, "src", "image_processor.cpp"),
        ],
        include_dirs=[
            os.path.join(cpp_dir, "include"),
            pybind11.get_include(),
        ],
        language='c++',
        extra_compile_args=[
            '-std=c++17',
            '-O3',
            '-DNDEBUG',
            '-Wall',
            '-Wextra',
            '-D_GNU_SOURCE',
            '-fpermissive'
        ],
    ),
]

setup(
    name="yolov10_cpp_module",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.8",
)
