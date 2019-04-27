cmake_minimum_required (VERSION 3.5)
project (NanoVGTest)

set (CMAKE_CXX_STANDARD 11)

include (${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable (nanovgtest nanovgtest.cpp)
target_compile_definitions(nanovgtest PRIVATE NANOVG_GL2_IMPLEMENTATION)
conan_target_link_libraries (nanovgtest)
