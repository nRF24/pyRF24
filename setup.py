import setuptools

long_description = ""
with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrf24",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
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