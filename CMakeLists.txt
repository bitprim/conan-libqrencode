project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()
set(CMAKE_MODULE_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/sources/cmake ${CMAKE_MODULE_PATH} )
add_subdirectory(sources)

