#!/usr/bin/env python3
"""
Setup script for YOLOv10 C++ Enhancement Module
Uses pybind11's build system for proper Python library linking
"""

from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11
import os
import sys

# Get the directory containing this file
cpp_dir = os.path.dirname(os.path.abspath(__file__))

# Set compiler to MSYS2/MinGW
os.environ['CC'] = 'C:/msys64/ucrt64/bin/gcc.exe'
os.environ['CXX'] = 'C:/msys64/ucrt64/bin/g++.exe'

# Define the extension module
ext_modules = [
    Pybind11Extension(
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
        cxx_std=17,
        extra_compile_args=[
            '-O3', '-DNDEBUG', '-march=native', '-Wall', '-Wextra',
            '-D_GNU_SOURCE', '-fpermissive'
        ],
    ),
]

setup(
    name="yolov10_cpp_module",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
)
