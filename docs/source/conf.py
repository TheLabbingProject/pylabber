# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import django
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pylabber.settings")
django.setup()

# -- Project information -----------------------------------------------------

project = "pylabber"
copyright = "2020, Zvi Baratz"
author = "Zvi Baratz"

# The full version, including alpha/beta/rc tags
release = "0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
]

EXCLUDED_MEMBERS = (
    "id",
    "DoesNotExist",
    "MultipleObjectsReturned",
    "get_next_by_date_joined",
    "get_previous_by_date_joined",
    "get_next_by_created",
    "get_previous_by_created",
    "get_next_by_modified",
    "get_previous_by_modified",
    "auth_token",
    "objects",
    "user_id",
    "study_id",
    "Meta",
)

autodoc_default_options = {
    "exclude-members": ", ".join(EXCLUDED_MEMBERS),
    "undoc-members": False,
    "member-order": "groupwise",
}

# Allow safely referencing sections between documents.
# See: https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#confval-autosectionlabel_prefix_document
autosectionlabel_prefix_document = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": ("http://django.readthedocs.org/en/latest/", None),
    "django_filters": (
        "https://django-filter.readthedocs.io/en/master/",
        None,
    ),
    "django_extensions": (
        "https://django-extensions.readthedocs.io/en/latest/",
        None,
    ),
}
