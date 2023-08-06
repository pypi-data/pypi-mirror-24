#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.tty',
  description = 'Functions related to terminals.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170903',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Environment :: Console', 'Operating System :: POSIX', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Terminals', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = '``ttysize(fd)``\n  return a namedtuple (rows, columns) with the current terminal size;\n  UNIX only (uses the stty command)\n``statusline(text,...)``\n  update the terminal status line with ``text``\n``statusline_bs(text,...)``\n  return a byte string to update the terminal status line with ``text``',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.tty'],
)
