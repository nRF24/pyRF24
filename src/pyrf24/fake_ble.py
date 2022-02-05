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
"""Original research was done by Dmitry Grinberg and his write-up can be found at
http://dmitry.gr/index.php?r=05.Projects&proj=11.%20Bluetooth%20LE%20fakery"""
# pylint: disable=too-few-public-methods,missing-docstring,too-many-instance-attributes
from os import urandom
import struct
from typing import Union, List
from .rf24 import RF24, RF24_CRC_DISABLED


def address_repr(buf, reverse: bool = True, delimit: str = "") -> str:
    """Convert a buffer into a hexlified string."""
    order = range(len(buf) - 1, -1, -1) if reverse else range(len(buf))
    # pylint: disable=consider-using-f-string
    return delimit.join(["%02X" % buf[byte] for byte in order])
    # pylint: enable=consider-using-f-string


def swap_bits(original: int) -> int:
    """This function reverses the bit order for a single byte."""
    original &= 0xFF
    reverse = 0
    for _ in range(8):
        reverse <<= 1
        reverse |= original & 1
        original >>= 1
    return reverse


def reverse_bits(original: bytearray) -> bytearray:
    """This function reverses the bit order for an entire buffer protocol object."""
    ret = bytearray(len(original))
    for i, byte in enumerate(original):
        ret[i] = swap_bits(byte)
    return ret


def chunk(buf: Union[bytes, bytearray], data_type: int = 0x16) -> bytearray:
    """This function is used to pack data values into a block of data that
    make up part of the BLE payload per Bluetooth Core Specifications."""
    return bytearray([len(buf) + 1, data_type & 0xFF]) + buf


def whitener(buf: Union[bytes, bytearray], coefficient: int) -> bytearray:
    """Whiten and de-whiten data according to the given coefficient."""
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
    """This function calculates a checksum of various sized buffers."""
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
"""The BLE channel number is different from the nRF channel number."""

TEMPERATURE_UUID = 0x1809  #: The Temperature Service UUID number
BATTERY_UUID = 0x180F  #: The Battery Service UUID number
EDDYSTONE_UUID = 0xFEAA  #: The Eddystone Service UUID number


class QueueElement:
    """A data structure used for storing received & decoded BLE payloads in
    the :attr:`~circuitpython_nrf24l01.fake_ble.FakeBLE.rx_queue`.

    :param bytes,bytearray buffer: the validated BLE payload (not including
        the CRC checksum). The buffer passed here is decoded into this class's
        properties.
    """

    def __init__(self, buffer: Union[bytes, bytearray]):
        #: The transmitting BLE device's MAC address as a `bytes` object.
        self.mac: bytes = bytes(buffer[2:8])
        self.name: bytes = None
        """The transmitting BLE device's name. This will be a `str`, `bytes` object (if
        a `UnicodeError` was caught), or `None` (if not included in the received
        payload)."""
        self.pa_level: int = None
        """The transmitting device's PA Level (if included in the received payload)
        as an `int`.

        .. note:: This value does not represent the received signal strength.
            The nRF24L01 will receive anything over a -64 dbm threshold."""
        self.data: List[Union[bytearray, bytes, ServiceData]] = []
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
            if service_data_uuid == TEMPERATURE_UUID:
                service = TemperatureServiceData()
                service.data = buf[3:]
                self.data.append(service)
            elif service_data_uuid == BATTERY_UUID:
                service = BatteryServiceData()
                service.data = buf[3:]
                self.data.append(service)
            elif service_data_uuid == EDDYSTONE_UUID:
                service = UrlServiceData()
                service.pa_level_at_1_meter = buf[4:5]
                service.data = buf[5:]
                self.data.append(service)
            else:
                self.data.append(buf)
        return True


class FakeBLE:
    """A class to implement BLE advertisements using the nRF24L01."""

    def __init__(self, radio: RF24):
        self._radio = radio
        self._curr_freq = 2
        self._show_dbm = False
        self._ble_name: Union[bytes, bytearray] = None
        self._mac = urandom(6)
        #: The internal queue of received BLE payloads' data.
        self.rx_queue = []
        self.rx_cache = bytearray(0)
        """The internal cache used when validating received BLE payloads."""

    def begin(self, ce_pin: int = None, csn: int = None) -> bool:
        """Initialize the radio using BLE specifications"""
        success = False
        if ce_pin is None and csn is None:
            success = self._radio.begin()
        else:
            success = self._radio.begin(ce_pin, csn)
        if not success:
            return False
        self._radio.crc_length = RF24_CRC_DISABLED
        self._radio.set_auto_ack(False)
        self._radio.dynamic_payloads = False
        self._radio.set_retries(0, 0)
        self._radio.address_width = 4  # use only 4 byte address length
        self._radio.open_tx_pipe(b"\x71\x91\x7D\x6B\0")
        self._radio.open_rx_pipe(0, b"\x71\x91\x7D\x6B\0")
        self.hop_channel()
        self._radio.power = True
        self._radio.listen = True
        return success

    @property
    def mac(self):
        """This attribute returns a 6-byte buffer that is used as the
        arbitrary mac address of the BLE device being emulated."""
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
        """The broadcasted BLE name of the nRF24L01."""
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
        the nRF24L01's :attr:`~circuitpython_nrf24l01.rf24.RF24.pa_level` in the
        advertisement."""
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
        of bits."""
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
            pa_level = chunk(struct.pack(">b", self._radio.pa_level), 0x0A)
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
        available in the next payload."""
        name_length = (len(self._ble_name) + 2) if self._ble_name is not None else 0
        return 18 - name_length - self._show_dbm * 3 - len(hypothetical)

    def advertise(self, buf: Union[bytes, bytearray] = b"", data_type: int = 0xFF):
        """This blocking function is used to broadcast a payload."""
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
        """A `bool` describing if there is a payload in the `rx_queue`."""
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


class ServiceData:
    """An abstract helper class to package specific service data using
    Bluetooth SIG defined 16-bit UUID flags to describe the data type."""

    def __init__(self, uuid):
        self._type = struct.pack("<H", uuid)
        self._data = b""

    @property
    def uuid(self) -> bytes:
        """This returns the 16-bit Service UUID as a `bytearray` in little
        endian. (read-only)"""
        return self._type

    @property
    def data(self) -> bytes:
        """This attribute is a `bytearray` or `bytes` object."""
        return self._data

    @data.setter
    def data(self, value):
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
    temperature data values as a `float` value."""

    def __init__(self):
        super().__init__(TEMPERATURE_UUID)

    @property
    def data(self) -> float:
        """This attribute is a `float` value."""
        return struct.unpack("<i", self._data[:3] + b"\0")[0] * 10**-2

    @data.setter
    def data(self, value: float):
        if isinstance(value, float):
            value = struct.pack("<i", int(value * 100) & 0xFFFFFF)
            self._data = value[:3] + bytes([0xFE])
        elif isinstance(value, (bytes, bytearray)):
            self._data = value

    def __repr__(self) -> str:
        return f"Temperature: {self.data} C"


class BatteryServiceData(ServiceData):
    """This derivative of the `ServiceData` class can be used to represent
    battery charge percentage as a 1-byte value."""

    def __init__(self):
        super().__init__(BATTERY_UUID)

    @property
    def data(self) -> int:
        """The attribute is a 1-byte unsigned `int` value."""
        return int(self._data[0])

    @data.setter
    def data(self, value: int):
        if isinstance(value, int):
            self._data = struct.pack("B", value)
        elif isinstance(value, (bytes, bytearray)):
            self._data = value

    def __repr__(self) -> str:
        return f"Battery capacity remaining: {self.data}%"


class UrlServiceData(ServiceData):
    """This derivative of the `ServiceData` class can be used to represent
    URL data as a `bytes` value."""

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
    def pa_level_at_1_meter(self, value):
        if isinstance(value, int):
            self._type = self._type[:-1] + struct.pack(">b", int(value))
        elif isinstance(value, (bytes, bytearray)):
            self._type = self._type[:-1] + value[:1]

    @property
    def uuid(self) -> bytes:
        return self._type[:2]

    @property
    def data(self) -> str:
        """This attribute is a `str` of URL data."""
        value = self._data.decode()
        for i, b_code in enumerate(UrlServiceData.codex_prefix):
            value = value.replace(chr(i), b_code, 1)
        for i, b_code in enumerate(UrlServiceData.codex_suffix):
            value = value.replace(chr(i), b_code)
        return value

    @data.setter
    def data(self, value: str):
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
