cmake_minimum_required(VERSION 3.22)

project(structure_analysis CXX)

INCLUDE_DIRECTORIES("vmapplet/structure_analysis/src")

add_subdirectory("vmapplet/structure_analysis/src/stat_tool")
add_subdirectory("vmapplet/structure_analysis/src/sequence_analysis")

install(TARGETS sequence_analysis stat_tool)
