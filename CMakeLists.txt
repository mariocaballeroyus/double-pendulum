cmake_minimum_required(VERSION 3.14)
project(double_pendulum LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories (header files)
include_directories(${CMAKE_SOURCE_DIR}/external/eigen)
include_directories(${CMAKE_SOURCE_DIR}/include)

# Gather source files (except bindings)
file(GLOB_RECURSE SOURCES ${CMAKE_SOURCE_DIR}/source/*.cpp)
list(REMOVE_ITEM SOURCES ${CMAKE_SOURCE_DIR}/source/bindings.cpp)

# Add pybind11 as a submodule
add_subdirectory(external/pybind11)

# Add python module and set output directory
pybind11_add_module(doublePendulum source/bindings.cpp ${SOURCES})
set_target_properties(doublePendulum PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/scripts)