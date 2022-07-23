"""Build & Install script for the pyrf24 package or python wrappers about
the RF24 C++ libraries."""
import platform

IS_LINUX = platform.system().title() == "Linux"
if IS_LINUX:
    from skbuild import setup
else:
    from distutils.core import setup  # pylint: disable=deprecated-module


long_description = ""  # pylint: disable=invalid-name
with open("README.rst", "r", encoding="utf-8") as file_handle:
    long_description = file_handle.read()


def exclude_rf24_utility_folder(cmake_manifest):
    """Exclude unnecessary header files from the built python pkg."""
    return list(filter(lambda name: not (name.endswith(".h")), cmake_manifest))


kwargs = {
    "name": "pyrf24",
    "author": "2bndy5",
    "author_email": "2bndy5@gmail.com",
    "description": "A python package for the wrapping nRF24 related C++ libraries",
    "long_description": long_description,
    "long_description_content_type": "text/x-rst",
    "url": "https://github.com/nRF24/pyRF24",
    "packages": ["pyrf24"],
    "package_data": {"pyrf24": ["rf24.pyi", "rf24_network.pyi", "rf24_mesh.pyi"]},
    "package_dir": {"": "src"},
    "zip_safe": False,
    "license": "GNU General Public License v2 (GPLv2)",
    "classifiers": [
        "Development Status :: 4 - Beta",  # TODO change this when ready
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    "python_requires": ">=3.7",
    "keywords": "nrf24l01 nRF24L01+ raspberry pi driver radio transceiver",
    # Extra links for the sidebar on pypi
    "project_urls": {
        "Documentation": "http://nRF24.github.io/pyRF24",
    },
    "download_url": "https://github.com/nRF24/pyRF24/releases",
}

if IS_LINUX:
    kwargs["cmake_install_dir"] = "src/pyrf24"
    kwargs["cmake_args"] = ["-DRF24_DRIVER=SPIDEV"]
    kwargs["cmake_process_manifest_hook"] = exclude_rf24_utility_folder

setup(**kwargs)
