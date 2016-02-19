#!/usr/bin/env python
from setuptools import setup, find_packages

requires = [
    'setuptools',
    'pybrain'
]

setup(name='nn',
      version='0.0.1',
      scripts=['src/main.py'],
      packages=find_packages('src'),
      install_requires=requires)
