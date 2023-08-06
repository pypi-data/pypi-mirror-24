#!/usr/bin/env python
# coding = utf - 8
from setuptools import setup, find_packages

setup(
	name             = 'PyMea',
    version          = '0.0.1',
    description      = ('The Maximum Excursion Analysis (MEA) Python C extension module'),
    author           = 'fatfingererr',
    author_email     = 'fatfingererr@gmail.com',
    maintainer       = 'fatfingererr',
    maintainer_email = 'fatfingererr@gmail.com',
    license          = 'Apache License version 2',
    packages         = find_packages(),
    platforms        = ["all"],
    url              = 'https://github.com/fatfingererr/PyMea',
    classifiers      = [
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'
    ],
)