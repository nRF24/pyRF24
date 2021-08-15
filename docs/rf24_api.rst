RF24 API
========

Enum classes
------------

.. class:: pyrf24.rf24.rf24_crclength_e

    .. csv-table::
        :header: "length (enum value)", description

        "RF24_CRC_DISABLED (0)", "to disable using CRC checksums"
        "RF24_CRC_8 (1)", "to use 8-bit checksums"
        "RF24_CRC_16 (2)", "to use 16-bit checksums"

.. class:: pyrf24.rf24.rf24_datarate_e

    .. csv-table::
        :header: "speed (enum value)", description

        "RF24_1MBPS (0)", "for 1 Mbps"
        "RF24_2MBPS (1)", "for 2 Mbps"
        "RF24_250KBPS (2)", "for 250 kbps"


.. class:: pyrf24.rf24.rf24_pa_dbm_e

    .. csv-table::
        :header: "level (enum value)", "nRF24L01 description", "Si24R1 description when LNA enabled", "Si24R1 description when LNA disabled"

        "RF24_PA_MIN (0)", "-18 dBm", "-6 dBm", "-12 dBm"
        "RF24_PA_LOW (1)", "-12 dBm", "-0 dBm", "-4 dBm"
        "RF24_PA_HIGH (2)", "-6 dBm", "3 dBm", "1 dBm"
        "RF24_PA_MAX (3)", "0 dBm", "7 dBm", "4 dBm"

RF24 class
----------
Basic RF24 API
**************

.. autoclass:: pyrf24.rf24.RF24
    :members: __init__, begin, listen, available, read, write, open_tx_pipe, open_rx_pipe

Advanced RF24 API
*****************

.. autoattribute:: pyrf24.rf24.RF24.failure_detected
.. automethod:: pyrf24.rf24.RF24.print_details
.. automethod:: pyrf24.rf24.RF24.print_pretty_details
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
.. autoattribute:: pyrf24.rf24.RF24.is_valid
.. automethod:: pyrf24.rf24.RF24.close_rx_pipe
.. autoattribute:: pyrf24.rf24.RF24.is_plus_variant

Configurable RF24 API
*********************

.. .. automethod:: pyrf24.rf24.RF24.set_address_width
.. autoattribute:: pyrf24.rf24.RF24.address_width
.. automethod:: pyrf24.rf24.RF24.set_retries
.. autoattribute:: pyrf24.rf24.RF24.channel
.. autoattribute:: pyrf24.rf24.RF24.payload_size
.. automethod:: pyrf24.rf24.RF24.get_dynamic_payload_size
.. .. automethod:: pyrf24.rf24.RF24.enable_ack_payload
.. .. automethod:: pyrf24.rf24.RF24.disable_ack_payload
.. .. automethod:: pyrf24.rf24.RF24.enable_dynamic_payloads
.. .. automethod:: pyrf24.rf24.RF24.disable_dynamic_payloads
.. autoattribute:: pyrf24.rf24.RF24.ack_payloads
.. autoattribute:: pyrf24.rf24.RF24.dynamic_payloads
.. automethod:: pyrf24.rf24.RF24.enable_dynamic_ack
.. automethod:: pyrf24.rf24.RF24.set_auto_ack
.. automethod:: pyrf24.rf24.RF24.set_pa_level
.. automethod:: pyrf24.rf24.RF24.get_pa_level
.. .. automethod:: pyrf24.rf24.RF24.set_data_rate
.. .. automethod:: pyrf24.rf24.RF24.get_data_rate
.. autoattribute:: pyrf24.rf24.RF24.data_rate
.. .. automethod:: pyrf24.rf24.RF24.set_crc_length
.. .. automethod:: pyrf24.rf24.RF24.get_crc_length
.. autoattribute:: pyrf24.rf24.RF24.crc_length
.. automethod:: pyrf24.rf24.RF24.mask_irq
.. automethod:: pyrf24.rf24.RF24.start_const_carrier
.. automethod:: pyrf24.rf24.RF24.stop_const_carrier
