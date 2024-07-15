# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

import datetime
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("../.."))

# Allow reading Django files/syntax, in order to generate docs from them.
import django
from django.conf import settings
from adminlte2_pdq import __version__


# -- Project information -----------------------------------------------------

project = "Django-AdminLTE2-PDQ"
copyright = f"{datetime.date.today().year}, David Barnes"
author = "David Barnes"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Configure autosection so that duplicated titles are unique per page.
autosectionlabel_prefix_document = True

# Configure autosection so that it will not look any deeper than 3 levels.
# This should help when we are listing the same files as headings in examples.
autosectionlabel_maxdepth = 4


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# -- Django Configuration ----------------------------------------------------
settings.configure(
    SECRET_KEY="something-to-make-Django-happy",
    INSTALLED_APPS=[
        "adminlte2_pdq",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
    ],
)
django.setup()
