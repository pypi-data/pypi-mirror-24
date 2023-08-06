# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@Author: Huang Sizhe
@Date:   06-Apr-2017
@Email:  hsz1273327@gmail.com
# @Last modified by:   Huang Sizhe
# @Last modified time: 08-Apr-2017
@License: MIT
@Description:
"""

from codecs import open
from setuptools import setup, find_packages
from os import path

PACKAGES = find_packages(exclude=['contrib', 'docs', 'test'])

required = ["motor>=1.1",
            "pymongo>=3.4.0",
            "sanic>=0.4.1",
            "user_agents>=1.1.0"]


HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
setup(
    name='sanic-mongo',
    version='1.6.0',
    author='Huang Sizhe',
    author_email='hsz1273327@gmail.com',
    packages=PACKAGES,
    license='Apache License 2.0',
    description='a simple sanic extension for using motor',
    long_description=LONG_DESCRIPTION,
    install_requires=required,
    url="https://sanic-extensions.github.io/sanic-mongo/",
    data_files=[('requirements', ['requirements.txt'])]
)
