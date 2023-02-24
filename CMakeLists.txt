cmake_minimum_required(VERSION 3.12)

project(structure_analysis CXX)

# use cmake_args from conda env to use the env's compiler toolchain
set(CMAKE_ARGS "${CMAKE_ARGS}")
set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)

INCLUDE_DIRECTORIES("vmapplet/tools/structure_analysis/src")

add_subdirectory("vmapplet/tools/structure_analysis/src/stat_tool")
add_subdirectory("vmapplet/tools/structure_analysis/src/sequence_analysis")

install(TARGETS sequence_analysis stat_tool)
