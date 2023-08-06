#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.portfwd',
  description = 'Manage persistent ssh tunnels and port forwards.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170906',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['portfwd = cs.app.portfwd:main']},
  install_requires = ['cs.app.flag', 'cs.app.svcd', 'cs.env', 'cs.logutils', 'cs.pfx', 'cs.psutils', 'cs.py.func', 'cs.sh'],
  keywords = ['python2', 'python3'],
  long_description = 'Portfwd runs a collection of ssh tunnel commands persistently,\neach it its own `cs.app.svcd <https://pypi.org/project/cs.app.svcd>`_ instance\nwith all the visibility and process control that SvcD brings.\n\nIt reads tunnel preconditions from special comments within the ssh config file.\nIt uses the configuration options from the config file\nas the SvcD signature function\nthus restarting particular ssh tunnels when their specific configuration changes.\nIt has an "automatic" mode (the -A option)\nwhich monitors the desired list of tunnels\nfrom status expressed via `cs.app.flag <https://pypi.org/project/cs.app.flag>`_\nwhich allows live addition or removal of tunnels as needed.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.portfwd'],
)
