Introduction
============

This is the official home of the python wrappers for the RF24 stack. It is meant for Linux-based
SoC boards like the Raspberry Pi.

Pinout
======

.. image:: https://lastminuteengineers.com/wp-content/uploads/2018/07/Pinout-nRF24L01-Wireless-Transceiver-Module.png
    :target: https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/#nrf24l01-transceiver-module-pinout

The nRF24L01's CE and IRQ pins can be connected to other GPIO pins on the SoC. The MISO, MOSI, SCK
are limited to the corresponding counterparts on the SoC's SPI bus. The CSN pin is limited to the
chosen SPI bus's "Chip Select" options (Also labeled as "CE" pins on many Raspberry Pi pinout
diagrams). The following table shows the default pins used in all the
`examples <examples.html>`_ for this package.

.. csv-table::
    :header: nRF24L01, Raspberry Pi

    GND, GND
    VCC, 3V
    CE, GPIO22
    CSN, "GPIO8 (CE0)"
    SCK, "GPIO11 (SCK)"
    MOSI, "GPIO10 (MOSI)"
    MISO, "GPIO9 (MISO)"
    IRQ, GPIO12

The IRQ pin is not typically connected, and it is only used in the interrupt_configure example.

.. warning:: If connecting a nRF24L01+PA+LNA module to the Raspberry Pi, you MUST use a external 3V
    power supply because the Raspberry Pi (all models) do not provide enough power for the
    nRF24L01+PA+LNA modules.

.. important:: It is highly recommended that the nRF24L01's VCC and GND pins have a parallel
    capacitor to stablize the power supply. Usually 100 microfarad is enough, but the capacitance
    ultimately depends on the nature of your power supply's stability.

Dependencies
============

To build this python package locally, you need to have cloned this library's repository with its submodules.

.. code-block:: bash

    git clone --recurse-submodules https://github.com/nRF24/pyRF24.git
    cd pyRF24

It is advised that some dependencies be installed manually to ensure up-to-date stable releases are used.

.. note::
    Notice that RPi.GPIO (for python) is used to manage the GPIO pins on the Raspberry Pi
    (excusively during the `interrupt_configure.py <examples.html#interrupt-configure>`_ example).

    RPi.GPIO is not required for normal usage.

.. code-block:: bash

    sudo apt install python3-dev python3-rpi.gpio cmake

The following dependencies are also installed during build process.

    * setuptools >= 42
    * wheel
    * pybind11 >= 2.7.1
    * scikit-build
    * cmake (though it may be out-of-date)
    * ninja (not actually used but needed to satisfy scikit-build dependency)

Lastly, use the following command to install the python package from the root directory of this
library's repository:

.. code-block:: shell

    python3 -m pip install .

Documentation
=============

Before submitting contributions, you should make sure that any documentation changes builds
successfully. This can be done locally.

Documentation Dependencies
--------------------------

This package's documentation is built with the python package Sphinx and the readthedocs theme for
sphinx.

.. note::
    If you installed sphinx using ``apt``, then it is likely out-of-date and will override any virtual
    python environments installation of Sphinx. Simply uninstall sphinx (using ``apt``) will remedy
    this problem.

.. code-block:: bash

    python3 -m pip install Sphinx sphinx-rtd-theme

or optioinally use the following command from the repository's root directory

.. code-block:: bash

    python3 -m pip install -r docs/requirements.txt

.. important::
    If pip outputs a warning about your ``path/to/Python/Python3x/Scripts`` folder not
    added to your OS environment variable ``PATH``, then you will likely get an error message like
    ``sphinx-build command not found`` when building the documentation. For more information on
    installing sphinx, see the
    `official Sphinx install instructions
    <https://www.sphinx-doc.org/en/master/usage/installation.html>`_.

To build the documentation locally, the pyrf24 package needs to be installed first. Then run:

.. code-block:: bash

    cd docs
    sphinx-build -E -W . _build

The ``docs/_build`` folder should now contain the html files that would be hosted on deployment.
Direct your internet browser to the html files in this folder to make sure your changes have been
rendered correctly.

.. note::
    The flags ``-E`` and ``-W`` will ensure the docs fail to build on any error or warning
    (just like it does when deploying the docs online).
