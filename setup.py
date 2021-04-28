# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="mrc",
    version='1.7',
    py_modules=['clickUtil.ffcstartPY'],
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mrc=clickUtil.ffcstartPY:climain
    ''',
)

#pip install --editable .
#conda install -c conda-forge cdo

