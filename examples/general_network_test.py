"""
An all-purpose example of using the nRF24L01 transceiver in a network of nodes.

See documentation at https://nRF24.github.io/pyRF24
"""

import time
import struct
from pyrf24 import (
    RF24,
    RF24Network,
    RF24NetworkHeader,  # only need to construct frame headers for RF24Network.write()
    RF24Mesh,
    MAX_PAYLOAD_SIZE,
    MESH_DEFAULT_ADDRESS,
    RF24_PA_LOW,
    RF24_DRIVER,
)

print(__file__)  # print example name

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

IS_MESH = (
    (
        input("Would you like to run as a mesh network node (y/n)? Defaults to 'Y' ")
        or "Y"
    )
    .upper()
    .startswith("Y")
)

# to use different addresses on a set of radios, we need a variable to
# uniquely identify this radio.
THIS_NODE = 0
print(
    "Remember, the master node always uses `0` as the mesh_address and node_id."
    "\nWhich node is this? Enter",
    end=" ",
)
if IS_MESH:
    # node_id must be less than 256
    THIS_NODE = int(input("a unique int. Defaults to '0' ") or "0") & 0xFF
else:
    # logical node_address is in octal
    THIS_NODE = int(input("an octal int. Defaults to '0' ") or "0", 8)

if not radio.begin():
    # this is done with mesh.begin(), but it helps to check if the radio hardware is ok
    raise OSError("radio hardware not responding")
print("    radio hardware initialized")
if IS_MESH:
    mesh.node_id = THIS_NODE
    if THIS_NODE:
        print(f"Connecting to mesh network as node_id {THIS_NODE}...", end=" ")
    else:
        print("Acting as mesh master node.")
    # RF24Mesh C++ library uses channel 97 by default
    if not mesh.begin():
        print("failed. Try again with mesh.renew_address()")
    elif THIS_NODE:
        print(f"ok. Using assigned address {oct(mesh.mesh_address)}")
else:
    # C++ examples use channel 90 for RF24Network library
    radio.channel = 90
    network.begin(THIS_NODE)
    if THIS_NODE:
        print(f"Using network address {oct(THIS_NODE)}.")
    else:
        print("Acting as network master node.")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity
radio.pa_level = RF24_PA_LOW

# This example covers fragmented payloads also. Set a sentinel for readability.
MAX_FRAG_SIZE = 24

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our number of the payloads sent
packets_sent = [0]


def idle(timeout: int = 30, strict_timeout: bool = False):
    """Listen for any payloads and print the transaction

    :param int timeout: The number of seconds to wait (with no transmission)
        until exiting function.
    :param bool strict_timeout: If set to True, then the timer is not reset when
        processing incoming traffic
    """
    print("idling for", timeout, "seconds")
    start_timer = time.monotonic()
    while (time.monotonic() - start_timer) < timeout:
        if IS_MESH and mesh.update() and not mesh.node_id:
            # if this is a mesh master node and update() returned a non-zero value
            mesh.dhcp()  # only needed for master node
        else:
            network.update()  # keep the network layer current
        while network.available():
            if not strict_timeout:
                start_timer = time.monotonic()  # reset timer
            header, payload = network.read()
            payload_len = len(payload)
            print("Received payload", end=" ")
            # C++ examples only use 1 or 2 long ints as small messages
            if payload_len < MAX_FRAG_SIZE and payload_len % 4 == 0:
                # if not a large fragmented message and multiple of 4 bytes
                fmt = "<" + "L" * int(payload_len / 4)
                print(struct.unpack(fmt, payload), end=" ")
            print(header.to_string(), "length", payload_len)


def emit(
    node: int = not THIS_NODE, frag: bool = False, count: int = 5, interval: int = 1
):
    """Transmits 1 (or 2) integers or a large buffer

    :param int node: The target node for network transmissions.
        If using RF24Mesh, this is a unique node_id.
        If using RF24Network, this is the node's logical address.
    :param bool frag: Only use fragmented messages?
    :param int count: The max number of messages to transmit.
    :param int interval: time (in seconds) between transmitting messages.
    """
    while count:
        # for this example, we use idle() to update() the network/mesh layer
        idle(interval, True)  # idle till its time to emit
        count -= 1
        packets_sent[0] += 1
        # TMRh20's RF24Mesh examples use 1 long int containing a timestamp (in ms)
        message = struct.pack("<L", int(time.monotonic() * 1000))
        if frag:
            message = bytes(range((packets_sent[0] + MAX_FRAG_SIZE) % MAX_PAYLOAD_SIZE))
        elif not IS_MESH:  # if using RF24Network
            # TMRh20's RF24Network examples use 2 long ints, so add another
            message += struct.pack("<L", packets_sent[0])
        result = False
        start = time.monotonic_ns()
        if IS_MESH:  # write() is a little different for RF24Mesh vs RF24Network
            result = mesh.write(message, ord("M"), node)
        else:
            result = network.write(RF24NetworkHeader(node, ord("T")), message)
        end = time.monotonic_ns()
        print(
            f"Sending {packets_sent[0]} (len {len(message)})...",
            "ok." if result else "failed.",
            f"Transmission took {int((end - start) / 1000000)} ms",
        )


def set_role():
    """Set the role using stdin stream. Timeout arg for idle() can be
    specified using a space delimiter (e.g. 'I 10' calls `idle(10)`)
    """
    prompt = (
        "*** Enter 'I' for idle role.\n"
        "*** Enter 'E <node number>' for emitter role.\n"
        "*** Enter 'E <node number> 1' to emit fragmented messages.\n"
    )
    if IS_MESH and THIS_NODE:  # if a mesh node and not a master node
        if mesh.mesh_address == MESH_DEFAULT_ADDRESS:
            prompt += "!!! Mesh node not connected.\n"
        prompt += "*** Enter 'C' to connect to to mesh master node.\n"
    user_input = (input(prompt + "*** Enter 'Q' to quit example.\n") or "?").split()
    if user_input[0].upper().startswith("C") and IS_MESH:
        print("Connecting to mesh network...", end=" ")
        result = mesh.renew_address(*[int(x) for x in user_input[1:2]])
        result = result != MESH_DEFAULT_ADDRESS
        print(("assigned address " + oct(mesh.mesh_address)) if result else "failed.")
        return True
    if user_input[0].upper().startswith("I"):
        idle(*[int(x) for x in user_input[1:3]])
        return True
    if user_input[0].upper().startswith("E"):
        emit(*[int(x) for x in user_input[1:5]])
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
        print(" Keyboard Interrupt detected. Powering down radio...")
        radio.power = False
elif IS_MESH and mesh.mesh_address != MESH_DEFAULT_ADDRESS:
    print("    Run idle() to receive or forward messages in the network.")
    print("    Run emit(<node number>) to transmit.")
    print("    Pass keyword arg `frag=True` to emit() fragmented messages.")
