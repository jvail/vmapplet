cmake_minimum_required(VERSION 3.12)

project(structure_analysis CXX)

# use cmake_args from conda env to use the env's compiler toolchain
set(CMAKE_ARGS "${CMAKE_ARGS}")

set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

INCLUDE_DIRECTORIES("src")

add_subdirectory("src/stat_tool")
add_subdirectory("src/sequence_analysis")
