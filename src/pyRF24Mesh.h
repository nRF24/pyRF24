#include <pybind11/pybind11.h>
#include "pyRF24Network.cpp"
#include <RF24Mesh.h>

namespace py = pybind11;

class RF24MeshWrapper : public RF24Mesh
{
public:
    RF24MeshWrapper(RF24Wrapper& _radio, RF24NetworkWrapper& _network)
        : RF24Mesh(static_cast<RF24&>(_radio), static_cast<RF24Network&>(_network))
    {
    }

    // needed for polymorphic recognition
    virtual ~RF24MeshWrapper() = default;

    bool write(py::buffer buf, uint8_t msg_type, uint8_t nodeID = 0)
    {
        return RF24Mesh::write(
            get_bytes_or_bytearray_str(buf),
            msg_type,
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            nodeID);
    }

    bool write(uint16_t to_node, py::buffer buf, uint8_t msg_type)
    {
        return RF24Mesh::write(
            to_node,
            get_bytes_or_bytearray_str(buf),
            msg_type,
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)));
    }

    uint8_t get_node_id()
    {
        return RF24Mesh::_nodeID;
    }

    py::list get_addrList()
    {
        py::list list;
        for (uint8_t i = 0; i < RF24Mesh::addrListTop; ++i) {
            list.append(RF24Mesh::addrList[i]);
        }
        return list;
    }
};
