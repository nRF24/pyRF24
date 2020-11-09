Introduction
============

This is the official home of the python wrappers for the RF24 stack. It is meant for Linux-based SoC boards like the Raspberry Pi.

.. warning:: This repo is currently under construction and is meant as a place holder for the proper package name on pypi.org

Pinout
======

.. image:: https://lastminuteengineers.com/wp-content/uploads/2018/07/Pinout-nRF24L01-Wireless-Transceiver-Module.png
    :target: https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/#nrf24l01-transceiver-module-pinout

The nRF24L01's CE and IRQ pins can be connected to other GPIO pins on the SoC. The MISO, MOSI, SCK are limited to the corresponding counterparts on the SoC's SPI bus. The CSN pin is limited to the chosen SPI bus's "Chip Select" options (Also labeled as "CE" pins on many Raspberry Pi pinout diagrams). The following table shows the default pins used in all the `examples <examples.html>`_ for this package.

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

.. warning:: If connecting a nRF24L01+PA+LNA module to the Raspberry Pi, you MUST use a external 3V power supply because the Raspberry Pi (all models) do not provide enough power for the nRF24L01+PA+LNA modules.

.. important:: It is highly recommended that the nRF24L01's VCC and GND pins have a parallel capacitor to stablize the power supply. Usually 100 microfarad is enough, but the capacitance ultimately depends on the nature of your power supply's stability.

Dependencies
============

To build this python package locally, you need to have boost.python installed.

.. code-block::

    sudo apt install libboost-python-dev

Make sure that the following dependencies are also installed (sometimes the OS comes with these included). Notice that RPi.GPIO (for python) is used to manage the GPIO pins on the Raspberry Pi.

.. code-block::

    sudo apt install python3-dev python3-setuptools python3-rpi.gpio

Documentation
=============

Before submitting contributions, you should make sure that any documentation changes builds successfully. This can be done locally.

Documentation Dependencies
--------------------------

This package's documentation is built with the python package Sphinx and the readthedocs theme for sphinx.

.. code-block::

    pip install Sphinx sphinx-rtd-theme

To build the documentation locally:

.. code-block::

    cd docs
    sphinx build -E -W . _build

The "docs/_build" folder should now contain the html files that would be hosted on deployment. direct your internet browser to the html files in this folder to make sure your changes have been rendered correctly.

.. note:: The flags ``-E`` and ``-W`` will ensure the docs fail to build on any error or warning (just like it does when deploying the docs online).
