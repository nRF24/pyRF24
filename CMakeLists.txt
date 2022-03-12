cmake_minimum_required(VERSION 3.15)

# Set the project name to your project name
project(pyrf24)

if(SKBUILD)
  message(STATUS "This project is being built using scikit-build & pybind11")
endif()

add_subdirectory(pybind11)
add_subdirectory(RF24/utility) # configure the RF24_DRIVER
include(cmake/using_flags.cmake)

################################# RF24 #############################

pybind11_add_module(rf24 src/pyrf24/pyRF24.cpp)
target_include_directories(rf24 PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
target_sources(rf24 PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24.cpp
    ${CMAKE_CURRENT_LIST_DIR}/RF24/nRF24L01.h
    ${CMAKE_CURRENT_LIST_DIR}/RF24/RF24_config.h
    ${RF24_DRIVER_SOURCES}
)
apply_flags(rf24)

################################# RF24NETWORK #############################

pybind11_add_module(rf24_network src/pyrf24/pyRF24Network.cpp)
target_include_directories(rf24_network PUBLIC
    RF24
    RF24Network
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
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

pybind11_add_module(rf24_mesh src/pyrf24/pyRF24Mesh.cpp)
target_include_directories(rf24_mesh PUBLIC
    RF24
    RF24Network
    RF24Mesh
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
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
