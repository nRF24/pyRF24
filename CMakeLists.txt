cmake_minimum_required(VERSION 3.15)

# Set the project name to your project name
project(pyrf24)

if(SKBUILD)
    message(STATUS "This project is being built using scikit-build & pybind11")
endif()

include(cmake/using_flags.cmake)

add_subdirectory(pybind11)
include(RF24/cmake/AutoConfig_RF24_DRIVER.cmake)
add_subdirectory(RF24/utility) # configure the RF24_DRIVER

if(NOT "${RF24_LINKED_DRIVER}" STREQUAL "")
    message(STATUS "Linking to utility driver '${RF24_LINKED_DRIVER}'")
endif()

# suplement our copy of linux/gpio.h into SPIDEV driver sources
set(SUPPLEMENT_LINUX_GPIO_H FALSE)

if("${RF24_DRIVER}" STREQUAL "SPIDEV")
    set(SUPPLEMENT_LINUX_GPIO_H TRUE)
    message(STATUS "Supplementing ${RF24_DRIVER} driver with linux/gpio.h")
    list(APPEND RF24_DRIVER_SOURCES src/linux/gpio.h)
endif()

# ## Build python bindings for RF24 stack into 1 binary
pybind11_add_module(pyrf24
    RF24/RF24.cpp
    ${RF24_DRIVER_SOURCES}
    RF24Network/RF24Network.cpp
    RF24Mesh/RF24Mesh.cpp
    src/pyRF24.cpp
    src/pyRF24Network.cpp
    src/pyRF24Mesh.cpp
    src/glue.cpp
)

# don't let source look for an installed RF24 lib
target_compile_definitions(pyrf24 PUBLIC USE_RF24_LIB_SRC)

if(SUPPLEMENT_LINUX_GPIO_H)
    target_include_directories(pyrf24 PUBLIC src)
endif()

target_include_directories(pyrf24 PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
    RF24Network
    RF24Mesh
)

if(NOT "${RF24_LINKED_DRIVER}" STREQUAL "")
    if("${RF24_DRIVER}" STREQUAL "wiringPi")
        target_link_libraries(pyrf24 PUBLIC rt crypt ${RF24_LINKED_DRIVER})
    else()
        target_link_libraries(pyrf24 PUBLIC ${RF24_LINKED_DRIVER})
    endif()
endif()

apply_flags(pyrf24)

# ############################### INSTALL RULES ####################################
# these are needed since the resulting .so files are copied into
# the binary distribution wheels (.whl files) for python.
install(TARGETS pyrf24 DESTINATION .)

# ## uncomment to show compiler args used in build logs
# set(CMAKE_VERBOSE_MAKEFILE ON)
