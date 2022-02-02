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
    capacitor to stabilize the power supply. Usually 100 microfarad is enough, but the capacitance
    ultimately depends on the nature of your power supply's stability.

.. note::
    Notice that RPi.GPIO (for python) is used to manage the GPIO pins on the Raspberry Pi
    (exclusively during the `interrupt_configure.py <examples.html#interrupt-configure>`_ example).

    RPi.GPIO is not required for normal usage (when not using the radio's IRQ pin).

    .. code-block:: bash

        sudo apt install python3-rpi.gpio

Installing from Source
======================

Installing from source will require CMake and CPython headers:

.. code-block:: bash

    sudo apt install python3-dev cmake

To build this python package locally, you need to have cloned this library's repository with its submodules.

.. code-block:: bash

    git clone --recurse-submodules https://github.com/nRF24/pyRF24.git
    cd pyRF24
    python -m pip install .

Using a specific RF24 driver
----------------------------

If you want to build the package using a different RF24 driver (like MRAA, RPi, wiringPi, etc), then
it is appropriate to pass an additional argument to the install command:

.. note::
    This approach cannot be done with the ``pip install .`` command.

.. code-block:: bash

    python setup.py install -DRF24_DRIVER=RPi

Building a wheel
-----------------

Building a somewhat portable binary distribution for python packages involves building a
.whl file known as a wheel. This wheel can be used to install the pyrf24 package on systems using the
same version of CPython, CPU architecture, and C standard lib.

1. Because building wheels is not done in an isolated build environment, it is advised that
   some build-time dependencies be installed manually to ensure up-to-date stable releases are used.

   .. code-block:: bash

       python -m pip install scikit-build ninja

2. Using the same directory that you cloned the pyrf24 library into:

   .. code-block:: bash

       python setup.py bdist_wheel


   .. important::
       It is recommended to purge any previous build artifacts before re-building the package.

       .. code-block:: bash

           rm -r _skbuild/

3. To install a built wheel, simply pass the wheel's path and file name to ``pip install``:
   
   .. code-block:: bash

       python -m pip install dist/pyrf24-MAJOR.MINOR.PATCH-cp3X-cp3X-linux_ARCH.whl

   Where the following would be replaced accordingly:
   
   - ``MAJOR.MINOR.PATCH`` is the current version of the pyrf24 package
   - ``cp3X`` is the version of python used to build the wheel (ie ``cp39`` for CPython 3.9)
     The second occurrence of ``cp3X`` describes the CPython ABI compatibility.
   - ``ARCH`` is the architecture type of the CPU. This corresponds to the compiler used.
     On Raspberry Pi OS (32 bit), this will be ``armv7l``.

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

    python -m pip install -r docs/requirements.txt

.. important::
    If pip outputs a warning about your ``path/to/Python/Python3x/Scripts`` folder not
    added to your OS environment variable ``PATH``, then you will likely get an error message like
    ``sphinx-build command not found`` when building the documentation. For more information on
    installing sphinx, see the
    `official Sphinx install instructions
    <https://www.sphinx-doc.org/en/master/usage/installation.html>`_.

    .. warning::
        This documentation's theme requires Sphinx v4.0+. So, it is not recommended to install
        sphinx from ``apt`` on Linux because the version distributed with the OS's PPA repository
        may not be the most recent version of sphinx.

Building the Documentation
--------------------------

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
