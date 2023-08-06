#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.pfx',
  description = 'Easy context prefixes for messages.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170903',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3', 'cs.x'],
  keywords = ['python2', 'python3'],
  long_description = 'The primary facility here is Pfx,\na context manager which manitains a per thread stack of context prefixes.\nUsage is like this::\n\n  from cs.pfx import Pfx\n  ...\n  def parser(filename):\n    with Pfx("parse(%r)", filename):\n      with open(filename) as f:\n        for line, lineno in enumerate(f, 1):\n          with Pfx("%d", lineno) as P:\n            if line_is_invalid(line):\n              raise ValueError("problem!")\n            P.info("line = %r", line)\n\nThis produces log messages like::\n\n  datafile: 1: line = \'foo\\n\'\n\nand exception messages like::\n\n  datafile: 17: problem!\n\nwhich lets one put just the relevant complaint in exception and log\nmessages and get useful calling context on the output.\nThis does make for wordier logs and exceptions\nbut used with a little discretion produces far more debugable results.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.pfx'],
)
