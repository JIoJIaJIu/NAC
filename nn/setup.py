#!/usr/bin/env python
from setuptools import setup, find_packages

requires = [
    'setuptools',
    'pybrain'
]


setup(name='nn',
    version='0.0.1',
    packages=find_packages(),
    entry_points = {
        'distutils.commands': [
            'train=tools:TrainCommand',
        ]
    },
    install_requires=requires)
