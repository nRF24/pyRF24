# The MIT License (MIT)
#
# Copyright (c) 2019 Brendan Doherty
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""This module uses the `RF24` class to make the nRF24L01 imitate a
Bluetooth-Low-Emissions (BLE) beacon. A BLE beacon can send data (referred to as
advertisements) to any BLE compatible device (ie smart devices with Bluetooth
4.0 or later) that is listening.

Original research was done by `Dmitry Grinberg and his write-up (including C
source code) can be found here
<http://dmitry.gr/index.php?r=05.Projects&proj=11.%20Bluetooth%20LE%20fakery>`_
As this technique can prove invaluable in certain project designs, the code
here has been adapted to work with Python.

.. important:: Because the nRF24L01 wasn't designed for BLE advertising, it
    has some limitations that helps to be aware of.

    1. The maximum payload length is shortened to **18** bytes (when not
       broadcasting a device
       :py:attr:`~pyrf24.fake_ble.FakeBLE.name` nor
       the nRF24L01
       :py:attr:`~pyrf24.fake_ble.FakeBLE.show_pa_level`).
       This is calculated as:

       **32** (nRF24L01 maximum) - **6** (MAC address) - **5** (required
       flags) - **3** (CRC checksum) = **18**

       Use the helper function
       :py:func:`~pyrf24.fake_ble.FakeBLE.len_available()` to
       determine if your payload can be transmit.
    2. the channels that BLE use are limited to the following three: 2.402
       GHz, 2.426 GHz, and 2.480 GHz. We have provided a tuple of these
       specific channels for convenience (See `BLE_FREQ` and
       :py:func:`~pyrf24.fake_ble.FakeBLE.hop_channel()`).
    3. :py:attr:`~pyrf24.RF24.crc_length` is disabled in the
       nRF24L01 firmware because BLE  specifications require 3 bytes
       (:py:func:`~pyrf24.fake_ble.crc24_ble()`), and the
       nRF24L01 firmware can only handle a maximum of 2.
       Thus, we have appended the required 3 bytes of CRC24 into the payload.
    4. :py:attr:`~pyrf24.RF24.address_width` of BLE
       packet only uses 4 bytes, so we have set that accordingly.
    5. The auto-ack (automatic acknowledgment) feature of the nRF24L01 is useless
       when transmitting to BLE devices, thus it is disabled as well as automatic
       re-transmit (:py:meth:`~pyrf24.RF24.get_arc()`) and custom ACK
       payloads (:py:attr:`~pyrf24.RF24.ack_payloads`) features
       which both depend on the automatic acknowledgments feature.
    6. The :py:attr:`~pyrf24.RF24.dynamic_payloads`
       feature of the nRF24L01 isn't compatible with BLE specifications. Thus,
       we have disabled it.
    7. BLE specifications only allow using 1 Mbps RF
       :py:attr:`~pyrf24.RF24.data_rate`, so that too has
       been hard coded.
    8. Only the "on data sent" & "on data ready" events will have
       an effect on the interrupt (IRQ) pin. The "on data fail"  is never
       triggered because auto-ack feature is disabled. Keep this in mind when using
       `mask_irq()`.
"""

from os import urandom
import struct
from typing import Union, List, Optional
from .pyrf24 import ( # type: ignore
    RF24,
    RF24_CRC_DISABLED,
    RF24_PA_HIGH,
    RF24_PA_LOW,
    RF24_PA_MIN,
)


def address_repr(buf, reverse: bool = True, delimit: str = "") -> str:
    """Convert a buffer into a hexlified string.

    This method is primarily used to display how the address is used by the radio.

    .. code-block:: python

        >>> from pyrf24.fake_ble import address_repr
        >>> address_repr(b"1Node")
        '65646F4E31'

    :param bytes,bytearray buf: The buffer of bytes to convert into a hexlified
        string.
    :param bool reverse: A `bool` to control the resulting endianess. `True`
        outputs the result as big endian. `False` outputs the result as little
        endian. This parameter defaults to `True` since `bytearray` and `bytes`
        objects are stored in big endian but written in little endian.
    :param str delimit: A `chr` or `str` to use as a delimiter between bytes.
        Defaults to an empty string.

    :Returns:
        A string of hexadecimal characters in big endian form of the
        specified ``buf`` parameter.
    """
    order = range(len(buf) - 1, -1, -1) if reverse else range(len(buf))
    return delimit.join(["%02X" % buf[byte] for byte in order])


def swap_bits(original: int) -> int:
    """This function reverses the bit order for a single byte.

    :returns:
        An `int` containing the byte whose bits are reversed
        compared to the value passed to the ``original`` parameter.
    :param int original: This is truncated to a single unsigned byte,
        meaning this parameter's value can only range from 0 to 255.
    """
    original &= 0xFF
    reverse = 0
    for _ in range(8):
        reverse <<= 1
        reverse |= original & 1
        original >>= 1
    return reverse


def reverse_bits(original: Union[bytes, bytearray]) -> bytearray:
    """This function reverses the bit order for an entire buffer protocol object.

    :returns:
       A `bytearray` whose byte order remains the same, but each
       byte's bit order is reversed.
    :param bytearray,bytes original: The original buffer whose bits are to be
       reversed.
    """
    ret = bytearray(len(original))
    for i, byte in enumerate(original):
        ret[i] = swap_bits(byte)
    return ret


def chunk(buf: Union[bytes, bytearray], data_type: int = 0x16) -> bytearray:
    """This function is used to pack data values into a block of data that
    make up part of the BLE payload per Bluetooth Core Specifications.

    :param bytearray,bytes buf: The actual data contained in the block.
    :param int data_type: The type of data contained in the chunk. This is a
        predefined number according to BLE specifications. The default value
        ``0x16`` describes all service data. ``0xFF`` describes manufacturer
        information. Any other values are not applicable to BLE
        advertisements.

    .. important:: This function is called internally by
        :py:func:`~pyrf24.fake_ble.FakeBLE.advertise()`.
        To pack multiple data values into a single payload, use this function
        for each data value and pass a `list` or `tuple` of the returned
        results to
        :py:func:`~pyrf24.fake_ble.FakeBLE.advertise()`
        (see example code in documentation about
        :py:func:`~pyrf24.fake_ble.FakeBLE.advertise()`
        for more detail). Remember that broadcasting multiple data values may
        require the :py:attr:`~pyrf24.fake_ble.FakeBLE.name`
        be set to `None` and/or the
        :py:attr:`~pyrf24.fake_ble.FakeBLE.show_pa_level` be
        set to `False` for reasons about the payload size with
        `BLE Limitations`_.
    """
    return bytearray([len(buf) + 1, data_type & 0xFF]) + buf


def whitener(buf: Union[bytes, bytearray], coefficient: int) -> bytearray:
    """Whiten and de-whiten data according to the given coefficient.

    This is a helper function to `FakeBLE.whiten()`. It has been broken out of the
    `FakeBLE` class to allow whitening and dewhitening a BLE payload without the
    hardcoded coefficient.

    :param bytes,bytearray buf: The BLE payloads data. This data should include the
        CRC24 checksum.
    :param int coefficient: The whitening coefficient used to avoid repeating binary patterns.
        This is the index (plus 37) of `BLE_FREQ` tuple for nRF24L01 channel that the
        payload transits.

        .. code-block:: python

            rx_channel = radio.channel
            coef = (
                index + 37 for index, chl in enumerate(BLE_FREQ) if chl == rx_channel
            )

        .. note::
            If currently used nRF24L01 channel is different from the channel in which
            the payload was received, then set this parameter accordingly.
    """
    data = bytearray(buf)
    for i, byte in enumerate(data):
        res, mask = (0, 1)
        for _ in range(8):
            if coefficient & 1:
                coefficient ^= 0x88
                byte ^= mask
            mask <<= 1
            coefficient >>= 1
        data[i] = byte ^ res
    return data


def crc24_ble(
    data: Union[bytes, bytearray], deg_poly: int = 0x65B, init_val: int = 0x555555
) -> bytearray:
    """This function calculates a checksum of various sized buffers.

    This is exposed for convenience and should not be used for other buffer
    protocols that require big endian CRC24 format.

    :param bytearray,bytes data: The buffer of data to be uncorrupted.
    :param int deg_poly: A preset "degree polynomial" in which each bit
        represents a degree who's coefficient is 1. BLE specifications require
        ``0x00065b`` (default value).
    :param int init_val: This will be the initial value that the checksum
        will use while shifting in the buffer data. BLE specifications require
        ``0x555555`` (default value).
    :returns: A 24-bit `bytearray` representing the checksum of the data (in
        proper little endian).
    """
    crc = init_val
    for byte in data:
        crc ^= swap_bits(byte) << 16
        for _ in range(8):
            if crc & 0x800000:
                crc = (crc << 1) ^ deg_poly
            else:
                crc <<= 1
        crc &= 0xFFFFFF
    return reverse_bits((crc).to_bytes(3, "big"))


BLE_FREQ = (2, 26, 80)
"""The BLE channel number is different from the nRF channel number.

This tuple contains the relative predefined channels used:

.. csv-table::
    :header: "nRF24L01 channel", "BLE channel"

    2, 37
    26, 38
    80, 39
"""

TEMPERATURE_UUID = 0x1809  #: The Temperature Service UUID number
BATTERY_UUID = 0x180F  #: The Battery Service UUID number
EDDYSTONE_UUID = 0xFEAA  #: The Eddystone Service UUID number


class QueueElement:
    """A data structure used for storing received & decoded BLE payloads in
    the :attr:`~pyrf24.fake_ble.FakeBLE.rx_queue`.

    :param bytes,bytearray buffer: the validated BLE payload (not including
        the CRC checksum). The buffer passed here is decoded into this class's
        properties.
    """

    def __init__(self, buffer: Union[bytes, bytearray]):
        #: The transmitting BLE device's MAC address as a `bytes` object.
        self.mac: bytes = bytes(buffer[2:8])
        self.name: Optional[Union[bytes, str]] = None
        """The transmitting BLE device's name. This will be a `str`, `bytes` object (if
        a `UnicodeError` was caught), or `None` (if not included in the received
        payload)."""
        self.pa_level: Optional[int] = None
        """The transmitting device's PA Level (if included in the received payload)
        as an `int`.

        .. note:: This value does not represent the received signal strength.
            The nRF24L01 will receive anything over a -64 dbm threshold."""
        self.data: List[Union[bytearray, bytes, ServiceDataType]] = []
        """A `list` of the transmitting device's data structures (if any).
        If an element in this `list` is not an instance (or descendant) of the
        `ServiceData` class, then it is likely a custom, user-defined, or unsupported
        specification - in which case it will be a `bytearray` object."""

        end = buffer[1] + 2
        i = 8
        while i < end:
            size = buffer[i]
            if size + i + 1 > end or i + 1 > end or not size:
                # data seems malformed. just append the buffer & move on
                self.data.append(buffer[i:end])
                break
            result = self._decode_data_struct(buffer[i + 1 : i + 1 + size])
            if not result:  # decoding failed
                self.data.append(buffer[i : i + 1 + size])
            i += 1 + size

    def _decode_data_struct(self, buf: Union[bytes, bytearray]) -> bool:
        """Decode a data structure in a received BLE payload."""
        # print("decoding", address_repr(buf, 0, " "))
        if buf[0] not in (0x16, 0x0A, 0x08, 0x09):
            return False  # unknown/unsupported "chunk" of data
        if buf[0] == 0x0A and len(buf) == 2:  # if data is the device's TX-ing PA Level
            self.pa_level = struct.unpack("b", buf[1:2])[0]
        if buf[0] in (0x08, 0x09):  # if data is a BLE device name
            try:
                self.name = buf[1:].decode()
            except UnicodeError:
                self.name = bytes(buf[1:])
        if buf[0] == 0xFF:  # if it is a custom/user-defined data format
            self.data.append(buf)  # return the raw buffer as a value
        if buf[0] == 0x16:  # if it is service data
            service_data_uuid = struct.unpack("<H", buf[1:3])[0]
            service: ServiceDataType
            if service_data_uuid == TEMPERATURE_UUID:
                service = TemperatureServiceData()
                service.data = buf[3:]  # type: ignore
                self.data.append(service)
            elif service_data_uuid == BATTERY_UUID:
                service = BatteryServiceData()
                service.data = buf[3:]  # type: ignore
                self.data.append(service)
            elif service_data_uuid == EDDYSTONE_UUID:
                service = UrlServiceData()
                service.pa_level_at_1_meter = buf[4:5]  # type: ignore
                service.data = buf[5:]  # type: ignore
                self.data.append(service)
            else:
                self.data.append(buf)
        return True


class FakeBLE:
    """A class to implement BLE advertisements using the nRF24L01.

    Per the limitations of this technique, only some of underlying
    :py:class:`~pyrf24.RF24` functionality is
    available for configuration when implementing BLE transmissions.
    See the `Restricted RF24 functionality`_ for more details.

    :param RF24 radio: The RF24 object that will be used to access the radio's
        hardware.

        .. seealso::
            See the :py:class:`~pyrf24.RF24` class' constructor documentation.
    """

    def __init__(self, radio: RF24):
        self._radio = radio
        self._curr_freq = 2
        self._show_dbm = False
        self._ble_name: Optional[Union[bytes, bytearray]] = None
        self._mac = urandom(6)
        self.rx_queue: List[QueueElement] = []
        """The internal queue of received BLE payloads' data.

        Each Element in this queue is a `QueueElement` object whose members are set
        according to the its internal decoding algorithm. The
        :meth:`~pyrf24.fake_ble.FakeBLE.read()` function will remove & return the first
        element in this queue.

        .. hint::
            This attribute is exposed for debugging purposes, but it can also be used
            by applications.
        """
        self.rx_cache = bytearray(0)
        """The internal cache used when validating received BLE payloads.

        This attribute is only used by :meth:`~pyrf24.fake_ble.FakeBLE.available()`
        to cache the data from the top level of the radio's RX FIFO then validate and
        decode it.

        .. hint::
            This attribute is exposed for debugging purposes.
        """

    def begin(
        self, ce_pin: Optional[int] = None, csn_pin: Optional[int] = None
    ) -> bool:
        """Initialize the radio using BLE specifications.

        Internally, this function also calls :meth:`~pyrf24.RF24.begin()`, so
        there's no need to initialized the radio's hardware before calling this
        function.

        If dynamically specifying the radio's GPIO pins, then 2 positional arguments are supported.

        :param int ce_pin: The pin number connected to the radio's CE pin.
        :param int csn_pin: The pin number connected to the radio's CSN pin.
        """
        success = False
        if ce_pin is None and csn_pin is None:
            success = self._radio.begin()
        else:
            success = self._radio.begin(ce_pin, csn_pin)
        if not success:
            return False
        self._radio.crc_length = RF24_CRC_DISABLED
        self._radio.set_auto_ack(False)
        self._radio.dynamic_payloads = False
        self._radio.set_retries(0, 0)
        self._radio.address_width = 4  # use only 4 byte address length
        self._radio.open_tx_pipe(b"\x71\x91\x7d\x6b\0")
        self._radio.open_rx_pipe(0, b"\x71\x91\x7d\x6b\0")
        self.hop_channel()
        self._radio.power = True
        self._radio.listen = True
        return success

    @property
    def mac(self):
        """This attribute returns a 6-byte buffer that is used as the
        arbitrary mac address of the BLE device being emulated.

        You can set this attribute using a 6-byte `int` or `bytearray`. If this is
        set to `None`, then a random 6-byte address is generated.
        """
        return self._mac

    @mac.setter
    def mac(self, address):
        if address is None:
            self._mac = urandom(6)
        if isinstance(address, int):
            self._mac = (address).to_bytes(6, "little")
        elif isinstance(address, (bytearray, bytes)):
            self._mac = address
        if len(self._mac) < 6:
            self._mac += urandom(6 - len(self._mac))

    @property
    def name(self):
        """The broadcasted BLE name of the nRF24L01.

        This is not required. In fact, setting this attribute will subtract from
        the available payload length (in bytes). Set this attribute to `None` to
        disable advertising the device name.

        Valid inputs are `str`, `bytes`, `bytearray`, or `None`. A `str` will be
        converted to a `bytes` object automatically.

        .. note::
            This information occupies (in the TX FIFO) an extra 2 bytes plus
            the length of the name set by this attribute.
        """
        return self._ble_name

    @name.setter
    def name(self, _name):
        if _name is not None:
            if isinstance(_name, str):
                _name = _name.encode("utf-8")
            if not isinstance(_name, (bytes, bytearray)):
                raise ValueError("name must be a bytearray or bytes object.")
            if len(_name) > (18 - self._show_dbm * 3):
                raise ValueError("name length exceeds maximum.")
        self._ble_name = _name

    @property
    def show_pa_level(self) -> bool:
        """If this attribute is `True`, the payload will automatically include
        the nRF24L01's :py:attr:`~pyrf24.RF24.pa_level` in the
        advertisement.

        The default value of `False` will exclude this optional information.

        .. note:: This information occupies (in the TX FIFO) an extra 3 bytes, and is
            really only useful for some applications to calculate proximity to the
            nRF24L01 transceiver.
        """
        return bool(self._show_dbm)

    @show_pa_level.setter
    def show_pa_level(self, enable: bool):
        if enable and len(self.name) > 16:
            raise ValueError("there is not enough room to show the pa_level.")
        self._show_dbm = bool(enable)

    def hop_channel(self):
        """Trigger an automatic change of BLE compliant channels."""
        self._curr_freq += 1 if self._curr_freq < 2 else -2
        self._radio.channel = BLE_FREQ[self._curr_freq]

    def whiten(self, data) -> bytearray:
        """Whitening the BLE packet data ensures there's no long repetition
        of bits.

        This is done according to BLE specifications.

        :param bytearray,bytes data: The packet to whiten.
        :returns: A `bytearray` of the ``data`` with the whitening algorithm
            applied.

        .. note::
            `advertise()` and :meth:`~pyrf24.fake_ble.FakeBLE.available()` uses
            this function internally to prevent improper usage.
        .. warning::
            This function uses the currently set BLE channel as a
            base case for the whitening coefficient.

            Do not call `hop_channel()` before calling
            :meth:`~pyrf24.fake_ble.FakeBLE.available()`
            because this function needs to know the correct BLE channel to
            properly de-whiten received payloads.
        """
        coefficient = (self._curr_freq + 37) | 0x40
        # print("buffer: 0x" + address_repr(data, 0))
        # print(
        #     "Whiten Coefficient: {} on channel {}".format(
        #         hex(coefficient), BLE_FREQ[self._curr_freq]
        #     )
        # )
        data = whitener(data, coefficient)
        # print("whitened: 0x" + address_repr(data, 0))
        return data

    def _make_payload(self, payload) -> bytes:
        """Assemble the entire packet to be transmitted as a payload."""
        if self.len_available(payload) < 0:
            raise ValueError(
                "Payload length exceeds maximum buffer size by "
                + f"{abs(self.len_available(payload))} bytes"
            )
        name_length = (len(self.name) + 2) if self.name is not None else 0
        pl_size = 9 + len(payload) + name_length + self._show_dbm * 3
        buf = bytes([0x42, pl_size]) + self.mac
        buf += chunk(b"\x05", 1)
        pa_level = b""
        if self._show_dbm:
            lvl = self._radio.pa_level
            # assume this radio is an actual nRF24L01 (& not a clone)
            nordic_lvl = 0  # default to RF24_PA_MAX
            if lvl == RF24_PA_HIGH:
                nordic_lvl = -6
            elif lvl == RF24_PA_LOW:
                nordic_lvl = -12
            elif lvl == RF24_PA_MIN:
                nordic_lvl = -18
            pa_level = chunk(struct.pack(">b", nordic_lvl), 0x0A)
        buf += pa_level
        if name_length:
            buf += chunk(self.name, 0x08)
        buf += payload
        # print("PL: {} CRC: {}".format(
        #     address_repr(buf, 0), address_repr(crc24_ble(buf), 0)
        # ))
        buf += crc24_ble(buf)
        return buf

    def len_available(self, hypothetical=b"") -> int:
        """This function will calculates how much length (in bytes) is
        available in the next payload.

        This is determined from the current state of `name` and `show_pa_level`
        attributes.

        :param bytearray,bytes hypothetical: Pass a potential `chunk()` of
            data to this parameter to calculate the resulting left over length
            in bytes. This parameter is optional.
        :returns: An `int` representing the length of available bytes for
            a single payload.
        """
        name_length = (len(self._ble_name) + 2) if self._ble_name is not None else 0
        return 18 - name_length - self._show_dbm * 3 - len(hypothetical)

    def advertise(self, buf: Union[bytes, bytearray] = b"", data_type: int = 0xFF):
        """This blocking function is used to broadcast a payload.

        :returns: Nothing as every transmission will register as a success
            under the required settings for BLE beacons.

        :param bytearray buf: The payload to transmit. This bytearray must have
            a length greater than 0 and less than 22 bytes Otherwise a
            `ValueError` exception is thrown whose prompt will tell you the
            maximum length allowed under the current configuration. This can
            also be a list or tuple of payloads (`bytearray`); in which case,
            all items in the list/tuple are processed are packed into 1
            payload for a single transmissions. See example code below about
            passing a `list` or `tuple` to this parameter.
        :param int data_type: This is used to describe the buffer data passed
            to the ``buf`` parameter. ``0x16`` describes all service data. The
            default value ``0xFF`` describes manufacturer information. This
            parameter is ignored when a `tuple` or `list` is passed to the
            ``buf`` parameter. Any other values are not applicable to BLE
            advertisements.

        .. important:: If the name and/or TX power level of the emulated BLE
            device is also to be broadcast, then the `name` and/or
            `show_pa_level` attribute(s) should be set prior to calling
            `advertise()`.

        To pass multiple data values to the ``buf`` parameter see the
        following code as an example:

        .. code-block:: python

            # let UUIDs be the 16-bit identifier that corresponds to the
            # BLE service type. The following values are not compatible with
            # BLE advertisements.
            UUID_1 = 0x1805
            UUID_2 = 0x1806
            service1 = ServiceData(UUID_1)
            service2 = ServiceData(UUID_2)
            service1.data = b"some value 1"
            service2.data = b"some value 2"

            # make a tuple of the buffers
            buffers = (
                chunk(service1.buffer),
                chunk(service2.buffer)
            )

            # let `ble` be the instantiated object of the FakeBLE class
            ble.advertise(buffers)
            ble.hop_channel()
        """
        if not isinstance(buf, (bytearray, bytes, list, tuple)):
            raise ValueError("buffer is an invalid format")
        payload = b""
        if isinstance(buf, (list, tuple)):
            for byte in buf:
                payload += byte
        else:
            payload = chunk(buf, data_type) if buf else b""
        payload = self.whiten(self._make_payload(payload))
        # print("original: 0x{}".format(address_repr(payload)))
        # print("reversed: 0x{}".format(address_repr(reverse_bits(payload))))
        self._radio.write(reverse_bits(payload))

    def print_pretty_details(self):
        self._radio.print_pretty_details()
        print(f"BLE device name           {str(self.name)}")
        print(f"Broadcasting PA Level     {self.show_pa_level}")

    def available(self) -> bool:
        """A `bool` describing if there is a payload in the `rx_queue`.

        This method will take the first available data from the radio's RX FIFO and
        validate the payload using the 24bit CRC checksum at the end of the payload.
        If the payload is indeed a valid BLE transmission that fit within the 32 bytes
        that the nRF24L01 can capture, then this method will decipher the data within
        the payload and enqueue the resulting `QueueElement` in the `rx_queue`.

        .. tip:: Use :meth:`~pyrf24.fake_ble.FakeBLE.read()` to fetch the
            decoded data.

        :Returns:
            - `True` if payload was received *and* validated
            - `False` if no payload was received or the received payload could not be
              deciphered.
        """
        if self._radio.available():
            self.rx_cache = self._radio.read(self._radio.payload_size)
            self.rx_cache = self.whiten(reverse_bits(self.rx_cache))
            end = self.rx_cache[1] + 2
            self.rx_cache = self.rx_cache[: end + 3]
            if end < 30 and self.rx_cache[end : end + 3] == crc24_ble(
                self.rx_cache[:end]
            ):
                # print("recv'd:", self.rx_cache)
                # print("crc:", self.rx_cache[end: end + 3])
                self.rx_queue.append(QueueElement(self.rx_cache))
        return bool(self.rx_queue)

    def read(self) -> Optional[QueueElement]:
        """Get the First Out element from the queue.

        :Returns:
            - `None` if nothing is the internal `rx_queue`
            - A `QueueElement` object from the front of the `rx_queue`
              (like a FIFO buffer).
        """
        if self.rx_queue:
            ret_val = self.rx_queue[0]
            del self.rx_queue[0]
            return ret_val
        return None


class ServiceData:
    """An abstract helper class to package specific service data using
    Bluetooth SIG defined 16-bit UUID flags to describe the data type.

    :param int uuid: The 16-bit UUID `"GATT Service assigned number"
        <https://specificationrefs.bluetooth.com/assigned-values/
        16-bit%20UUID%20Numbers%20Document.pdf#page=19>`_ defined by the
        Bluetooth SIG to describe the service data. This parameter is
        required.
    """

    def __init__(self, uuid):
        self._type = struct.pack("<H", uuid)
        self._data = b""

    @property
    def uuid(self) -> bytes:
        """This returns the 16-bit Service UUID as a `bytearray` in little
        endian. (read-only)"""
        return self._type

    @property
    def data(self) -> Union[float, int, str, bytes, bytearray]:
        """This attribute is a `bytearray` or `bytes` object."""
        return self._data

    @data.setter
    def data(self, value: Union[float, int, str, bytes, bytearray]):
        self._data = value

    @property
    def buffer(self) -> bytes:
        """Get the representation of the instantiated object as an
        immutable `bytes` object (read-only)."""
        return bytes(self._type + self._data)

    def __len__(self) -> int:
        """For convenience, this class is compatible with python's builtin
        :py:func:`len()` method. In this context, this will return the length
        of the object (in bytes) as it would appear in the advertisement
        payload."""
        return len(self._type) + len(self._data)

    def __repr__(self) -> str:
        """For convenience, this class is compatible with python's builtin
        :py:func:`repr()` method. In this context, it will return a string of
        data with applicable suffixed units."""
        return address_repr(self.buffer, False)


class TemperatureServiceData(ServiceData):
    """This derivative of the `ServiceData` class can be used to represent
    temperature data values as a `float` value.

    .. seealso:: Bluetooth Health Thermometer Measurement format as defined in the
        `GATT Specifications Supplement.
        <https://www.bluetooth.org/DocMan/handlers/
        DownloadDoc.ashx?doc_id=502132&vId=542989>`_
    """

    def __init__(self):
        super().__init__(TEMPERATURE_UUID)

    @property  # type: ignore[override]
    def data(self) -> float:
        """This attribute is a `float` value."""
        return struct.unpack("<i", self._data[:3] + b"\0")[0] * 10**-2

    @data.setter
    def data(self, value: Union[bytes, bytearray, float]):
        if isinstance(value, float):
            value = struct.pack("<i", int(value * 100) & 0xFFFFFF)
            self._data = value[:3] + bytes([0xFE])
        elif isinstance(value, (bytes, bytearray)):
            self._data = value

    def __repr__(self) -> str:
        return f"Temperature: {self.data} C"


class BatteryServiceData(ServiceData):
    """This derivative of the `ServiceData` class can be used to represent
    battery charge percentage as a 1-byte value.

    .. seealso:: The Bluetooth Battery Level format as defined in the
        `GATT Specifications Supplement.
        <https://www.bluetooth.org/DocMan/handlers/
        DownloadDoc.ashx?doc_id=502132&vId=542989>`_
    """

    def __init__(self):
        super().__init__(BATTERY_UUID)

    @property  # type: ignore[override]
    def data(self) -> int:
        """The attribute is a 1-byte unsigned `int` value."""
        return int(self._data[0])

    @data.setter
    def data(self, value: Union[bytes, bytearray, int]):
        if isinstance(value, int):
            self._data = struct.pack("B", value)
        elif isinstance(value, (bytes, bytearray)):
            self._data = value

    def __repr__(self) -> str:
        return f"Battery capacity remaining: {self.data}%"


class UrlServiceData(ServiceData):
    """This derivative of the `ServiceData` class can be used to represent
    URL data as a `bytes` value.

    .. seealso::
        Google's `Eddystone-URL specifications
        <https://github.com/google/eddystone/tree/master/eddystone-url>`_.
    """

    def __init__(self):
        super().__init__(EDDYSTONE_UUID)
        self._type += bytes([0x10]) + struct.pack(">b", -25)

    codex_prefix = ["http://www.", "https://www.", "http://", "https://"]
    codex_suffix = [".com", ".org", ".edu", ".net", ".info", ".biz", ".gov"]
    codex_suffix = [suffix + "/" for suffix in codex_suffix] + codex_suffix

    @property
    def pa_level_at_1_meter(self) -> int:
        """The TX power level (in dBm) at 1 meter from the nRF24L01. This
        defaults to -25 (due to testing when broadcasting with 0 dBm) and must
        be a 1-byte signed `int`."""
        return struct.unpack(">b", self._type[-1:])[0]

    @pa_level_at_1_meter.setter
    def pa_level_at_1_meter(self, value: Union[bytes, bytearray, int]):
        if isinstance(value, int):
            self._type = self._type[:-1] + struct.pack(">b", int(value))
        elif isinstance(value, (bytes, bytearray)):
            self._type = self._type[:-1] + value[:1]

    @property
    def uuid(self) -> bytes:
        return self._type[:2]

    @property  # type: ignore[override]
    def data(self) -> str:
        """This attribute is a `str` of URL data."""
        value = self._data.decode()
        for i, b_code in enumerate(UrlServiceData.codex_prefix):
            value = value.replace(chr(i), b_code, 1)
        for i, b_code in enumerate(UrlServiceData.codex_suffix):
            value = value.replace(chr(i), b_code)
        return value

    @data.setter
    def data(self, value: Union[bytes, bytearray, str]):
        if isinstance(value, str):
            for i, b_code in enumerate(UrlServiceData.codex_prefix):
                value = value.replace(b_code, chr(i), 1)
            for i, b_code in enumerate(UrlServiceData.codex_suffix):
                value = value.replace(b_code, chr(i))
            self._data = value.encode("utf-8")
        elif isinstance(value, (bytes, bytearray)):
            self._data = value

    def __repr__(self) -> str:
        return "Advertised URL: " + self.data


# A type alias to explain the funky inheritance
ServiceDataType = Union[BatteryServiceData, TemperatureServiceData, UrlServiceData]
