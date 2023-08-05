#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup, find_packages

def read(filename):
    return open(path.join(path.dirname(__file__), filename)).read()


def parse_requirements(filename):
    return [line.strip()
        for line in read(filename).strip().split('\n')
        if line.strip()]


pkg = {}
exec(read('hudai/__init__.py'), pkg)

readme = read('README.md')
requirements = parse_requirements('requirements.txt')


setup(
    name = pkg['__package_name__'],
    version = pkg['__version__'],
    url = pkg['__url__'],
    license = pkg['__license__'],
    author = pkg['__author__'],
    author_email = pkg['__email__'],
    description = pkg['__description__'],
    long_description = readme,
    packages = find_packages(exclude=['test']),
    install_requires = requirements,
    download_url = '{}/releases/{}.tar.gz'.format(pkg['__url__'], pkg['__version__']),
    keywords = pkg['__keywords__'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
