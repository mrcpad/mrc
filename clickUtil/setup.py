# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="mrc",
    version='1.5',
    py_modules=['ffcstartPY'],
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mrc=ffcstartPY:climain
    ''',
)

#pip install --editable .


