"""
This example uses the nRF24L01 as a 'fake' BLE Beacon
"""
import time
from pyrf24 import (
    RF24,
    RF24_PA_LOW,
    RF24_DRIVER,
    FakeBLE,
    chunk,
    address_repr,
    UrlServiceData,
    BatteryServiceData,
    TemperatureServiceData,
)



# initialize the nRF24L01 on the spi bus object as a BLE compliant radio
CSN_PIN = 0  # aka CE0 on SPI bus 0: /dev/spidev0.0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15  # for GPIO22
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3  # for GPIO22
else:
    CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)
ble = FakeBLE(radio)
# On Linux, csn value is a bit coded
#                 0 = bus 0, CE0  # SPI bus 0 is enabled by default
#                10 = bus 1, CE0  # enable SPI bus 2 prior to running this
#                21 = bus 2, CE1  # enable SPI bus 1 prior to running this

if not ble.begin():
    raise OSError("radio hardware not responding")

# the name parameter is going to be its broadcasted BLE name
# this can be changed at any time using the `name` attribute
# ble.name = b"foobar"

# you can optionally set the arbitrary MAC address to be used as the
# BLE device's MAC address. Otherwise this is randomly generated upon
# instantiation of the FakeBLE object.
# ble.mac = b"\x19\x12\x14\x26\x09\xE0"

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceiver in close proximity to the
# BLE scanning application
radio.pa_level = RF24_PA_LOW


def _prompt(remaining):
    if remaining % 5 == 0 or remaining < 5:
        if remaining - 1:
            print(remaining, "advertisements left to go!")
        else:
            print(remaining, "advertisement left to go!")


# create an object for manipulating the battery level data
battery_service = BatteryServiceData()
# battery level data is 1 unsigned byte representing a percentage
battery_service.data = 85


def master(count=50):
    """Sends out the device information."""
    # using the "with" statement is highly recommended if the nRF24L01 is
    # to be used for more than a BLE configuration
    ble.name = b"nRF24L01"
    # include the radio's pa_level attribute in the payload
    ble.show_pa_level = True
    print(
        "available bytes in next payload:",
        ble.len_available(chunk(battery_service.buffer)),
    )  # using chunk() gives an accurate estimate of available bytes
    radio.listen = False  # ensure radio is in TX mode
    for i in range(count):  # advertise data this many times
        if ble.len_available(chunk(battery_service.buffer)) >= 0:
            _prompt(count - i)  # something to show that it isn't frozen
            # broadcast the device name, MAC address, &
            # battery charge info; 0x16 means service data
            ble.advertise(battery_service.buffer, data_type=0x16)
            # channel hoping is recommended per BLE specs
            ble.hop_channel()
            time.sleep(0.5)  # wait till next broadcast
    ble.show_pa_level, ble.name = (False, None)


# create an object for manipulating temperature measurements
temperature_service = TemperatureServiceData()
# temperature's float data has up to 2 decimal places of percision
temperature_service.data = 42.0


def send_temp(count=50):
    """Sends out a fake temperature."""
    ble.name = b"nRF24L01"
    print(
        "available bytes in next payload:",
        ble.len_available(chunk(temperature_service.buffer)),
    )
    radio.listen = False  # ensure radio is in TX mode
    for i in range(count):
        if ble.len_available(chunk(temperature_service.buffer)) >= 0:
            _prompt(count - i)
            # broadcast a temperature measurement; 0x16 means service data
            ble.advertise(temperature_service.buffer, data_type=0x16)
            ble.hop_channel()
            time.sleep(0.2)
    ble.name = None


# use the Eddystone protocol from Google to broadcast a URL as
# service data. We'll need an object to manipulate that also
url_service = UrlServiceData()
# the data attribute converts a URL string into a simplified
# bytes object using byte codes defined by the Eddystone protocol.
url_service.data = "http://www.google.com"
# Eddystone protocol requires an estimated TX PA level at 1 meter
# lower this estimate since we lowered the actual `ble.pa_level`
url_service.pa_level_at_1_meter = -45  # defaults to -25 dBm


def send_url(count=50):
    """Sends out a URL."""
    print(
        "available bytes in next payload:",
        ble.len_available(chunk(url_service.buffer)),
    )
    # NOTE we did NOT set a device name in this with block
    radio.listen = False  # ensure radio is in TX mode
    for i in range(count):
        # URLs easily exceed the nRF24L01's max payload length
        if ble.len_available(chunk(url_service.buffer)) >= 0:
            _prompt(count - i)
            ble.advertise(url_service.buffer, 0x16)
            ble.hop_channel()
            time.sleep(0.2)


def slave(timeout=6):
    """read and decipher BLE payloads for `timeout` seconds."""
    radio.listen = True  # ensure radio is in RX mode
    end_timer = time.monotonic() + timeout
    while time.monotonic() <= end_timer:
        if ble.available():
            result = ble.read()
            print(
                "received payload from MAC address",
                address_repr(result.mac, delimit=":")
            )
            if result.name is not None:
                print("\tdevice name:", result.name)
            if result.pa_level is not None:
                print("\tdevice transmitting PA Level:", result.pa_level, "dbm")
            for service_data in result.data:
                if isinstance(service_data, (bytearray, bytes)):
                    print("\traw buffer:", address_repr(service_data, False, " "))
                else:
                    print("\t" + repr(service_data))
    radio.listen = False  # ensure radio is in TX mode (preferred when idling)


def set_role():
    """Set the role using stdin stream. Count arg for all functions can be
    specified using a space delimiter (e.g. 'T 10' calls `send_temp(10)`)
    """
    user_input = (
        input(
            "*** Enter 'M' to broadcast the device name, pa_level, & battery"
            " charge.\n"
            "*** Enter 'T' to broadcast the device name & a temperature\n"
            "*** Enter 'U' to broadcast a custom URL link\n"
            "*** Enter 'R' to receive BLE payloads\n"
            "*** Enter 'Q' to quit example.\n"
        )
        or "?"
    )
    user_input = user_input.split()
    if user_input[0].upper().startswith("M"):
        master(*[int(x) for x in user_input[1:]])
        return True
    if user_input[0].upper().startswith("T"):
        send_temp(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("U"):
        send_url(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("R"):
        slave(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("Q"):
        ble.power = False
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return set_role()


print("    nRF24L01 fake BLE beacon test")

if __name__ == "__main__":
    try:
        while set_role():
            pass  # continue example until 'Q' is entered
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Powering down radio...")
        ble.power = False
else:
    print("    Run master() to broadcast the device name, pa_level, & battery charge")
    print("    Run send_temp() to broadcast the device name & a temperature")
    print("    Run send_url() to broadcast a custom URL link")
    print("    Run slave() to receive BLE payloads.")
