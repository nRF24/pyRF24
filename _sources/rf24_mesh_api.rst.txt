RF24Mesh API
============

.. automodule:: pyrf24.rf24_mesh

RF24Mesh class
**************

.. autoclass:: pyrf24.rf24_mesh.RF24Mesh

    Basic RF24Mesh API
    ------------------

    .. automethod:: __init__
    .. automethod:: begin
    .. automethod:: update
    .. automethod:: write
    .. autoattribute:: node_id
    .. automethod:: renew_address

    Advanced RF24Mesh API
    ---------------------

    .. automethod:: check_connection
    .. autoattribute:: mesh_address
    .. automethod:: release_address
    .. automethod:: get_node_id
    .. automethod:: get_address
    .. automethod:: set_address
    .. automethod:: set_channel
    .. automethod:: set_child
    .. autoattribute:: addr_list

AddrListStruct class
********************

The properties of this class are read-only because they can only be set by the master node upon
successful connection to a child node.

.. hint::
    The `AddrListStruct` class supports the python "magic method" :py:func:`repr()`. So, you can
    easily pass an instantiated `AddrListStruct` object to the :py:func:`print()` function.

.. autoclass:: pyrf24.rf24_mesh.AddrListStruct
    
    .. autoattribute:: node_id
    .. autoattribute:: address

Mesh Constants
**************

These are the pre-defined constants provided for convenience and code readability.

.. autoattribute:: pyrf24.rf24_mesh.MESH_DEFAULT_ADDRESS

    A reserved valid address for use with RF24Mesh (when a mesh node requests an assigned address)

Reserved System Message Types
-----------------------------

.. autoattribute:: pyrf24.rf24_mesh.MESH_ADDR_LOOKUP

    This message type is used to fetch (from the master node) an allocated Logical
    Address (`mesh_address`) corresponding to specified a mesh node's
    :py:attr:`~RF24Mesh.node_id`.

    This is exclusively used by `get_address()`.

.. autoattribute:: pyrf24.rf24_mesh.MESH_ID_LOOKUP

    This message type is used to fetch (from the master node) a mesh node's
    :py:attr:`~RF24Mesh.node_id` corresponding to an specified Logical Address
    (`mesh_address`).

    This is exclusively used by `get_node_id()`.

.. autoattribute:: pyrf24.rf24_mesh.MESH_ADDR_RELEASE

    This message type is used when mesh nodes are consciously disconnecting from the
    network. It is used to unassign the Logical Address allocated the mesh node's
    :py:attr:`~RF24Mesh.node_id`.

    This is exclusively used by `release_address()`.
