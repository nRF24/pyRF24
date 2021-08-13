#include <pybind11/pybind11.h>
#include <RF24.h>
#include <nRF24L01.h>

namespace py = pybind11;

class RF24Wrapper : public RF24
{

public:

    RF24Wrapper(uint16_t _ce_pin, uint16_t _csn_pin, uint32_t _spi_speed = 10000000) : RF24(_ce_pin, _csn_pin, _spi_speed)
    {
    }

    RF24Wrapper(uint32_t _spi_speed = 10000000) : RF24(_spi_speed)
    {
    }

    std::tuple<bool, uint8_t> available_pipe()
    {
        uint8_t pipe = 7;
        bool is_available = RF24::available(&pipe);
        return std::tuple<bool, uint8_t>(is_available, pipe);
    }

    std::tuple<bool, bool, bool> what_happened()
    {
        bool ds = 0, df = 0, dr = 0;
        RF24::whatHappened(ds, df, dr);
        return std::tuple<bool, bool, bool>(ds, df, dr);
    }

    py::bytearray read(const uint8_t length)
    {
        uint8_t *payload = new uint8_t[length];
        RF24::read(&payload, length);
        py::bytearray buf = py::bytearray(reinterpret_cast<char *>(payload));
        delete[] payload;
        return buf;
    }

    void startFastWrite(char *buf, const bool multicast = false, bool startTx = true)
    {
        RF24::startFastWrite(buf, static_cast<uint8_t>(strlen(buf)), multicast, startTx);
    }

    bool startWrite(char *buf, const bool multicast)
    {
        return RF24::startWrite(buf, static_cast<uint8_t>(strlen(buf)), multicast);
    }

    bool writeFast(char *buf, const bool multicast = false)
    {
        return RF24::writeFast(buf, static_cast<uint8_t>(strlen(buf)), multicast);
    }

    bool write(char *buf, const bool multicast = false)
    {
        return RF24::write(buf, static_cast<uint8_t>(strlen(buf)), multicast);
    }

    bool writeBlocking(char *buf, uint32_t timeout)
    {
        return RF24::writeBlocking(buf, static_cast<uint8_t>(strlen(buf)), timeout);
    }

    bool writeAckPayload(uint8_t pipe, char *buf)
    {
        return RF24::writeAckPayload(pipe, buf, static_cast<uint8_t>(strlen(buf)));
    }

    /*********************************************************************************/
    /* wrappers for python-like properties */

    bool is_dynamic_payloads_enabled()
    {
        return read_register(DYNPD);
    }

    void dynamic_payloads(const bool enable)
    {
        if (enable)
            RF24::enableDynamicPayloads();
        else
            RF24::disableDynamicPayloads();
    }

    bool isPowerUp()
    {
        return read_register(NRF_CONFIG) & _BV(PWR_UP);
    }

    void power(const bool enable)
    {
        if (enable)
            powerUp();
        else
            powerDown();
    }

    bool isListening()
    {
        return read_register(NRF_CONFIG) & _BV(PRIM_RX);
    }

    void listen(const bool enable)
    {
        if (enable)
            startListening();
        else
            stopListening();
    }
};

PYBIND11_MODULE(rf24, m) {

    // ********************** Enum structs
    py::enum_<rf24_crclength_e>(m, "rf24_crclength_e")
        .value("RF24_CRC_DISABLED", RF24_CRC_DISABLED)
        .value("RF24_CRC_8", RF24_CRC_8)
        .value("RF24_CRC_16", RF24_CRC_16)
        .export_values();

    py::enum_<rf24_datarate_e>(m, "rf24_datarate_e")
        .value("RF24_1MBPS", RF24_1MBPS)
        .value("RF24_2MBPS", RF24_2MBPS)
        .value("RF24_250KBPS", RF24_250KBPS)
        .export_values();

    py::enum_<rf24_pa_dbm_e>(m, "rf24_pa_dbm_e")
        .value("RF24_PA_MIN", RF24_PA_MIN)
        .value("RF24_PA_LOW", RF24_PA_LOW)
        .value("RF24_PA_HIGH", RF24_PA_HIGH)
        .value("RF24_PA_MAX", RF24_PA_MAX)
        // .value("RF24_PA_ERROR", RF24_PA_ERROR)
        .export_values();


    // ******************** RF24 class  **************************
    py::class_<RF24Wrapper>(m, "RF24")

        // functions that take no args & have no overloads
        .def("flush_tx", &RF24Wrapper::flush_tx)
        .def("flush_rx", &RF24Wrapper::flush_rx)
        .def("disable_crc", &RF24Wrapper::disableCRC)
        .def("get_crc_length", &RF24Wrapper::getCRCLength)
        .def("get_data_rate", &RF24Wrapper::getDataRate)
        .def("get_dynamic_payload_size", &RF24Wrapper::getDynamicPayloadSize)
        .def("get_pa_level", &RF24Wrapper::getPALevel)
        .def("enable_ack_payload", &RF24Wrapper::enableAckPayload)
        .def("enable_dynamic_ack", &RF24Wrapper::enableDynamicAck)
        .def("enable_dynamic_payloads", &RF24Wrapper::enableDynamicPayloads)
        .def("disable_dynamic_payloads", &RF24Wrapper::disableDynamicPayloads)
        .def("power_down", &RF24Wrapper::powerDown)
        .def("power_up", &RF24Wrapper::powerUp)
        .def("print_details", &RF24Wrapper::printDetails)
        .def("print_pretty_details", &RF24Wrapper::printPrettyDetails)
        .def("reuse_tx", &RF24Wrapper::reUseTX)
        .def("start_listening", &RF24Wrapper::startListening)
        .def("stop_listening", &RF24Wrapper::stopListening)
        .def("stop_const_carrier", &RF24Wrapper::stopConstCarrier)
        .def("is_valid", &RF24Wrapper::isValid)
        .def("is_plus_variant", &RF24Wrapper::isPVariant)
        .def("test_rpd", &RF24Wrapper::testRPD)
        .def("rx_fifo_full", &RF24Wrapper::rxFifoFull)
        .def("what_happened", &RF24Wrapper::whatHappened)
        .def("available_pipe", &RF24Wrapper::available_pipe)

        // functions that take args
        .def("set_retries", &RF24Wrapper::setRetries)
        .def("set_crc_length", &RF24Wrapper::setCRCLength)
        .def("set_data_rate", &RF24Wrapper::setDataRate)
        .def("set_address_width", &RF24Wrapper::setAddressWidth)
        .def("close_rx_pipe", &RF24Wrapper::closeReadingPipe)
        .def("start_const_carrier", &RF24Wrapper::startConstCarrier)
        .def("set_pa_level", &RF24Wrapper::setPALevel, py::arg("level"), py::arg("lna_enable") = true)
        .def("mask_irq", &RF24Wrapper::maskIRQ)
        .def("read", &RF24Wrapper::read)

        // functions that have overloads
        .def(py::init<uint8_t, uint8_t>())
        #if !defined (MRAA)
        .def(py::init<uint8_t, uint8_t, uint32_t>())
        .def(py::init<uint32_t>())
        .def(py::init<>())
        #endif
        .def("begin", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::begin))
        .def("begin", static_cast<bool (RF24Wrapper::*)(uint16_t, uint16_t)>(&RF24Wrapper::begin))
        .def("available", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::available))
        .def("open_rx_pipe", static_cast<void (RF24Wrapper::*)(uint8_t, const uint8_t*)>(&RF24Wrapper::openReadingPipe))
        .def("open_rx_pipe", static_cast<void (RF24Wrapper::*)(uint8_t, uint64_t)>(&RF24Wrapper::openReadingPipe))
        .def("open_tx_pipe", static_cast<void (RF24Wrapper::*)(const uint8_t*)>(&RF24Wrapper::openWritingPipe))
        .def("open_tx_pipe", static_cast<void (RF24Wrapper::*)(uint64_t)>(&RF24Wrapper::openWritingPipe))
        .def("set_auto_ack", static_cast<void (RF24Wrapper::*)(bool)>(&RF24Wrapper::setAutoAck))
        .def("set_auto_ack", static_cast<void (RF24Wrapper::*)(uint8_t, bool)>(&RF24Wrapper::setAutoAck))
        .def("tx_standby", static_cast<bool (RF24Wrapper::*)(uint32_t, bool)>(&RF24Wrapper::txStandBy))
        .def("tx_standby", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::txStandBy))

        // functions wrapped into python object's properties
        .def_property("channel", &RF24Wrapper::getChannel, &RF24Wrapper::setChannel)
        .def_property("payload_size", &RF24Wrapper::getPayloadSize, &RF24Wrapper::setPayloadSize)
        .def_property("data_rate", &RF24Wrapper::getDataRate, &RF24Wrapper::setDataRate)
        .def_property("crc_length", &RF24Wrapper::getCRCLength, &RF24Wrapper::setCRCLength)
        .def_property("power", &RF24Wrapper::isPowerUp, &RF24Wrapper::power)
        .def_property("listen", &RF24Wrapper::isListening, &RF24Wrapper::listen)
        .def_property("dynamic_payloads", &RF24Wrapper::is_dynamic_payloads_enabled, &RF24Wrapper::dynamic_payloads)
    #if defined (FAILURE_HANDLING)
        .def_readwrite("failure_detected", &RF24Wrapper::failureDetected)
    #endif // defined (FAILURE_HANDLING)
        .def_property_readonly("is_valid", &RF24Wrapper::isValid)
        .def_property_readonly("is_plus_variant", &RF24Wrapper::isPVariant)
        .def_property_readonly("rpd", &RF24Wrapper::testRPD)
        .def_property_readonly("rx_fifo_full", &RF24Wrapper::rxFifoFull)

        // functions that need python's bytearray wrapped/casted to char *buffer
        .def("start_fast_write", &RF24Wrapper::startFastWrite, py::arg("buf"), py::arg("multicast") = false, py::arg("start_tx") = true)
        .def("start_write", &RF24Wrapper::startWrite, py::arg("buf"), py::arg("multicast") = false)
        .def("write", &RF24Wrapper::write, py::arg("buf"), py::arg("multicast") = false)
        .def("write_ack_payload", &RF24Wrapper::writeAckPayload, py::arg("pipe"), py::arg("buf"))
        .def("write_blocking", &RF24Wrapper::writeBlocking, py::arg("buf"), py::arg("timeout"))
        .def("write_fast", &RF24Wrapper::writeFast, py::arg("buf"), py::arg("multicast") = false);
}
