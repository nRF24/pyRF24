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
set(SUPPLEMENT_LINUX_GPIO_H FALSE)
if("${RF24_DRIVER}" STREQUAL "RPi" OR "${RF24_DRIVER}" STREQUAL "SPIDEV")
    set(SUPPLEMENT_LINUX_GPIO_H TRUE)
    message(STATUS "Supplementing ${RF24_DRIVER} driver with linux/gpio.h")
    # file(COPY src/linux/gpio.h DESTINATION RF24/utility/${RF24_DRIVER}/linux)
    list(APPEND RF24_DRIVER_SOURCES src/linux/gpio.h)
endif()

### Build C++ RF24 stack as static libraries (for linking to pyRF24*)

################################# RF24 C++ #########################
add_library(cpp_rf24 SHARED
    RF24/RF24.cpp
    ${RF24_DRIVER_SOURCES}
)
if(SUPPLEMENT_LINUX_GPIO_H)
    target_include_directories(cpp_rf24 PUBLIC src)
endif()
target_include_directories(cpp_rf24 PUBLIC utility)
if(NOT "${RF24_LINKED_DRIVER}" STREQUAL "")
    if("${RF24_DRIVER}" STREQUAL "wiringPi")
        target_link_libraries(cpp_rf24 PUBLIC rt crypt ${RF24_LINKED_DRIVER})
    else()
        target_link_libraries(cpp_rf24 PUBLIC ${RF24_LINKED_DRIVER})
    endif()
endif()
apply_flags(cpp_rf24)

################################# RF24Network C++ #########################
add_library(cpp_rf24_network SHARED
    RF24Network/RF24Network.cpp
)
# don't let source look for an installed RF24 lib
target_compile_definitions(cpp_rf24_network PUBLIC USE_RF24_LIB_SRC)
target_include_directories(cpp_rf24_network PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
    RF24Network
)
target_link_libraries(cpp_rf24_network PUBLIC cpp_rf24)
apply_flags(cpp_rf24_network)

################################# RF24Mesh C++ #########################
add_library(cpp_rf24_mesh SHARED
    RF24Mesh/RF24Mesh.cpp
)
# don't let source look for an installed RF24 lib
target_compile_definitions(cpp_rf24_mesh PUBLIC USE_RF24_LIB_SRC)
target_include_directories(cpp_rf24_mesh PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
    RF24Network
    RF24Mesh
)
target_link_libraries(cpp_rf24_mesh PUBLIC cpp_rf24_network)
apply_flags(cpp_rf24_mesh)

################################# RF24 #############################
pybind11_add_module(rf24 src/pyRF24.cpp)
target_link_libraries(rf24 PUBLIC cpp_rf24)
target_include_directories(rf24 PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
)
apply_flags(rf24)

################################# RF24NETWORK #############################

pybind11_add_module(rf24_network src/pyRF24Network.cpp)
target_include_directories(rf24_network PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
    RF24Network
)
# don't let source look for an installed RF24 lib
target_compile_definitions(rf24_network PUBLIC USE_RF24_LIB_SRC)
target_link_libraries(rf24_network PUBLIC cpp_rf24_network)
apply_flags(rf24_network)


################################# RF24MESH #############################

pybind11_add_module(rf24_mesh src/pyRF24Mesh.cpp)
target_include_directories(rf24_mesh PUBLIC
    RF24
    RF24/utility
    RF24/utility/${RF24_DRIVER}
    RF24Network
    RF24Mesh
)
target_link_libraries(rf24_mesh PUBLIC cpp_rf24_mesh)
# don't let source look for an installed RF24 lib
target_compile_definitions(rf24_mesh PUBLIC USE_RF24_LIB_SRC)
apply_flags(rf24_mesh)


################################ INSTALL RULES ####################################
# these are needed for scikit builds since the resulting .so files are copied into
# the binary distribution wheels (.whl files) for python.
install(TARGETS rf24 DESTINATION .)
install(TARGETS rf24_network DESTINATION .)
install(TARGETS rf24_mesh DESTINATION .)

# uncomment to show compiler args used in build logs
# set(CMAKE_VERBOSE_MAKEFILE ON)
