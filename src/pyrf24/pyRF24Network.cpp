#include "RF24.h"
#include "RF24Network.h"
#include "pybind11/pybind11.h"

namespace py = pybind11;

class RF24NetworkWrapper : public RF24Network
{
public:

    RF24NetworkWrapper(RF24 & radio) : RF24Network(radio)
    {
    }

    uint16_t peek_header(RF24NetworkHeader &header)
    {
        return RF24Network::peek(header);
    }

    std::tuple<RF24NetworkHeader, py::bytearray> peek_frame(uint8_t maxlen = MAX_PAYLOAD_SIZE)
    {
        RF24NetworkHeader header;
        maxlen = rf24_min(maxlen, RF24Network::peek(header));
        char buf[maxlen];
        RF24Network::peek(header, buf, maxlen);
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py::bytearray(buf, maxlen));
    }
#if defined (RF24NetworkMulticast)
    bool multicast(RF24NetworkHeader header, char *buf, uint8_t level = 7)
    {
        return RF24Network::multicast(header, buf, strlen(buf), level);
    }

    void set_multicast_level(uint8_t level)
    {
        RF24Network::multicast_level(level);
    }

    uint8_t get_multicast_level()
    {
        return RF24Network::_multicast_level;
    }
#endif // defined (RF24NetworkMulticast)

    std::tuple<RF24NetworkHeader, py::bytearray> read(size_t maxlen = MAX_PAYLOAD_SIZE)
    {
        char *buf = new char[maxlen + 1];
        RF24NetworkHeader header;

        uint16_t len = RF24Network::read(header, buf, maxlen);
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py::bytearray(buf, len));
    }

    bool write(RF24NetworkHeader &header, char *buf)
    {
        return RF24Network::write(header, buf, strlen(buf));
    }

    uint16_t get_node_address()
    {
        return RF24Network::_node_address;
    }
};


PYBIND11_MODULE(rf24_network, m)
{
    // **************** RF24NetworkHeader exposed  *****************
    //
    py::class_<RF24NetworkHeader>(m, "RF24NetworkHeader")
        .def(py::init<>())
        .def(py::init<uint16_t>())
        .def(py::init<uint16_t, uint8_t>())
        .def("to_string", &RF24NetworkHeader::toString)
        .def_readwrite("from_node", &RF24NetworkHeader::from_node)
        .def_readwrite("id", &RF24NetworkHeader::id)
        .def_readwrite("reserved", &RF24NetworkHeader::reserved)
        .def_readwrite("to_node", &RF24NetworkHeader::to_node)
        .def_readwrite("type", &RF24NetworkHeader::type)
        .def_readwrite_static("next_id", &RF24NetworkHeader::next_id);


    // *********************** RF24Network exposed ******************
    //
    py::class_<RF24NetworkWrapper>(m, "RF24Network")
        .def(py::init<RF24 &>())
        .def("available", &RF24NetworkWrapper::available)
        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin))
        .def("begin", static_cast<void (RF24NetworkWrapper::*)(uint8_t, uint16_t)>(&RF24NetworkWrapper::begin))
        .def_property("node_address", &RF24NetworkWrapper::get_node_address, static_cast<void (RF24NetworkWrapper::*)(uint16_t)>(&RF24NetworkWrapper::begin))

        .def("parent", &RF24NetworkWrapper::parent)
        .def_property_readonly("parent", &RF24NetworkWrapper::parent)

        .def("read", &RF24NetworkWrapper::read, py::arg("maxlen") = MAX_PAYLOAD_SIZE)
        .def("peek", &RF24NetworkWrapper::peek_header)
        .def("peek", &RF24NetworkWrapper::peek_frame, py::arg("maxlen") = MAX_PAYLOAD_SIZE)
        .def("update", &RF24NetworkWrapper::update)
        .def("write", &RF24NetworkWrapper::write, py::arg("header"), py::arg("buf"))
#if defined RF24NetworkMulticast
        .def_property("multicast_level", &RF24NetworkWrapper::get_multicast_level, &RF24NetworkWrapper::set_multicast_level)
        .def("multicast_level", &RF24NetworkWrapper::multicastLevel)
        .def("multicast", &RF24NetworkWrapper::multicast, py::arg("header"), py::arg("buf"), py::arg("level") = 7)
        .def_readwrite("multicast_relay", &RF24NetworkWrapper::multicastRelay)
#endif // defined RF24NetworkMulticast
        .def("is_valid_address", &RF24NetworkWrapper::is_valid_address)
        .def_readwrite("tx_timeout", &RF24NetworkWrapper::txTimeout)
        .def_readwrite("routeTimeout", &RF24Network::routeTimeout)
        .def_readwrite("networkFlags", &RF24Network::networkFlags);
}
