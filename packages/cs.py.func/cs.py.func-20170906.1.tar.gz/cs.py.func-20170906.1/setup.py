#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.func',
  description = 'Convenience facilities related to Python functions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170906.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.excutils'],
  keywords = ['python2', 'python3'],
  long_description = "* funcname: return a function's name, preferably __name__\n* funccite: cite a function (name and code location)\n* @prop: replacement for @property which turns internal AttributeErrors into RuntimeErrors\n* some decorators to verifying the return types of functions",
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.func'],
)
