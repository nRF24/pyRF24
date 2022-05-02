#include <pybind11/pybind11.h>
#include "pyRF24.cpp"
#include <RF24Network.h>
// #include <queue>
// #include <pybind11/stl.h>

namespace py = pybind11;

/* 
namespace pybind11 {
namespace detail {

    template<typename Type, typename Alloc>
    struct type_caster<std::queue<Type, Alloc>> : list_caster<std::queue<Type, Alloc>, Type>
    {
    };
} // namespace detail
} // namespace pybind11

struct RF24NetworkFrameWrapper : public RF24NetworkFrame
{
    RF24NetworkFrameWrapper() : RF24NetworkFrame()
    {
    }

    RF24NetworkFrameWrapper(RF24NetworkHeader& header, py::object message)
    {
        RF24NetworkFrame::header = header;
        set_message(message);
    }

    py::bytearray get_message()
    {
        char* buf = new char[RF24NetworkFrame::message_size];
        memcpy(reinterpret_cast<uint8_t*>(buf), RF24NetworkFrame::message_buffer, RF24NetworkFrame::message_size);
        py::bytearray py_ba = py::bytearray(buf, RF24NetworkFrame::message_size);
        delete[] buf;
        return py_ba;
    }

    void set_message(py::object message)
    {
        RF24NetworkFrame::message_size = static_cast<uint16_t>(get_bytes_or_bytearray_ln(message));
        memcpy(RF24NetworkFrame::message_buffer, reinterpret_cast<uint8_t*>(get_bytes_or_bytearray_str(message)), RF24NetworkFrame::message_size);
    }
};
*/
class RF24NetworkWrapper : public RF24Network
{
public:
    RF24NetworkWrapper(RF24Wrapper& _radio) : RF24Network(_radio)
    {
    }

    // needed for polymorphic recognition
    virtual ~RF24NetworkWrapper() = default;

    uint16_t peek_header(RF24NetworkHeader& header)
    {
        return RF24Network::peek(header);
    }

    std::tuple<RF24NetworkHeader, py::bytearray> peek_frame(uint8_t maxlen = MAX_PAYLOAD_SIZE)
    {
        RF24NetworkHeader header;
        maxlen = static_cast<uint8_t>(rf24_min(maxlen, RF24Network::peek(header)));
        char* buf = new char[maxlen + 1];
        RF24Network::peek(header, buf, maxlen);
        py::bytearray py_ba = py::bytearray(buf, maxlen);
        delete[] buf;
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py_ba);
    }

#if defined(RF24NetworkMulticast)
    bool multicast(RF24NetworkHeader header, py::object buf, uint8_t level = 7)
    {
        return RF24Network::multicast(
            header,
            get_bytes_or_bytearray_str(buf),
            static_cast<uint16_t>(get_bytes_or_bytearray_ln(buf)),
            level);
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
        char* buf = new char[maxlen + 1];
        RF24NetworkHeader header;
        uint16_t len = RF24Network::read(header, buf, maxlen);
        py::bytearray py_ba = py::bytearray(buf, len);
        delete[] buf;
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py_ba);
    }

    bool write(RF24NetworkHeader& header, py::object buf, uint16_t writeDirect = NETWORK_AUTO_ROUTING)
    {
        return RF24Network::write(
            header,
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            writeDirect);
    }

    uint16_t get_node_address()
    {
        return RF24Network::node_address;
    }
};

PYBIND11_MODULE(rf24_network, m)
{
    m.doc() = "A Python module that wraps the RF24Network C++ library's API";
    py::options options;
    options.disable_function_signatures();

    // **************** Module level constants *********************
    //
    m.attr("MAX_USER_DEFINED_HEADER_TYPE") = MAX_USER_DEFINED_HEADER_TYPE;
    m.attr("MAX_PAYLOAD_SIZE") = MAX_PAYLOAD_SIZE;
    m.attr("NETWORK_ADDR_RESPONSE") = NETWORK_ADDR_RESPONSE;
    m.attr("NETWORK_PING") = NETWORK_PING;
    m.attr("EXTERNAL_DATA_TYPE") = EXTERNAL_DATA_TYPE;
    m.attr("NETWORK_FIRST_FRAGMENT") = NETWORK_FIRST_FRAGMENT;
    m.attr("NETWORK_MORE_FRAGMENTS") = NETWORK_MORE_FRAGMENTS;
    m.attr("NETWORK_LAST_FRAGMENT") = NETWORK_LAST_FRAGMENT;
    m.attr("NETWORK_ACK") = NETWORK_ACK;
    m.attr("NETWORK_POLL") = NETWORK_POLL;
    m.attr("NETWORK_REQ_ADDRESS") = NETWORK_REQ_ADDRESS;
    m.attr("FLAG_FAST_FRAG") = FLAG_FAST_FRAG;
    m.attr("FLAG_NO_POLL") = FLAG_NO_POLL;

    // **************** RF24NetworkHeader exposed  *****************
    //
    py::class_<RF24NetworkHeader>(m, "RF24NetworkHeader")
        .def(py::init<>(), R"docstr(
            __init__() \
            __init__(to_node: int, type: int = 0)
        )docstr")

        // *****************************************************************************

        .def(py::init<uint16_t, uint8_t>(), R"docstr(
            Create a RF24NetworkHeader object.

            :param int to_node: Set the header's `to_node` attribute.
            :param int type: Set the header's `type` attribute.
                Default value is ``0`` if the ``to_node`` parameter is specified.

            .. hint:: These parameters can be left unspecified to create a blank object that can
                be augmented after instantiation. However, the header's ``RF24NetworkHeader.next_id``
                is not automatically incremented when no parameters are given.
        )docstr",
             py::arg("to_node"), py::arg("type") = 0)

        // *****************************************************************************

        .def("to_string", &RF24NetworkHeader::toString, R"docstr(
            to_string() -> str

            A convenience function to represent most of the header's publicly-used attributes as a `str`.

            :Returns: A `str` representing the header's `from_node`, `to_node`, `id`, and `type` attributes.
        )docstr")

        // *****************************************************************************

        .def_readwrite("from_node", &RF24NetworkHeader::from_node, R"docstr(
            The origin of the frame. This is a `Logical Address <logical_address>` (set in octal format).
        )docstr")

        // *****************************************************************************

        .def_readwrite("id", &RF24NetworkHeader::id, R"docstr(
            The sequential identifying number of the frame. This is not incremented on fragmented
            messages (see `reserved` attribute).
        )docstr")

        // *****************************************************************************

        .def_readwrite("reserved", &RF24NetworkHeader::reserved, R"docstr(
            A single byte reserved for system usage. This will be the sequential identifying number
            for fragmented frames. On the last fragment, this attribute will contain the actual frame's
            `type`.
        )docstr")

        // *****************************************************************************

        .def_readwrite("to_node", &RF24NetworkHeader::to_node, R"docstr(
            The destination of the frame. This is a `Logical Address <logical_address>` (set in octal format).
        )docstr")

        // *****************************************************************************

        .def_readwrite("type", &RF24NetworkHeader::type, R"docstr(
            The type of frame sent. Users are encouraged to use an integer in range [0, 127]
            because integers in range [128, 255] are reserved for system usage.

            .. seealso:: :ref:`reserved_sys_msgs`

        )docstr")

        // *****************************************************************************

        .def_readonly_static("next_id", &RF24NetworkHeader::next_id, R"docstr(
            The next sequential identifying number used for the next created frame.
        )docstr")

        // *****************************************************************************

        .def("__repr__", [](RF24NetworkHeader& obj) { return std::string("<RF24NetworkHeader ") + std::string(obj.toString()) + std::string(">"); });

    // *********************** RF24NetworkFrame exposed ******************
    /*
    py::class_<RF24NetworkFrameWrapper>(m, "RF24NetworkFrame")
        .def(py::init<RF24NetworkHeader&, py::object>(), R"docstr(
            __init__(header: RF24NetworkHeader = None, message: Union[bytes, bytearray] = None)

            :param RF24NetworkHeader header: The RF24NetworkHeader associated with the frame.
            :param bytes,bytearray message: The 'message' or data.
        )docstr")

        // *****************************************************************************

        .def(py::init<>(), R"docstr(
            .. tip::
                Simply constructs a blank frame with no parameters. Frames are generally used internally.
                See :py:class:`RF24NetworkHeader`.
        )docstr")

        // *****************************************************************************

        .def_readwrite("header", &RF24NetworkFrameWrapper::header, R"docstr(
            The :py:class:`~pyrf24.rf24_network.RF24NetworkHeader` object about the frame's message.
        )docstr")

        // *****************************************************************************

        .def_property("message_buffer", &RF24NetworkFrameWrapper::get_message, &RF24NetworkFrameWrapper::set_message, R"docstr(
            The frame's message buffer. This is typically a `bytearray`.
        )docstr")

        // *****************************************************************************

        .def_readonly("message_size", &RF24NetworkFrameWrapper::message_size, R"docstr(
            A read-only attribute that returns the length of the message. This is set accordingly
            when the :py:attr:`~pyrf24.rf24_network.RF24NetworkFrame.message_buffer` is changed.
        )docstr");
    */

    // *********************** RF24Network exposed ******************
    //
    py::class_<RF24NetworkWrapper>(m, "RF24Network")
        .def(py::init<RF24Wrapper&>(), R"docstr(
            __init__(radio: RF24)

            Create a RF24Network object.

            :param RF24 radio: The `RF24` object used to control the radio transceiver.
        )docstr",
             py::arg("radio"))

        // *****************************************************************************

        .def("available", &RF24NetworkWrapper::available, R"docstr(
            available() -> bool

            :Returns: `True` if there is a frame in the queue, otherwise `False`.
        )docstr")

        // *****************************************************************************

        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            begin(node_address: int) \
            begin(channel: int, node_address: int)

            Give the instantiated network node a `Logical Address <logical_address>`.

            :param int node_address: This is a `Logical Address <logical_address>` (typically an octal integer).
        )docstr",
             py::arg("node_address"))

        // *****************************************************************************

        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint8_t, uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            :param int channel: The desired channel used by the network.
                Using this parameter is the deprecated form of this function.

                .. seealso:: Use :py:attr:`~pyrf24.rf24.RF24.channel` attribute to change the radio
                    channel.
        )docstr",
             py::arg("channel"), py::arg("node_address"))

        // *****************************************************************************

        .def_property("node_address", &RF24NetworkWrapper::get_node_address, static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin), R"docstr(
            The instantiated network node's `Logical Address <logical_address>`. This is a 2-byte integer in octal format.
        )docstr")

        // *****************************************************************************

        // .def("parent", &RF24NetworkWrapper::parent, R"docstr(
        //     parent -> int

        //     The `Logical Address <logical_address>` (in octal) of the parent to the instantiated network node.
        // )docstr")

        // *****************************************************************************

        .def_property_readonly("parent", &RF24NetworkWrapper::parent, R"docstr(
            The `Logical Address <logical_address>` (in octal) of the parent to the instantiated network node.

            :Returns:
                This node's parent address, or 65535 if this is the master node.
        )docstr")

        // *****************************************************************************

        .def("read", &RF24NetworkWrapper::read, R"docstr(
            read(maxlen: int = 144) -> Tuple[RF24NetworkHeader, bytearray]

            Fetch the next available frame received by the network node. This differs from `peek()` as it removes the frame from the queue.

            :param int maxlen: The maximum length of the frame's message to be returned. If this parameter is unspecified, then the entire
                length of the frame's message is returned.

            :Returns: A `tuple` in which

                - index 0 is the frame's `RF24NetworkHeader`
                - index 1 is the frame's message (as a mutable `bytearray`)
        )docstr",
             py::arg("maxlen") = MAX_PAYLOAD_SIZE)

        // *****************************************************************************

        .def("peek", &RF24NetworkWrapper::peek_header, R"docstr(
            peek(header: RF24NetworkHeader) -> int \
            peek(maxlen: int) -> Tuple[RF24NetworkHeader, bytearray]
            To fetch the next available frame's header received by the network node, the parameter and return type is as follows:

            :param RF24NetworkHeader header: The object to save the header information to.
            :Returns: The frame's message size (not including the 8-byte header saved to the ``header`` parameter).
        )docstr",
             py::arg("header"))

        // *****************************************************************************

        .def("peek", &RF24NetworkWrapper::peek_frame, R"docstr(
            To fetch the next available frame received by the network node, the parameter and return type is as follows:

            :param int maxlen: The maximum length of the message to fetch. If this parameter is unspecified or greater than
                the actual frame's message size, then only the frame's full message size is used.

            :Returns: A 2-tuple containing the frame's header (of type `RF24NetworkHeader`) and the frame's message (of type `bytearray`).
        )docstr",
             py::arg("maxlen") = MAX_PAYLOAD_SIZE)

        // *****************************************************************************

        .def("update", &RF24NetworkWrapper::update, R"docstr(
            update() -> int

            Keep the network layer current. This function should be called regularly in the application.
            For applications that have a long-running operations in 1 "loop"/iteration, then it is advised to call this function more than once.

            :Returns: The `int` of the last received header's :py:attr:`~pyrf24.rf24_network.RF24NetworkHeader.type`
        )docstr")

        // *****************************************************************************

        .def("write", &RF24NetworkWrapper::write, R"docstr(
            write(header: RF24NetworkHeader, buf: Union[bytes, bytearray], write_direct: int = 0o70) -> bool

            Send an outgoing frame over the network.

            :param RF24NetworkHeader header: The outgoing frame's `RF24NetworkHeader` about the outgoing message.
            :param bytes,bytearray buf: The outgoing frame's message (AKA buffer).
            :param int write_direct: An optional parameter to route the message directly to a specified node.
                The default value will invoke automatic routing.

            :Returns: `True` if the frame was successfully sent or otherwise `False`.
        )docstr",
             py::arg("header"), py::arg("buf"), py::arg("write_direct") = NETWORK_AUTO_ROUTING)

#if defined RF24NetworkMulticast
        // *****************************************************************************

        .def_property("multicast_level", &RF24NetworkWrapper::get_multicast_level, &RF24NetworkWrapper::set_multicast_level, R"docstr(
            The network level of the instantiated network node used for multicasted frames. Setting this attribute will override the
            default value set by `begin()` or `node_address`.
        )docstr")

        // *****************************************************************************

        // .def("set_multicast_level", &RF24NetworkWrapper::multicastLevel, R"docstr(
        //     Set the network level of the instantiated network node used for multicasted frames. Using this function will override the
        //     default value set by `begin()` or `node_address`.
        // )docstr")

        // *****************************************************************************

        .def("multicast", &RF24NetworkWrapper::multicast, R"docstr(
            multicast(header: RF24NetworkHeader, buf: Union[bytes, bytearray], level: int = 7) -> bool

            Broadcast a message to all nodes in a network level.

            :param RF24NetworkHeader header: The outgoing frame's header. The only value of this
                object that is not overridden by this function is the `RF24NetworkHeader.type` attribute.
            :param bytes,bytearray buf: The outgoing frame's message (AKA buffer).
            :param int level: The network level to broadcast the message to. If this parameter is not specified,
                then the current network level of the instantiated node is used (see `multicast_level`).

            :Returns: This function will always return `True` as multicasted messages do not use the radio's auto-ack feature.
        )docstr",
             py::arg("header"), py::arg("buf"), py::arg("level") = 7)

        // *****************************************************************************

        .def_readwrite("multicast_relay", &RF24NetworkWrapper::multicastRelay, R"docstr(
            This `bool` attribute determines if any received multicasted messages should be forwarded to the next highest network level.
            Defaults to `False`.
        )docstr")
#endif // defined RF24NetworkMulticast

        // *****************************************************************************

        .def("is_address_valid", &RF24NetworkWrapper::is_valid_address, R"docstr(
            is_address_valid(address: int) -> bool

            Use this function to verify if an integer can be used as a valid `Logical Address <logical_address>` for network nodes.

            :param int address: The integer to validate.

            :Returns: `True` if the given integer is a valid `Logical Address <logical_address>`, otherwise `False`.
        )docstr",
             py::arg("address"))

        // *****************************************************************************

        .def_readwrite("tx_timeout", &RF24NetworkWrapper::txTimeout, R"docstr(
            The timeout `int` value (in milliseconds) to ensure a frame is properly sent. Defaults to 25.
        )docstr")

        // *****************************************************************************

        .def_readwrite("route_timeout", &RF24Network::routeTimeout, R"docstr(
            The timeout `int` value (in milliseconds) used to wait for a Network ACK message. Defaults to 75.
        )docstr")

        // *****************************************************************************

        .def_readwrite("return_sys_msgs", &RF24Network::returnSysMsgs, R"docstr(
            This `bool` attribute is used by RF24Mesh to force :py:meth:`~pyrf24.rf24_network.RF24Network.update()`
            to return when handling a frame containing a system message.

            When this attribute is enabled, the following system messages are not returned because they are handled
            internally.

            .. csv-table::
                :header: Message Name, Numeric Value, Additional Context

                :py:attr:`~pyrf24.rf24_network.NETWORK_ADDR_RESPONSE`, 128, 
                :py:attr:`~pyrf24.rf24_network.NETWORK_ACK`, 193,
                :py:attr:`~pyrf24.rf24_network.NETWORK_PING`, 130,
                :py:attr:`~pyrf24.rf24_network.NETWORK_POLL`, 194,  With multicast enabled (which is enabled by default)
                :py:attr:`~pyrf24.rf24_network.NETWORK_REQ_ADDRESS`, 195,
            
            .. seealso::
                There's a more complete list (with behavioral descriptions) of the :ref:`reserved_sys_msgs`.
        )docstr")

        // *****************************************************************************

        /// TODO: need to write a custom type caster for std::queue to expose the external_queue member
        // .def_readwrite("external_queue", &RF24NetworkWrapper::external_queue, R"docstr(
        //     Data with a header type of :py:attr:`~pyrf24.rf24_network.EXTERNAL_DATA_TYPE` will be loaded into a separate queue.
        // )docstr")

        // *****************************************************************************

        /// TODO: Optionally expose the frame_buffer member as mutable bytearray (or immutable bytes) object.

        // *****************************************************************************

        .def_readwrite("network_flags", &RF24Network::networkFlags, R"docstr(
            A 4-bit integer used to indicate special system behavior. Currently only bit positions 2 and 3 are used.

            .. csv-table::
                :header: Flags, Value, Description

                :py:attr:`~pyrf24.rf24_network.FLAG_FAST_FRAG`, 4 (bit 2 asserted), INTERNAL: Replaces the fastFragTransfer variable and allows for faster transfers between directly connected nodes.
                :py:attr:`~pyrf24.rf24_network.FLAG_NO_POLL`, 8 (bit 3 asserted), EXTERNAL/USER: Disables NETWORK_POLL responses on a node-by-node basis.
        )docstr");
}
