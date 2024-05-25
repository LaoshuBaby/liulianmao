# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------

project = 'liulianmao'
author = 'LaoshuBaby'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
