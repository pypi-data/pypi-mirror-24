#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'pylutron_koreth',
    version = '0.1.1',
    license = 'MIT',
    description = 'Python library for Lutron RadioRA 2',
    author = 'Steven Grimm',
    author_email = 'koreth@gmail.com',
    url = 'http://github.com/koreth/pylutron',
    packages=find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    zip_safe=True,
)
