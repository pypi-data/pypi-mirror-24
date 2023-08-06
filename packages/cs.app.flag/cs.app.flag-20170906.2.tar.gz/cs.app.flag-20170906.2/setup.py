#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.flag',
  description = 'Persistent filesystem based flags for state and control.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170906.2',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.env', 'cs.lex'],
  keywords = ['python2', 'python3'],
  long_description = 'Filesystem visible boolean flags\nfor control and status,\nallowing easy monitoring of services or other status,\nand control by flag management\nfor programmes which also monitor the flags.\n\nThe flags are expressed as individual files with uppercase names\nin a common directory ($HOME/var/flags by default);\nan empty or missing file is "false"\nand a nonempty file is "true".\n\nThe Flags class provides easy Pythonic access to this directory.\nIt presents as a modifiable mapping whose keys are the flag names::\n\n  flags = Flags()\n  flags[\'UNTOPPOST\'] = True\n\nThe is also a FlaggedMixin class providing convenient methods and attributes\nfor maintaining a collection of flags associated with some object\nwith flag names prefixed by the object\'s .name attribute uppercased and with an underscore appended::\n\n  class SvcD(...,FlaggedMixin):\n    def __init__(self, name, ...)\n      self.name = name\n      FlaggedMixin.__init__(self)\n      ...\n    def disable(self):\n      self.flag_disabled = True\n    def restart(self):\n      self.flag_restart = True\n    def _restart(self):\n      self.flag_restart = False\n      ... restart the SvcD ...',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.flag'],
)
