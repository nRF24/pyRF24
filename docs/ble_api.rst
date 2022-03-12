BLE API
=================

BLE Limitations
---------------

.. automodule:: pyrf24.fake_ble


``fake_ble`` module helpers
---------------------------

.. autofunction:: pyrf24.fake_ble.address_repr
.. autofunction:: pyrf24.fake_ble.swap_bits
.. autofunction:: pyrf24.fake_ble.reverse_bits
.. autofunction:: pyrf24.fake_ble.crc24_ble
.. autofunction:: pyrf24.fake_ble.chunk
.. autofunction:: pyrf24.fake_ble.whitener
.. autodata:: pyrf24.fake_ble.BLE_FREQ

QueueElement class
------------------

.. autoclass:: pyrf24.fake_ble.QueueElement
    :members:

FakeBLE class
-------------

.. autoclass:: pyrf24.fake_ble.FakeBLE
    :members:

Restricted RF24 functionality
******************************

The following `RF24` functionality should not be used when `FakeBLE`
objects are instantiated with an `RF24` object:

- :py:attr:`~pyrf24.rf24.RF24.dynamic_payloads`
- :py:attr:`~pyrf24.rf24.RF24.data_rate`
- :py:attr:`~pyrf24.rf24.RF24.address_width`
- :py:meth:`~pyrf24.rf24.RF24.set_auto_ack()`
- :py:attr:`~pyrf24.rf24.RF24.ack_payloads`
- :py:attr:`~pyrf24.rf24.RF24.crc_length`
- :py:meth:`~pyrf24.rf24.RF24.open_rx_pipe()`
- :py:meth:`~pyrf24.rf24.RF24.open_tx_pipe()`


Service related classes
-----------------------

Abstract Parent
***************

.. autoclass:: pyrf24.fake_ble.ServiceData
    :members:
    :special-members: __len__,__repr__

Service data UUID numbers
*************************

These are the 16-bit UUID numbers used by the
`Derivative Children of the ServiceData class <ble_api.html#derivative-children>`_

.. autodata:: pyrf24.fake_ble.TEMPERATURE_UUID
    :annotation: = 0x1809
.. autodata:: pyrf24.fake_ble.BATTERY_UUID
    :annotation: = 0x180F
.. autodata:: pyrf24.fake_ble.EDDYSTONE_UUID
    :annotation: = 0xFEAA

Derivative Children
*******************

.. autoclass:: pyrf24.fake_ble.TemperatureServiceData
    :members: data
    :show-inheritance:

.. autoclass:: pyrf24.fake_ble.BatteryServiceData
    :members: data
    :show-inheritance:

.. autoclass:: pyrf24.fake_ble.UrlServiceData
    :members: pa_level_at_1_meter, data
    :show-inheritance:
