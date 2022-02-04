"""
Simple example of using 1 nRF24L01 to receive data from up to 6 other
transceivers. This technique is called "multiceiver" in the datasheet.
"""
import sys
import argparse
import time
import struct
from pyrf24 import RF24, RF24_PA_LOW

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use
# their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..
radio = RF24(22, 0)

# setup the addresses for all transmitting nRF24L01 nodes
addresses = [
    b"\x78" * 5,
    b"\xF1\xB6\xB5\xB4\xB3",
    b"\xCD\xB6\xB5\xB4\xB3",
    b"\xA3\xB6\xB5\xB4\xB3",
    b"\x0F\xB6\xB5\xB4\xB3",
    b"\x05\xB6\xB5\xB4\xB3",
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
# A byte and an int occupy 5 bytes in memory using struct.calcsize()
# "<bi" means a little endian unsigned byte and int
radio.payload_size = struct.calcsize("<bi")

# for debugging
radio.print_pretty_details()


def base(timeout=10):
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
            node_id, payload_id = struct.unpack("<bi", radio.read(8))
            # show the pipe number that received the payload
            print(
                f"Received {length} bytes on pipe {pipe_number} from node {node_id}.",
                f"PayloadID: {payload_id}",
            )
            start_timer = time.monotonic()  # reset timer with every payload
    radio.listen = False


def node(node_number: int = 0, count: int = 10):
    """start transmitting to the base station.

    :param int node_number: the node's identifying index (from the
        the `addresses` list). This is a required parameter
    :param int count: the number of times that the node will transmit
        to the base station.
    """
    radio.listen = False
    # set the TX address to the address of the base station.
    radio.open_tx_pipe(addresses[node_number])
    counter = 0
    # use the node_number to identify where the payload came from
    while counter < count:
        counter += 1
        # payloads will include the node_number and a payload ID character
        payload = struct.pack("<bi", node_number, counter)
        start_timer = time.monotonic_ns()
        report = radio.write(payload)
        end_timer = time.monotonic_ns()
        # show something to see it isn't frozen
        if report:
            print(
                f"Transmission of payloadID {counter} as node {node_number} successfull!",
                f"Transmission time: {(end_timer - start_timer) / 1000} us",
            )
        else:
            print("Transmission failed or timed out")
        time.sleep(0.5)  # slow down the test for readability


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
        base(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("T"):
        node(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("Q"):
        radio.power = False
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return set_role()


print(sys.argv[0])  # print example name


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-r",
        "--role",
        type=int,
        choices=range(2),
        help="'1' specifies the TX role. '0' specifies the RX role.",
    )
    args = parser.parse_args()  # parse any CLI args

    try:
        if args.role is None:  # if not specified with CLI arg '-r'
            while set_role():
                pass  # continue example until 'Q' is entered
        elif bool(args.role):  # if role was set using CLI args, run role once and exit
            node()
        else:
            base()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        radio.power = False
        sys.exit()
else:
    print("    Run base() on the receiver\n    Run node(node_number) on a transmitter")
    print("        node()'s parameter, `node_number`, must be in range [0, 5]")
