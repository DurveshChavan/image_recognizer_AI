#include <cstring>
#include <cstdlib>

// Fix for missing strdup on Windows - define before pybind11 includes
#ifdef _WIN32
extern "C" {
    char* strdup(const char* s) {
        size_t len = strlen(s) + 1;
        char* dup = (char*)malloc(len);
        if (dup) {
            memcpy(dup, s, len);
        }
        return dup;
    }
}
#endif

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "image_processor.h"
#include <iostream>

namespace py = pybind11;

PYBIND11_MODULE(yolov10_cpp_module, m) {
    m.doc() = "YOLOv10 C++ Enhancement Module";
    
    // Bind the ImageProcessor class
    py::class_<yolov10_cpp::ImageProcessor>(m, "ImageProcessor")
        .def(py::init<>())
        .def("preprocess_image", &yolov10_cpp::ImageProcessor::preprocess_image,
             "Process an image for YOLO inference")
        .def("get_image_statistics", &yolov10_cpp::ImageProcessor::get_image_statistics,
             "Get image statistics");
    
    // Simple binding for cv::Size without readwrite (to avoid template issues)
    py::class_<cv::Size>(m, "Size")
        .def(py::init<int, int>())
        .def("get_width", [](const cv::Size& self) { return self.width; })
        .def("get_height", [](const cv::Size& self) { return self.height; })
        .def("set_width", [](cv::Size& self, int w) { self.width = w; })
        .def("set_height", [](cv::Size& self, int h) { self.height = h; });
    
    // Simple binding for cv::Scalar without array member
    py::class_<cv::Scalar>(m, "Scalar")
        .def(py::init<double, double, double, double>())
        .def("get_val", [](const cv::Scalar& self, int i) { 
            return (i >= 0 && i < 4) ? self.val[i] : 0.0; 
        })
        .def("set_val", [](cv::Scalar& self, int i, double v) { 
            if (i >= 0 && i < 4) self.val[i] = v; 
        });
    
    // Simple binding for cv::Mat
    py::class_<cv::Mat>(m, "Mat")
        .def(py::init<int, int>())
        .def("get_rows", [](const cv::Mat& self) { return self.rows; })
        .def("get_cols", [](const cv::Mat& self) { return self.cols; })
        .def("at", [](const cv::Mat& self, int i, int j) {
            if (i >= 0 && i < self.rows && j >= 0 && j < self.cols) {
                return self.at(i, j);
            }
            return 0.0f;
        })
        .def("set_at", [](cv::Mat& self, int i, int j, float value) {
            if (i >= 0 && i < self.rows && j >= 0 && j < self.cols) {
                self.at(i, j) = value;
            }
        });
    
    // Utility functions
    m.def("create_test_image", [](int rows, int cols) {
        cv::Mat mat(rows, cols);
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                mat.at(i, j) = (i + j) % 255;
            }
        }
        return mat;
    });
    
    m.def("print_matrix_info", [](const cv::Mat& mat) {
        std::cout << "Matrix: " << mat.rows << "x" << mat.cols << std::endl;
        if (mat.rows > 0 && mat.cols > 0) {
            std::cout << "First element: " << mat.at(0, 0) << std::endl;
            std::cout << "Last element: " << mat.at(mat.rows-1, mat.cols-1) << std::endl;
        }
    });
    
    // Module-level functions
    m.def("get_version", []() {
        return "YOLOv10 C++ Enhancement Module v1.0.0";
    });
    
    m.def("test_compilation", []() {
        std::cout << "C++ module compiled successfully!" << std::endl;
        return true;
    });
}
