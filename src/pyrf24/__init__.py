# pylint: disable=import-error,missing-module-docstring
from .rf24 import (
    RF24,
    RF24_CRC_DISABLED,
    RF24_CRC_8,
    RF24_CRC_16,
    RF24_1MBPS,
    RF24_2MBPS,
    RF24_250KBPS,
    RF24_PA_MIN,
    RF24_PA_LOW,
    RF24_PA_HIGH,
    RF24_PA_MAX,
)
from .rf24_network import (
    RF24Network,
    RF24NetworkHeader,
    # RF24NetworkFrame,
    MAX_USER_DEFINED_HEADER_TYPE,
    MAX_PAYLOAD_SIZE,
    NETWORK_ADDR_RESPONSE,
    NETWORK_PING,
    EXTERNAL_DATA_TYPE,
    NETWORK_FIRST_FRAGMENT,
    NETWORK_MORE_FRAGMENTS,
    NETWORK_LAST_FRAGMENT,
    NETWORK_ACK,
    NETWORK_POLL,
    NETWORK_REQ_ADDRESS,
    FLAG_FAST_FRAG,
    FLAG_NO_POLL,
)
from .rf24_mesh import (
    RF24Mesh,
    MESH_DEFAULT_ADDRESS,
    MESH_ADDR_LOOKUP,
    MESH_ADDR_RELEASE,
    MESH_ID_LOOKUP,
)


def address_repr(buf, reverse: bool = True, delimit: str = "") -> str:
    """Convert a buffer into a hexlified string."""
    order = range(len(buf) - 1, -1, -1) if reverse else range(len(buf))
    return delimit.join(["%02X" % buf[byte] for byte in order])
