#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.upd',
  description = 'Single line status updates with minimal update sequences.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170903',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.lex', 'cs.tty'],
  keywords = ['python2', 'python3'],
  long_description = '* Upd: a class accepting update strings which emits minimal text to update a progress line.\n\n-- out(s): update the line to show the string ``s``\n\n-- nl(s): flush the output line, write ``s`` with a newline, restore the status line\n\n-- without(func,...): flush the output line, call func, restore the status line\n\nThis is available as an output mode in cs.logutils.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.upd'],
)
