# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# General information about the project.
project = "HLPR"
copyright = "2014—{}, Jiangwei Chong".format(datetime.datetime.now().year)

author = "Jiangwei Chong"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "venv"]

root_doc = "index"

# Enable figure numbering.
numfig = True

numfig_format = {
    "figure": "Fig. %s.",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"

html_theme_options = {
    "logo": "hlprlogo.png",
    "description": "An attempt to document and exploit the in-game physics of Half-Life.",
    "font_size": "13pt",
    "font_family": '"minion pro", georgia, serif',
    "code_font_size": "85%",
    "base_bg": "#fafaf4",
    "analytics_id": "UA-67469786-1",
}

html_last_updated_fmt = "%b %d, %Y"

html_static_path = ["_static"]
