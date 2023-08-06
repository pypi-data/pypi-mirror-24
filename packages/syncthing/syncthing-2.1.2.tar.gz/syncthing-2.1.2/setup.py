#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'syncthing',
    version = '2.1.2',
    author = 'Blake VandeMerwe',
    author_email = 'blakev@null.net',
    description = 'Python bindings to the Syncthing REST interface, targeting v0.14.36',
    url = 'https://github.com/blakev/python-syncthing',
    license = 'The MIT License',
    install_requires = [
        'requests>=2.17.3',
        'six==1.10.0'
    ],
    packages = [
        'syncthing'
    ],
    package_dir = {
        'syncthing': 'syncthing'
    },
    include_package_data = True,
    zip_safe = True,
    keywords = 'syncthing,sync,rest,backup,api',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Archiving :: Mirroring'
    ],
)