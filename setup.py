# -*- coding: utf-8 -*-

import sys
import os
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

here = os.path.dirname(__file__)

with open(os.path.join(here, 'csquery', '__init__.py'), 'r') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

readme = open(os.path.join(here, 'README.rst')).read()

requires = [
    'six'
]

tests_require = [
    'pytest-cov',
    'pytest',
    'mock',
]


classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='csquery',
    version=version,
    description='A simple query builder for Amazon Cloudsearch structured query parser.',  # NOQA
    long_description=readme,
    url='https://github.com/tell-k/csquery',
    keywords='aws amazon cloudsearch querybuilder structured',
    author='tell-k',
    author_email='ffk2005 at gmail.com',
    classifiers=classifiers,
    install_requires=requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    packages=find_packages(exclude=['tests']),
    license='MIT',
)
