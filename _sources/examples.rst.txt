Examples
==============

RF24 examples
***************

getting_started
---------------

A simple example of using the RF24 class

.. literalinclude:: ../examples/getting_started.py
    :caption: examples/getting_started.py
    :end-before: set_role
    :linenos:

acknowledgement_payloads
------------------------

A simple example of using the RF24 class to attach an Acknowledgement (ACK) payload the automatically generated ACK packet.

.. literalinclude:: ../examples/acknowledgement_payloads.py
    :caption: examples/acknowledgement_payloads.py
    :end-before: set_role
    :linenos:

manual_acknowledgements
-----------------------

A simple example of using the RF24 class to receive a payload and then send a responding payload as an Acknowledgement. This functionality is similar to using the nRF24L01's ACK payload feature, but doe not append ACK payloads to the ACK packets.

.. literalinclude:: ../examples/manual_acknowledgements.py
    :caption: examples/manual_acknowledgements.py
    :end-before: set_role
    :linenos:

multiceiver_demo
----------------
A simple example of using the RF24 class to receive data from multiple transmitting nRF24L01 transceivers. This technique is trademarked by Nordic Semiconductors as "Multiceiver\ :sup:`TM`"

.. literalinclude:: ../examples/multiceiver_demo.py
    :caption: examples/multiceiver_demo.py
    :end-before: set_role
    :linenos:

streaming_data
--------------
A simple example of using the RF24 class to stream data.

.. literalinclude:: ../examples/streaming_data.py
    :caption: examples/streaming_data.py
    :end-before: set_role
    :linenos:

interrupt_configure
-------------------

A simple example of using the nRF24L01's IRQ pin to catch different interrupt request events.

.. literalinclude:: ../examples/interrupt_configure.py
    :caption: examples/interrupt_configure.py
    :linenos:

Fake BLE example
*****************

A simple example of using the nRF24L01 as fake BLE beacon.

.. literalinclude:: ../examples/fake_ble_test.py
    :caption: examples/fake_ble_test.py
    :end-before: set_role
    :linenos:

Networking examples
***********************

RF24Network examples
--------------------

A simple example of using the nRF24L01 as network child (non-master) node.

.. literalinclude:: ../examples/network_helloworld_tx.py
    :caption: examples/network_helloworld_tx.py
    :linenos:

A simple example of using the nRF24L01 as a network's master node.

.. literalinclude:: ../examples/network_helloworld_rx.py
    :caption: examples/network_helloworld_rx.py
    :linenos:

RF24Mesh examples
--------------------

A simple example of using the nRF24L01 as mesh network child (non-master) node.

.. literalinclude:: ../examples/mesh_example.py
    :caption: examples/mesh_example.py
    :linenos:

A simple example of using the nRF24L01 as a mesh network's master node.

.. literalinclude:: ../examples/mesh_example_master.py
    :caption: examples/mesh_example_master.py
    :linenos:

Generic Network example
------------------------

A generic example demonstrating the differences in code for using RF24Network or RF24Mesh API.

.. literalinclude:: ../examples/general_network_test.py
    :caption: examples/general_network_test.py
    :end-before: set_role
    :linenos:
