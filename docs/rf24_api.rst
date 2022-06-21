RF24 API
========

Enum classes
------------

.. autoclass:: pyrf24.rf24.rf24_crclength_e
    :members: RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16

.. autoclass:: pyrf24.rf24.rf24_datarate_e
    :members: RF24_1MBPS, RF24_2MBPS, RF24_250KBPS

.. autoclass:: pyrf24.rf24.rf24_pa_dbm_e
    :members: RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX

RF24 class
----------
Basic RF24 API
**************

.. autoclass:: pyrf24.rf24.RF24
    :members: begin, listen, available, read, write, open_tx_pipe, open_rx_pipe
    :special-members: __init__

Advanced RF24 API
*****************

.. autoattribute:: pyrf24.rf24.RF24.failure_detected
.. automethod:: pyrf24.rf24.RF24.print_details
.. automethod:: pyrf24.rf24.RF24.print_pretty_details
.. automethod:: pyrf24.rf24.RF24.sprintf_pretty_details
.. automethod:: pyrf24.rf24.RF24.available_pipe
.. automethod:: pyrf24.rf24.RF24.is_fifo
.. .. autoattribute:: pyrf24.rf24.RF24.rx_fifo_full
.. .. automethod:: pyrf24.rf24.RF24.power_up
.. .. automethod:: pyrf24.rf24.RF24.power_down
.. autoattribute:: pyrf24.rf24.RF24.power
.. automethod:: pyrf24.rf24.RF24.write_fast
.. automethod:: pyrf24.rf24.RF24.write_blocking
.. automethod:: pyrf24.rf24.RF24.tx_standby
.. automethod:: pyrf24.rf24.RF24.write_ack_payload
.. automethod:: pyrf24.rf24.RF24.what_happened
.. automethod:: pyrf24.rf24.RF24.start_fast_write
.. automethod:: pyrf24.rf24.RF24.start_write
.. automethod:: pyrf24.rf24.RF24.reuse_tx
.. automethod:: pyrf24.rf24.RF24.flush_rx
.. automethod:: pyrf24.rf24.RF24.flush_tx
.. .. automethod:: pyrf24.rf24.RF24.test_rpd
.. autoattribute:: pyrf24.rf24.RF24.rpd
.. automethod:: pyrf24.rf24.RF24.close_rx_pipe
.. autoattribute:: pyrf24.rf24.RF24.is_plus_variant
.. autoattribute:: pyrf24.rf24.RF24.is_valid
.. autoattribute:: pyrf24.rf24.RF24.is_chip_connected

Configurable RF24 API
*********************

.. .. automethod:: pyrf24.rf24.RF24.set_address_width
.. autoattribute:: pyrf24.rf24.RF24.address_width

.. automethod:: pyrf24.rf24.RF24.set_retries
.. automethod:: pyrf24.rf24.RF24.get_arc

.. autoattribute:: pyrf24.rf24.RF24.channel

.. autoattribute:: pyrf24.rf24.RF24.payload_size
.. automethod:: pyrf24.rf24.RF24.get_dynamic_payload_size
.. .. automethod:: pyrf24.rf24.RF24.enable_ack_payload
.. .. automethod:: pyrf24.rf24.RF24.disable_ack_payload
.. .. automethod:: pyrf24.rf24.RF24.enable_dynamic_payloads
.. .. automethod:: pyrf24.rf24.RF24.disable_dynamic_payloads
.. autoattribute:: pyrf24.rf24.RF24.dynamic_payloads
.. autoattribute:: pyrf24.rf24.RF24.ack_payloads

.. automethod:: pyrf24.rf24.RF24.enable_dynamic_ack
.. automethod:: pyrf24.rf24.RF24.set_auto_ack

.. automethod:: pyrf24.RF24.toggle_all_pipes

.. automethod:: pyrf24.RF24.set_radiation
.. automethod:: pyrf24.rf24.RF24.set_pa_level
.. .. automethod:: pyrf24.rf24.RF24.get_pa_level
.. autoattribute:: pyrf24.rf24.RF24.pa_level
.. .. automethod:: pyrf24.rf24.RF24.set_data_rate
.. .. automethod:: pyrf24.rf24.RF24.get_data_rate
.. autoattribute:: pyrf24.rf24.RF24.data_rate

.. .. automethod:: pyrf24.rf24.RF24.set_crc_length
.. .. automethod:: pyrf24.rf24.RF24.get_crc_length
.. autoattribute:: pyrf24.rf24.RF24.crc_length

.. automethod:: pyrf24.rf24.RF24.mask_irq

.. automethod:: pyrf24.rf24.RF24.start_const_carrier
.. automethod:: pyrf24.rf24.RF24.stop_const_carrier
