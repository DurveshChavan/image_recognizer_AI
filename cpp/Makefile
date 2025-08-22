# YOLOv10 C++ Enhancement Makefile
# Uses MSYS2/MinGW for Windows

# Compiler settings
CC = C:/msys64/ucrt64/bin/gcc.exe
CXX = C:/msys64/ucrt64/bin/g++.exe
MAKE = C:/msys64/ucrt64/bin/mingw32-make.exe

# Compiler flags
CXXFLAGS = -std=c++17 -O3 -DNDEBUG -march=native -fPIC -Wall -Wextra -D_GNU_SOURCE -fpermissive
CFLAGS = -O3 -DNDEBUG -march=native -fPIC -Wall -Wextra -D_GNU_SOURCE

# Python settings
PYTHON_INCLUDE = C:/Users/durve/AppData/Local/Programs/Python/Python312/include
PYTHON_LIB = C:/Users/durve/AppData/Local/Programs/Python/Python312/libs
PYTHON_LIBRARY = python312.lib

# Get Python version for library name
PYTHON_VERSION = 312

# pybind11 settings
PYBIND11_INCLUDE = $(shell python -c "import pybind11; print(pybind11.get_include())")

# Check if OpenCV is available
OPENCV_AVAILABLE = $(shell python -c "import cv2; print('yes')" 2>/dev/null || echo "no")

# Directories
SRC_DIR = src
INCLUDE_DIR = include
BUILD_DIR = build
LIB_DIR = lib

# Source files
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

# Target library
TARGET_LIB = $(LIB_DIR)/libyolov10_cpp.a
TARGET_MODULE = yolov10_cpp_module.so

# Default target
all: $(TARGET_LIB) $(TARGET_MODULE)

# Create build directories
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(LIB_DIR):
	mkdir -p $(LIB_DIR)

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) -I$(PYTHON_INCLUDE) -I$(PYBIND11_INCLUDE) -c $< -o $@

# Build static library
$(TARGET_LIB): $(OBJECTS) | $(LIB_DIR)
	ar rcs $@ $^

# Build Python module with proper Python library linking
$(TARGET_MODULE): $(SRC_DIR)/python_bindings.cpp $(SRC_DIR)/image_processor.cpp
	$(CXX) $(CXXFLAGS) -shared -I$(INCLUDE_DIR) -I$(PYTHON_INCLUDE) -I$(PYBIND11_INCLUDE) \
		-L$(PYTHON_LIB) -lpython$(PYTHON_VERSION) \
		$(SRC_DIR)/python_bindings.cpp $(SRC_DIR)/image_processor.cpp -o $@

# Install module to project root
install: $(TARGET_MODULE)
	cp $(TARGET_MODULE) ../

# Clean build files
clean:
	rm -rf $(BUILD_DIR) $(LIB_DIR) $(TARGET_MODULE) ../$(TARGET_MODULE)

# Show help
help:
	@echo "Available targets:"
	@echo "  all      - Build library and Python module"
	@echo "  install  - Install Python module to project root"
	@echo "  clean    - Remove build files"
	@echo "  help     - Show this help"
	@echo "Python version: $(PYTHON_VERSION)"
	@echo "Python library: $(PYTHON_LIBRARY)"
	@echo "OpenCV available: $(OPENCV_AVAILABLE)"

.PHONY: all install clean help
