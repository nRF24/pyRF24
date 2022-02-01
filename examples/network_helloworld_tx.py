#!/usr/bin/env python
"""
Simplest possible example of using RF24Network,

TRANSMITTER NODE
Sends messages from to receiver.
"""
import struct
import time
from pyrf24 import RF24, RF24Network, RF24NetworkHeader


radio = RF24(22, 0)
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

while True:
    network.update()
    now = time.monotonic_ns() / 1000000

    # If it's time to send a message, send it!
    if now - LAST_SENT >= INTERVAL:
        LAST_SENT = now
        PACKETS_SENT += 1
        payload = struct.pack("<LL", now, PACKETS_SENT)
        ok = network.write(RF24NetworkHeader(OTHER_NODE), payload)
        print("Sending...", ("ok" if ok else "failed"))
