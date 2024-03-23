cmake_minimum_required(VERSION 3.15)

# Set the project name to your project name
project(pyrf24)

if(SKBUILD)
  message(STATUS "This project is being built using scikit-build & pybind11")
endif()

set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)

include(cmake/using_flags.cmake)

add_subdirectory(pybind11)
include(RF24/cmake/AutoConfig_RF24_DRIVER.cmake)
add_subdirectory(RF24/utility) # configure the RF24_DRIVER
if(NOT "${RF24_LINKED_DRIVER}" STREQUAL "")
    message(STATUS "Linking to utility driver '${RF24_LINKED_DRIVER}'")
endif()

# suplement our copy of linux/gpio.h into SPIDEV & RPi driver sources
set(SUPPLEMEN_LINUX_GPIO_H FALSE)
if("${RF24_DRIVER}" STREQUAL "RPi" OR "${RF24_DRIVER}" STREQUAL "SPIDEV")
    set(SUPPLEMEN_LINUX_GPIO_H TRUE)
    message(STATUS "Supplementing ${RF24_DRIVER} driver with linux/gpio.h")
    # file(COPY src/linux/gpio.h DESTINATION RF24/utility/${RF24_DRIVER}/linux)
    list(APPEND RF24_DRIVER_SOURCES src/linux/gpio.h)
endif()

################################# RF24 #############################
set(CMAKE_VERBOSE_MAKEFILE ON)
pybind11_add_module(rf24 src/pyRF24.cpp)
target_include_directories(rf24 PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
if(SUPPLEMEN_LINUX_GPIO_H)
    target_include_directories(rf24 PUBLIC src)
endif()
target_sources(rf24 PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24/nRF24L01.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24_config.h
    ${RF24_DRIVER_SOURCES}
)
apply_flags(rf24)

################################# RF24NETWORK #############################

pybind11_add_module(rf24_network src/pyRF24Network.cpp)
target_include_directories(rf24_network PUBLIC
    RF24
    RF24Network
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
if(SUPPLEMEN_LINUX_GPIO_H)
    target_include_directories(rf24_network PUBLIC src)
endif()
# don't let source look for an installed RF24 lib
target_compile_definitions(rf24_network PUBLIC USE_RF24_LIB_SRC)
target_sources(rf24_network PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24/nRF24L01.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24_config.h
    ${RF24_DRIVER_SOURCES}
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network_config.h
)
apply_flags(rf24_network)


################################# RF24MESH #############################

pybind11_add_module(rf24_mesh src/pyRF24Mesh.cpp)
target_include_directories(rf24_mesh PUBLIC
    RF24
    RF24Network
    RF24Mesh
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
if(SUPPLEMEN_LINUX_GPIO_H)
    target_include_directories(rf24_mesh PUBLIC src)
endif()
# don't let source look for an installed RF24 lib
target_compile_definitions(rf24_mesh PUBLIC USE_RF24_LIB_SRC)
target_sources(rf24_mesh PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24/nRF24L01.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24_config.h
    ${RF24_DRIVER_SOURCES}
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24Network/RF24Network_config.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24Mesh/RF24Mesh.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24Mesh/RF24Mesh.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24Mesh/RF24Mesh_config.h
)
apply_flags(rf24_mesh)


################################ INSTALL RULES ####################################
# these are needed for scikit builds since the resulting .so files are copied into
# the binary distribution wheels (.whl files) for python.
install(TARGETS rf24 DESTINATION .)
install(TARGETS rf24_network DESTINATION .)
install(TARGETS rf24_mesh DESTINATION .)
