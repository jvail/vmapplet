set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR})
file(GLOB_RECURSE SRC_FILES "${SRC_DIR}/*.cpp")

add_library(sequence_analysis SHARED ${SRC_FILES})
