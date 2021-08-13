cmake_minimum_required(VERSION 3.15)

# Set the project name to your project name
project(pyrf24)

add_subdirectory(pybind11)
add_subdirectory(RF24)

# add a global ALIAS for the RF24 lib for direct inclusioin with a larger build-system
add_library(rf24_alias ALIAS rf24)

add_subdirectory(RF24Network)

# add a global ALIAS for the RF24 lib for direct inclusioin with a larger build-system
# add_library(rf24network_alias ALIAS rf24network)

add_subdirectory(RF24Mesh)

pybind11_add_module(core src/pyrf24/pyRF24.cpp)
target_include_directories(core PRIVATE RF24)

pybind11_add_module(rf24_network
    src/pyrf24/pyRF24Network.cpp
)
target_compile_definitions(rf24_network PUBLIC USE_RF24_LIB_SRC)
target_include_directories(rf24_network PRIVATE RF24 RF24Network)

pybind11_add_module(rf24_mesh src/pyrf24/pyRF24Mesh.cpp)
target_compile_definitions(rf24_mesh PUBLIC USE_RF24_LIB_SRC)
target_include_directories(rf24_mesh PRIVATE RF24 RF24Network RF24Mesh)
