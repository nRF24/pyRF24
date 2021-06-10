#include "RF24/RF24.h"
#include "pybind11/pybind11.h"

namespace py = pybind11;

PYBIND11_MODULE(rf24, m) {

    // ********************** Enum structs
    py::enum_<rf24_crclength_e>("rf24_crclength_e")
        .value("RF24_CRC_DISABLED", RF24_CRC_DISABLED)
        .value("RF24_CRC_8", RF24_CRC_8)
        .value("RF24_CRC_16", RF24_CRC_16)
        .export_values();

    py::enum_<rf24_datarate_e>("rf24_datarate_e")
        .value("RF24_1MBPS", RF24_1MBPS)
        .value("RF24_2MBPS", RF24_2MBPS)
        .value("RF24_250KBPS", RF24_250KBPS)
        .export_values();

    py::enum_<rf24_pa_dbm_e>("rf24_pa_dbm_e")
        .value("RF24_PA_MIN", RF24_PA_MIN)
        .value("RF24_PA_LOW", RF24_PA_LOW)
        .value("RF24_PA_HIGH", RF24_PA_HIGH)
        .value("RF24_PA_MAX", RF24_PA_MAX)
        .value("RF24_PA_ERROR", RF24_PA_ERROR)
        .export_values();


    // ******************** RF24 class  **************************
    py::class_<RF24>(m, "RF24")

        // functions that take no args & have no overloads
        .def("isPVariant", &RF24::isPVariant)
        .def("isValid", &RF24::isValid)
        .def("flush_tx", &RF24::flush_tx)
        .def("flush_rx", &RF24::flush_rx)
        .def("disableCRC", &RF24::disableCRC)
        .def("getCRCLength", &RF24::getCRCLength)
        .def("getDataRate", &RF24::getDataRate)
        .def("getDynamicPayloadSize", &RF24::getDynamicPayloadSize)
        .def("getPALevel", &RF24::getPALevel)
        .def("isAckPayloadAvailable", &RF24::isAckPayloadAvailable)
        .def("enableAckPayload", &RF24::enableAckPayload)
        .def("enableDynamicAck", &RF24::enableDynamicAck)
        .def("enableDynamicPayloads", &RF24::enableDynamicPayloads)
        .def("disableDynamicPayloads", &RF24::disableDynamicPayloads)
        .def("powerDown", &RF24::powerDown)
        .def("powerUp", &RF24::powerUp)
        .def("printDetails", &RF24::printDetails)
        .def("reUseTX", &RF24::reUseTX)
        .def("rxFifoFull", &RF24::rxFifoFull)
        .def("startListening", &RF24::startListening)
        .def("stopListening", &RF24::stopListening)
        .def("testCarrier", &RF24::testCarrier)
        .def("testRPD", &RF24::testRPD)
        .def("stopConstCarrier", &RF24::stopConstCarrier)

        // functions that take args
        .def("setRetries", &RF24::setRetries)
        .def("setCRCLength", &RF24::setCRCLength)
        .def("setDataRate", &RF24::setDataRate)
        .def("setAddressWidth", &RF24::setAddressWidth)
        .def("closeReadingPipe", &RF24::closeReadingPipe)
        .def("startConstCarrier", &RF24::startConstCarrier)
        .def("maskIRQ", &RF24::maskIRQ)
        // args contain return values (pass-by-reference)
        .def("read", &RF24::read)
        .def("whatHappened", &RF24::whatHappened)

        // functions that have overloads
        .def(py::init<uint8_t, uint8_t>())
        #if !defined (MRAA)
        .def(py::init<uint8_t, uint8_t, uint32_t>())
        .def(py::init<uint32_t>())
        .def(py::init<>())
        #endif
        .def("begin", static_cast<bool (RF24::*)()>(&RF24::begin))
        .def("begin", static_cast<bool (RF24::*)(uint8_t, uint8_t)>(&RF24::begin))
        .def("available", static_cast<bool (RF24::*)()>(&RF24::available))
        .def("available", static_cast<bool (RF24::*)(uint8_t*)>(&RF24::available)) // (pass-by-reference)
        .def("openReadingPipe", static_cast<void (RF24::*)(uint8_t, const uint8_t*)>(&RF24::openReadingPipe))
        .def("openReadingPipe", static_cast<void (RF24::*)(uint8_t, uint64_t)>(&RF24::openReadingPipe))
        .def("openWritingPipe", static_cast<void (RF24::*)(const uint8_t*)>(&RF24::openWritingPipe))
        .def("openWritingPipe", static_cast<void (RF24::*)(uint64_t)>(&RF24::openWritingPipe))
        .def("setAutoAck", static_cast<void (RF24::*)(bool)>(&RF24::setAutoAck))
        .def("setAutoAck", static_cast<void (RF24::*)(bool, uint8_t)>(&RF24::setAutoAck))
        .def("setPALevel", static_cast<void (RF24::*)(uint8_t, bool)>(&RF24::setPALevel))
        .def("setPALevel", static_cast<void (RF24::*)(uint8_t)>(&RF24::setPALevel))
        .def("txStandBy", static_cast<bool (RF24::*)(uint32_t, bool)>(&RF24::txStandBy))
        .def("txStandBy", static_cast<bool (RF24::*)()>(&RF24::txStandBy))

        // functions wrapped into python object's properties
        .add_property("channel", &RF24::getChannel, &RF24::setChannel)
        .add_property("payloadSize", &RF24::getPayloadSize, &RF24::setPayloadSize)
        .def_readwrite("failureDetected", &RF24::failureDetected);

        // old wrapper from boost.python usage
        .def("startFastWrite", &startFastWrite_wrap1, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast")))
        .def("startFastWrite", &startFastWrite_wrap2, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast"), bp::arg("startTx")))
        .def("startWrite", &startWrite_wrap, (bp::arg("buf"), bp::arg("len"), bp::arg("multicast")))
        .def("write", &write_wrap1, (bp::arg("buf")))
        .def("write", &write_wrap2, (bp::arg("buf"), bp::arg("multicast")))
        .def("writeAckPayload", writeAckPayload_wrap, (bp::arg("pipe"), bp::arg("buf")))
        .def("writeBlocking", &writeBlocking_wrap, (bp::arg("buf"), bp::arg("timeout")))
        .def("writeFast", &writeFast_wrap1, (bp::arg("buf")))
        .def("writeFast", &writeFast_wrap2, (bp::arg("buf"), bp::arg("multicast")))
}
