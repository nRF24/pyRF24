.. |piwheels-badge| image:: https://img.shields.io/piwheels/v/pyrf24?color=informational
    :target: https://www.piwheels.org/project/pyrf24/
    :alt: piwheels
.. |rtd-badge| image:: https://img.shields.io/readthedocs/pyrf24?label=ReadTheDocs&logo=readthedocs&logoColor=white
    :target: https://pyrf24.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |pypi-downloads| image:: https://img.shields.io/pepy/dt/pyrf24?label=PyPI%20Downloads&color=blue
    :target: https://pepy.tech/project/pyrf24
    :alt: PyPI Downloads
.. |ci-badge| image:: https://github.com/nRF24/pyRF24/actions/workflows/build.yml/badge.svg
    :target: https://github.com/nRF24/pyRF24/actions/workflows/build.yml
    :alt: Build CI

|piwheels-badge| |rtd-badge| |pypi-downloads| |ci-badge|

Introduction
============

This is the official home of the python wrappers for the RF24 stack. It is meant for Linux-based
SoC boards like the Raspberry Pi. Documentation is hosted at http://pyrf24.rtfd.io/.

Pinout
~~~~~~

.. image:: https://lastminuteengineers.com/wp-content/uploads/2018/07/Pinout-nRF24L01-Wireless-Transceiver-Module.png
    :target: https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/#nrf24l01-transceiver-module-pinout

The nRF24L01's CE and IRQ pins can be connected to other GPIO pins on the SoC. The MISO, MOSI, SCK
are limited to the corresponding counterparts on the SoC's SPI bus. The CSN pin is limited to the
chosen SPI bus's "Chip Select" options (also labeled as "CE" pins on many Raspberry Pi pinout
diagrams). The following table shows the default pins used in all the
`examples <https://pyrf24.readthedocs.io/en/latest/examples.html>`_ for this package.

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
    Notice that `gpiod <https://pypi.org/project/gpiod>`_ is used to watch the radio's IRQ pin
    (exclusively during the
    `interrupt_configure.py <https://pyrf24.readthedocs.io/en/latest/examples.html#interrupt-configure>`_
    example).

    `gpiod <https://pypi.org/project/gpiod>`_ is not required for normal usage (when not using the radio's IRQ pin).

    .. code-block:: bash

        sudo apt install python3-dev
        pip install gpiod

Installing from PyPI
~~~~~~~~~~~~~~~~~~~~

Simply use:

.. code-block:: python

    python -m pip install pyrf24

We have distributed binary wheels to pypi.org for easy installation and automated dependency.
These wheels specifically target any Linux platform on ``aarch64`` architecture.
If you're using Raspberry Pi OS (32 bit), then the above command will fetch ``armv7l`` binary
wheels from the piwheels index (which is already configured for use in the Raspberry Pi OS).

.. note::
    If you're installing from a Linux machine that is not using an architecture ``aarch64``
    or ``armv7l``, then pip may try to build the package from source code.
    In this case, you'll likely need to install some extra build dependencies:

    .. code-block:: bash

        sudo apt install python3-dev cmake

Installing from Github
~~~~~~~~~~~~~~~~~~~~~~

Installing from source will require CMake and CPython headers:

.. code-block:: bash

    sudo apt install python3-dev cmake

To build this python package locally, you need to have cloned this library's repository with its submodules.

.. code-block:: bash

    git clone --recurse-submodules https://github.com/nRF24/pyRF24.git
    cd pyRF24
    python -m pip install . -v

.. hint::
    For consecutive build attempts, it is recommended to delete any previous build artifacts
    before attempting to build again.

    .. code-block:: bash

        rm -r build/ dist/

.. note::
    The ``-v`` is optional. Here, we use it to show that pip isn't frozen during the
    build process.

    Installing the package can take a long time, and you might think that pip is frozen
    on the step labeled "Building wheel for pyrf24 (pyproject.toml)". Just wait for about
    5 minutes (maybe longer on older/slower variants of Raspberry Pi).

Building a wheel
-----------------

Building a somewhat portable binary distribution for python packages involves building a
.whl file known as a wheel. This wheel can be used to install the pyrf24 package on systems using the
same version of CPython, CPU architecture, and C standard lib.

1. Because building wheels is not done in an isolated build environment, it is advised that
   some build-time dependencies be installed manually to ensure up-to-date stable releases are used.
   Execute the following from the root directory of this repo:

   .. code-block:: bash

       python -m pip install -r requirements.txt

   .. note::
       This step only needs to be done once.

2. Using the same directory that you cloned the pyrf24 library into:

   .. code-block:: bash

       python -m pip wheel -w dist .


   .. important::
       It is recommended to purge any previous build artifacts before re-building the package.

       .. code-block:: bash

           rm -r build/ dist/

3. To install a built wheel, simply pass the wheel's path and file name to ``pip install``:

   .. code-block:: bash

       python -m pip install dist/pyrf24-MAJOR.MINOR.PATCH-cp3X-cp3X-linux_ARCH.whl

   Where the following would be replaced accordingly:

   - ``MAJOR.MINOR.PATCH`` is the current version of the pyrf24 package.

     - If not building a tagged commit, then the version will describe the commit relative to
       the number of commits since the latest tag. For example, ``0.1.1.post1.dev3`` is
       the third commit (``dev3``) since the first "post release" (``post1``) after the
       tagged version ``0.1.1``. This adhere's to `PEP440 <https://peps.python.org/pep-0440>`_.
   - ``cp3X`` is the version of python used to build the wheel (ie ``cp39`` for CPython 3.9)
     The second occurrence of ``cp3X`` describes the CPython ABI compatibility.
   - ``ARCH`` is the architecture type of the CPU. This corresponds to the compiler used.
     On Raspberry Pi OS (32 bit), this will be ``armv7l``.

.. _using-specific-driver:

Using a specific RF24 driver
----------------------------

By default, this package is built using the RF24 driver ``SPIDEV``. If you want to build the
package using a different RF24 driver (like ``RPi``, ``MRAA``, ``wiringPi``, or ``pigpio``),
then it is necessary to use an environment variable containing additional arguments for CMake:

.. code-block:: bash

    export CMAKE_ARGS="-DRF24_DRIVER=RPi"

.. hint::
    You can also use this environment variable to enable debug output from different
    layers of the RF24 stack. For a list of supported options, look at the script in
    `this repository's cmake/using_flags.cmake <https://github.com/nRF24/pyRF24/blob/main/cmake/using_flags.cmake>`_.

    The following value will turn on debug output for the RF24Mesh and RF24Network
    classes (respectively).

    .. code-block:: bash

        export CMAKE_ARGS="-DMESH_DEBUG=ON -DSERIAL_DEBUG=ON"

Then just build and install the package from source as usual.

.. code-block:: bash

    python -m pip install . -v

Differences in API
~~~~~~~~~~~~~~~~~~

This package intentionally adheres to `PEP8 <https://pep8.org/>`_ standards as much as possible.
This means that class members' names use snake casing  (eg. ``get_dynamic_payload_size()``)
instead of using the C++ conventional camel casing (eg. ``getDynamicPayloadSize()``). However,
the older python wrappers provided with each C++ library (RF24, RF24Network, & RF24Mesh) had used
camel casing. So, the API provided by this package exposes both snake cased and camel cased
versions of the API. The camel cased API is not documented to avoid duplicate and
complicated documentation.

.. code-block:: py

    radio.print_details()  # documented
    # can also be invoked as
    radio.printDetails()  # not documented

Some of the C++ functions that do not accept arguments are wrapped as a class property. But, the C++
style functions are still exposed. For example:

.. code-block:: py

    radio.listen = False
    # is equivalent to
    radio.stopListening()  # not documented

    radio.listen = True
    # is equivalent to
    radio.startListening()  # not documented

Migrating to pyrf24
-------------------

If you have a project that uses code from the older individually installed wrappers,
then you can use this package as a drop-in replacement. You only need to change the
import statements in your project's source. Everything from the old individual wrappers
is exposed through the ``pyrf24`` package.

.. list-table::
    :header-rows: 1

    * - Using the old individual wrappers
      - Using the pyrf24 package
    * - .. code-block:: python

            from RF24 import RF24, RF24_PA_LOW
      - .. code-block:: python

            from pyrf24 import RF24, RF24_PA_LOW
    * - .. code-block:: python

            from RF24 import RF24
            from RF24Network import RF24Network, RF24NetworkHeader
      - .. code-block:: python

            from pyrf24 import RF24, RF24Network, RF24NetworkHeader
    * - .. code-block:: python

            from RF24 import RF24
            from RF24Network import RF24Network
            from RF24Mesh import RF24Mesh
      - .. code-block:: python

            from pyrf24 import RF24, RF24Network, RF24Mesh

Python Type Hints
-----------------

This package is designed to only function on Linux devices. But, it is possible to install this
package on non-Linux devices to get the stub files which help auto-completion and type checking
in various development environments.

Documentation
~~~~~~~~~~~~~

Each release has corresponding documentation hosted at http://pyrf24.rtfd.io/.

Before submitting contributions, you should make sure that any documentation changes build
successfully. This can be done locally but **on Linux only**. The documentation of API requires
this package (& all its latest changes) be installed.

This package's documentation is built with the python package Sphinx and the sphinx-immaterial theme.
It also uses the dot tool provided by the graphviz software to generate graphs.

1. Install Graphviz

   .. code-block:: shell

       sudo apt-get install graphviz

2. Installing Sphinx necessities

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
           may not be the most recent version of Sphinx.

3. Building the Documentation

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
