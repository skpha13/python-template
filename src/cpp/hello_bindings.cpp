#include <pybind11/pybind11.h>

#include "hello.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_hello_cpp, m) {
    m.doc() = "C++ hello world extension";
    m.def("hello_world", &hello_world, "Returns a hello world string from C++");
}
