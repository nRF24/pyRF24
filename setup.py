import os
import sys
import setuptools
import crossunixccompiler

long_description = ""
with open("README.rst", "r") as fh:
    long_description = fh.read()


def process_configparams():

    with open("../Makefile.inc") as f:
        config_lines = f.read().splitlines()

    cflags = os.getenv("CFLAGS", "")
    for line in config_lines:
        identifier, value = line.split("=", 1)
        if identifier == "CPUFLAGS":
            cflags += " " + value
        elif identifier == "HEADER_DIR":
            cflags += " -I" + os.path.dirname(value)
        elif identifier == "LIB_DIR":
            cflags += " -L" + value
        elif identifier in ("CC", "CXX"):
            os.environ[identifier] = value

    os.environ["CFLAGS"] = cflags


if sys.version_info >= (3,):
    BOOST_LIB = "boost_python3"
else:
    BOOST_LIB = "boost_python"

process_configparams()
crossunixccompiler.register()

module_RF24 = setuptools.Extension(
    "RF24",
    libraries=["rf24", BOOST_LIB],
    sources=["pyRF24.cpp"]
)

module_RF24Network = setuptools.Extension(
    "RF24Network",
    libraries=["rf24network", BOOST_LIB],
    sources=["pyRF24Network.cpp"]
)

module_RF24Mesh = setuptools.Extension(
    "RF24Mesh",
    libraries=["rf24mesh", "rf24network", BOOST_LIB],
    sources=["pyRF24Mesh.cpp"],
)

setuptools.setup(
    name="pyrf24",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="TMRh20 Avamander mz-fuzzy haseebehsan wamonite 2bndy5",
    author_email="tmrh20@gmail.com avamander@gmail.com "
    "mzfuzzy800@gmail.com fa14-bse-081@student.comsats.edu.pk "
    "2bndy5@gmail.com",
    description="A python package for the wrapping RF24 related C++ libraries",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/nRF24/pyRF24",
    packages=["pyrf24"],
    license="GNU General Public License v2 (GPLv2)",
    classifiers=[
        "Development Status :: 1 - Planning",  # TODO change this when ready
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    keywords="nrf24l01 nRF24L01+ raspberry pi driver radio transceiver",
    # Extra links for the sidebar on pypi
    project_urls={
        "Documentation": "http://nRF24.github.io/pyRF24",
    },
    download_url="https://github.com/nRF24/pyRF24/releases",
)