"""
Simple example of using the RF24 class to transmit and respond with
acknowledgment (ACK) transmissions. Notice that the auto-ack feature is
enabled, but this example doesn't use automatic ACK payloads because automatic
ACK payloads' data will always be outdated by 1 transmission. Instead, this
example uses a call and response paradigm.

See documentation at https://nRF24.github.io/pyRF24
"""

import time
import struct
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER

print(__file__)  # print example name

########### USER CONFIGURATION ###########
# CE Pin uses GPIO number with RPi and SPIDEV drivers, other drivers use
# their own pin numbering
# CS Pin corresponds the SPI bus number at /dev/spidev<a>.<b>
# ie: radio = RF24(<ce_pin>, <a>*10+<b>)
# where CS pin for /dev/spidev1.0 is 10, /dev/spidev1.1 is 11 etc...
CSN_PIN = 0  # aka CE0 on SPI bus 0: /dev/spidev0.0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15  # for GPIO22
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3  # for GPIO22
else:
    CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)

# For this example, we will use different addresses
# An address need to be a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
# It is very helpful to think of an address as a path instead of as
# an identifying device destination

# to use different addresses on a pair of radios, we need a variable to
# uniquely identify which address this radio will use to transmit
# 0 uses address[radio_number] to transmit, 1 uses address[not radio_number] to transmit
radio_number = bool(
    int(input("Which radio is this? Enter '0' or '1'. Defaults to '0' ") or 0)
)

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# set TX address of RX node (uses pipe 0)
radio.stop_listening(address[radio_number])  # enter inactive TX mode

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# To save time during transmission, we'll set the payload size to be only what
# we need. A float value occupies 4 bytes in memory using struct.calcsize()
# "<b" means a little endian unsigned byte
# we also need an addition 7 bytes for the payload message
radio.payload_size = struct.calcsize("<b") + 7

# for debugging
radio.print_pretty_details()

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our float number for the payloads sent
payload = [0]


def master(count: int = 10):
    """Transmits a message and an incrementing integer every second"""
    radio.listen = False  # ensures the nRF24L01 is in TX mode

    while count:  # only transmit `count` packets
        # use struct.pack() to pack your data into a usable payload
        # "<b" means a single little endian unsigned byte.
        # NOTE we added a b"\x00" byte as a c-string's NULL terminating 0
        buffer = b"Hello \x00" + struct.pack("<b", payload[0])
        start_timer = time.monotonic_ns()  # start timer
        result = radio.write(buffer)
        if not result:
            print("Transmission failed or timed out")
        else:
            radio.listen = True
            timeout = time.monotonic() * 1000 + 200  # use 200 ms timeout
            ack = b"\x00" * len(buffer)  # variable used for the response
            while ack[0] == 0 and time.monotonic() * 1000 < timeout:
                if radio.available():
                    # get the response & save it to ack variable
                    ack = radio.read(radio.payload_size)
            end_timer = time.monotonic_ns()  # end timer
            radio.listen = False
            print(
                "Transmission successful. Sent: ",
                f"{buffer[:6].decode('utf-8')}{payload[0]}.",
                end=" ",
            )
            if ack[0] == 0:
                print("No response received.")
            else:
                # decode response's text as an string
                # NOTE ack[:6] ignores the NULL terminating 0
                response = ack[:6].decode("utf-8")
                # use struct.unpack() to get the response's appended int
                # NOTE ack[7:] discards NULL terminating 0, and
                # "<b" means its a single little endian unsigned byte
                payload[0] = struct.unpack("<b", ack[7:])[0]
                print(
                    f"Received: {response}{payload[0]}. Roundtrip delay:",
                    f"{(end_timer - start_timer) / 1000} us.",
                )
        time.sleep(1)  # make example readable by slowing down transmissions
        count -= 1


def slave(timeout: int = 6):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    radio.listen = True  # put radio into RX mode

    start_timer = time.monotonic()  # start a timer to detect timeout
    while (time.monotonic() - start_timer) < timeout:
        # receive payloads or wait 6 seconds till timing out
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            length = radio.payload_size  # grab the payload length
            received = radio.read(length)  # fetch 1 payload from RX FIFO
            # use struct.unpack() to get the payload's appended int
            # NOTE received[7:] discards NULL terminating 0, and
            # "<b" means its a single little endian unsigned byte
            payload[0] = struct.unpack("<b", received[7:])[0] + 1
            # use bytes() to pack our data into a usable payload
            # NOTE b"\x00" byte is a c-string's NULL terminating 0
            buffer = b"World \x00" + bytes([payload[0]])
            radio.listen = False  # set radio to TX mode
            radio.write_fast(buffer)  # load payload into radio's RX buffer
            # keep retrying to send response for 150 milliseconds
            response = radio.tx_standby(150)  # save response's result
            radio.listen = True  # set radio back into RX mode
            # print the payload received and the response's payload
            print(
                f"Received {length} bytes on pipe {pipe_number}:",
                f"{received[:6].decode('utf-8')}{payload[0] - 1}.",
                end=" ",
            )
            if response:
                print(f"Sent: {buffer[:6].decode('utf-8')}{payload[0]}")
            else:
                print("Response failed or timed out")
            start_timer = time.monotonic()  # reset the timeout timer

    # recommended behavior is to keep radio in TX mode while idle
    radio.listen = False  # enter inactive TX mode


def set_role():
    """Set the role using stdin stream. Timeout arg for slave() can be
    specified using a space delimiter (e.g. 'R 10' calls `slave(10)`)

    :return:
        - True when role is complete & app should continue running.
        - False when app should exit
    """
    user_input = (
        input(
            "*** Enter 'R' for receiver role.\n"
            "*** Enter 'T' for transmitter role.\n"
            "*** Enter 'Q' to quit example.\n"
        )
        or "?"
    )
    user_input = user_input.split()
    if user_input[0].upper().startswith("R"):
        slave(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("T"):
        master(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("Q"):
        radio.power = False
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return set_role()


if __name__ == "__main__":
    try:
        while set_role():
            pass  # continue example until 'Q' is entered
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        radio.power = False
else:
    print("    Run slave() on receiver\n    Run master() on transmitter")
