# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ccHBGF'
copyright = '2025, E. H. von Rein'
author = 'E. H. von Rein'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_title = 'ccHBGF 0.1.0'
html_logo = "_static/logo.png"
html_static_path = ['_static']

html_theme_options = {
    "repository_url": "https://github.com/ehvr20/ccHBGF",
    "repository_branch": "main",
    "path_to_docs": "docs/",
    "use_repository_button": True,
    "use_issues_button": False,
    "use_edit_page_button": True,
    "home_page_in_toc": True,
    "show_navbar_depth": 2,  # Controls the depth of the sidebar navigation
    "show_toc_level": 2,     # Number of levels to show in the Table of Contents
}
