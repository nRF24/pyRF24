"""
Example of using the rf24_mesh module to operate the nRF24L01 transceiver as
a Mesh network master node.

See documentation at https://nRF24.github.io/pyRF24
"""

from pyrf24 import RF24, RF24Network, RF24Mesh, RF24_DRIVER

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
mesh = RF24Mesh(radio, network)
mesh.node_id = 0
if not mesh.begin():
    # if mesh.begin() returns false for a master node,
    # then radio.begin() returned false.
    raise OSError("Radio hardware not responding.")
radio.print_pretty_details()

try:
    while True:
        mesh.update()
        mesh.dhcp()

        while network.available():
            header, payload = network.read()
            print(f"Received message {header.to_string()}")
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
