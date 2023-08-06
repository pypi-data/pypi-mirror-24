#!/usr/bin/env python
#coding=utf-8

from setuptools import setup, find_packages


import sys
import re


if sys.version_info < (2, 6):
    sys.exit('Python 2.5 or greater is required.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as fp:
    readme = fp.read()


setup(
    name = 'DoraClient',
    version = '0.1.2',
    keywords = ('monitor','DoraClient'),
    description = 'monitor client',

    long_description = readme,

    license = 'Apache Licence 2.0',

    url = 'https://github.com/x0hcker/dora-client',
    author = 'x0hcker@gmail.com',
    author_email = 'x0hcker@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],

    scripts=[
        'DoraClient/bin/dora_client',
        'DoraClient/bin/dora_update',
    ],
)
