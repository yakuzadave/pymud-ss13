# Copyright (c) 2018-2021 mudpy authors. Permission to use, copy,
# modify, and distribute this software is granted under terms
# provided in the LICENSE file distributed with this software.

import collections
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'mudpy'

add_function_parentheses = True
add_module_names = True
copyright = '2004-2021, mudpy authors'
extensions = ['sphinx.ext.autodoc']
html_favicon = '_static/logo.svg'
html_logo = '_static/logo.svg'
html_sidebars = {'**': [
    'about.html',
    'donate.html',
    'navigation.html',
    'relations.html',
    'searchbox.html',
]}
html_theme_options = {
    'description': 'The mudpy MUD server engine.',
    'extra_nav_links': collections.OrderedDict((
        ('Browse Source', 'https://mudpy.org/code/mudpy/'),
        ('Bug Reporting', 'https://mudpy.org/bugs/mudpy/'),
        ('Git Clone URL', 'https://mudpy.org/code/mudpy/'),
        ('Release Files', 'https://mudpy.org/dist/mudpy/'),
    )),
    'fixed_sidebar': True,
    'logo_name': True,
    'logo_text_align': 'center',
}
html_title = 'mudpy'
htmlhelp_basename = '%sdoc' % project
latex_documents = [(
    'index', '%s.tex' % project, '%s' % project, 'Jeremy Stanley', 'manual')]
pygments_style = 'sphinx'
source_suffix = '.rst'
