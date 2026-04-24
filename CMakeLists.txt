cmake_minimum_required(VERSION 3.15)
project(python_template LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_hello_cpp
    src/cpp/hello.cpp
    src/cpp/hello_bindings.cpp
)

install(TARGETS _hello_cpp DESTINATION src/hello_world_cpp)
