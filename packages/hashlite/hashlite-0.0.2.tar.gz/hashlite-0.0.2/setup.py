#!/usr/bin/env python

import os
import ast
from setuptools import setup, find_packages

with open('hashlite/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            ver = ast.parse(line).body[0].value.s
            break

# reading requirements from requirements.txt
ignore_dir = ['.git']

setup(
    name='hashlite',
    version=ver,
    description='light weight json db implemented using python dicts',
    author='samvaran kashyap rallabandi',
    author_email='samvaran.kashyap@gmail.com',
    url='https://github.com/samvarankashyap/hashlite',
    setup_requires=[],
    install_requires=[],
    entry_points='''
        [console_scripts]
        hashlite=shell:runcli
    ''',
    extras_require={
    },
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True
)
