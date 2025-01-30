"""
Example of library usage for streaming multiple payloads.

See documentation at https://nRF24.github.io/pyRF24
"""

import time
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER

print(__file__)  # print example name

########### USER CONFIGURATION ###########
# CE Pin uses GPIO number with RPi and SPIDEV drivers, other drivers use
# their own pin numbering.
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
# 0 uses address[0] to transmit, 1 uses address[1] to transmit
radio_number = bool(
    int(input("Which radio is this? Enter '0' or '1'. Defaults to '0' ") or 0)
)

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# set TX address of RX node into the TX pipe
radio.open_tx_pipe(address[radio_number])  # always uses pipe 0

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# for debugging
radio.print_pretty_details()


def make_buffer(buf_iter: int, size: int = 32):
    """return a list of payloads"""
    # we'll use `size` for the number of payloads in the list and the
    # payloads' length
    # prefix payload with a sequential letter to indicate which
    # payloads were lost (if any)
    buff = bytes([buf_iter + (65 if 0 <= buf_iter < 26 else 71)])
    for j in range(size - 1):
        char = bool(j >= (size - 1) / 2 + abs((size - 1) / 2 - buf_iter))
        char |= bool(j < (size - 1) / 2 - abs((size - 1) / 2 - buf_iter))
        buff += bytes([char + 48])
    return buff


def master(count: int = 1, size: int = 32):
    """Uses all 3 levels of the TX FIFO `RF24.writeFast()`"""
    if size < 6:
        print("setting size to 6;", size, "is not allowed for this test.")
        size = 6

    # save on transmission time by setting the radio to only transmit the
    #  number of bytes we need to transmit
    radio.payload_size = size  # the default is the maximum 32 bytes

    radio.listen = False  # ensures the nRF24L01 is in TX mode
    for cnt in range(count):  # transmit the same payloads this many times
        radio.flush_tx()  # clear the TX FIFO so we can use all 3 levels
        # NOTE the write_only parameter does not initiate sending
        buf_iter = 0  # iterator of payloads for the while loop
        failures = 0  # keep track of manual retries
        start_timer = time.monotonic() * 1000  # start timer
        while buf_iter < size:  # cycle through all the payloads
            buf = make_buffer(buf_iter, size)  # make a payload
            if not radio.write_fast(buf):
                # reception failed; we need to reset the irq_rf flag
                failures += 1  # increment manual retries
                radio.reuse_tx()
                if failures > 99 and buf_iter < 7 and cnt < 2:
                    # we need to prevent an infinite loop
                    print("Make sure slave() node is listening. Quitting master_fifo()")
                    buf_iter = size + 1  # be sure to exit the while loop
                    radio.flush_tx()  # discard all payloads in TX FIFO
                    break
            buf_iter += 1
        radio.failure_detected = 0
        radio.tx_standby()
        failures += radio.failure_detected
        end_timer = time.monotonic() * 1000  # end timer
        print(
            f"Transmission took {end_timer - start_timer} ms with",
            f"{failures} failures detected.",
        )


def slave(timeout: int = 5, size: int = 32):
    """Stops listening after a `timeout` with no response"""
    # set address of TX node into an RX pipe. NOTE you MUST specify

    # save on transmission time by setting the radio to only transmit the
    #  number of bytes we need to transmit
    radio.payload_size = size  # the default is the maximum 32 bytes

    radio.listen = True  # put radio into RX mode and power up
    count = 0  # keep track of the number of received payloads
    start_timer = time.monotonic()  # start timer
    while time.monotonic() < start_timer + timeout:
        if radio.available():
            count += 1
            # retrieve the received packet's payload
            length = radio.get_dynamic_payload_size()
            receive_payload = radio.read(length)
            print(f"Received: {receive_payload} - {count}")
            start_timer = time.monotonic()  # reset timer on every RX payload

    # recommended behavior is to keep in TX mode while idle
    radio.listen = False  # put the nRF24L01 is in TX mode


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
        slave(*[int(x) for x in user_input[1:3]])
        return True
    if user_input[0].upper().startswith("T"):
        master(*[int(x) for x in user_input[1:3]])
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
