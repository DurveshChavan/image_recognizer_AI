#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(test_simple, m) {
    m.doc() = "Simple test module";
    
    m.def("hello", []() {
        return "Hello from C++!";
    });
    
    m.def("add", [](int a, int b) {
        return a + b;
    });
}
