"""
Simple example of detecting (and verifying) the IRQ (interrupt) pin on the
nRF24L01
"""

import sys
import time
import RPi.GPIO as GPIO
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER

# RPi.GPIO will show a warning if any pin is setup() that is already been
# setup() for use without calling cleanup() first
GPIO.cleanup()  # call this now in case it wasn't called on last program exit

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use
# their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..
CSN_PIN = 0  # aka CE0 on SPI bus 0: /dev/spidev0.0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15  # for GPIO22
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3  # for GPIO22
else:
    CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)

# select your digital input pin that's connected to the IRQ pin on the nRF24L01
IRQ_PIN = 12

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

# this example uses the ACK payload to trigger the IRQ pin active for
# the "on data received" event
radio.ack_payloads = True  # enable ACK payloads

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# set TX address of RX node into the TX pipe
radio.open_tx_pipe(address[radio_number])  # always uses pipe 0

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# for debugging
radio.print_pretty_details()

# For this example, we'll be using a payload containing
# a string that changes on every transmission. (successful or not)
# Make a couple tuples of payloads & an iterator to traverse them
pl_iterator = [0]  # use a 1-item list instead of python's global keyword
tx_payloads = (b"Ping ", b"Pong ", b"Radio", b"1FAIL")
ack_payloads = (b"Yak ", b"Back", b" ACK")


def interrupt_handler():
    """This function is called when IRQ pin is detected active LOW"""
    print("IRQ pin went active LOW.")
    tx_ds, tx_df, rx_dr = radio.what_happened()  # update IRQ status flags
    print(f"\ttx_ds: {tx_ds}, tx_df: {tx_df}, rx_dr: {rx_dr}")
    if pl_iterator[0] == 0 and rx_dr:
        print("'data ready' event test", ("passed" if rx_dr else "failed"))
    elif pl_iterator[0] == 1:
        print("'data sent' event test", ("passed" if tx_ds else "failed"))
    elif pl_iterator[0] == 2:
        print("'data fail' event test", ("passed" if tx_df else "failed"))


# setup IRQ GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(IRQ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IRQ_PIN, GPIO.FALLING, callback=interrupt_handler)


def _wait_for_irq():
    """Wait till IRQ_PIN goes active then inactive.
    IRQ pin is LOW when activated. Otherwise it is always HIGH

    In this example, the "data fail" event is always configured to
    trigger the IRQ pin active. Because the auto-ACK feature is on by
    default, the timeout in GPIO.wait_for_edge() is inconsequential.
    """
    # wait up to 1 second for event to be cleared.
    # GPIO.RISING means whatHappened() was called.
    channel = GPIO.wait_for_edge(IRQ_PIN, GPIO.RISING, timeout=1000)
    if channel is None:  # channel should be equal to GPIO.HIGH
        raise RuntimeError("Interrupt event not detected. Check your wiring.")
    # wait for half a second for interrupt_handler() to complete
    time.sleep(0.5)


def master():
    """Transmits 3 times: successfully receive ACK payload first, successfully
    transmit on second, and intentionally fail transmit on the third"""
    radio.listen = False  # ensures the nRF24L01 is in TX mode

    # on data ready test
    print("\nConfiguring IRQ pin to only ignore 'on data sent' event")
    radio.mask_irq(True, False, False)  # args = tx_ds, tx_df, rx_dr
    print("    Pinging slave node for an ACK payload...", end=" ")
    pl_iterator[0] = 0
    radio.start_write(tx_payloads[0], False)  # False means expecting an ACK
    _wait_for_irq()

    # on "data sent" test
    print("\nConfiguring IRQ pin to only ignore 'on data ready' event")
    radio.mask_irq(False, False, True)  # args = tx_ds, tx_df, rx_dr
    print("    Pinging slave node again...             ", end=" ")
    pl_iterator[0] = 1
    radio.start_write(tx_payloads[1], False)  # False means expecting an ACK
    _wait_for_irq()

    # trigger slave node to exit by filling the slave node's RX FIFO
    print("\nSending one extra payload to fill RX FIFO on slave node.")
    if radio.write(tx_payloads[2]):
        # when send_only parameter is True, send() ignores RX FIFO usage
        print("Slave node should not be listening anymore.")
    else:
        print("Slave node was unresponsive.")

    # on "data fail" test
    print("\nConfiguring IRQ pin to go active for all events.")
    radio.mask_irq(False, False, False)  # args = tx_ds, tx_df, rx_dr
    print("    Sending a ping to inactive slave node...", end=" ")
    radio.flush_tx()  # just in case any previous tests failed
    pl_iterator[0] = 2
    radio.start_write(tx_payloads[3], False)  # False means expecting an ACK
    _wait_for_irq()
    radio.flush_tx()  # flush artifact payload in TX FIFO from last test
    # all 3 ACK payloads received were 4 bytes each, and RX FIFO is full
    # so, fetching 12 bytes from the RX FIFO also flushes RX FIFO
    print("\nComplete RX FIFO:", radio.read(12))


def slave(timeout=6):  # will listen for 6 seconds before timing out
    """Only listen for 3 payload from the master node"""
    # setup radio to receive pings, fill TX FIFO with ACK payloads
    radio.write_ack_payload(1, ack_payloads[0])
    radio.write_ack_payload(1, ack_payloads[1])
    radio.write_ack_payload(1, ack_payloads[2])
    radio.listen = True  # start listening & clear irq_dr flag
    start_timer = time.monotonic()  # start timer now
    while not radio.is_fifo(False, False) and time.monotonic() - start_timer < timeout:
        # if RX FIFO is not full and timeout is not reached, then keep waiting
        pass
    time.sleep(0.5)  # wait for last ACK payload to transmit
    radio.listen = False  # put radio in TX mode & discard any ACK payloads
    if radio.available():  # if RX FIFO is not empty (timeout did not occur)
        # all 3 payloads received were 5 bytes each, and RX FIFO is full
        # so, fetching 15 bytes from the RX FIFO also flushes RX FIFO
        print("Complete RX FIFO:", radio.read(15))


print(
    f"""\
    {sys.argv[0]}\n\
    Make sure the IRQ pin is connected to the RPi GPIO12\n\
    Run slave() on receiver\n\
    Run master() on transmitter"""
)
