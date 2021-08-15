#include <pybind11/pybind11.h>
#include <RF24.h>
#include <RF24Network.h>

namespace py = pybind11;

class RF24NetworkWrapper : public RF24Network
{
public:

    RF24NetworkWrapper(RF24 &_radio) : RF24Network(_radio)
    {
    }

    uint16_t peek_header(RF24NetworkHeader &header)
    {
        return RF24Network::peek(header);
    }

    std::tuple<RF24NetworkHeader, py::bytearray> peek_frame(uint8_t maxlen = MAX_PAYLOAD_SIZE)
    {
        RF24NetworkHeader header;
        maxlen = static_cast<uint8_t>(rf24_min(maxlen, RF24Network::peek(header)));
        char *buf = new char[maxlen];
        RF24Network::peek(header, buf, maxlen);
        py::bytearray py_ba = py::bytearray(buf, maxlen);
        delete[] buf;
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py_ba);
    }
#if defined (RF24NetworkMulticast)
    bool multicast(RF24NetworkHeader header, char *buf, uint8_t level = 7)
    {
        return RF24Network::multicast(header, buf, static_cast<uint8_t>(strlen(buf)), level);
    }

    void set_multicast_level(uint8_t level)
    {
        RF24Network::multicastLevel(level);
    }

    uint8_t get_multicast_level()
    {
        return RF24Network::_multicast_level;
    }
#endif // defined (RF24NetworkMulticast)

    std::tuple<RF24NetworkHeader, py::bytearray> read(uint16_t maxlen = MAX_PAYLOAD_SIZE)
    {
        char *buf = new char[maxlen];
        RF24NetworkHeader header;
        uint16_t len = RF24Network::read(header, buf, maxlen);
        py::bytearray py_ba = py::bytearray(buf, len);
        delete[] buf;
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py_ba);
    }

    bool write(RF24NetworkHeader &header, char *buf)
    {
        return RF24Network::write(header, buf, static_cast<uint8_t>(strlen(buf)));
    }

    uint16_t get_node_address()
    {
        return RF24Network::node_address;
    }
};


PYBIND11_MODULE(rf24_network, m)
{
    m.doc() = "A Python module that wraps all RF24Network C++ library's API";
    py::options options;
    options.disable_function_signatures();

    // **************** RF24NetworkHeader exposed  *****************
    //
    py::class_<RF24NetworkHeader>(m, "RF24NetworkHeader")
        .def(py::init<>())
        .def(py::init<uint16_t, uint8_t>(), R"docstr(
            __init__(to_node: int = None, type: int = None)

            Create a RF24NetworkHeader object.

            :param int to_node: Set the header's `to_node` attribute.
            :param int type: Set the header's `type` attribute.

            .. hint:: These parameters can be left unspecified to create a blank object that can
                be augmented after instantiation.
        )docstr", py::arg("to"), py::arg("type") = 0)
        .def("to_string", &RF24NetworkHeader::toString, R"docstr(
            to_string() -> str

            A convenience function to represent most of the header's publicly-used attributes as a `str`.

            :Returns: A `str` representing the header's `from_node`, `to_node`, `id`, and `type` attributes.
        )docstr")
        .def_readwrite("from_node", &RF24NetworkHeader::from_node, R"docstr(
            The origin of the frame. This is a logical address (set in octal format).
        )docstr")
        .def_readwrite("id", &RF24NetworkHeader::id, R"docstr(
            The sequential identifying number of the frame. This is not incremented on fragmented
            messages (see `reserved` attribute).
        )docstr")
        .def_readwrite("reserved", &RF24NetworkHeader::reserved, R"docstr(
            A single byte reserved for system usage. This will be the sequential identifying number
            for fragmented frames. On the last fragment, this attribute will contain the actual frame's
            `type`.
        )docstr")
        .def_readwrite("to_node", &RF24NetworkHeader::to_node, R"docstr(
            The destination of the frame. This is a logical address (set in octal format).
        )docstr")
        .def_readwrite("type", &RF24NetworkHeader::type, R"docstr(
            The type of frame sent. Users are encouraged to use an integer in range [0, 127] as
            integers in range [128, 255] are reserved for system usage.
        )docstr")
        .def_readwrite_static("next_id", &RF24NetworkHeader::next_id, R"docstr(
            The next sequential identiying number used for the next created frame. It is not
            advised to alter this attribute.
        )docstr");


    // *********************** RF24Network exposed ******************
    //
    py::class_<RF24NetworkWrapper>(m, "RF24Network")
        .def(py::init<RF24 &>(), R"docstr(
            __init__(radio: RF24)

            Create a RF24Network object.

            :param RF24 radio: The `RF24` object used to control the radio transceiver.
        )docstr", py::arg("radio"))
        .def("available", &RF24NetworkWrapper::available, R"docstr(
            available() -> bool

            :Returns: `True` if there is a frame in the queue, otherwise `False`.
        )docstr")
        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            begin(node_address: int)

            Give the instantiated network node a logical address.

            :param int node_addess: This is a logical address (set in octal format).
        )docstr", py::arg("node_address"))
        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint8_t, uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            If using the deprecated form of this function, the parameters are as follows:

            :param int channel: The desired channel used by the network.

                .. seealso:: Use :py:attr:`~pyrf24.rf24.RF24.channel` attribute to change the radio
                    channel.
            :param int node_address: This is a logical address (set in octal format).
        )docstr", py::arg("channel"), py::arg("node_address"))
        .def_property("node_address", &RF24NetworkWrapper::get_node_address, static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            The instantiated network node's logical address. This is a 2-byte integer in octal format.
        )docstr")

        // .def("parent", &RF24NetworkWrapper::parent, R"docstr(
        //     parent -> int

        //     The logical address (in octal) of the parent to the instantiated network node.
        // )docstr")
        .def_property_readonly("parent", &RF24NetworkWrapper::parent, R"docstr(
            The logical address (in octal) of the parent to the instantiated network node.
        )docstr")

        .def("read", &RF24NetworkWrapper::read, R"docstr(
            read(maxlen: int = 144) -> Tuple(RF24NetworkHeader, bytearray)

            Fetch the next available frame received by the network node. This differs from `peek()` as it removes the frame from the queue.

            :param int maxlen: The maximum length of the frame's message to be returned. If this parameter is unspecified, then the entire
                length of the frame's message is returned.

            :Returns: A `tuple` in which

                - index 0 is the frame's `RF24NetworkHeader`
                - index 1 is the frame's message (as a mutable `bytearray`)
        )docstr", py::arg("maxlen") = MAX_PAYLOAD_SIZE)
        .def("peek", &RF24NetworkWrapper::peek_header, R"docstr(
            peek(arg: Union(RF24NetworkHeader, int)) -> Union(int, Tuple(RF24NetworkHeader, bytearray))
            To fetch the next available frame's header received by the network node, the parameter and return type is as follows:

            :param RF24NetworkHeader header: The object to save the header information to.
            :Returns: The frame's message size (not including the 8-byte header saved to the ``header`` parameter).
        )docstr", py::arg("header"))
        .def("peek", &RF24NetworkWrapper::peek_frame, R"docstr(
            To fetch the next available frame received by the network node, the parameter and return type is as follows:

            :param int maxlen: The maximum length of the message to fetch. If this parameter is unspecified or greater than
                the actual frame's message size, then only the frame's full message size is used.

            :Returns: A 2-tuple containing the frame's header (of type `RF24NetworkHeader`) and the frame's message (of type `bytearray`).
        )docstr", py::arg("maxlen") = MAX_PAYLOAD_SIZE)
        .def("update", &RF24NetworkWrapper::update, R"docstr(
            update() -> int

            Keep the network layer current. This function should be called regularly in the application.
            For applications that have a long-running operations in 1 "loop"/iteration, then it is advised to call this function more than once.

            :Returns: the `int` of the last received header's :py:attr:`~pyrf24.rf24_network.RF24NetworkHeader.type`
        )docstr")
        .def("write", &RF24NetworkWrapper::write, R"docstr(
            write(header: RF24NetworkHeader, buf: bytes) -> bool

            Send an outgoing frame over the network.

            :param RF24NetworkHeader header: The outgoing frame's `RF24NetworkHeader` about the outgoing message.
            :param bytes,bytearray buf: The outgoing frame's message (AKA buffer).

            :Returns: `True` if the frame was succefully sent or otherwise `False`.
        )docstr", py::arg("header"), py::arg("buf"))
#if defined RF24NetworkMulticast
        .def_property("multicast_level", &RF24NetworkWrapper::get_multicast_level, &RF24NetworkWrapper::set_multicast_level, R"docstr(
            The network level of the instantiated network node used for multicasted frames. Setting this attribute will override the
            default value set by `begin()` or `node_address`.
        )docstr")
        // .def("set_multicast_level", &RF24NetworkWrapper::multicastLevel, R"docstr(
        //     Set the network level of the instantiated network node used for multicasted frames. Using this function will override the
        //     default value set by `begin()` or `node_address`.
        // )docstr")
        .def("multicast", &RF24NetworkWrapper::multicast, R"docstr(
            multicast(header: RF24NetworkHeader, buf: bytes, level: int = 7) -> bool

            Broadcast a message to all nodes in a network level.

            :param RF24NetworkHeader header: The outgoing frame's header. The only value of this
                object that is not overridden by this function is the `RF24NetworkHeader.type` attribute.
            :param bytes,bytearray buf: The outgoing frame's message (AKA buffer).
            :param int level: The network level to broadcast the message to. If this parameter is not specified,
                then the current network level of the instantiated node is used (see `multicast_level`).

            :Returns: This function will always return `True` as multicasted messages do not use the radio's auto-ack feature.
        )docstr", py::arg("header"), py::arg("buf"), py::arg("level") = 7)
        .def_readwrite("multicast_relay", &RF24NetworkWrapper::multicastRelay, R"docstr(
            This attribute detirmines if any received multicasted messages should be forwarded to the next highest network level.
            Defaults to `False`.
        )docstr")
#endif // defined RF24NetworkMulticast
        .def("is_address_valid", &RF24NetworkWrapper::is_valid_address, R"docstr(
            is_address_valid(address: int) -> bool

            Use this function to verify if an integer can be used as a valid logical address for network nodes.

            :param int address: The integer to validate.

            :Returns: `True` if the given integer is a valid logical address, otherwise `False`.
        )docstr", py::arg("address"))
        .def_readwrite("tx_timeout", &RF24NetworkWrapper::txTimeout, R"docstr(
            The timeout value (in milliseconds) to ensure a frame is properly sent. Defaults to 25.
        )docstr")
        .def_readwrite("route_timeout", &RF24Network::routeTimeout, R"docstr(
            The timeout value (in milliseconds) used to wait for a Network ACK message. Defaults to 75.
        )docstr")
        .def_readwrite("return_sys_msgs", &RF24Network::returnSysMsgs, R"docstr(
            This `bool` attribute is used by RF24Mesh to force
            :py:meth:`~pyrf24.rf24_network.RF24Network.update()` to return when handling a frame containing a system message.
        )docstr")
        .def_readwrite("network_flags", &RF24Network::networkFlags, R"docstr(
            A 4-bit integer used to indicate special system behavior. Currently only bit positions 2 and 3 are used.
        )docstr");
}
