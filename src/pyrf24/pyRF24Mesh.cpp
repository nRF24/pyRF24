#include <pybind11/pybind11.h>
#include <RF24.h>
#include <RF24Network.h>
#include <RF24Mesh.h>

namespace py = pybind11;

class RF24MeshWrapper : public RF24Mesh
{
public:
    RF24MeshWrapper(RF24 &_radio, RF24Network &_network) : RF24Mesh(_radio, _network)
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

    uint8_t get_node_id()
    {
        return RF24Mesh::_nodeID;
    }
};


PYBIND11_MODULE(rf24_mesh, m)
{
    m.doc() = "A Python module that wraps all RF24Mesh C++ library's API";
    py::options options;
    options.disable_function_signatures();

    py::class_<RF24MeshWrapper>(m, "RF24Mesh")
        .def(py::init<RF24 &, RF24Network &>(), R"docstr(
            __init__(radio: RF24, network: RF24Network)

            Create a RF24Mesh object.

            :param RF24 radio: The `RF24` object used to control the radio.
            :param RF24Network network: The `RF24Network` object used to provide the base
                networking layer.
        )docstr", py::arg("radio"), py::arg("network"))
        .def("begin", &RF24MeshWrapper::begin, R"docstr(
            begin() -> bool

            :Returns: `True` if the radio's hardware was properly intialized and the node
                successfully connected to the mesh network.

                .. seealso:: Use `renew_address()` in the event that the node becomes disconnected
                    from the mesh network.
        )docstr")
        .def("update", &RF24MeshWrapper::update, R"docstr(
            update() -> int

            Keep the mesh network layer current. This function should be called regularly in the application.
            For applications that have a long-running operations in 1 "loop"/iteration, then it is advised to call this function more than once.

            :Returns: the `int` of the last received header's :py:attr:`~pyrf24.rf24_network.RF24NetworkHeader.type`
        )docstr")
        .def("write", static_cast<bool (RF24MeshWrapper::*)(char *, uint8_t, uint8_t)>(&RF24MeshWrapper::write), R"docstr(
            write(buf: bytes, message_type: int, to_node_id: int = 0) -> bool

            Transmit a message to a unique `node_id` of a mesh network node.

            :param bytes,bytearray buf: The message to transmit.
            :param int message_type: The :py:attr:`~pyrf24.rf24_network.RF24NetworkHeader.type` to
                be used in the frame's header.
            :param int node_id: The destination node's unique `node_id`. If this parameter is not
                specified, then the message is sent to the mesh network's master node.

            :Returns: `True` if the message was successfully sent, otherwise `False`
        )docstr", py::arg("buf"), py::arg("msg_type"), py::arg("node_id") = 0)
        .def("write", static_cast<bool (RF24MeshWrapper::*)(uint16_t, char *, uint8_t)>(&RF24MeshWrapper::write), R"docstr(
            When the network node's logical address is already known, the parameters to
            Transmit a message to a specific logical address of a network node are as follows:

            :param int node_address: The destination node's logical address.
            :param bytes,bytearray buf: The message to transmit.
            :param int message_type: The :py:attr:`~pyrf24.rf24_network.RF24NetworkHeader.type` to
                be used in the frame's header.

            :Returns: `True` if the message was successfully sent, otherwise `False`
        )docstr")
        .def_property("node_id", &RF24MeshWrapper::getNodeID, &RF24MeshWrapper::setNodeID, R"docstr(
            The instantiated RF24Mesh object's unique identifying number. This value must range [0, 255].
        )docstr")
        .def_readwrite("mesh_address", &RF24MeshWrapper::mesh_address, R"docstr(
            The assigned logical address (in octal) given to the node by the mesh network's master node.
        )docstr")
        .def("set_node_id", &RF24MeshWrapper::setNodeID, R"docstr(
            Configure the `node_id` attribute.
        )docstr")
        .def("get_node_id", &RF24MeshWrapper::getNodeID, R"docstr(
            get_node_id(address: int) -> int

            Translates a `node_id` into the corresponding `mesh_address`

            :param int address: The logical address for which to the `node_id` is assigned.

            :Returns:

                - A positive `int` that represents the assigned address.
                - A negative `int` that represents a transaction failure.

                  * ``-1`` means the given does not have an assigned `node_id`.
                  * ``-2`` means the mesh network's master node could not be reached to fetch the data.
        )docstr")
        .def("dhcp", &RF24MeshWrapper::DHCP, R"docstr(
            dhcp()

            Keep the master node's list of assigned addresses up-to-date.

            .. tip:: This function should be called on mesh network's master nodes only just after
                calling :py:meth:`~pyrf24.rf24_mesh.RF24Mesh.update()`.
        )docstr")
        .def("check_connection", &RF24MeshWrapper::checkConnection, R"docstr(
            check_connection() -> bool

            Check for connectivity with the mesh network.

            .. seealso:: Use `renew_address()` to reconnect to the mesh network.

            :Returns: `True` if connected, otherwise `False`
        )docstr")
        .def("renew_address", &RF24MeshWrapper::renewAddress, R"docstr(
            renew_address(timeout: Union(int, float) = 7.5) -> int

            Attempt to get a new logical address assigned from the mesh network's master node.

            :param int,float timeout: The maximum amount of time (in seconds) spent while attempting
                to communicate with the mesh network's master node.

            :Retruns:
                - If successful, this function returns the newly assigned logical address.
                - If unsuccessfull, the returned integer will be the default address used by any
                  node not connected to the mesh network. This default address is ``0o4444`` (or
                  ``2340`` in decimal).
        )docstr", py::arg("timeout") = 7.5)
        .def("release_address", &RF24MeshWrapper::releaseAddress, R"docstr(
            release_address() -> bool

            Use this function to manually expire a leased logical address from the mesh network's master node.

            .. tip:: This function allows re-use of the assigned address for other mesh network nodes.
                Call this function from mesh network nodes that are going offline (or to sleep).

            :Returns: `True` if the mesh network's master node recieved the request to de-allocate
                the assigned address. `False` means the wireless transaction did not complete.
        )docstr")
        .def("get_address", &RF24MeshWrapper::getAddress, R"docstr(
            get_address(node_id: int) -> int

            Translates a `node_id` into the corresponding `mesh_address`

            :Returns:

                - A positive `int` that represents the assigned address.
                - A negative `int` that represents a transaction failure.

                  * ``-1`` means the `node_id` does not have an assigned address.
                  * ``-2`` means the mesh network's master node could not be reached to fetch the data.
        )docstr", py::arg("node_id"))
        .def("set_channel", &RF24MeshWrapper::setChannel, R"docstr(
            set_channel(channel: int)

            This function controls the radio's configured `channel` (AKA frequency).
        )docstr", py::arg("channel"))
        .def("set_child", &RF24MeshWrapper::setChild, R"docstr(
            set_child(allow: bool)

            Control the node's ability to have child nodes connect to it.

            :param bool allow: Allow or disallow (`True`/`False`) the instantiated mesh network node
                to resond to other mesh network nodes attempting to connect to the network.
        )docstr", py::arg("allow"))
        .def("set_address", &RF24MeshWrapper::setAddress, R"docstr(
            set_address(node_id: int, address: int, search_by_address: bool = False)

            Call this function on a mesh network's master node to manually assign a logical
            address to a unique `node_id`. This function is meant to inlude RF24Network nodes in
            mesh networks.

            :param int node_id: The unique identifying number for the connected node.
            :param int address: The logical address for the connected node.
            :param bool search_by_address: Set this parameter to `True` traverse the list of
                assigned addresses by address. The default value of `False` traverses the list of
                assigned addresses by node_id.
        )docstr", py::arg("node_id"), py::arg("address"), py::arg("search_by_address") = false)
        .def("save_dhcp", &RF24MeshWrapper::saveDHCP, R"docstr(
            save_dhcp()

            Call this function on the mesh network's master node to save the current list of
            assigned addresses to a local binary text file. This is meant for persistence when the
            master node needs to go offline.
        )docstr")
        // .def("set_static_address", &RF24MeshWrapper::setStaticAddress, R"docstr(
        //     set_static_address(node_id: int, address: int)

        //     For backwards compatiblity, this function is similar to the `set_address()` function.
        // )docstr", py::arg("node_id"), py::arg("address"))
        .def("load_dhcp", &RF24MeshWrapper::loadDHCP, R"docstr(
            load_dhcp()

            Call this function on the mesh network's master node to read and load the saved list of
            assigned addresses from a local binary text file. This is meant for persistence when the
            master node needs resumes operation after being offline.
        )docstr");
}
