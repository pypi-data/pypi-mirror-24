#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.env',
  description = 'a few environment related functions',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170905',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.lex'],
  keywords = ['python2', 'python3'],
  long_description = "* LOGDIR, VARRUN, FLAGDIR: constants defining standard places used in other modules\n\n* envsub: replace substrings of the form '$var' with the value of 'var' from `environ`.\n\n* getenv: fetch environment value, optionally performing substitution",
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.env'],
)
