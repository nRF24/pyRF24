#include "RF24.h"
#include "RF24Network.h"
#include "RF24Mesh.h"
#include "pybind11/pybind11.h"

namespace py = pybind11;

class RF24MeshWrapper : public RF24Mesh
{
public:
    RF24MeshWrapper(RF24 &radio, RF24Network &network) : RF24Mesh(radio, network)
    {
    }

    bool write(char *buf, uint8_t msg_type, uint8_t nodeID = 0)
    {
        return RF24Mesh::write(buf, msg_type, strlen(buf), nodeID);
    }

    bool write(uint16_t to_node, char *buf, uint8_t msg_type)
    {
        return RF24Mesh::write(to_node, buf, msg_type, strlen(buf));
    }
};


PYBIND11_MODULE(rf24_mesh, m)
{
    py::class_<RF24MeshWrapper>(m, "RF24Mesh")
        .def(py::init<RF24 &, RF24Network &>())
        .def("begin", &RF24MeshWrapper::begin)
        .def("update", &RF24MeshWrapper::update)
        .def("write", static_cast<bool (RF24MeshWrapper::*)(char *, uint8_t, uint8_t)>(&RF24MeshWrapper::write), py::arg("buf"), py::arg("msg_type"), py::arg("node_id") = 0)
        .def("write", static_cast<bool (RF24MeshWrapper::*)(uint16_t, char *, uint8_t)>(&RF24MeshWrapper::write))
        // .def_property("node_id", &RF24MeshWrapper::_nodeID, &RF24MeshWrapper::setNodeID)
        .def_readwrite("mesh_address", &RF24MeshWrapper::mesh_address)
        .def("set_node_id", &RF24MeshWrapper::setNodeID)
        .def("get_node_id", &RF24MeshWrapper::getNodeID)
        .def("dhcp", &RF24MeshWrapper::DHCP)
        .def("check_connection", &RF24MeshWrapper::checkConnection)
        .def("renew_address", &RF24MeshWrapper::renewAddress)
        .def("release_address", &RF24MeshWrapper::releaseAddress)
        .def("get_address", &RF24MeshWrapper::getAddress)
        .def("set_channel", &RF24MeshWrapper::setChannel)
        .def("set_child", &RF24MeshWrapper::setChild)
        .def("set_address", &RF24MeshWrapper::setAddress)
        .def("save_dhcp", &RF24MeshWrapper::saveDHCP)
        .def("load_dhcp", &RF24MeshWrapper::loadDHCP)
        .def("set_static_address", &RF24MeshWrapper::setStaticAddress);
}
