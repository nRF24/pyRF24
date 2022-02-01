"""
Simple example of using the library to transmit
and retrieve custom automatic acknowledgment payloads.
"""
import time
from pyrf24 import RF24, RF24_PA_LOW

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use
# their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..

# Generic:
radio = RF24(22, 0)

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our integer number for the payloads' counter
counter = [0]

# For this example, we will use different addresses
# An address need to be a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
# It is very helpful to think of an address as a path instead of as
# an identifying device destination

# to use different addresses on a pair of radios, we need a variable to
# uniquely identify which address this radio will use to transmit
# 0 uses address[0] to transmit, 1 uses address[1] to transmit
radio_number = bool(
    int(
        input(
            "Which radio is this? Enter '0' or '1'. Defaults to '0' "
        ) or 0
    )
)

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# ACK payloads are dynamically sized, so we need to enable that feature also
radio.dynamic_payloads = True

# to enable the custom ACK payload feature
radio.enable_ack_payload()

# set TX address of RX node into the TX pipe
radio.open_tx_pipe(address[radio_number])  # always uses pipe 0

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# for debugging
radio.print_pretty_details()


def master(count=5):  # count = 5 will only transmit 5 packets
    """Transmits a payload every second and prints the ACK payload"""
    radio.listen = False  # put radio in TX mode

    while count:
        # construct a payload to send
        buffer = b"Hello \x00" + bytes([counter[0]])

        # send the payload and prompt
        start_timer = time.monotonic_ns()  # start timer
        result = radio.write(buffer)  # save the report
        end_timer = time.monotonic_ns()  # stop timer
        if result:
            # print timer results upon transmission success
            print(
                "Transmission successful! Time to transmit:",
                f"{int((end_timer - start_timer) / 1000)} us. Sent:",
                f"{buffer[:6].decode('utf-8')}{counter[0]}",
                end=" "
            )
            if radio.available():
                # print the received ACK that was automatically sent
                result = radio.read(radio.get_dynamic_payload_size())
                print(f" Received: {result[:6].decode('utf-8')}{result[7:8][0]}")
                counter[0] += 1  # increment payload counter
            else:
                print(" Received an empty ACK packet")
        else:
            print("Transmission failed or timed out")
        time.sleep(1)  # let the RX node prepare a new ACK payload
        count -= 1


def slave():
    """Prints the received value and sends an ACK payload"""
    radio.listen = True  # put radio into RX mode, power it up

    # setup the first transmission's ACK payload
    buffer = b"World \x00" + bytes([counter[0]])
    # we must set the ACK payload data and corresponding
    # pipe number [0,5]
    radio.write_ack_payload(1, buffer)  # load ACK for first response

    start = time.monotonic()  # start timer
    while (time.monotonic() - start) < 6:  # use 6 second timeout
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            length = radio.get_dynamic_payload_size()  # grab the payload length
            received = radio.read(length)  # fetch 1 payload from RX FIFO
            # increment counter from received payload
            counter[0] = received[7:8][0] + 1
            print(
                f"Received {length} bytes on pipe {pipe_number}:",
                f"{received[:6].decode('utf-8')}{received[7:8][0]} Sent:",
                f"{buffer[:6].decode('utf-8')}{counter[0]}"
            )
            start = time.monotonic()  # reset timer

            # build a new ACK payload
            buffer = b"World \x00" + bytes([counter[0]])
            radio.write_ack_payload(1, buffer)  # load ACK for next response

    # recommended behavior is to keep in TX mode while idle
    radio.listen = False  # put radio in TX mode & flush unused ACK payloads


print(
    """\
    nRF24L01 ACK test\n\
    Run slave() on receiver\n\
    Run master() on transmitter"""
)
