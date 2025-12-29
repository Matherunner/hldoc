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

extensions = []

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

html_logo = "static/hlprlogo.png"

html_title = "Half-Life Physics Reference"

html_theme_options = {}

# html_theme_options = {
# "logo": "hlprlogo.png",
# "description": "An attempt to document and exploit the in-game physics of Half-Life.",
# "font_size": "18px",
# "font_family": "sans-serif",
# "page_width": "1150px",
# "sidebar_width": "250px",
# "code_font_size": "85%",
# "base_bg": "#fafaf4",
# "body_text": "rgb(59, 50, 40)",
# "analytics_id": "UA-67469786-1",
# }

# html_sidebars = {
#     "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
# }

html_last_updated_fmt = "%b %d, %Y"

html_static_path = ["static"]
html_css_files = ["css/custom.css"]

html_copy_source = False
html_show_sourcelink = False

pygments_style = "sphinx"
pygments_dark_style = "monokai"
