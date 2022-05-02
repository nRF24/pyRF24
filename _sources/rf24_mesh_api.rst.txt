RF24Mesh API
============

.. automodule:: pyrf24.rf24_mesh

Basic RF24Mesh API
------------------

.. autoclass:: pyrf24.rf24_mesh.RF24Mesh
    :members: begin, update, write, node_id, renew_address
    :special-members: __init__

Advanced RF24Mesh API
---------------------

.. automethod:: pyrf24.rf24_mesh.RF24Mesh.check_connection
.. autoattribute:: pyrf24.rf24_mesh.RF24Mesh.mesh_address
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.release_address
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.get_node_id
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.get_address
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.set_address
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.set_channel
.. automethod:: pyrf24.rf24_mesh.RF24Mesh.set_child
.. autoattribute:: pyrf24.rf24_mesh.RF24Mesh.addr_list

AddrListStruct class
--------------------

.. autoclass:: pyrf24.rf24_mesh.AddrListStruct
    :members:

Mesh Constants
----------------

These are the pre-defined constants provided for convenience and code readability.

.. autoattribute:: pyrf24.rf24_mesh.MESH_DEFAULT_ADDRESS

    A reserved valid address for use with RF24Mesh (when a mesh node requests an assigned address)

Reserved System Message Types
*****************************

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
