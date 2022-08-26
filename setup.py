"""Build & Install script for the pyrf24 package or python wrappers about
the RF24 C++ libraries."""
import os
import platform
import subprocess
import sys
from pathlib import Path
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

IS_LINUX = platform.system().title() == "Linux"


class CMakeExtension(Extension):
    """A class that wraps the generic mechanism for compiling a python C-extension.

    A CMakeExtension needs a sourcedir instead of a file list.
    The name must be the single output extension from the CMake build.
    """
    def __init__(self, name, sourcedir="", **kwargs):
        kwargs.pop("sources", None)
        Extension.__init__(self, name, sources=[], **kwargs)
        self.sourcedir = str(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    """A class that wraps the builtin mechanism for building a
    distributable wheel from a compiled c-extension"""
    def build_extension(self, ext: Extension):
        extdir = str(
            (Path(self.get_ext_fullpath(ext.name)).parent / ext.name).resolve()
        )

        # required for auto-detection & inclusion of auxiliary "native" libs
        if not extdir.endswith(os.sep):
            extdir += os.sep

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-DCMAKE_INSTALL_PREFIX={Path('src/pyrf24').resolve().as_posix()}",
        ]
        build_args = []
        for key, value in ext.define_macros:
            macro = f"-D{key}"
            if value:
                macro += f"={value}"
            build_args.append(macro)

        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]
        # lastly, specify the RF24_DRIVER to configure the build with
        for arg in cmake_args:
            if arg.startswith("-DRF24_DRIVER"):
                break
        else:
            driver = os.environ.get("RF24_DRIVER", "SPIDEV")
            cmake_args.append(f"-DRF24_DRIVER={driver}")

        build_temp = Path(self.build_temp, ext.name)
        if not build_temp.exists():
            build_temp.mkdir(parents=True)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        # for verbose make output:
        # build_args.append("--verbose")
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)


setup_args = dict(
    zip_safe=False,
    packages=["pyrf24"],
    package_dir={"pyrf24": "src/pyrf24"},
    package_data={"pyrf24": ["rf24.pyi", "rf24_network.pyi", "rf24_mesh.pyi"]},
)

if IS_LINUX:
    setup_args["cmdclass"] = {"build_ext": CMakeBuild}
    setup_args["ext_modules"] = [CMakeExtension("pyrf24")]
    # We could define compile-time macros here:
    #
    # ext_module = CMakeExtension(
    #     "pyrf24",
    #     define_macros = [
    #         (MESH_DEBUG, 1), # <-- results in -DMESH_DEBUG=1
    #     ]
    # )
    # setup_args["ext_modules"] = [ext_module]
    #
    # But, we have a better solution using CMake options.
    # Instead, we look for an env var named ``CMAKE_ARGS``. For example,
    # the following cmd done before ``pip install`` will turn on all debugging output:
    #
    # export CMAKE_ARGS="-DRF24_DEBUG=ON -DSERIAL_DEBUG=ON -DMESH_DEBUG=ON"

setup(**setup_args)
