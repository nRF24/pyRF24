"""
Simple example of using 1 nRF24L01 to receive data from up to 6 other
transceivers. This technique is called "multiceiver" in the datasheet.

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

# setup the addresses for all transmitting nRF24L01 nodes
addresses = [
    b"\x78" * 5,
    b"\xf1\xb6\xb5\xb4\xb3",
    b"\xcd\xb6\xb5\xb4\xb3",
    b"\xa3\xb6\xb5\xb4\xb3",
    b"\x0f\xb6\xb5\xb4\xb3",
    b"\x05\xb6\xb5\xb4\xb3",
]
# It is very helpful to think of an address as a path instead of as
# an identifying device destination

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# To save time during transmission, we'll set the payload size to be only what
# we need.
# 2 int occupy 8 bytes in memory using len(struct.pack())
# "<ii" means 2x little endian unsigned int
radio.payload_size = struct.calcsize("<ii")

# for debugging
radio.print_pretty_details()


def master(node_number: int = 0, count: int = 6):
    """start transmitting to the base station.

    :param int node_number: the node's identifying index (from the
        the `addresses` list). This is a required parameter
    :param int count: the number of times that the node will transmit
        to the base station.
    """
    # According to the datasheet, the auto-retry features's delay value should
    # be "skewed" to allow the RX node to receive 1 transmission at a time.
    # So, use varying delay between retry attempts and 15 (at most) retry attempts
    radio.set_retries(((node_number * 3) % 12) + 3, 15)  # max value is 15 for both args

    radio.listen = False
    # set the TX address to the address of the base station.
    radio.open_tx_pipe(addresses[node_number])
    counter = 0
    # use the node_number to identify where the payload came from
    while counter < count:
        counter += 1
        # payloads will include the node_number and a payload ID character
        payload = struct.pack("<ii", node_number, counter)
        start_timer = time.monotonic_ns()
        report = radio.write(payload)
        end_timer = time.monotonic_ns()
        # show something to see it isn't frozen
        if report:
            print(
                f"Transmission of payloadID {counter} as node {node_number}",
                f"successful! Transmission time: {(end_timer - start_timer) / 1000}",
                "us",
            )
        else:
            print("Transmission failed or timed out")
        time.sleep(0.5)  # slow down the test for readability


def slave(timeout=10):
    """Use the nRF24L01 as a base station for listening to all nodes"""
    # write the addresses to all pipes.
    for pipe_n, addr in enumerate(addresses):
        radio.open_rx_pipe(pipe_n, addr)
    radio.listen = True  # put base station into RX mode
    start_timer = time.monotonic()  # start timer
    while time.monotonic() - start_timer < timeout:
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            length = radio.payload_size  # grab the payload length
            # unpack payload
            node_id, payload_id = struct.unpack("<ii", radio.read(radio.payload_size))
            # show the pipe number that received the payload
            print(
                f"Received {length} bytes on pipe {pipe_number} from node {node_id}.",
                f"PayloadID: {payload_id}",
            )
            start_timer = time.monotonic()  # reset timer with every payload
    radio.listen = False


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
            "    Use 'T n' to transmit as node n; n must be in range [0, 5].\n"
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
    print("    Run slave() on the receiver")
    print("    Run master(node_number) on a transmitter")
    print("        master()'s parameter, `node_number`, must be in range [0, 5]")
