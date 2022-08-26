# pylint: skip-file
from typing import Tuple, Union, overload

class rf24_crclength_e:
    RF24_CRC_DISABLED: "rf24_crclength_e"
    RF24_CRC_8: "rf24_crclength_e"
    RF24_CRC_16: "rf24_crclength_e"

RF24_CRC_DISABLED: rf24_crclength_e = rf24_crclength_e.RF24_CRC_DISABLED
RF24_CRC_8: rf24_crclength_e = rf24_crclength_e.RF24_CRC_8
RF24_CRC_16: rf24_crclength_e = rf24_crclength_e.RF24_CRC_16

class rf24_datarate_e:
    RF24_1MBPS: rf24_datarate_e
    RF24_2MBPS: rf24_datarate_e
    RF24_250KBPS: rf24_datarate_e

RF24_1MBPS: rf24_datarate_e = rf24_datarate_e.RF24_1MBPS
RF24_2MBPS: rf24_datarate_e = rf24_datarate_e.RF24_2MBPS
RF24_250KBPS: rf24_datarate_e = rf24_datarate_e.RF24_250KBPS

class rf24_pa_dbm_e:
    RF24_PA_MIN: rf24_pa_dbm_e
    RF24_PA_LOW: rf24_pa_dbm_e
    RF24_PA_HIGH: rf24_pa_dbm_e
    RF24_PA_MAX: rf24_pa_dbm_e

RF24_PA_MIN: rf24_pa_dbm_e = rf24_pa_dbm_e.RF24_PA_MIN
RF24_PA_LOW: rf24_pa_dbm_e = rf24_pa_dbm_e.RF24_PA_LOW
RF24_PA_HIGH: rf24_pa_dbm_e = rf24_pa_dbm_e.RF24_PA_HIGH
RF24_PA_MAX: rf24_pa_dbm_e = rf24_pa_dbm_e.RF24_PA_MAX

class RF24:
    @overload
    def __init__(self, ce_pin: int, csn_pin: int, spi_speed: int = 10000000) -> None: ...
    @overload
    def __init__(self, spi_speed: int = 10000000) -> None: ...
    def available(self) -> bool: ...
    def available_pipe(self) -> Tuple[bool, int]: ...
    @overload
    def begin(self) -> bool: ...
    @overload
    def begin(self, ce_pin: int = None, csn_pin: int = None) -> bool: ...
    def close_rx_pipe(self, pipe_number: int) -> None: ...
    def closeReadingPipe(self, pipe_number: int) -> None: ...
    def disableDynamicPayloads(self) -> None: ...
    def enableDynamicPayloads(self) -> None: ...
    def enable_dynamic_ack(self) -> None: ...
    def enableDynamicAck(self) -> None: ...
    def enableAckPayload(self) -> None: ...
    def flush_rx(self) -> None: ...
    def flush_tx(self) -> None: ...
    def get_arc(self) -> int: ...
    def getARC(self) -> int: ...
    def getChannel(self) -> int: ...
    def getCRCLength(self) -> rf24_crclength_e: ...
    def getDataRate(self) -> rf24_datarate_e: ...
    def get_dynamic_payload_size(self) -> int: ...
    def getDynamicPayloadSize(self) -> int: ...
    def getPALevel(self) -> int: ...
    def getPayloadSize(self) -> int: ...
    def isChipConnected(self) -> bool: ...
    def isPVariant(self) -> bool: ...
    def isValid(self) -> bool: ...
    def is_fifo(self, about_tx: bool, check_empty: bool = None) -> Union[bool, int]: ...
    def isFifo(self, about_tx: bool, check_empty: bool = None) -> Union[bool, int]: ...
    def mask_irq(self, tx_ok: bool, tx_fail: bool, rx_ready: bool) -> None: ...
    def maskIRQ(self, tx_ok: bool, tx_fail: bool, rx_ready: bool) -> None: ...
    def open_tx_pipe(self, address: Union[bytes, bytearray, int]) -> None: ...
    def openWritingPipe(self, address: Union[bytes, bytearray, int]) -> None: ...
    def open_rx_pipe(self, number: int, address: Union[bytes, bytearray, int]) -> None: ...
    def openReadingPipe(self, number: int, address: Union[bytes, bytearray, int]) -> None: ...
    def powerUp(self) -> None: ...
    def powerDown(self) -> None: ...
    def print_details(self) -> None: ...
    def printDetails(self) -> None: ...
    def print_pretty_details(self) -> None: ...
    def printPrettyDetails(self) -> None: ...
    def read(self, length: int) -> bytearray: ...
    def reuse_tx(self) -> None: ...
    def reUseTX(self) -> None: ...
    def rxFifoFull(self) -> bool: ...
    def setAddressWidth(self, width: int) -> None: ...
    @overload
    def set_auto_ack(self, number: int, enable: bool) -> None: ...
    @overload
    def set_auto_ack(self, enable: bool) -> None: ...
    @overload
    def setAutoAck(self, number: int, enable: bool) -> None: ...
    @overload
    def setAutoAck(self, enable: bool) -> None: ...
    def setChannel(self, channel: int) -> None: ...
    def setCRCLength(self, length: rf24_crclength_e) -> None: ...
    def setDataRate(self, speed: rf24_datarate_e) -> None: ...
    def set_pa_level(self, level: rf24_pa_dbm_e, lna_enable: bool = True) -> None: ...
    def setPALevel(self, level: rf24_pa_dbm_e, lna_enable: bool = True) -> None: ...
    def set_retries(self, delay: int, count: int) -> None: ...
    def setRetries(self, delay: int, count: int) -> None: ...
    def set_radiation(
        self, level: rf24_pa_dbm_e, speed: rf24_datarate_e, lna_enable: bool = True
    ) -> None: ...
    def setRadiation(
        self, level: rf24_pa_dbm_e, speed: rf24_datarate_e, lna_enable: bool = True
    ) -> None: ...
    def setPayloadSize(self, size: int) -> None: ...
    def sprintf_pretty_details(self) -> str: ...
    def sprintfPrettyDetails(self) -> str: ...
    def startListening(self) -> None: ...
    def stopListening(self) -> None: ...
    def start_const_carrier(self, level: rf24_pa_dbm_e, channel: int) -> None: ...
    def startConstCarrier(self, level: rf24_pa_dbm_e, channel: int) -> None: ...
    def start_fast_write(
        self,
        buf: Union[bytearray, bytes],
        multicast: bool = False,
        start_tx: bool = True,
    ) -> None: ...
    def startFastWrite(
        self,
        buf: Union[bytearray, bytes],
        multicast: bool = False,
        start_tx: bool = True,
    ) -> None: ...
    def start_write(
        self, buf: Union[bytearray, bytes], multicast: bool = False
    ) -> bool: ...
    def startWrite(
        self, buf: Union[bytearray, bytes], multicast: bool = False
    ) -> bool: ...
    def stop_const_carrier(self) -> None: ...
    def stopConstCarrier(self) -> None: ...
    def testRPD(self) -> bool: ...
    def toggle_all_pipes(self, enable: bool) -> None: ...
    def toggleAllPipes(self, enable: bool) -> None: ...
    def tx_standby(self, timeout: int = None, start_tx: bool = True) -> bool: ...
    def txStandBy(self, timeout: int = None, start_tx: bool = True) -> bool: ...
    def what_happened(self) -> Tuple[bool, bool, bool]: ...
    def whatHappened(self) -> Tuple[bool, bool, bool]: ...
    def write(self, buf: Union[bytearray, bytes], multicast: bool = False) -> bool: ...
    def write_ack_payload(self, pipe: int, buf: Union[bytearray, bytes]) -> bool: ...
    def writeAckPayload(self, pipe: int, buf: Union[bytearray, bytes]) -> bool: ...
    def write_blocking(self, buf: Union[bytearray, bytes], timeout: int) -> bool: ...
    def writeBlocking(self, buf: Union[bytearray, bytes], timeout: int) -> bool: ...
    def write_fast(
        self, buf: Union[bytearray, bytes], multicast: bool = False
    ) -> bool: ...
    def writeFast(
        self, buf: Union[bytearray, bytes], multicast: bool = False
    ) -> bool: ...
    @property
    def ack_payloads(self) -> bool: ...
    @ack_payloads.setter
    def ack_payloads(self, enable: bool) -> None: ...
    @property
    def address_width(self) -> int: ...
    @address_width.setter
    def address_width(self, length: int) -> None: ...
    @property
    def channel(self) -> int: ...
    @channel.setter
    def channel(self, value: int) -> None: ...
    @property
    def crc_length(self) -> rf24_crclength_e: ...
    @crc_length.setter
    def crc_length(self, value: rf24_crclength_e) -> None: ...
    @property
    def tx_delay(self) -> int: ...
    @tx_delay.setter
    def tx_delay(self, value: int) -> None: ...
    @property
    def txDelay(self) -> int: ...
    @txDelay.setter
    def txDelay(self, value: int) -> None: ...
    @property
    def data_rate(self) -> int: ...
    @data_rate.setter
    def data_rate(self, value: rf24_datarate_e) -> None: ...
    @property
    def dynamic_payloads(self) -> bool: ...
    @dynamic_payloads.setter
    def dynamic_payloads(self, value: bool) -> None: ...
    @property
    def failure_detected(self) -> int: ...
    @failure_detected.setter
    def failure_detected(self, value: int) -> None: ...
    @property
    def failureDetected(self) -> int: ...
    @failureDetected.setter
    def failureDetected(self, value: int) -> None: ...
    @property
    def is_chip_connected(self) -> bool: ...
    @property
    def is_plus_variant(self) -> bool: ...
    @property
    def is_valid(self) -> bool: ...
    @property
    def listen(self) -> bool: ...
    @listen.setter
    def listen(self, is_rx: bool) -> None: ...
    @property
    def payload_size(self) -> int: ...
    @payload_size.setter
    def payload_size(self, length: int) -> None: ...
    @property
    def payloadSize(self) -> int: ...
    @payloadSize.setter
    def payloadSize(self, length: int) -> None: ...
    @property
    def pa_level(self) -> rf24_pa_dbm_e: ...
    @pa_level.setter
    def pa_level(self, level: rf24_pa_dbm_e) -> None: ...
    @property
    def power(self) -> bool: ...
    @power.setter
    def power(self, is_on: bool) -> None: ...
    @property
    def rpd(self) -> bool: ...
    @property
    def rx_fifo_full(self) -> bool: ...
