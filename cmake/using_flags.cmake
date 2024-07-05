# ###################### DEBUG (& EXTRA) FLAGS ######################

# ## RF24 core specific options
option(RF24_DEBUG "enable/disable debugging output for RF24 lib" OFF)

# ## RF24Network specific options
option(RF24NETWORK_DEBUG "enable/disable debugging output for RF24Network lib" OFF)
option(RF24NETWORK_DEBUG_MINIMAL "enable/disable minimal debugging output for RF24Network lib" OFF)
option(RF24NETWORK_DEBUG_ROUTING
    "enable/disable debugging output related to transmission routing for RF24Network lib"
    OFF
)
option(RF24NETWORK_DEBUG_FRAGMENTATION
    "enable/disable debugging output related to message fragmentation for RF24Network lib"
    OFF
)
option(RF24NETWORK_DEBUG_FRAGMENTATION_L2
    "enable/disable debugging output related to fragmented messages' transmission success for RF24Network lib"
    OFF
)
option(DISABLE_FRAGMENTATION "disable message fragmentation for RF24Network lib" OFF)
option(DISABLE_DYNAMIC_PAYLOADS "force usage of static payload size for RF24Network lib" OFF)

# ### options with default values:

# SLOW_ADDR_POLL_RESPONSE
# This can be useful to set a custom delay (in microseconds) for the master node when a
# connecting child node is slow to execute.

# MAX_PAYLOAD_SIZE
# This can be used to increase/decrease the maximum size of a message (before fragmentation).
# A value <= 24 is a less efficient alternative to DISABLE_FRAGMENTATION option.

# ## RF24Mesh specific options
option(MESH_NOMASTER "exclude compiling code that is strictly for master nodes for RF24Mesh lib" OFF)
option(RF24MESH_DEBUG "enable/disable debugging output for RF24Mesh lib" OFF)
option(RF24MESH_DEBUG_MINIMAL "enable/disable minimal debugging output for RF24Mesh lib" OFF)

# ### options with default values:

# RF24MESH_CONN_CHECK_TYPE
# This can be used to control how RF24Mesh.check_connection() behaves.
# By default, check_connection() will simply ping the parent node (if any).
# Setting this to RF24MESH_CONN_CHECK_MASTER will resort to the old behavior
# which verified the assigned address with the master node.
# It is recommended that this be left as default for large mesh networks.

# MESH_CONNECTION_CHECK_ATTEMPTS
# the number of attempts to check_connection() with the mesh. Defaults to 3

# MESH_MAX_CHILDREN
# This can be used to prevent mesh child nodes from occupying all available pipes on network layers.
# Only recommended if combining RF24Network nodes w/ RF24Mesh nodes on the same network.

# MESH_DEFAULT_CHANNEL
# A compile time alternative to using radio.setChannel() at runtime. Accepted values range [0, 125].

# MESH_RENEWAL_TIMEOUT
# A compile time alternative to using the timeout parameter to mesh.renew_address() at runtime.

# MESH_MEM_ALLOC_SIZE
# Advanced usage only! This controls the initial allocated memory for the master node's DHCP list.

# MESH_LOOKUP_TIMEOUT
# This can be used to increase/decrease the time spent waiting for master node's respond to
# a lookup message.

# MESH_WRITE_TIMEOUT
# This can be used to increase/decrease the time spent ensuring success during
# mesh.write() (only when using node_id instead of a node's logical address).
# This is cumulative to MESH_LOOKUP_TIMEOUT.

# ##############################################
# function to apply flags to applicable targets
function(apply_flags target)
    # apply RF24 flags to cpp_rf24 target
    if(RF24_DEBUG)
        message(STATUS "RF24_DEBUG asserted")
        target_compile_definitions(${target} PUBLIC RF24_DEBUG)
    endif()

    # pass driver used to expose as a constant in rf24 module.
    target_compile_definitions(${target} PUBLIC RF24_DRIVER="${RF24_DRIVER}")

    # apply RF24Network flags to cpp_rf24_network target
    if(RF24NETWORK_DEBUG)
        message(STATUS "RF24NETWORK_DEBUG asserted")
        target_compile_definitions(${target} PUBLIC RF24NETWORK_DEBUG)
    endif()

    if(RF24NETWORK_DEBUG_MINIMAL)
        message(STATUS "RF24NETWORK_DEBUG_MINIMAL asserted")
        target_compile_definitions(${target} PUBLIC RF24NETWORK_DEBUG_MINIMAL)
    endif()

    if(RF24NETWORK_DEBUG_ROUTING)
        message(STATUS "RF24NETWORK_DEBUG_ROUTING asserted")
        target_compile_definitions(${target} PUBLIC RF24NETWORK_DEBUG_ROUTING)
    endif()

    if(RF24NETWORK_DEBUG_FRAGMENTATION)
        message(STATUS "RF24NETWORK_DEBUG_FRAGMENTATION asserted")
        target_compile_definitions(${target} PUBLIC RF24NETWORK_DEBUG_FRAGMENTATION)
    endif()

    if(RF24NETWORK_DEBUG_FRAGMENTATION_L2)
        message(STATUS "RF24NETWORK_DEBUG_FRAGMENTATION_L2 asserted")
        target_compile_definitions(${target} PUBLIC RF24NETWORK_DEBUG_FRAGMENTATION_L2)
    endif()

    if(DISABLE_FRAGMENTATION)
        message(STATUS "DISABLE_FRAGMENTATION asserted")
        target_compile_definitions(${target} PUBLIC DISABLE_FRAGMENTATION)
    endif()

    # for MAX_PAYLOAD_SIZE, we let the default be configured in source code
    if(DEFINED MAX_PAYLOAD_SIZE) # don't use CMake's `option()` for this one
        message(STATUS "MAX_PAYLOAD_SIZE set to ${MAX_PAYLOAD_SIZE}")
        target_compile_definitions(${target} PUBLIC MAX_PAYLOAD_SIZE=${MAX_PAYLOAD_SIZE})
    endif()

    if(DEFINED SLOW_ADDR_POLL_RESPONSE)
        message(STATUS "SLOW_ADDR_POLL_RESPONSE set to ${SLOW_ADDR_POLL_RESPONSE}")
        target_compile_definitions(${target} PUBLIC SLOW_ADDR_POLL_RESPONSE=${SLOW_ADDR_POLL_RESPONSE})
    endif()

    # apply RF24Mesh flags to cpp_rf24_mesh target
    if(MESH_NOMASTER)
        message(STATUS "MESH_NOMASTER asserted")
        target_compile_definitions(${target} PUBLIC MESH_NOMASTER)
    endif()

    if(RF24MESH_DEBUG)
        message(STATUS "RF24MESH_DEBUG asserted")
        target_compile_definitions(${target} PUBLIC RF24MESH_DEBUG)
    endif()

    if(RF24MESH_DEBUG_MINIMAL)
        message(STATUS "RF24MESH_DEBUG_MINIMAL asserted")
        target_compile_definitions(${target} PUBLIC RF24MESH_DEBUG_MINIMAL)
    endif()

    # for the following, we let the default be configured in source code
    if(DEFINED MESH_MAX_CHILDREN)
        message(STATUS "MESH_MAX_CHILDREN set to ${MESH_MAX_CHILDREN}")
        target_compile_definitions(${target} PUBLIC MESH_MAX_CHILDREN=${MESH_MAX_CHILDREN})
    endif()

    if(DEFINED MESH_DEFAULT_CHANNEL)
        message(STATUS "MESH_DEFAULT_CHANNEL set to ${MESH_DEFAULT_CHANNEL}")
        target_compile_definitions(${target} PUBLIC MESH_DEFAULT_CHANNEL=${MESH_DEFAULT_CHANNEL})
    endif()

    if(DEFINED MESH_RENEWAL_TIMEOUT)
        message(STATUS "MESH_RENEWAL_TIMEOUT set to ${MESH_RENEWAL_TIMEOUT}")
        target_compile_definitions(${target} PUBLIC MESH_RENEWAL_TIMEOUT=${MESH_RENEWAL_TIMEOUT})
    endif()

    if(DEFINED MESH_MEM_ALLOC_SIZE)
        message(STATUS "MESH_MEM_ALLOC_SIZE set to ${MESH_MEM_ALLOC_SIZE}")
        target_compile_definitions(${target} PUBLIC MESH_MEM_ALLOC_SIZE=${MESH_MEM_ALLOC_SIZE})
    endif()

    if(DEFINED MESH_LOOKUP_TIMEOUT)
        message(STATUS "MESH_LOOKUP_TIMEOUT set to ${MESH_LOOKUP_TIMEOUT}")
        target_compile_definitions(${target} PUBLIC MESH_LOOKUP_TIMEOUT=${MESH_LOOKUP_TIMEOUT})
    endif()

    if(DEFINED MESH_WRITE_TIMEOUT)
        message(STATUS "MESH_WRITE_TIMEOUT set to ${MESH_WRITE_TIMEOUT}")
        target_compile_definitions(${target} PUBLIC MESH_WRITE_TIMEOUT=${MESH_WRITE_TIMEOUT})
    endif()

    if(DEFINED RF24MESH_CONN_CHECK_TYPE)
        message(STATUS "RF24MESH_CONN_CHECK_TYPE set to &{RF24MESH_CONN_CHECK_TYPE}")
        target_compile_definitions(${target} PUBLIC RF24MESH_CONN_CHECK_TYPE=${RF24MESH_CONN_CHECK_TYPE})
    endif()

    if(DEFINED MESH_CONNECTION_CHECK_ATTEMPTS)
        message(STATUS "MESH_CONNECTION_CHECK_ATTEMPTS set to &{MESH_CONNECTION_CHECK_ATTEMPTS}")
        target_compile_definitions(${target} PUBLIC MESH_CONNECTION_CHECK_ATTEMPTS=${MESH_CONNECTION_CHECK_ATTEMPTS})
    endif()
endfunction()
