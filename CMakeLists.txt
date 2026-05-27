cmake_minimum_required(VERSION 3.18)

project(pyvoro LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

option(CYTHONIZE "Run Cython" OFF)

if(CYTHONIZE)

    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp

        COMMAND ${Python3_EXECUTABLE} -m cython
                ${CMAKE_CURRENT_SOURCE_DIR}/pyvoro/voroplusplus.pyx
                --cplus
                -o ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp

        DEPENDS pyvoro/voroplusplus.pyx
    )

    set(VORO_SOURCE
        ${CMAKE_CURRENT_BINARY_DIR}/voroplusplus.cpp
    )

else()

    set(VORO_SOURCE
        pyvoro/voroplusplus.cpp
    )

endif()

add_library(voroplusplus MODULE
    ${VORO_SOURCE}
    pyvoro/vpp.cpp
    src/voro++.cc
)

# Include directories

target_include_directories(voroplusplus PRIVATE
    src
    pyvoro
    ${Python3_INCLUDE_DIRS}
)

# Windows fixes
if(WIN32)
    target_compile_definitions(voroplusplus PRIVATE NOMINMAX)
endif()

# Python extension naming
set_target_properties(voroplusplus PROPERTIES
    PREFIX ""
    OUTPUT_NAME "voroplusplus"
    SUFFIX "${Python3_EXTENSION_MODULE_SUFFIX}"
)

# Install into wheel
install(TARGETS voroplusplus
        LIBRARY DESTINATION pyvoro
        RUNTIME DESTINATION pyvoro)