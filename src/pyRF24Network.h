#include <pybind11/pybind11.h>
#include "pyRF24.h"
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
    RF24NetworkWrapper(RF24Wrapper& _radio) : RF24Network(static_cast<RF24&>(_radio))
    {
    }

    // needed for polymorphic recognition
    virtual ~RF24NetworkWrapper() = default;

    uint16_t peek_header(RF24NetworkHeader& header)
    {
        return RF24Network::peek(header);
    }

    std::tuple<RF24NetworkHeader, py::bytearray> peek_frame(uint16_t maxlen = MAX_PAYLOAD_SIZE)
    {
        RF24NetworkHeader header;
        maxlen = static_cast<uint16_t>(rf24_min(maxlen, RF24Network::peek(header)));
        char* buf = new char[maxlen + 1];
        RF24Network::peek(header, buf, maxlen);
        py::bytearray py_ba = py::bytearray(buf, maxlen);
        delete[] buf;
        return std::tuple<RF24NetworkHeader, py::bytearray>(header, py_ba);
    }

#if defined(RF24NetworkMulticast)
    bool multicast(RF24NetworkHeader header, py::buffer buf, uint8_t level = 7)
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

    bool write(RF24NetworkHeader& header, py::buffer buf, uint16_t writeDirect = NETWORK_AUTO_ROUTING)
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
