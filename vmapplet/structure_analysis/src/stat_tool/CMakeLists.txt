set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR})
file(GLOB_RECURSE SRC_FILES "${SRC_DIR}/*.cpp")

add_library(stat_tool STATIC ${SRC_FILES})
