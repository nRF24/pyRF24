"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# pylint: disable=invalid-name
import os

try:
    from importlib.metadata import version as get_version
except ImportError:  # for python v3.7 or older
    from importlib_metadata import version as get_version  # type: ignore

# -- Project information -----------------------------------------------------

project = "pyRF24"
copyright = "2023, TMRh20 Avamander 2bndy5"  # pylint: disable=redefined-builtin
author = "TMRh20 Avamander 2bndy5"
language = "en"

# The full version, including alpha/beta/rc tags
release = get_version("pyrf24")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_immaterial",
    "sphinx_immaterial.graphviz",
    "sphinx_social_cards",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# autodoc gets confused about __init__() functions' signature when overloaded
#
# autodoc_class_signature = "separated"
# autoclass_content = "class"
# autodoc_docstring_signature = False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".env"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "any"


# -- Options for sphinx_social_cards -------------------------------------------------
social_cards = {
    "site_url": os.environ.get(
        "READTHEDOCS_CANONICAL_URL", "https://nrf24.github.io/pyRF24/"
    ),
    "description": (
        "A python package that wraps the RF24, RF24Network, and RF24Mesh C++ libraries."
    ),
    "image_paths": ["social_cards/images"],
    "cards_layout_dir": ["social_cards/layouts"],
    "cards_layout": "custom",
    "cards_layout_options": {
        "logo": {
            "image": "material/access-point",
            "color": "lime",
        },
        "background_color": "#2c2c2c",
        "background_image": "logo_large_no-bg.png",
        "color": "lime",
    },
    # "debug": {
    #     "enable": True,
    #     "color": "lime",
    # },
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_immaterial"
html_theme_options = {
    "features": [
        # "navigation.expand",
        "navigation.tabs",
        # "toc.integrate",
        # "navigation.sections",
        "navigation.instant",
        # "header.autohide",
        "navigation.top",
        # "search.highlight",
        "search.share",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "lime",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-blue",
            "accent": "green",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
    ],
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/nRF24/pyRF24/",
    "repo_name": "pyRF24",
    # If False, expand all TOC entries
    "globaltoc_collapse": False,
}

# turn off some features specific to sphinx-immaterial theme
object_description_options = [
    ("py:.*", dict(include_fields_in_toc=False, generate_synopses=None)),
    ("py:parameter", dict(include_in_toc=False)),
]

sphinx_immaterial_custom_admonitions = [
    {
        "name": "warning",
        "color": (255, 66, 66),
        "icon": "octicons/alert-24",
        "override": True,
    },
    {
        "name": "note",
        "icon": "octicons/pencil-24",
        "override": True,
    },
    {
        "name": "seealso",
        "color": (255, 66, 252),
        "icon": "octicons/eye-24",
        "title": "See Also",
        "override": True,
    },
    {
        "name": "hint",
        "icon": "material/school",
        "override": True,
    },
    {
        "name": "tip",
        "icon": "material/school",
        "override": True,
    },
    {
        "name": "important",
        "icon": "material/alert-decagram",
        "override": True,
    },
]

python_type_aliases = {
    "pyrf24.rf24.rf24_datarate_e": "rf24_datarate_e",
}

# Set link name generated in the top bar.
html_title = "pyRF24 library"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = ["custom_material.css"]

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = "_static/new_favicon.ico"

# project logo
html_logo = "_static/Logo_large.jpg"

# split site index page into 2 pages:
# 1 with only alphabet-like links to partial lists, 1 with full listing
html_split_index = True
