# -*- coding: utf-8 -*-
"""
"""
from __future__ import with_statement

import os

from setuptools import Command, setup
from setuptools.command.test import test


# include __about__.py.
__dir__ = os.path.dirname(__file__)
about = {}
with open(os.path.join(__dir__, 'gauge', '__about__.py')) as f:
    exec(f.read(), about)


# use pytest instead.
def run_tests(self):
    raise SystemExit(__import__('pytest').main(['-v']))
test.run_tests = run_tests


class Benchmark(Command):

    user_options = []
    initialize_options = finalize_options = lambda x: None

    def run(self):
        raise SystemExit(__import__('pytest').main(['gaugebenchmark.py']))


install_requires = ['six>=1.8.0', 'sortedcontainers>=0.8.2']
try:
    from weakref import WeakSet
except ImportError:
    # WeakSet was added in Python 2.7.
    install_requires.append('weakrefset>=1.0.0')
else:
    del WeakSet


setup(
    name='gauge',
    version=about['__version__'],
    license=about['__license__'],
    author=about['__author__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    url='https://github.com/what-studio/gauge',
    description='Deterministic linear gauge library',
    long_description=__doc__,
    platforms='any',
    packages=['gauge'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    install_requires=install_requires,
    tests_require=['pytest'],
    test_suite='...',
    cmdclass={'benchmark': Benchmark},
)
