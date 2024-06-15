/* The main module that allows compiling all bindings into 1 python extension.  */
#include "pyRF24.h"
#include "pyRF24Network.h"
#include "pyRF24Mesh.h"

PYBIND11_MODULE(pyrf24, m)
{
    m.doc() = "A Python module that wraps all RF24 C++ library's API";
    py::options options;
    options.disable_function_signatures();
    init_rf24(m);
    init_rf24network(m);
    init_rf24mesh(m);
}