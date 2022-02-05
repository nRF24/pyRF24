cmake_minimum_required(VERSION 3.15)

# Set the project name to your project name
project(pyrf24)

if(SKBUILD)
  message(STATUS "This project is being built using scikit-build & pybind11")
endif()

add_subdirectory(pybind11)
add_subdirectory(RF24/utility) # configure the RF24_DRIVER


####################### DEBUG (& EXTRA) FLAGS ######################

option(RF24_DEBUG "enable/disable debugging output for RF24 lib" OFF)
option(SERIAL_DEBUG "enable/disable debugging output for RF24Network lib" OFF)
option(SERIAL_DEBUG_MINIMAL "enable/disable minimal debugging output for RF24Network lib" OFF)
option(SERIAL_DEBUG_ROUTING
    "enable/disable debugging output related to transmission routing for RF24Network lib"
    OFF
)
option(SERIAL_DEBUG_FRAGMENTATION
    "enable/disable debugging output related to message fragmentation for RF24Network lib"
    OFF
)
option(SERIAL_DEBUG_FRAGMENTATION_L2
    "enable/disable debugging output related to fragmented messages' transmission success for RF24Network lib"
    OFF
)
option(DISABLE_FRAGMENTATION "disable message fragmentation for RF24Network lib" OFF)
option(DISABLE_DYNAMIC_PAYLOADS "force usage of static payload size for RF24Network lib" OFF)
option(MESH_NOMASTER "exclude compiling code that is strictly for master nodes for RF24Mesh lib" OFF)
option(MESH_DEBUG "enable/disable debugging output for RF24Mesh lib" OFF)
option(MESH_DEBUG_MINIMAL "enable/disable minimal debugging output for RF24Mesh lib" OFF)


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
if(RF24_DEBUG)
    message(STATUS "RF24_DEBUG asserted")
    target_compile_definitions(rf24 PUBLIC SERIAL_DEBUG)
endif()


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
if(SERIAL_DEBUG)
    message(STATUS "SERIAL_DEBUG asserted")
    target_compile_definitions(rf24_network PUBLIC SERIAL_DEBUG)
endif()
if(SERIAL_DEBUG_MINIMAL)
    message(STATUS "SERIAL_DEBUG_MINIMAL asserted")
    target_compile_definitions(rf24_network PUBLIC SERIAL_DEBUG_MINIMAL)
endif()
if(SERIAL_DEBUG_ROUTING)
    message(STATUS "SERIAL_DEBUG_ROUTING asserted")
    target_compile_definitions(rf24_network PUBLIC SERIAL_DEBUG_ROUTING)
endif()
if(SERIAL_DEBUG_FRAGMENTATION)
    message(STATUS "SERIAL_DEBUG_FRAGMENTATION asserted")
    target_compile_definitions(rf24_network PUBLIC SERIAL_DEBUG_FRAGMENTATION)
endif()
if(SERIAL_DEBUG_FRAGMENTATION_L2)
    message(STATUS "SERIAL_DEBUG_FRAGMENTATION_L2 asserted")
    target_compile_definitions(rf24_network PUBLIC SERIAL_DEBUG_FRAGMENTATION_L2)
endif()
if(DISABLE_FRAGMENTATION)
    message(STATUS "DISABLE_FRAGMENTATION asserted")
    target_compile_definitions(rf24_network PUBLIC DISABLE_FRAGMENTATION)
endif()
# for MAX_PAYLOAD_SIZE, we let the default be configured in source code
if(DEFINED MAX_PAYLOAD_SIZE) # don't use CMake's `option()` for this one
    message(STATUS "MAX_PAYLOAD_SIZE set to ${MAX_PAYLOAD_SIZE}")
    target_compile_definitions(rf24_network PUBLIC MAX_PAYLOAD_SIZE=${MAX_PAYLOAD_SIZE})
endif()
if(DEFINED SLOW_ADDR_POLL_RESPONSE)
    message(STATUS "SLOW_ADDR_POLL_RESPONSE set to ${SLOW_ADDR_POLL_RESPONSE}")
    target_compile_definitions(rf24_network PUBLIC SLOW_ADDR_POLL_RESPONSE=${SLOW_ADDR_POLL_RESPONSE})
endif()


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
if(MESH_NOMASTER)
    message(STATUS "MESH_NOMASTER asserted")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_NOMASTER)
endif()
if(MESH_DEBUG)
    message(STATUS "MESH_DEBUG asserted")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_DEBUG)
endif()
if(MESH_DEBUG_MINIMAL)
    message(STATUS "MESH_DEBUG_MINIMAL asserted")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_DEBUG_MINIMAL)
endif()
# for the following, we let the default be configured in source code
if(DEFINED MESH_MAX_CHILDREN)
    message(STATUS "MESH_MAX_CHILDREN set to ${MESH_MAX_CHILDREN}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_MAX_CHILDREN=${MESH_MAX_CHILDREN})
endif()
if(DEFINED MESH_DEFAULT_CHANNEL)
    message(STATUS "MESH_DEFAULT_CHANNEL set to ${MESH_DEFAULT_CHANNEL}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_DEFAULT_CHANNEL=${MESH_DEFAULT_CHANNEL})
endif()
if(DEFINED MESH_RENEWAL_TIMEOUT)
    message(STATUS "MESH_RENEWAL_TIMEOUT set to ${MESH_RENEWAL_TIMEOUT}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_RENEWAL_TIMEOUT=${MESH_RENEWAL_TIMEOUT})
endif()
if(DEFINED MESH_MEM_ALLOC_SIZE)
    message(STATUS "MESH_MEM_ALLOC_SIZE set to ${MESH_MEM_ALLOC_SIZE}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_MEM_ALLOC_SIZE=${MESH_MEM_ALLOC_SIZE})
endif()
if(DEFINED MESH_LOOKUP_TIMEOUT)
    message(STATUS "MESH_LOOKUP_TIMEOUT set to ${MESH_LOOKUP_TIMEOUT}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_LOOKUP_TIMEOUT=${MESH_LOOKUP_TIMEOUT})
endif()
if(DEFINED MESH_WRITE_TIMEOUT)
    message(STATUS "MESH_WRITE_TIMEOUT set to ${MESH_WRITE_TIMEOUT}")
    target_compile_definitions(${LibTargetName} PUBLIC MESH_WRITE_TIMEOUT=${MESH_WRITE_TIMEOUT})
endif()


################################ INSTALL RULES ####################################
# these are needed for scikit builds since the resulting .so files are copied into
# the binary distribution wheels (.whl files) for python.
install(TARGETS rf24 DESTINATION .)
install(TARGETS rf24_network DESTINATION .)
install(TARGETS rf24_mesh DESTINATION .)
