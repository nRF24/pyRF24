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

.. autoclass:: pyrf24.rf24.RF24

    Basic RF24 API
    **************
    
    .. automethod:: __init__

    .. automethod:: begin
    .. autoattribute:: listen
    .. automethod:: available
    .. automethod:: read
    .. automethod:: write
    .. automethod:: open_tx_pipe
    .. automethod:: open_rx_pipe

    Advanced RF24 API
    *****************

    .. automethod:: toggle_all_pipes
    .. autoattribute:: is_valid
    .. autoattribute:: is_chip_connected
    .. autoattribute:: is_plus_variant
    .. automethod:: what_happened

    Debugging Helpers
    ~~~~~~~~~~~~~~~~~

    .. autoattribute:: failure_detected
    .. automethod:: print_details
    .. automethod:: print_pretty_details
    .. automethod:: sprintf_pretty_details
    .. automethod:: get_arc
    
    Advanced Transmission
    ~~~~~~~~~~~~~~~~~~~~~

    .. automethod:: write_ack_payload
    .. automethod:: write_fast
    .. automethod:: reuse_tx
    .. automethod:: write_blocking
    .. automethod:: start_fast_write
    .. automethod:: start_write
    .. automethod:: tx_standby

    Power Management
    ~~~~~~~~~~~~~~~~

    .. autoattribute:: power

    FIFO Management
    ~~~~~~~~~~~~~~~

    .. autoattribute:: rx_fifo_full
    .. automethod:: flush_tx
    .. automethod:: flush_rx
    .. automethod:: is_fifo

    Ambiguous Signal Detection
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. autoattribute:: rpd
    .. automethod:: start_const_carrier
    .. automethod:: stop_const_carrier
    
    .. automethod:: available_pipe
    .. automethod:: close_rx_pipe

    Configurable RF24 API
    *********************

    .. autoattribute:: address_width
    .. automethod:: set_retries
    .. automethod:: mask_irq

    Channel (Frequency)
    ~~~~~~~~~~~~~~~~~~~

    .. autoattribute:: channel

    Dynamic Delays
    ~~~~~~~~~~~~~~

    .. autoattribute:: tx_delay

    Payload Sizes
    ~~~~~~~~~~~~~

    .. autoattribute:: payload_size
    .. autoattribute:: dynamic_payloads
    .. automethod:: get_dynamic_payload_size
    
    Auto-Acknowledgement
    ~~~~~~~~~~~~~~~~~~~~

    .. automethod:: set_auto_ack
    .. autoattribute:: ack_payloads
    .. automethod:: enable_dynamic_ack

    Radiation Options
    ~~~~~~~~~~~~~~~~~

    .. automethod:: set_pa_level
    .. autoattribute:: pa_level
    .. autoattribute:: data_rate
    .. automethod:: set_radiation

    CRC Lengths
    ~~~~~~~~~~~

    .. autoattribute:: crc_length
