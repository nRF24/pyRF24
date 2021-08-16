RF24Network API
===============


.. automodule:: pyrf24.rf24_network
    :members:

RF24Network class
-----------------

Basic RF24Network API
*********************

.. autoclass:: pyrf24.rf24_network.RF24Network
    :members: begin, update, available, peek, read, write, node_address
    :special-members: __init__

Advanced RF24Network API
************************

.. automethod:: pyrf24.rf24_network.RF24Network.multicast
.. automethod:: pyrf24.rf24_network.RF24Network.is_address_valid
.. autoattribute:: pyrf24.rf24_network.RF24Network.multicast_relay
.. autoattribute:: pyrf24.rf24_network.RF24Network.tx_timeout
.. autoattribute:: pyrf24.rf24_network.RF24Network.route_timeout
.. autoattribute:: pyrf24.rf24_network.RF24Network.multicast_level

External Systems or Applications
********************************

.. autoattribute:: pyrf24.rf24_network.RF24Network.return_sys_msgs
.. autoattribute:: pyrf24.rf24_network.RF24Network.network_flags

RF24NetworkHeader class
-----------------------

.. autoclass:: pyrf24.rf24_network.RF24NetworkHeader
    :members:
    :special-members:
