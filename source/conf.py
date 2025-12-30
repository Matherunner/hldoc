# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# General information about the project.
project = "HLPR"
copyright = "2014\u2013{}, Jiangwei Chong".format(datetime.datetime.now().year)

author = "Jiangwei Chong"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_proof"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "venv"]

root_doc = "index"

numfig = True
numfig_format = {
    "figure": "Fig. %s.",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

html_logo = "static/hlprlogo.svg"

html_title = "Half-Life Physics Reference"

html_theme_options = {
    "light_css_variables": {
        "color-foreground-primary": "rgb(59, 50, 40)",
        "color-background-primary": "#fcfcf6",
        "color-background-secondary": "#f9f9f0",
        "color-table-header-background": "#f2f2ee",
    },
}

html_last_updated_fmt = "%b %d, %Y"

html_static_path = ["static"]
html_css_files = []

html_copy_source = False
html_show_sourcelink = False

pygments_style = "sphinx"
pygments_dark_style = "monokai"
