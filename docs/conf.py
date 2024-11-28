# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import re
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "AMPAPI_Python"
copyright = "2024 - Present, Katelynn Cadwallader"  # noqa: A001
author = "Katelynn Cadwallader"

# The full version, including alpha/beta/rc tags
with open("../ampapi/__init__.py") as f:  # noqa: PTH123
    match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    version = match.group(1) if match is not None else ""

release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, pathlib.Path("..").as_posix())
sys.path.append(pathlib.Path().as_posix())
sys.path.append(pathlib.Path("./docs/extensions").as_posix())
sys.path.append(pathlib.Path("./docs/nodes").as_posix())

extensions = [
    "sphinx.ext.autodoc",  # Adds support for parsing autoDoc doc-strings.
    "sphinx.ext.viewcode",  # Adds the [source] link to functions and classes.
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",  # Supports .. todo:: // .. todolist::
    "sphinx.ext.intersphinx",  # Links to other Sphinx docs via .. ref::
    "sphinx.ext.autosectionlabel",  #
    "enum_tools.autoenum",  # Should handle enums for Sphinx docs.
    "prettyversion",  # Custom lib from dpy/Umbra
    "details",  # Custom lib from dpy/Umbra
    "exception_hierarchy",  # Custom lib from dpy/Umbra
]

_GITHUB: str = "https://github.com/k8thekat/AMPAPI_Python"
extlinks: dict[str, tuple[str, str]] = {"issue": (f"{_GITHUB}/issues/%s", "GH-%s")}
resource_links: dict[str, str] = {
    "github": _GITHUB,
    "issues": f"{_GITHUB}/issues",
    "discussions": f"{_GITHUB}/discussions",
    "examples": f"{_GITHUB}/tree/main/examples",
}

# Links used for cross-referencing other documentation
intersphinx_mapping: dict[str, tuple] = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable", None),
    # "setting_nodes": ("../nodes/setting_nodes.md", None),
    # "permission_nodes": ("../nodes/permission_nodes.md", None),
}


templates_path = ["_templates"]
# this is useful when using `.. include::`; make sure to exclude the file/directory below.
# eg. .. include:: ./events/*_events.rst needs to be excluded either via "events" or "*_events.rst"
exclude_patterns = [
    "build",
    "samples",
]

autodoc_member_order: str = "bysource"

# -- Napoleon Settings section ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_admonition_for_examples: bool = True
napoleon_use_admonition_for_notes: bool = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#confval-napoleon_preprocess_types
napoleon_preprocess_types = False

# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#confval-napoleon_type_aliases
napoleon_use_param = True  # Default True.
napoleon_type_aliases = None  # Default is None

# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#confval-napoleon_custom_sections
napoleon_custom_sections = None  # Default is None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["styles/furo.css"]

# Prolog for asynchronous functions
# Follows https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html structure.
rst_prolog: str = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
.. |classmethod| replace:: This function is a https://docs.python.org/3/library/functions.html#classmethod
"""
