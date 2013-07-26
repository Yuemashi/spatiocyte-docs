import sys, os

extensions = ['sphinx.ext.pngmath', 'sphinx.ext.autodoc']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'spatiocyte'
copyright = 'Satya Arjunan, 2013 E-Cell project'

version = '1.0'
release = '1.0'

exclude_trees = ['_build']

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

