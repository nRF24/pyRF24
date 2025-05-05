#include <pybind11/pybind11.h>
#include "pyRF24.h"

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

void init_rf24(py::module& m)
{
    m.doc() = "A Python module that wraps all RF24 C++ library's API";
    m.attr("RF24_DRIVER") = RF24_DRIVER;

    // ********************** Enum structs
    py::enum_<rf24_crclength_e>(m, "rf24_crclength_e")
        .value("RF24_CRC_DISABLED", RF24_CRC_DISABLED, R"docstr(
            to disable using CRC checksums
        )docstr")
        .value("RF24_CRC_8", RF24_CRC_8, R"docstr(
            to use 8-bit checksums
        )docstr")
        .value("RF24_CRC_16", RF24_CRC_16, R"docstr(
            to use 16-bit checksums
        )docstr")
        .export_values();

    py::enum_<rf24_datarate_e>(m, "rf24_datarate_e")
        .value("RF24_1MBPS", RF24_1MBPS, R"docstr(
            for 1 Mbps
        )docstr")
        .value("RF24_2MBPS", RF24_2MBPS, R"docstr(
            for 2 Mbps
        )docstr")
        .value("RF24_250KBPS", RF24_250KBPS, R"docstr(
            for 250 kbps
        )docstr")
        .export_values();

    py::enum_<rf24_fifo_state_e>(m, "rf24_fifo_state_e")
        .value("RF24_FIFO_OCCUPIED", RF24_FIFO_OCCUPIED, R"docstr(
            The FIFO is not full nor empty, but it is occupied with 1 or 2 payloads.
        )docstr")
        .value("RF24_FIFO_EMPTY", RF24_FIFO_EMPTY, R"docstr(
            The FIFO is empty.
        )docstr")
        .value("RF24_FIFO_FULL", RF24_FIFO_FULL, R"docstr(
            The FIFO is full.
        )docstr")
        .value("RF24_FIFO_INVALID", RF24_FIFO_INVALID, R"docstr(
            Represents corruption of data over SPI (when observed).
        )docstr")
        .export_values();

    py::enum_<rf24_irq_flags_e>(m, "rf24_irq_flags_e")
        .value("RF24_RX_DR", RF24_RX_DR, R"docstr(
                Represents an event where RX Data is Ready to `RF24.read()`.
            )docstr")
        .value("RF24_TX_DS", RF24_TX_DS, R"docstr(
                Represents an event where TX Data Sent successfully.
            )docstr")
        .value("RF24_TX_DF", RF24_TX_DF, R"docstr(
                Represents an event where TX Data Failed to send.
            )docstr")
        .value("RF24_IRQ_ALL", RF24_IRQ_ALL, R"docstr(
                Equivalent to ``RF24_RX_DR | RF24_TX_DS | RF24_TX_DF``.
            )docstr")
        .value("RF24_IRQ_NONE", RF24_IRQ_NONE, R"docstr(
                An alias of ``0`` to describe no IRQ events enabled.
            )docstr")
        .export_values();

    py::enum_<rf24_pa_dbm_e>(m, "rf24_pa_dbm_e")
        .value("RF24_PA_MIN", RF24_PA_MIN, R"docstr(
            +----------------------+--------------------+--------------------+
            | nRF24L01 description | Si24R1 description | Si24R1 description |
            |                      | when LNA enabled   | when LNA disabled  |
            +======================+====================+====================+
            |      -18 dBm         |      6 dBm         |     -12 dBm        |
            +----------------------+--------------------+--------------------+
        )docstr")
        .value("RF24_PA_LOW", RF24_PA_LOW, R"docstr(
            +----------------------+--------------------+--------------------+
            | nRF24L01 description | Si24R1 description | Si24R1 description |
            |                      | when LNA enabled   | when LNA disabled  |
            +======================+====================+====================+
            |      -12 dBm         |      0 dBm         |      -4 dBm        |
            +----------------------+--------------------+--------------------+
        )docstr")
        .value("RF24_PA_HIGH", RF24_PA_HIGH, R"docstr(
            +----------------------+--------------------+--------------------+
            | nRF24L01 description | Si24R1 description | Si24R1 description |
            |                      | when LNA enabled   | when LNA disabled  |
            +======================+====================+====================+
            |      -6 dBm          |      3 dBm         |       1 dBm        |
            +----------------------+--------------------+--------------------+
        )docstr")
        .value("RF24_PA_MAX", RF24_PA_MAX, R"docstr(
            +----------------------+--------------------+--------------------+
            | nRF24L01 description | Si24R1 description | Si24R1 description |
            |                      | when LNA enabled   | when LNA disabled  |
            +======================+====================+====================+
            |      0 dBm           |      7 dBm         |       4 dBm        |
            +----------------------+--------------------+--------------------+
        )docstr")
        // .value("RF24_PA_ERROR", RF24_PA_ERROR)
        .export_values();

    // ******************** RF24 class  **************************
    py::class_<RF24Wrapper>(m, "RF24")

        // *****************************************************************************
        // ***************************** functions that take no args & have no overloads

        .def("flush_tx", &RF24Wrapper::flush_tx, R"docstr(
            flush_tx()

            Flush all 3 levels of the radio's TX FIFO.
        )docstr")

        // *****************************************************************************

        .def("flush_rx", &RF24Wrapper::flush_rx, R"docstr(
            flush_rx()

            Flush all 3 levels of the radio's RX FIFO.
        )docstr")

        // *****************************************************************************

        .def("disableCRC", &RF24Wrapper::disableCRC, R"docstr(
            disableCRC()

            Disable the radio's CRC feature.

            .. note:: Enabling the radio's auto-ack feature will automatically enable the radio's
                CRC feature.
        )docstr")

        // *****************************************************************************

        .def("getCRCLength", &RF24Wrapper::getCRCLength, R"docstr(
            getCRCLength() -> pyrf24.rf24_crclength_e

            Get the current setting of the radio's CRC Length.
        )docstr")

        // *****************************************************************************

        .def("getChannel", &RF24Wrapper::getChannel, R"docstr(
            getChannel() -> int

            Get the current setting of the radio's channel.
        )docstr")

        // *****************************************************************************

        .def("getDataRate", &RF24Wrapper::getDataRate, R"docstr(
            getDataRate() -> pyrf24.rf24_datarate_e

            Get the current setting of the radio's Data Rate.
        )docstr")

        // *****************************************************************************

        .def("get_dynamic_payload_size", &RF24Wrapper::getDynamicPayloadSize, R"docstr(
            get_dynamic_payload_size() -> int

            Get the Dynamic Payload Size of the next available payload in the radio's RX FIFO.
        )docstr")

        .def("getDynamicPayloadSize", &RF24Wrapper::getDynamicPayloadSize, R"docstr(
            getDynamicPayloadSize() -> int
        )docstr")

        // *****************************************************************************

        .def("getPALevel", &RF24Wrapper::getPALevel, R"docstr(
            getPALevel() -> pyrf24.rf24_pa_dbm_e

            Get the current setting of the radio's Power Amplitude Level.
        )docstr")

        // *****************************************************************************

        .def("getPayloadSize", &RF24Wrapper::getPayloadSize, R"docstr(
            getPayloadSize() -> int

            Configure the radio's static payload size (outgoing and incoming) for all data pipes.

            :param int length: The length of static payloads used for all data pipes.
        )docstr")

        // *****************************************************************************

        .def("enableAckPayload", &RF24Wrapper::enableAckPayload, R"docstr(
            enableAckPayload()

            Enable the radio's Ack Payload feature.
        )docstr")

        // *****************************************************************************

        .def("enable_dynamic_ack", &RF24Wrapper::enableDynamicAck, R"docstr(
            enable_dynamic_ack()

            Enable the radio's Dynamic Ack feature.

            By default the multicast parameter to `write()` is ineffective unless this
            function is called. This design decision was made for compatibility with
            the cheap chinese Si24R1 clones.
        )docstr")

        .def("enableDynamicAck", &RF24Wrapper::enableDynamicAck, R"docstr(
            enableDynamicAck()
        )docstr")

        // *****************************************************************************

        .def("enableDynamicPayloads", &RF24Wrapper::enableDynamicPayloads, R"docstr(
            enableDynamicPayloads()

            Enable the radio's Dynamic Payloads feature.
        )docstr")

        // *****************************************************************************

        .def("disableDynamicPayloads", &RF24Wrapper::disableDynamicPayloads, R"docstr(
            disableDynamicPayloads()

            Disable the radio's Dynamic Payloads feature.
        )docstr")

        // *****************************************************************************

        .def("powerDown", &RF24Wrapper::powerDown, R"docstr(
            powerDown()

            Power down the radio.

            .. important::
                No transmissions can be received or transmitted when the radio is powered down.
        )docstr")

        // *****************************************************************************

        .def("powerUp", &RF24Wrapper::powerUp, R"docstr(
            powerUp()

            Power up the radio.
        )docstr")

        // *****************************************************************************

        .def("print_details", &RF24Wrapper::printDetails, R"docstr(
            print_details()

            Print out details about the radio's configuration.
        )docstr")

        .def("printDetails", &RF24Wrapper::printDetails, R"docstr(
            printDetails()
        )docstr")

        // *****************************************************************************

        .def("print_pretty_details", &RF24Wrapper::printPrettyDetails, R"docstr(
            print_pretty_details()

            Print out details about the radio's configuration. This function differs from
            `print_details()` as the output for this function is more human-friendly/readable.
        )docstr")

        .def("printPrettyDetails", &RF24Wrapper::printPrettyDetails, R"docstr(
            printPrettyDetails()
        )docstr")

        // *****************************************************************************

        .def("sprintf_pretty_details", &RF24Wrapper::sprintfDetails, R"docstr(
            sprintf_pretty_details() -> str

            Put details about the radio's configuration into a string. This function differs from
            `print_pretty_details()` as it does not use stdout output stream.

            :Returns: A string that describes the radio's details.
        )docstr")

        .def("sprintfPrettyDetails", &RF24Wrapper::sprintfDetails, R"docstr(
            sprintfPrettyDetails() -> str
        )docstr")

        // *****************************************************************************

        .def("reuse_tx", &RF24Wrapper::reUseTX, R"docstr(
            reuse_tx()

            Re-use the 1\ :sup:`st` level of the radio's TX FIFO.
        )docstr")

        .def("reUseTX", &RF24Wrapper::reUseTX, R"docstr(
            reUseTX()
        )docstr")

        // *****************************************************************************

        .def("start_listening", &RF24Wrapper::startListening, R"docstr(
            start_listening()

            Start listening on the pipes opened for receiving.
            This function is equivalent to calling ``radio.listen = True``.

            .. hint::

                1. Be sure to call :py:meth:`~pyrf24.RF24.open_rx_pipe()` before
                   calling this function.
                2. Do not call :py:meth:`~pyrf24.RF24.write()` while in RX mode, without
                   first setting :py:attr:`~pyrf24.RF24.listen` to `False` (or calling
                   `RF24.stop_listening()`).
                3. Call :py:meth:`~pyrf24.RF24.available()` to check for incoming traffic,
                   and use :py:meth:`~pyrf24.RF24.read()` to get it.

            .. code-block:: python
                :caption: Open reading pipe 1 using address ``b"\xCC\xCE\xCC\xCE\xCC"``

                address = bytes([0xCC, 0xCE, 0xCC, 0xCE, 0xCC])
                radio.open_rx_pipe(1, address)
                radio.start_listening()  # or radio.listen = True

            .. note::
                If there was a call to `RF24.open_rx_pipe()` about pipe 0 prior to
                calling this function, then this function will re-write the address
                that was last set to reading pipe 0. This is because `RF24.stop_listening()`
                (and `RF24.open_tx_pipe()`) will overwrite the address to reading pipe 0
                for proper auto-ack functionality.
        )docstr")

        .def("startListening", &RF24Wrapper::startListening, R"docstr(
            startListening()

            Put the radio into RX mode.
        )docstr")

        // *****************************************************************************

        .def("stop_const_carrier", &RF24Wrapper::stopConstCarrier, R"docstr(
            stop_const_carrier()

            End transmitting a constant carrier wave. This function also sets the `power` to `False`
            as recommended by the datasheet.
        )docstr")

        .def("stopConstCarrier", &RF24Wrapper::stopConstCarrier, R"docstr(
            stopConstCarrier()
        )docstr")

        // *****************************************************************************

        .def("isValid", &RF24Wrapper::isValid, R"docstr(
            isValid() -> bool

            Verify the configured pin numbers are indeed valid.

            :Returns: `True` if the radio's CE & CSN pins have been configured (using the
                RF24 class' constructor or :py:meth:`~pyrf24.RF24.begin()` function)
        )docstr")

        // *****************************************************************************

        .def("isPVariant", &RF24Wrapper::isPVariant, R"docstr(
            isPVariant() -> bool

            Is the detected radio compatible with the nRF24L01+ family?

            :Returns: `True` of the radio is a nRF24L01+ model (or compatible), otherwise `False`.
        )docstr")

        // *****************************************************************************

        .def("testRPD", &RF24Wrapper::testRPD, R"docstr(
            testRPD() -> bool

            :Returns: `True` if a signal (above -64 dbm) was detected in RX mode, otherwise `False`.
        )docstr")

        // *****************************************************************************

        .def("rxFifoFull", &RF24Wrapper::rxFifoFull, R"docstr(
            rxFifoFull() -> bool

            :Returns: `True` if all 3 levels of the radio's RX FIFO are occupied, otherwise `False`.
        )docstr")

        // *****************************************************************************

        .def("what_happened", &RF24Wrapper::what_happened, R"docstr(
            what_happened() -> Tuple[bool, bool, bool]

            Call this function when the radio's IRQ pin is active LOW.

            .. deprecated:: 0.5.0
                Use `clear_status_flags()` instead.

            :Returns: a 3-tuple of boolean values in which

                - index 0 represents a "data sent" event
                - index 1 represents a "data failed" event
                - index 2 represents a "data ready" event

            .. note::
                Calling this function also clears all status flags and resets the IRQ pin
                to inactive high.
            .. seealso::
                :py:meth:`~pyrf24.RF24.mask_irq()`
        )docstr")

        .def("whatHappened", &RF24Wrapper::what_happened, R"docstr(
            whatHappened() -> Tuple[bool, bool, bool]
        )docstr")

        // *****************************************************************************

        .def("available_pipe", &RF24Wrapper::available_pipe, R"docstr(
            available_pipe() -> Tuple[bool, int]

            Similar to :py:meth:`~pyrf24.RF24.available()`, but additionally returns the pipe
            number that received the next available payload.

            :Returns: A 2-tuple in which

                - index 0 is the `bool` value indicating if there is a available payload in the
                  radio's RX FIFO.
                - index 1 is the `int` value indicating the pipe number that received the next
                  available in the radio's RX FIFO. If there is no payload received, then this
                  number is set to an invalid value of 7.
        )docstr")

        // *****************************************************************************

        .def("get_arc", &RF24Wrapper::getARC, R"docstr(
            get_arc() -> int

            Returns automatic retransmission count (ARC_CNT)

            Value resets with each new transmission. Allows roughly estimating signal strength.

            :Returns: Returned values range from 0 to 15.
        )docstr")

        .def("getARC", &RF24Wrapper::getARC, R"docstr(
            getARC() -> int
        )docstr")

        // *****************************************************************************
        // **************************************** functions that take args

        .def("set_radiation", &RF24Wrapper::set_radiation, R"docstr(
            set_radiation(level: rf24_pa_dbm_e, speed: rf24_datarate_e, lna_enable: bool = True)

            Configure the RF_SETUP register in 1 SPI transaction.

            :param rf24_pa_dbm_e level: The desired Power Amplitude level. Options are defined in the
                `rf24_pa_dbm_e` enum.
            :param rf24_datarate_e speed: The desired RF data rate. Options are defined in the
                `rf24_datarate_e` enum.
            :param bool lna_enable: A toggle for radio's that support controlling the Low Noise
                Amplifier feature. This is always enabled by default and when not specified.

            .. seealso::

                - :py:meth:`~pyrf24.RF24.set_pa_level()`
                - :py:attr:`~pyrf24.RF24.pa_level`
                - :py:attr:`~pyrf24.RF24.data_rate`
        )docstr",
             py::arg("level"), py::arg("speed"), py::arg("lna_enable") = true)

        .def("setRadiation", &RF24Wrapper::set_radiation, R"docstr(
            setRadiation(level: rf24_pa_dbm_e, speed: rf24_datarate_e, lna_enable: bool = True)
        )docstr",
             py::arg("level"), py::arg("speed"), py::arg("lna_enable") = true)

        // *****************************************************************************

        .def("set_retries", &RF24Wrapper::setRetries, R"docstr(
            set_retries(delay: int, count: int)

            Configure the radio's auto-retries feature.

            :param int delay: A number in the range [0, 15] used as a multiple of 250. This
                controls the amount of time (in microseconds) the radio waits for an
                auto-acknowledgment.
            :param int count: A number in range [0, 15]. This is the amount of automatic retries
                that the radio attempts when an automatic acknowledgment is not received.
        )docstr",
             py::arg("delay"), py::arg("count"))

        .def("setRetries", &RF24Wrapper::setRetries, R"docstr(
            setRetries(delay: int, count: int)
        )docstr",
             py::arg("delay"), py::arg("count"))

        // *****************************************************************************

        .def("setCRCLength", &RF24Wrapper::setCRCLength, R"docstr(
            setCRCLength(length: rf24_crclength_e)

            Configure the radio's CRC Length feature.

            :param rf24_crclength_e length: The number of bytes used in the radio's CRC checksum.

                .. seealso:: Values accepted by the parameter are predefined in the
                    `rf24_crclength_e` enum struct.
        )docstr",
             py::arg("length"))

        // *****************************************************************************

        .def("setChannel", &RF24Wrapper::setChannel, R"docstr(
            setChannel(channel: int)

            Set the current setting of the radio's channel.
        )docstr",
             py::arg("channel"))

        // *****************************************************************************

        .def("setDataRate", &RF24Wrapper::setDataRate, R"docstr(
            setDataRate(rate: rf24_datarate_e)

            Configure the radio's Data Rate feature.

            :param rf24_datarate_e rate: The speed in which the radio send out data over the air. Values
                accepted for this parameter are pre-defined in the `rf24_datarate_e` enum struct.
        )docstr",
             py::arg("rate"))

        // *****************************************************************************

        .def("setAddressWidth", &RF24Wrapper::setAddressWidth, R"docstr(
            setAddressWidth(width: int)

            Configure the radio's Address Width feature.

            :param int width: The number of bytes used for address' length assigned to the data
                pipes. Accepted values are clamped to range [3, 5].
        )docstr",
             py::arg("width"))

        // *****************************************************************************

        .def("close_rx_pipe", &RF24Wrapper::closeReadingPipe, R"docstr(
            close_rx_pipe(pipe: int)

            Close a data pipe for receiving.

            :param int pipe: The identifying data pipe number to close. Remember there are
                only 6 data pipes (identified by the numbers 0-5).
        )docstr",
             py::arg("pipe"))

        .def("closeReadingPipe", &RF24Wrapper::closeReadingPipe, R"docstr(
            closeReadingPipe(pipe: int)
        )docstr",
             py::arg("pipe"))

        // *****************************************************************************

        .def("toggle_all_pipes", &RF24Wrapper::toggleAllPipes, R"docstr(
            toggle_all_pipes(enable: bool)

            Open or close all pipes with 1 SPI transaction. This does not alter the addresses assigned to
            the data pipes (using `open_rx_pipe()` or `open_tx_pipe()`).

            :param bool enable: `True` opens all data pipes for RX operation.
                `False` closes all data pipes for RX operation.
        )docstr",
             py::arg("enable"))

        .def("toggleAllPipes", &RF24Wrapper::toggleAllPipes, R"docstr(
            toggleAllPipes(enable: bool)
        )docstr",
             py::arg("enable"))

        // *****************************************************************************

        .def("start_const_carrier", &RF24Wrapper::startConstCarrier, R"docstr(
            start_const_carrier(level: rf24_pa_dbm_e, channel: int)

            Start a constant carrier wave. This is used (in conjunction with `rpd`) to test the
            radio's hardware.

            :param rf24_pa_dbm_e level: The value used to configure Power Amplitude level. Accepted
                values are pre-defined in the `rf24_pa_dbm_e` enum struct.
            :param int channel: The  channel to broadcast on.
        )docstr",
             py::arg("level"), py::arg("channel"))

        .def("startConstCarrier", &RF24Wrapper::startConstCarrier, R"docstr(
            startConstCarrier(level: rf24_pa_dbm_e, channel: int)
        )docstr")

        // *****************************************************************************

        .def("set_pa_level", &RF24Wrapper::setPALevel, R"docstr(
            set_pa_level(level: rf24_pa_dbm_e, lna_enable: bool = True)

            Configure the radio's Power Amplitude Level.

            :param rf24_pa_dbm_e level: The value used to configure Power Amplitude level. Accepted
                values are pre-defined in the `rf24_pa_dbm_e` enum struct.
            :param bool lna_enable: This parameter configures the LNA (Low Noise Amplifier)
                feature of the radio. This feature can only be configured on non-plus models of
                the nRF24L01 (or the Si24R1 clone).
        )docstr",
             py::arg("level"), py::arg("lna_enable") = true)

        .def("setPALevel", &RF24Wrapper::setPALevel, R"docstr(
            setPALevel(level: rf24_pa_dbm_e, lna_enable: bool = True)
        )docstr",
             py::arg("level"), py::arg("lna_enable") = true)

        // *****************************************************************************

        .def("mask_irq", &RF24Wrapper::maskIRQ, R"docstr(
            mask_irq(tx_ok: bool, tx_fail: bool, rx_ready: bool)

            Configure the radio's IRQ pin to go active on certain events.

            .. deprecated:: 0.5.0
                Use `set_status_flags()` instead.

            .. important:: The IRQ pin is only active when LOW.

            :param bool tx_ok: `True` ignores the "data sent" event, `False` reflects the
                "data sent" event on the IRQ pin.
            :param bool tx_fail: `True` ignores the "data failed" event, `False` reflects the
                "data failed" event on the IRQ pin.
            :param bool rx_ready: `True` ignores the "data ready" event, `False` reflects the
                "data ready" event on the IRQ pin.
        )docstr",
             py::arg("tx_ok"), py::arg("tx_fail"), py::arg("rx_ready"))

        .def("maskIRQ", &RF24Wrapper::maskIRQ, R"docstr(
            maskIRQ(tx_ok: bool, tx_fail: bool, rx_ready: bool)
        )docstr",
             py::arg("tx_ok"), py::arg("tx_fail"), py::arg("rx_ready"))

        // *****************************************************************************

        .def("set_status_flags", &RF24::setStatusFlags, R"docstr(
            set_status_flags(flags: int = RF24_IRQ_NONE.value) -> None

            Set which flags shall be reflected on the radio's IRQ pin (when active LOW).

            .. note:: This function is similar to `mask_irq()` but with less confusing parameters.

            :param flags: A value of `rf24_irq_flags_e` to influence the radio's IRQ pin.
                The default value (``RF24_IRQ_NONE``) will disable the radio's IRQ pin.
                Multiple events can be enabled by OR-ing `rf24_irq_flags_e` values together.

                .. code-block:: python

                    radio.set_status_flags(int(RF24_IRQ_ALL))
                    # is equivalent to
                    radio.set_status_flags(
                        int(RF24_RX_DR) | int(RF24_TX_DS) | int(RF24_TX_DF)
                    )
        )docstr",
             py::arg("flags") = RF24_IRQ_NONE)

        .def("setStatusFlags", &RF24::setStatusFlags, R"docstr(
            setStatusFlags(flags: int = RF24_IRQ_NONE.value) -> None
        )docstr",
             py::arg("flags") = RF24_IRQ_NONE)

        // *****************************************************************************

        .def("clear_status_flags", &RF24::clearStatusFlags, R"docstr(
            clear_status_flags(flags: int = RF24_IRQ_ALL.value) -> int

            Clear the Status flags that caused an interrupt event.

            .. note::
                This function is similar to `what_happened()` because it also returns the
                status flags that caused the interrupt event. However, this function takes
                a 1-byte integer instead of bit-banging each flag into 3 1-byte booleans.

            .. caution::
                When used in an ISR (Interrupt Service routine), there is a chance that the
                returned bits ``0b1110`` (RX pipe number) is inaccurate. See the
                datasheet for more detail.

            :param flags: The IRQ flags to clear. Default value is all of them (``RF24_IRQ_ALL``).
                Multiple flags can be cleared by OR-ing `rf24_irq_flags_e` values together.

                .. code-block:: python

                    radio.clear_status_flags()
                    # is equivalent to
                    radio.clear_status_flags(int(RF24_IRQ_ALL))
                    # is equivalent to
                    radio.clear_status_flags(
                        int(RF24_RX_DR) | int(RF24_TX_DS) | int(RF24_TX_DF)
                    )

            :Returns: The STATUS byte from the radio's register before it was modified. Use
                enumerations of `rf24_irq_flags_e` as masks to interpret the STATUS byte's meaning(s).
        )docstr",
             py::arg("flags") = RF24_IRQ_ALL)

        .def("clearStatusFlags", &RF24::clearStatusFlags, R"docstr(
            clearStatusFlags(flags: int = RF24_IRQ_ALL.value) -> int
        )docstr",
             py::arg("flags") = RF24_IRQ_ALL)

        // *****************************************************************************

        .def("get_status_flags", &RF24::getStatusFlags, R"docstr(
            get_status_flags() -> int

            Get the latest STATUS byte returned from the last SPI transaction.

            .. note:: This does not actually perform any SPI transaction with the radio.
                Use `RF24.update()` instead to get a fresh copy of the Status flags at
                the slight cost of performance.

            :Returns: The STATUS byte from the radio's register as the latest SPI transaction. Use
                enumerations of `rf24_irq_flags_e` as masks to interpret the STATUS byte's meaning(s).
        )docstr")

        .def("getStatusFlags", &RF24::getStatusFlags, R"docstr(
            getStatusFlags() -> int
        )docstr")

        // *****************************************************************************

        .def("update", &RF24::update, R"docstr(
            update() -> int

            Get an updated STATUS byte from the radio.

            :returns: The STATUS byte fetched from the radio's register. Use enumerations of
                `rf24_irq_flags_e` as masks to interpret the STATUS byte's meaning(s).
        )docstr")

        // *****************************************************************************

        .def("print_status", &RF24Wrapper::printStatus, R"docstr(
            print_status(flags: int) -> None

            A convenient function to display the meaning of the STATUS byte
            returned from `RF24.get_status_flags()`, `RF24.update()`,
            or `RF24.clear_status_flags()`.
        )docstr",
             py::arg("flags"))

        .def("printStatus", &RF24Wrapper::printStatus, R"docstr(
            printStatus(flags: int) -> None
        )docstr",
             py::arg("flags"))

        // *****************************************************************************

        .def("ce_pin", &RF24::ce, R"docstr(
            ce_pin(level: bool) -> None

            Set radio's CE (Chip Enable) pin state.

            .. warning:: Please see the datasheet for a much more detailed description of this pin.

            .. note:: This is only publicly exposed for advanced use cases such as complex networking or
                streaming consecutive payloads without robust error handling.
                Typical uses are satisfied by simply using `RF24.start_listening()` for RX mode or
                `RF24.stop_listening()` and `RF24.write()` for TX mode.

            :param level: In RX mode, `True` (``HIGH``) causes the radio to begin actively listening.
                In TX mode, `True` (``HIGH``) (+ 130 microsecond delay) causes the radio to begin transmitting.
                Setting this to `False` (``LOW``) will cause the radio to stop transmitting or receiving in any mode.
        )docstr",
             py::arg("level"))

        .def("ce", &RF24::ce, R"docstr(
            ce(level: bool) -> None
        )docstr",
             py::arg("level"))

        // *****************************************************************************

        .def("read", &RF24Wrapper::read, R"docstr(
            read(length: int) -> bytearray

            Fetch data from the radio's RX FIFO.

            :param int length: The number of bytes to fetch from the radio's RX FIFO.
                If this parameter is not specified, then the length of the next available payload
                is used. The maximum number of bytes that can be fetched at once is 32 bytes.

                - If the value specified by this parameter is less than the length of the next
                  available payload, then the payload will remain in the RX FIFO.
                - If the value specified by this parameter is greater than the length of the next
                  available payload, then the data from the next level of the RX FIFO is returned
                  (if any).
                - If the value specified by this parameter is greater than the length of the last
                  available payload, then the payload's last byte is returned repeatedly until the
                  length value is fulfilled.
            :Returns: A `bytearray` of the specified ``length`` containing the data from the
                payload in the RX FIFO.

            .. seealso::

                - :py:attr:`~pyrf24.RF24.payload_size`
                - :py:meth:`~pyrf24.RF24.get_dynamic_payload_size()`
                - :py:meth:`~pyrf24.RF24.available()`
        )docstr",
             py::arg("length") = 0)

        // *****************************************************************************
        // ************************** functions that have overloads

        .def(py::init<rf24_gpio_pin_t, rf24_gpio_pin_t, uint32_t>(), R"docstr(
            __init__(ce_pin: int, csn_pin: int, spi_speed: int = 10000000)
            __init__(spi_speed: int = 10000000)

            Create a RF24 object.

            :param int ce_pin: The pin number connected to the radio's CE pin.
            :param int csn_pin: The pin number connected to the radio's CSN pin.
            :param int spi_speed: The SPI bus speed (in Hz). Defaults to 10 MHz when not specified.
        )docstr",
             py::arg("ce_pin") = RF24_PIN_INVALID, py::arg("csn_pin") = RF24_PIN_INVALID, py::arg("spi_speed") = 10000000)

        // *****************************************************************************

        .def(py::init<uint32_t>(), R"docstr(
            If it is desirable to create a RF24 object in which the pin numbers are dynamically
            configured, the ``ce_pin`` and ``csn_pin`` parameters can be omitted.

            .. important:: If dynamically configuring the pin numbers, then they must be set using
                the overloaded :py:meth:`~pyrf24.RF24.begin()` function.
        )docstr",
             py::arg("spi_speed") = 10000000)

        // *****************************************************************************

        .def("begin", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::begin), R"docstr(
            begin() -> bool \
            begin(ce_pin: int, csn_pin: int) -> bool

            Initialize the radio's hardware.
        )docstr")

        // *****************************************************************************

        .def("begin", static_cast<bool (RF24Wrapper::*)(rf24_gpio_pin_t, rf24_gpio_pin_t)>(&RF24Wrapper::begin), R"docstr(
            If configuring the radio's CE & CSN pins dynamically, then the respective pin numbers must be passed to this function.

            :param int ce_pin: The pin number connected to the radio's CE pin.
            :param int csn_pin: The pin number connected to the radio's CSN pin.

            :Returns: `True` if the radio was configured successfully, otherwise `False`.
        )docstr",
             py::arg("ce_pin"), py::arg("csn_pin"))

        // *****************************************************************************

        .def("available", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::available), R"docstr(
            available() -> bool

            Check if there is an available payload in the radio's RX FIFO.

            :Returns: `True` if there is a payload in the radio's RX FIFO, otherwise `False`.

            .. seealso::
                Use :py:meth:`~pyrf24.RF24.available_pipe()` to get the pipe number that received the
                next available payload.
        )docstr")

        // *****************************************************************************

        .def("open_rx_pipe", &RF24Wrapper::open_rx_pipe, R"docstr(
            open_rx_pipe(pipe_number: int, address: Union[bytearray, bytes, int])

            Open a data pipe for receiving.

            :param int pipe_number: The pipe number to use for receiving transmissions. This value should be in range [0, 5].
            :param bytes,bytearray,int address: The address assigned to the specified data pipe for receiving transmissions.

                .. deprecated:: 0.2.1
                    Use `bytes` or `bytearray` to specify address.

                    Using an `int` to specify the address has been deprecated because of
                    inconsistent endianess and needless memory consumption.
        )docstr",
             py::arg("pipe_number"), py::arg("address"))

        .def("openReadingPipe", &RF24Wrapper::open_rx_pipe, R"docstr(
            openReadingPipe(pipe_number: int, address: Union[bytearray, bytes])
        )docstr",
             py::arg("pipe_number"), py::arg("address"))

        // *****************************************************************************

        .def("open_rx_pipe", static_cast<void (RF24Wrapper::*)(uint8_t, uint64_t)>(&RF24Wrapper::openReadingPipe), R"docstr(
            .. deprecated:: 0.2.1 Use a `bytes` or `bytearray` address instead of an `int` address.

                For backward compatibility, this function's ``address`` parameter can also take a 64-bit integer.
        )docstr",
             py::arg("pipe_number"), py::arg("address"))

        .def("openReadingPipe", static_cast<void (RF24Wrapper::*)(uint8_t, uint64_t)>(&RF24Wrapper::openReadingPipe), R"docstr(
            openReadingPipe(pipe_number: int, address: int)
        )docstr",
             py::arg("pipe_number"), py::arg("address"))

        // *****************************************************************************

        .def("open_tx_pipe", &RF24Wrapper::open_tx_pipe, R"docstr(
            open_tx_pipe(address: Union[bytearray, bytes, int])

            Open data pipe 0 for transmitting to a specified address.

            .. deprecated:: 0.5.0 Use `RF24.stop_listening()` instead.

            :param bytes,bytearray,int address: The address assigned to data pipe 0 for outgoing transmissions.

                .. deprecated:: 0.2.1
                    Use `bytes` or `bytearray` to specify address.

                    Using an `int` to specify the address has been deprecated because of
                    inconsistent endianess and needless memory consumption.
        )docstr",
             py::arg("address"))

        .def("openWritingPipe", &RF24Wrapper::open_tx_pipe, R"docstr(
            openWritingPipe(address: Union[bytearray, bytes])
        )docstr",
             py::arg("address"))

        // *****************************************************************************

        .def("open_tx_pipe", static_cast<void (RF24Wrapper::*)(uint64_t)>(&RF24Wrapper::openWritingPipe), R"docstr(

            .. deprecated:: 0.2.1 Use a `bytes` or `bytearray` address instead of an `int` address.

                For backward compatibility, this function's ``address`` parameter can also take a 64-bit integer.
        )docstr",
             py::arg("address"))

        .def("openWritingPipe", static_cast<void (RF24Wrapper::*)(uint64_t)>(&RF24Wrapper::openWritingPipe), R"docstr(
            openWritingPipe(address: int)
        )docstr",
             py::arg("address"))

        // *****************************************************************************

        .def("stopListening", static_cast<void (RF24Wrapper::*)(void)>(&RF24Wrapper::stopListening), R"docstr(
            stopListening() -> None

            Put the radio into TX mode.
        )docstr")

        // *****************************************************************************

        .def("stop_listening", static_cast<void (RF24Wrapper::*)(void)>(&RF24Wrapper::stopListening), R"docstr(
            stop_listening() -> None
        )docstr")

        // *****************************************************************************

        .def("stopListening", static_cast<void (RF24Wrapper::*)(py::buffer)>(&RF24Wrapper::stop_listening), R"docstr(
            stopListening(tx_address: bytes | bytearray) -> None

            Put the radio into TX mode.
        )docstr",
             py::arg("tx_address"))

        // *****************************************************************************

        .def("stop_listening", static_cast<void (RF24Wrapper::*)(py::buffer)>(&RF24Wrapper::stop_listening), R"docstr(
            stop_listening(tx_address: bytes | bytearray) -> None

            Stop listening for incoming messages, set the TX address, and switch to transmit mode.

            .. code-block:: python
                :caption: Do this to set the TX address (and enter TX mode) before calling `RF24.write()`

                radio.stop_listening(b"1Node")
                radio.write(data)

            .. warning:: When the ACK payloads feature is enabled, the TX FIFO buffers are
                flushed when calling this function. This is meant to discard any ACK
                payloads that were not appended to acknowledgment packets.
        )docstr",
             py::arg("tx_address"))

        // *****************************************************************************

        .def("set_auto_ack", static_cast<void (RF24Wrapper::*)(bool)>(&RF24Wrapper::setAutoAck), R"docstr(
            set_auto_ack(enable: bool) \
            set_auto_ack(pipe_number: int, enable: bool)

            Configure the radio's automatic acknowledgement feature for all data pipes or a specific data pipe.

            :param bool enable: Enable/disable (`True`/`False`) the radio's auto-ack feature for all data pipes or for the specified
                ``pipe_number``.
            :param int pipe_number: The pipe number for which the ``enable`` parameter is about. This value must be in range [0, 5].
        )docstr",
             py::arg("enable"))

        .def("setAutoAck", static_cast<void (RF24Wrapper::*)(bool)>(&RF24Wrapper::setAutoAck), R"docstr(
            setAutoAck(enable: bool) \
            setAutoAck(pipe_number: int, enable: bool)
        )docstr",
             py::arg("enable"))

        // *****************************************************************************

        .def("set_auto_ack", static_cast<void (RF24Wrapper::*)(uint8_t, bool)>(&RF24Wrapper::setAutoAck),
             py::arg("pipe_number"), py::arg("enable"))

        .def("setAutoAck", static_cast<void (RF24Wrapper::*)(uint8_t, bool)>(&RF24Wrapper::setAutoAck),
             py::arg("pipe_number"), py::arg("enable"))

        // *****************************************************************************

        .def("setPayloadSize", &RF24Wrapper::setPayloadSize, R"docstr(
            setPayloadSize(length: int)

            Configure the radio's static payload size (outgoing and incoming) for all data pipes.

            :param int length: The length of static payloads used for all data pipes.
        )docstr",
             py::arg("length"))

        // *****************************************************************************

        .def("tx_standby", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::txStandBy), R"docstr(
            tx_standby() -> bool \
            tx_standby(timeout: int, start_tx: bool = True) -> bool

            When using `write_fast()` to fill the radio's TX FIFO, call this blocking function to allow the radio time to transmit.

            The default timeout value is 95 milliseconds. Any failed transmissions will be re-attempted until successfully
            transmitted or timeout occurs.
        )docstr")

        .def("txStandBy", static_cast<bool (RF24Wrapper::*)()>(&RF24Wrapper::txStandBy), R"docstr(
            txStandBy() -> bool
        )docstr")

        // *****************************************************************************

        .def("tx_standby", static_cast<bool (RF24Wrapper::*)(uint32_t, bool)>(&RF24Wrapper::txStandBy), R"docstr(
            Optionally, a timeout value can be supplied to augment how long the function will block during transmission.

            :param int timeout: The maximum time (in milliseconds) to allow for transmission. This value is added to the
                default 95 milliseconds.
            :param bool start_tx: Set this parameter to `False` if the radio's CE pin is already active. This parameter is optional.
        )docstr",
             py::arg("timeout"), py::arg("start_tx") = true)

        .def("txStandBy", static_cast<bool (RF24Wrapper::*)(uint32_t, bool)>(&RF24Wrapper::txStandBy), R"docstr(
            txStandBy(timeout: int, start_tx: bool = True) -> bool
        )docstr",
             py::arg("timeout"), py::arg("start_tx") = true)

        // *****************************************************************************

        .def("is_fifo", static_cast<bool (RF24Wrapper::*)(bool, bool)>(&RF24Wrapper::isFifo), R"docstr(
            is_fifo(about_tx: bool, check_empty: bool) -> bool \
            is_fifo(about_tx: bool) -> rf24_fifo_state_e


            Get information about a specified FIFO buffers.

            :param bool about_tx: Ensure the returned data is about the TX FIFO. Set this to `False`
                to make returned data describe the RX FIFO.
            :param bool check_empty: Check if the specified FIFO is empty. Set this to `False` to
                check if the specified FIFO is full.

                .. deprecated:: 0.4.4
                    Use ``is_fifo(about_tx: bool)`` for better precision.

                    The ``is_fifo(about_tx: bool, check_empty: bool)`` signature may yield
                    inaccurate information when data suffers corruption over the SPI bus'
                    MISO line.
        )docstr",
             py::arg("about_tx"), py::arg("check_empty"))

        .def("isFifo", static_cast<bool (RF24Wrapper::*)(bool, bool)>(&RF24Wrapper::isFifo), R"docstr(
            isFifo(about_tx: bool, check_empty: bool) -> bool
        )docstr",
             py::arg("about_tx"), py::arg("check_empty"))

        // *****************************************************************************

        .def("is_fifo", static_cast<rf24_fifo_state_e (RF24Wrapper::*)(bool)>(&RF24Wrapper::isFifo), R"docstr(
            :Returns:
                - A `bool` describing if the specified FIFO is empty or full
                  if the ``check_empty`` parameter was specified.
                - An enumeration of `rf24_fifo_state_e` describing the specifed FIFO's state
                  if the ``check_empty`` parameter was unspecified.
        )docstr",
             py::arg("about_tx"))

        .def("isFifo", static_cast<rf24_fifo_state_e (RF24Wrapper::*)(bool)>(&RF24Wrapper::isFifo), R"docstr(
            isFifo(about_tx: bool) -> rf24_fifo_state_e
        )docstr",
             py::arg("about_tx"))

        // *****************************************************************************
        // *********************************** functions wrapped into python object's properties

        .def_property("channel", &RF24Wrapper::getChannel, &RF24Wrapper::setChannel, R"docstr(
            This `int` attribute represents the radio's configured channel (AKA frequency). This roughly translates to frequency (in Hz).
            So, channel 76 (the default setting) is

            | 2400 MHz + 76 = 2.4076 GHz
        )docstr")

        // *****************************************************************************

        .def_property("pa_level", &RF24Wrapper::get_pa_level, &RF24Wrapper::set_pa_level, R"docstr(
            This attribute represents the radio's configured Power Amplitude level.

            .. seealso:: Accepted values are defined in the `rf24_pa_dbm_e` enum struct.
        )docstr")

        // *****************************************************************************

        .def_property("payload_size", &RF24Wrapper::getPayloadSize, &RF24Wrapper::setPayloadSize, R"docstr(
            This `int` attribute represents the radio's static payload lengths. Maximum length is 32 bytes; minimum is 1 byte.

            .. note:: This attribute is only used when the radio's `dynamic_payloads` feature is disabled
                (which is disabled by default).
        )docstr")

        .def_property("payloadSize", &RF24Wrapper::getPayloadSize, &RF24Wrapper::setPayloadSize)

        // *****************************************************************************

        .def_property("data_rate", &RF24Wrapper::get_data_rate, &RF24Wrapper::setDataRate, R"docstr(
            This attribute represents the radio's OTA data rate.

            .. hint:: The units "BPS" stand for "Bits Per Second" (not Bytes per second).
            .. seealso:: Accepted values are pre-defined in the `rf24_datarate_e` enum struct.
        )docstr")

        // *****************************************************************************

        .def_property("crc_length", &RF24Wrapper::getCRCLength, &RF24Wrapper::setCRCLength, R"docstr(
            This attribute represents the radio's CRC checksum length (in bits).

            .. seealso:: Accepted values are predefined in the `rf24_crclength_e` enum struct.
            .. note::
                The radio automatically uses CRC checksums when the auto-ack feature is enabled.
                This attribute may not reflect this situation if CRC is disabled when auto-ack is enabled.
        )docstr")

        // *****************************************************************************

        .def_property("power", &RF24Wrapper::isPowerUp, &RF24Wrapper::power, R"docstr(
            This `bool` attribute represents the radio's power status. `False` means the radio
            is powered down.
        )docstr")

        // *****************************************************************************

        .def_property("listen", &RF24Wrapper::isListening, &RF24Wrapper::listen, R"docstr(
            This `bool` attribute represents the radio's primary mode (RX/TX).

            .. hint::

                1. Be sure to call :py:meth:`~pyrf24.RF24.open_rx_pipe()` before
                   setting :py:attr:`~pyrf24.RF24.listen` to `True`.
                2. Do not call :py:meth:`~pyrf24.RF24.write()` while in RX mode, without
                   first setting :py:attr:`~pyrf24.RF24.listen` to `False`.
                3. Call :py:meth:`~pyrf24.RF24.available()` to check for incoming traffic,
                   and use :py:meth:`~pyrf24.RF24.read()` to get it.

            .. important::
                If there was a call to :py:meth:`~pyrf24.RF24.open_rx_pipe()`
                about pipe 0 prior to setting this attribute to `False`, then this attribute
                will re-write the address that was last set to RX pipe 0.
                This is because :py:meth:`~pyrf24.RF24.open_tx_pipe()`
                will overwrite the address to RX pipe 0 for proper auto-ack
                functionality.
            .. note::
                When the ACK payloads feature is enabled, the TX FIFO buffers are
                flushed when changing this attribute to `True` (RX mode). This is meant to
                discard any ACK payloads that were not appended to acknowledgment packets
                during TX mode.
        )docstr")

        // *****************************************************************************

        .def_property("dynamic_payloads", &RF24Wrapper::is_dynamic_payloads_enabled, &RF24Wrapper::dynamic_payloads, R"docstr(
            This `bool` attribute represents the radio's dynamic payload length feature for all data pipes.

            .. note::
                Since `ack_payloads` requires Dynamic Payload lengths,
                `ack_payloads` are also disabled when setting this attribute is set to `False`.
        )docstr")

        // *****************************************************************************

        .def_property("ack_payloads", &RF24Wrapper::is_ack_payloads_enabled, &RF24Wrapper::toggle_ack_payloads, R"docstr(
            This `bool` attribute represents the status of the radio's acknowledgement payload
            feature for appending data to automatic acknowledgement packets.

            .. important::
                To use acknowledgement payloads, the `dynamic_payloads` and auto-ack features must be enabled.

                This attribute does not automatically enable the auto-ack feature
                on pipe 0 because the auto-ack feature is enabled for all pipes by default.
            .. seealso::
                Review `write_ack_payload()` and `set_auto_ack()`. Use :meth:`~RF24.available()` and
                :meth:`~RF24.read()` to fetch a received acknowledgement payload.
        )docstr")

        // *****************************************************************************

        .def_property("address_width", &RF24Wrapper::get_address_width, &RF24Wrapper::setAddressWidth, R"docstr(
            This `int` attribute represents length of addresses used on the radio's data pipes.
            Accepted values range [2, 5].

            .. warning::
                Using an address width of 2 bytes is not officially supported by the nRF24L01.
                This ability is exposed for advanced reverse engineering purposes.
        )docstr")

#if defined(FAILURE_HANDLING)
        // *****************************************************************************

        .def_readwrite("failure_detected", &RF24Wrapper::failureDetected, R"docstr(
            The number of accumulative transmission failures specific to the life
            cycle of the `RF24` object.
        )docstr")

        .def_readwrite("failureDetected", &RF24Wrapper::failureDetected, R"docstr(
            The number of accumulative transmission failures specific to the life
            cycle of the `RF24` object.
        )docstr")
#endif // defined (FAILURE_HANDLING)

        // *****************************************************************************

        .def_property_readonly("is_valid", &RF24Wrapper::isValid, R"docstr(
            This read-only attribute represents if the radio's CE & CSN pins are configured properly.
        )docstr")

        // *****************************************************************************

        .def_property_readonly("is_plus_variant", &RF24Wrapper::isPVariant, R"docstr(
            This read-only `bool` attribute represents if the detected radio is a nRF24L01+ model.
        )docstr")

        // *****************************************************************************

        .def_property_readonly("rpd", &RF24Wrapper::testRPD, R"docstr(
            This read-only `bool` attribute represents if the radio detected a signal above -64 dbm in RX mode.

            .. hint::
                RPD stands for "Received Power Detection". Non-plus variants of nRF24L01
                call this attribute CD (short for "Carrier Detection") because this feature
                was originally made available for government mandated hardware tests.
        )docstr")

        // *****************************************************************************

        .def_property_readonly("rx_fifo_full", &RF24Wrapper::rxFifoFull, R"docstr(
            This `bool` attribute represents if all 3 levels of the radio's RX FIFO are occupied.
        )docstr")

        // *****************************************************************************

        .def_readwrite("cs_delay", &RF24Wrapper::csDelay, R"docstr(
            The `int` number of microseconds used as a delay when the radio's CSN pin is made active.
        )docstr")

        // *****************************************************************************

        .def_property_readonly("is_chip_connected", &RF24Wrapper::isChipConnected, R"docstr(
            Check if the SPI bus is working with the radio. This read-only `bool` attribute assumes that
            :py:meth:`~pyrf24.RF24.begin()` returned `True`.
        )docstr")

        .def("isChipConnected", &RF24Wrapper::isChipConnected, R"docstr(
            isChipConnected() -> bool
        )docstr")

        // *****************************************************************************

        .def_readwrite("tx_delay", &RF24Wrapper::txDelay, R"docstr(
            The driver will delay for this duration (`int` in microseconds) when `listen` is set to `False`.

            When responding to payloads, faster devices like ARM(RPi) are much faster than Arduino:

            1. Arduino sends data to RPi, switches to RX mode
            2. The RPi receives the data, switches to TX mode and sends before the Arduino radio is in RX mode
            3. If AutoACK is disabled, this can be set as low as 0. If AutoACK enabled, set to 100uS minimum on RPi

            .. warning::
                If set to 0, ensure 130uS delay after `listen` is set to `False` before any transmitting.
        )docstr")

        .def_readwrite("txDelay", &RF24Wrapper::txDelay)

        // *****************************************************************************
        // **************** functions that accept python's buffer protocol objects (bytes, bytearray)

        .def("start_fast_write", &RF24Wrapper::startFastWrite, R"docstr(
            start_fast_write(buf: Union[bytearray, bytes], multicast: bool = False, start_tx: bool = True) -> None

            Write a payload to the radio's TX FIFO.

            .. seealso::
                Use `tx_standby()` to ensure the radio has had time to transmit the payload(s) from the TX FIFO.

            :param bytes,bytearray buf: The payload to load into the TX FIFO.
            :param bool multicast: Set this parameter to `True` to flag the payload for
                no acknowledgement. This parameter makes use of the radio's ``NO_ACK`` flag
                for the individual payload. Defaults to `False`.

                .. important:: This parameter requires that the `enable_dynamic_ack()` function
                    is called at least once prior to calling this function.
            :param bool start_tx: Set this parameter to `True` to activate transmission. By
                default this parameter is set to `True`. Notice this parameter controls the radio's
                CE pin as required. Setting this parameter to `False` will only leave the radio's
                CE pin unchanged.
        )docstr",
             py::arg("buf"), py::arg("multicast") = false, py::arg("start_tx") = true)

        .def("startFastWrite", &RF24Wrapper::startFastWrite, R"docstr(
            startFastWrite(buf: Union[bytearray, bytes], multicast: bool = False, start_tx: bool = True) -> None
        )docstr",
             py::arg("buf"), py::arg("multicast") = false, py::arg("start_tx") = true)

        // *****************************************************************************

        .def("start_write", &RF24Wrapper::startWrite, R"docstr(
            start_write(buf: Union[bytearray, bytes], multicast: bool = False) -> bool

            For backward compatibility, this function is similar to `start_fast_write()`.

            :param bytes,bytearray buf: The payload to load into the TX FIFO.
            :param bool multicast: Set this parameter to `True` to flag the payload for
                no acknowledgement. This parameter makes use of the radio's ``NO_ACK`` flag
                for the individual payload. Defaults to `False`.

                .. important:: This parameter requires that the `enable_dynamic_ack()` function
                    is called at least once prior to calling this function.

            :Returns: `True` if the payload was loaded into the radio's TX FIFO, otherwise `False`.
        )docstr",
             py::arg("buf"), py::arg("multicast") = false)

        .def("startWrite", &RF24Wrapper::startWrite, R"docstr(
            startWrite(buf: Union[bytearray, bytes], multicast: bool = False) -> bool
        )docstr",
             py::arg("buf"), py::arg("multicast") = false)

        // *****************************************************************************

        .def("write", &RF24Wrapper::write, R"docstr(
            write(buf: Union[bytearray, bytes], multicast: bool = False) -> bool

            Transmit a single payload.

            :param bytes,bytearray buf: The payload to load into the TX FIFO.
            :param bool multicast: Set this parameter to `True` to flag the payload for
                no acknowledgement. This parameter makes use of the radio's ``NO_ACK`` flag
                for the individual payload. Defaults to `False`.

                .. important:: This parameter requires that the `enable_dynamic_ack()` function
                    is called at least once prior to calling this function.

            :Returns: `True` if the payload was successfully transmitted, otherwise `False`.
        )docstr",
             py::arg("buf"), py::arg("multicast") = false)

        // *****************************************************************************

        .def("write_ack_payload", &RF24Wrapper::writeAckPayload, R"docstr(
            write_ack_payload(pipe: int, buf: Union[bytearray, bytes]) -> bool

            Load a payload into the TX FIFO to be used in the ACK packet of automatic acknowledgements.

            :param int pipe: The pipe number to use for the acknowledging payload.

                .. seealso:: Set the pipe's assigned address using `open_rx_pipe()`
            :param bytes,bytearray buf: The payload to load into the TX FIFO.

            :Returns: `True` if the payload was loaded into the radio's TX FIFO, otherwise `False`.
        )docstr",
             py::arg("pipe"), py::arg("buf"))

        .def("writeAckPayload", &RF24Wrapper::writeAckPayload, R"docstr(
            writeAckPayload(pipe: int, buf: Union[bytearray, bytes]) -> bool
        )docstr",
             py::arg("pipe"), py::arg("buf"))

        // *****************************************************************************

        .def("write_blocking", &RF24Wrapper::writeBlocking, R"docstr(
            write_blocking(buf: Union[bytearray, bytes], timeout: int) -> bool

            A blocking function to load a payload into the radio's TX FIFO. If there is no un-occupied
            level of the TX FIFO, this function waits until a level becomes available or the specified
            timeout is reached.

            :param bytes,bytearray buf: The payload to load into the TX FIFO.
            :param int timeout: The amount of time (in milliseconds) to wait while there is no
                available level in the TX FIFO.

            :Returns: `True` if the payload was loaded into the radio's TX FIFO, otherwise `False`.
        )docstr",
             py::arg("buf"), py::arg("timeout"))

        .def("writeBlocking", &RF24Wrapper::writeBlocking, R"docstr(
            writeBlocking(buf: Union[bytearray, bytes], timeout: int) -> bool
        )docstr",
             py::arg("buf"), py::arg("timeout"))

        // *****************************************************************************

        .def("write_fast", &RF24Wrapper::writeFast, R"docstr(
            write_fast(buf: Union[bytearray, bytes], multicast: bool = False) -> bool

            Simply load a payload into the radio's TX FIFO and assert the radio's CE pin to activate transmission.

            .. seealso::
                Use `tx_standby()` to ensure the radio has had time to transmit the payload(s) from the TX FIFO.

            :param bytes,bytearray buf: The payload to load into the TX FIFO.
            :param bool multicast: Set this parameter to `True` to flag the payload for
                no acknowledgement. This parameter makes use of the radio's ``NO_ACK`` flag
                for the individual payload. Defaults to `False`.

                .. important:: This parameter requires that the `enable_dynamic_ack()` function
                    is called at least once prior to calling this function.

            :Returns: `True` if the payload was loaded into the radio's TX FIFO, otherwise `False`.
        )docstr",
             py::arg("buf"), py::arg("multicast") = false)

        .def("writeFast", &RF24Wrapper::writeFast, R"docstr(
            writeFast(buf: Union[bytearray, bytes], multicast: bool = False) -> bool
        )docstr",
             py::arg("buf"), py::arg("multicast") = false);
}
