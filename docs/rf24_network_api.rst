:description: How to use the radio as a static network node.

RF24Network API
===============

.. currentmodule:: pyrf24

RF24Network class
-----------------


.. autoclass:: pyrf24.RF24Network
    
    Basic RF24Network API
    *********************

    .. automethod:: __init__
    .. automethod:: begin
    .. automethod:: update
    .. automethod:: available
    .. automethod:: peek
    .. automethod:: read
    .. automethod:: write
    .. autoattribute:: node_address

    Advanced RF24Network API
    ************************

    .. automethod:: multicast
    .. automethod:: is_address_valid
    .. autoattribute:: multicast_relay
    .. autoattribute:: tx_timeout
    .. autoattribute:: route_timeout
    .. autoattribute:: multicast_level

External Systems or Applications
********************************

.. autoattribute:: pyrf24.RF24Network.return_sys_msgs
.. autoattribute:: pyrf24.RF24Network.network_flags

RF24NetworkHeader class
-----------------------

.. hint::
    The `RF24NetworkHeader` class supports the python "magic method" :py:func:`repr()`. So, you can
    easily pass an instantiated `RF24NetworkHeader` object to the :py:func:`print()` function.

.. autoclass:: pyrf24.RF24NetworkHeader
    
    .. autoattribute:: to_node
    .. autoattribute:: type
    .. autoattribute:: from_node
    .. autoattribute:: id
    .. autoattribute:: reserved
    .. autoattribute:: to_string

    .. property:: next_id
        :classmethod:

        The next sequential identifying number used for the next created header's `id`.

Constants
----------

The following are predefined module-level constants that can be used for comparisons and
code readability.

.. autoattribute:: pyrf24.MAX_USER_DEFINED_HEADER_TYPE
    
    The maximum of user defined message types.

.. autoattribute:: pyrf24.MAX_PAYLOAD_SIZE

    Maximum size of fragmented network frames and fragmentation cache.

.. _reserved_sys_msgs:

Reserved System Message Types
******************************

The network will determine whether to automatically acknowledge payloads based on their general
:py:attr:`RF24NetworkHeader.type`.

- **User types** (1 - 127) 1 - 64 will NOT be acknowledged
- **System types** (128 - 255) 192 - 255 will NOT be acknowledged

System types can also contain message data.

.. autoattribute:: pyrf24.NETWORK_ADDR_RESPONSE

    A ``NETWORK_ADDR_RESPONSE`` type is utilized to manually route custom messages containing a
    single RF24Network address.

    Used by RF24Mesh

    If a node receives a message of this type that is directly addressed to it, it will read the
    included message, and forward the payload on to the proper recipient.

    This allows nodes to forward multicast messages to the master node, receive a response, and
    forward it back to the requester.

.. autoattribute:: pyrf24.NETWORK_PING

    Messages of type ``NETWORK_PING`` will be dropped automatically by the recipient.
    A `NETWORK_ACK` or automatic radio-ack will indicate to the sender whether the payload was
    successful. The time it takes to successfully send a ``NETWORK_PING`` is the round-trip-time.

.. autoattribute:: pyrf24.EXTERNAL_DATA_TYPE

    External data types are used to define messages that will be passed to an external data system.
    This allows RF24Network to route and pass any type of data, such as TCP/IP frames, while still
    being able to utilize standard RF24Network messages etc.

.. autoattribute:: pyrf24.NETWORK_FIRST_FRAGMENT

    Messages of this type designate the first of two or more message fragments, and will be re-assembled automatically.

.. autoattribute:: pyrf24.NETWORK_MORE_FRAGMENTS

    Messages of this type indicate a fragmented payload with two or more message fragments.

.. autoattribute:: pyrf24.NETWORK_LAST_FRAGMENT

    Messages of this type indicate the last fragment in a sequence of message fragments.
    Messages of this type do not receive a `NETWORK_ACK`.

.. autoattribute:: pyrf24.NETWORK_ACK

    Messages of this type signal the sender that a network-wide transmission has been completed.

    - **Not fool-proof**

      RF24Network does not directly have a built-in transport layer protocol, so message delivery is
      not 100% guaranteed. Messages can be lost via corrupted dynamic payloads, or a ``NETWORK_ACK`` can
      fail (despite successful transmission of the message).
    - **Traffic analysis**

      ``NETWORK_ACK`` messages can be utilized as a traffic/flow control mechanism. Transmitting nodes
      that emit ``NETWORK_ACK`` qualifying messages will be forced to wait, before sending additional
      data, until the payload is transmitted across the network and acknowledged.
    - **Different from Radio ACK Packets**

      In the event that the transmitting device will be sending directly to a parent or child node,
      a ``NETWORK_ACK`` is not required. This is because the radio's auto-ack feature is utilized for
      connections between directly related network nodes. For example: nodes ``0o1`` and ``0o11`` use the
      radio's auto-ack feature for transmissions between them, but nodes ``0o1`` and ``0o2`` do not use
      the radio's auto-ack feature for transmissions between them as messages will be routed through
      other nodes.
  
      Multicasted messages do use the radio's auto-ack feature because of the hardware limitations of
      nRF24L01 transceivers. This applies to all multicasted messages (directly related nodes or
      otherwise).
 
    .. hint::
        Remember, user messages types with a decimal value of ``64`` or less will not be acknowledged across
        the network via ``NETWORK_ACK`` messages.

    .. note::
        ``NETWORK_ACK`` messages are only sent by the last node in the route to a target node.
        ie: When node ``0o0`` sends an instigating message to node ``0o11``, node ``0o1`` will send the
        ``NETWORK_ACK`` message to ``0o0`` upon successful delivery of instigating message to node ``0o11``.

.. autoattribute:: pyrf24.NETWORK_POLL

    Used by RF24Mesh.

    Messages of this type are used with multi-casting, to find active/available nodes.
    Any node receiving a NETWORK_POLL sent to a multicast address will respond directly to the sender with a blank message, indicating the
    address of the available node via the header.

.. autoattribute:: pyrf24.NETWORK_REQ_ADDRESS

    Used by RF24Mesh

    Messages of this type are used to request information from the master node, generally via a unicast (direct) write.
    Any (non-master) node receiving a message of this type will manually forward it to the master node using a normal network write.

Network flag mnemonics
***********************

.. autoattribute:: pyrf24.FLAG_FAST_FRAG

    This flag (when asserted in :py:attr:`~RF24Network.network_flags`) prevents repetitively configuring the
    radio during transmission of fragmented messages.

.. autoattribute:: pyrf24.FLAG_NO_POLL

    This flag (when asserted in :py:attr:`~RF24Network.network_flags`) prevents a node from responding to
    mesh nodes looking to connect to the network. Calling :py:func:`~pyrf24.RF24Mesh.set_child()` uses this flag
    accordingly.
