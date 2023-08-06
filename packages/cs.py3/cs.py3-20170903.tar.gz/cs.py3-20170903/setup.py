#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py3',
  description = 'Aids for code sharing between python2 and python3.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170903',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Presents various names in python 3 flavour for common use in python 2 and python 3.',
  package_dir = {'': 'lib/python'},
  packages = ['cs.py3'],
)
