cmake_minimum_required(VERSION 3.12)

project(markov CXX)

# use cmake_args from conda env to use the env's compiler toolchain
set(CMAKE_ARGS "${CMAKE_ARGS}")

set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)

# message(STATUS "CXX_COMPILER = ${CMAKE_CXX_COMPILER}")

INCLUDE_DIRECTORIES("src")

add_subdirectory("src/stat_tool")
add_subdirectory("src/sequence_analysis")

# add_library(markov SHARED "src/markov.h")
# set_target_properties(markov PROPERTIES LINKER_LANGUAGE CXX)
# target_link_libraries(markov stat_tool sequence_analysis)
