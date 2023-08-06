#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.excutils',
  description = 'Convenience facilities for managing exceptions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20170904',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Presents:\n\n* return_exc_info: call supplied function with arguments, return either (function_result, None) or (None, exc_info) if an exception was raised.\n\n* @returns_exc_info, a decorator for a function which wraps in it return_exc_info.\n\n* @noexc, a decorator for a function whose exceptions should never escape; instead they are logged. The initial use case was inside logging functions, where I have had a failed logging action abort a program. Obviously this is a decorator which should see very little use.\n\n* @noexc_gen, a decorator for generators with similar effect to @noexc for ordinary functions.\n\n* NoExceptions, a context manager to intercept most exceptions\n\n* LogExceptions, a context manager to log exceptions\n\n* @logexc, a decorator to make a function log exceptions it raises\n\n* @transmute, a decorator to transmute an inner exception to another exception type\n\n* @unattributable, a decorator to transmute inner AttributeError into a RuntimeError\n\n* @unimplemented, a decorator to make a method raise NotImplementedError',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.excutils'],
)
