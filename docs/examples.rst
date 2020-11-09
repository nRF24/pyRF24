RF24
====

getting_started
---------------

A simple example of using the RF24 class

.. literalinclude:: ../examples/RF24_getting_started.py
    :caption: examples/RF24_getting_started.py
    :linenos:

acknowledgement_payloads
------------------------

A simple example of using the RF24 class to attach an Acknowledgement (ACK) payload the automatically generated ACK packet.

.. literalinclude:: ../examples/RF24_acknowledgement_payloads.py
    :caption: examples/RF24_acknowledgement_payloads.py
    :linenos:

manual_acknowledgements
-----------------------

A simple example of using the RF24 class to receive a payload and then send a responding payload as an Acknowledgement. This functionality is similar to using the nRF24L01's ACK payload feature, but doe not append ACK payloads to the ACK packets.

.. literalinclude:: ../examples/RF24_manual_acknowledgements.py
    :caption: examples/RF24_manual_acknowledgements.py
    :linenos:

multiceiver_demo
----------------
A simple example of using the RF24 class to receive data from multiple transmitting nRF24L01 transceivers. This technique is trademarked by Nordic Semiconductors as "Multiceiver\ :sup:`TM`"

.. literalinclude:: ../examples/RF24_multiceiver_demo.py
    :caption: examples/RF24_multiceiver_demo.py
    :linenos:

streaming_data
--------------
A simple example of using the RF24 class to stream data.

.. literalinclude:: ../examples/RF24_streaming_data.py
    :caption: examples/RF24_streaming_data.py
    :linenos:

interrupt_configure
-------------------

A simple example of using the nRF24L01's IRQ pin to catch different interrupt request events.

.. literalinclude:: ../examples/RF24_interrupt_configure.py
    :caption: examples/RF24_interrupt_configure.py
    :linenos:
