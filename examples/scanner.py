"""
This is an example of how to use the nRF24L01's builtin
Received Power Detection (RPD) to scan for possible interference.
This example does not require a counterpart node.
"""
# pylint: disable=consider-using-f-string
import time
from pyrf24 import RF24, RF24_CRC_DISABLED, address_repr


########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use
# their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..
radio = RF24(22, 0)

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# turn off RX features specific to the nRF24L01 module
radio.set_auto_ack(False)
radio.dynamic_payloads = False
radio.crc_length = RF24_CRC_DISABLED
radio.set_retries(0, 0)

# use reverse engineering tactics for a better "snapshot"
radio.address_width = 2
radio.open_rx_pipe(0, b"\x55\x55")
radio.open_rx_pipe(1, b"\xAA\xAA")
radio.open_rx_pipe(2, b"\xA0\xAA")
radio.open_rx_pipe(3, b"\x0A\xAA")
radio.open_rx_pipe(4, b"\xA5\xAA")
radio.open_rx_pipe(5, b"\x5A\xAA")

def scan(timeout: int = 30):
    """Traverse the spectrum of accessible frequencies and print any detection
    of ambient signals.

    :param int timeout: The number of seconds in which scanning is performed.
    """
    # print the vertical header of channel numbers
    print("0" * 100 + "1" * 26)
    for i in range(13):
        print(str(i % 10) * (10 if i < 12 else 6), sep="", end="")
    print("")  # endl
    for i in range(126):
        print(str(i % 10), sep="", end="")
    print("\n" + "~" * 126)

    signals = [0] * 126  # store the signal count for each channel
    curr_channel = 0
    start_timer = time.monotonic()  # start the timer
    while time.monotonic() - start_timer < timeout:
        radio.channel = curr_channel
        radio.listen = 1  # start a RX session
        time.sleep(0.00013)  # wait 130 microseconds
        found_signal = radio.rpd
        radio.listen = 0  # end the RX session
        found_signal = found_signal or radio.rpd or radio.available()

        # count signal as interference
        signals[curr_channel] += found_signal
        # clear the RX FIFO if a signal was detected/captured
        if found_signal:
            radio.flush_rx()  # flush the RX FIFO because it asserts the RPD flag
        curr_channel = curr_channel + 1 if curr_channel < 125 else 0

        # output the signal counts per channel
        sig_cnt = signals[curr_channel]
        print(
            ("%X" % min(15, sig_cnt)) if sig_cnt else "-",
            sep="",
            end="" if curr_channel < 125 else "\r",
        )
    # finish printing results and end with a new line
    while curr_channel < len(signals) - 1:
        curr_channel += 1
        sig_cnt = signals[curr_channel]
        print(("%X" % min(15, sig_cnt)) if sig_cnt else "-", sep="", end="")
    print("")


def noise(timeout: int = 1, channel: int = None):
    """print a stream of detected noise for duration of time.

    :param int timeout: The number of seconds to scan for ambient noise.
    :param int channel: The specific channel to focus on. If not provided, then the
        radio's current setting is used.
    """
    if channel is not None:
        radio.channel = channel
    radio.listen = True
    timeout += time.monotonic()
    while time.monotonic() < timeout:
        signal = radio.read(radio.payload_size)
        if signal:
            print(address_repr(signal, False, " "))
    radio.listen = False
    while not radio.is_fifo(False, True):
        # dump the left overs in the RX FIFO
        print(address_repr(radio.read(), False, " "))


def set_role():
    """Set the role using stdin stream. Timeout arg for scan() can be
    specified using a space delimiter (e.g. 'S 10' calls `scan(10)`)
    """
    user_input = (
        input(
            "*** Enter 'S' to perform scan.\n"
            "*** Enter 'N' to display noise.\n"
            "*** Enter 'Q' to quit example.\n"
        ) or "?"
    )
    user_input = user_input.split()
    if user_input[0].upper().startswith("S"):
        scan(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("N"):
        noise(*[int(x) for x in user_input[1:3]])
        return True
    if user_input[0].upper().startswith("Q"):
        radio.power = False
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return set_role()


print("    nRF24L01 scanner test")
print(
    "!!!Make sure the terminal is wide enough for 126 characters on 1 line."
    " If this line is wrapped, then the output will look bad!"
)

if __name__ == "__main__":
    try:
        while set_role():
            pass  # continue example until 'Q' is entered
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Powering down radio...")
        radio.power = False
else:
    print("    Run scan() to initiate scan for ambient signals.")
    print("    Run noise() to display ambient signals' data (AKA noise).")
