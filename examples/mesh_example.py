"""
Simplest RF24Mesh example that transmits a time stamp (in milliseconds) 1 per second.
"""

import sys
import time
import struct
from pyrf24 import RF24, RF24Network, RF24Mesh, MESH_DEFAULT_ADDRESS, RF24_DRIVER

start = time.monotonic()


def millis():
    """:Returns: Delta time since started example in milliseconds. Wraps value around
    the width of a ``long`` integer."""
    return int((time.monotonic() - start) * 1000) % (2**32)


CSN_PIN = 0  # aka CE0 on SPI bus 0: /dev/spidev0.0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15  # for GPIO22
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3  # for GPIO22
else:
    CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

mesh.node_id = 4
print("starting nodeID", mesh.node_id)
if not mesh.begin():
    if radio.is_chip_connected:
        try:
            print("Could not connect to network.\nConnecting to mesh...")
            while mesh.renew_address() == MESH_DEFAULT_ADDRESS:
                print("Could not connect to network.\nConnecting to mesh...")
        except KeyboardInterrupt:
            radio.power = False
            sys.exit()
    else:
        raise OSError("Radio hardware not responding or could not connect to mesh.")
radio.print_pretty_details()

TIMER = 0

try:
    while True:
        # Call mesh.update to keep the network updated
        mesh.update()

        if (millis() - TIMER) >= 1000:
            TIMER = millis()

            if not mesh.write(struct.pack("L", TIMER), ord("M")):
                # If a write fails, check connectivity to the mesh network
                if not mesh.check_connection():
                    # The address could be refreshed per a specified time frame
                    # or only when sequential writes fail, etc.
                    print("Send fail. Renewing Address...")
                    while mesh.renew_address() == MESH_DEFAULT_ADDRESS:
                        print("Renewing Address...")
                else:
                    print("Send fail, Test OK")
            else:
                print("Send OK:", TIMER)
        time.sleep(0.001)  # delay 1 ms
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
