#include <pybind11/pybind11.h>
#include <RF24.h>
#include <nRF24L01.h>

namespace py = pybind11;

void throw_ba_exception(void)
{
    PyErr_SetString(PyExc_TypeError, "buf parameter must be bytes or bytearray");
    py::error_already_set();
}

char* get_bytes_or_bytearray_str(py::object buf)
{
    PyObject* py_ba;
    py_ba = buf.ptr();
    if (PyByteArray_Check(py_ba))
        return PyByteArray_AsString(py_ba);
    else if (PyBytes_Check(py_ba))
        return PyBytes_AsString(py_ba);
    else
        throw_ba_exception();

    return NULL;
}

int get_bytes_or_bytearray_ln(py::object buf)
{
    PyObject* py_ba;
    py_ba = buf.ptr();
    if (PyByteArray_Check(py_ba))
        return PyByteArray_Size(py_ba);
    else if (PyBytes_Check(py_ba))
        return PyBytes_Size(py_ba);
    else
        throw_ba_exception();

    return 0;
}

class RF24Wrapper : public RF24
{

public:
    RF24Wrapper(rf24_gpio_pin_t _ce_pin, rf24_gpio_pin_t _csn_pin, uint32_t _spi_speed = 10000000) : RF24(_ce_pin, _csn_pin, _spi_speed)
    {
    }

    RF24Wrapper(uint32_t _spi_speed = 10000000) : RF24(_spi_speed)
    {
    }

    // needed for polymorphic recognition
    virtual ~RF24Wrapper() = default;

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

    void open_tx_pipe(py::buffer address)
    {
        RF24::openWritingPipe(reinterpret_cast<uint8_t*>(get_bytes_or_bytearray_str(address)));
    }

    void open_rx_pipe(uint8_t number, py::buffer address)
    {
        RF24::openReadingPipe(number, reinterpret_cast<uint8_t*>(get_bytes_or_bytearray_str(address)));
    }

    py::bytearray read(uint8_t length = 0)
    {
        if (!length)
            length = RF24::dynamic_payloads_enabled ? RF24::getDynamicPayloadSize() : RF24::getPayloadSize();
        else
            length = rf24_min(length, static_cast<uint8_t>(32));
        char* payload = new char[length + 1];
        RF24::read(payload, length);
        payload[length] = '\0';
        py::bytearray buf = py::bytearray(payload, length);
        delete[] payload;
        return buf;
    }

    void startFastWrite(py::buffer buf, const bool multicast = false, bool startTx = true)
    {
        RF24::startFastWrite(
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            multicast, startTx);
    }

    bool startWrite(py::buffer buf, const bool multicast)
    {
        return RF24::startWrite(
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            multicast);
    }

    bool writeFast(py::buffer buf, const bool multicast = false)
    {
        return RF24::writeFast(
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            multicast);
    }

    bool write(py::buffer buf, const bool multicast = false)
    {
        return RF24::write(
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            multicast);
    }

    bool writeBlocking(py::buffer buf, uint32_t timeout)
    {
        return RF24::writeBlocking(
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)),
            timeout);
    }

    bool writeAckPayload(uint8_t pipe, py::buffer buf)
    {
        return RF24::writeAckPayload(
            pipe,
            get_bytes_or_bytearray_str(buf),
            static_cast<uint8_t>(get_bytes_or_bytearray_ln(buf)));
    }

    char* sprintfDetails()
    {
        char* debug_info = new char[870];
        RF24::sprintfPrettyDetails(debug_info);
        return debug_info;
    }

    void set_radiation(rf24_pa_dbm_e level, rf24_datarate_e speed, bool lna_enable = true)
    {
        RF24::setRadiation(level, speed, lna_enable);
    }

    /*********************************************************************************/
    /* wrappers for python-like properties */

    uint8_t get_address_width()
    {
        return RF24::addr_width;
    }

    bool is_ack_payloads_enabled()
    {
        return RF24::ack_payloads_enabled;
    }

    void toggle_ack_payloads(const bool enable)
    {
        if (enable)
            RF24::enableAckPayload();
        else
            RF24::disableAckPayload();
    }

    bool is_dynamic_payloads_enabled()
    {
        return RF24::dynamic_payloads_enabled;
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

    void set_pa_level(rf24_pa_dbm_e level)
    {
        RF24::setPALevel(level);
    }

    rf24_pa_dbm_e get_pa_level()
    {
        uint8_t ret_val = RF24::getPALevel();
        if (ret_val == RF24_PA_MAX)
            return RF24_PA_MAX;
        if (ret_val == RF24_PA_HIGH)
            return RF24_PA_HIGH;
        if (ret_val == RF24_PA_LOW)
            return RF24_PA_LOW;
        // if (ret_val == RF24_PA_MIN)
        return RF24_PA_MIN;
    }

    rf24_datarate_e get_data_rate()
    {
        uint8_t ret_val = RF24::getDataRate();
        if (ret_val == RF24_2MBPS)
            return RF24_2MBPS;
        if (ret_val == RF24_1MBPS)
            return RF24_1MBPS;
        // if (ret_val == RF24_250KBPS)
        return RF24_250KBPS;
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
