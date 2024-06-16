#!/usr/bin/env python
"""
Simplest possible example of using RF24Network.

TRANSMITTER NODE
Sends messages from to receiver.

See documentation at https://nRF24.github.io/pyRF24
"""

import struct
import time
from pyrf24 import RF24, RF24Network, RF24NetworkHeader, RF24_DRIVER

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
network = RF24Network(radio)

# Address of our node in Octal format (01,021, etc)
THIS_NODE = 0o1

# Address of the other node
OTHER_NODE = 0o0

# milliseconds - How long to wait before sending the next message
INTERVAL = 2000


# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.channel = 90
network.begin(THIS_NODE)
radio.print_pretty_details()

PACKETS_SENT = 0
LAST_SENT = time.monotonic_ns() / 1000000

try:
    while True:
        network.update()
        now = int(time.monotonic_ns() / 1000000)

        # If it's time to send a message, send it!
        if now - LAST_SENT >= INTERVAL:
            LAST_SENT = now
            PACKETS_SENT += 1
            payload = struct.pack("<LL", now, PACKETS_SENT)
            ok = network.write(RF24NetworkHeader(OTHER_NODE), payload)
            print(f"Sending {PACKETS_SENT}...", ("ok" if ok else "failed"))
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
