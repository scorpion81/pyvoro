cmake_minimum_required(VERSION 3.18)
project(pyvoro LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

option(CYTHONIZE "Run Cython" OFF)

# --------------------------------------------------
# Cython
# --------------------------------------------------
if(CYTHONIZE)
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp
        COMMAND ${Python3_EXECUTABLE} -m cython
                ${CMAKE_CURRENT_SOURCE_DIR}/pyvoro/voroplusplus.pyx
                --cplus
                -o ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp
        DEPENDS pyvoro/voroplusplus.pyx
        VERBATIM
    )

    set(SRC ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp)
else()
    set(SRC pyvoro/voroplusplus.cpp)
endif()

# --------------------------------------------------
# Python module
# --------------------------------------------------
add_library(voroplusplus MODULE
    ${SRC}
    pyvoro/vpp.cpp
    src/voro++.cc
)

target_include_directories(voroplusplus PRIVATE
    src
    pyvoro
)

target_link_libraries(voroplusplus PRIVATE Python3::Module)

if(WIN32)
    target_compile_definitions(voroplusplus PRIVATE NOMINMAX)
endif()

# --------------------------------------------------
# CRITICAL FIX: correct Python extension suffix (ALWAYS WORKS)
# --------------------------------------------------
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c
        "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))"
    OUTPUT_VARIABLE PY_EXT_SUFFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "Python EXT_SUFFIX = ${PY_EXT_SUFFIX}")

set_target_properties(voroplusplus PROPERTIES
    PREFIX ""
    OUTPUT_NAME "voroplusplus"
    SUFFIX "${PY_EXT_SUFFIX}"
)

# --------------------------------------------------
# Install into wheel
# --------------------------------------------------
install(TARGETS voroplusplus
    LIBRARY DESTINATION pyvoro
    RUNTIME DESTINATION pyvoro
)