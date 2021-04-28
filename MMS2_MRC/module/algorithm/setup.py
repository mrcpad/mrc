#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: 
@author: 
@site: 
@software: PyCharm
@file: 
@time: 
"""

import sys
sys.path.append(r'E:\Work\Hitec\MSZC\MSS2\05source\MMS2_MRC')
from setuptools import setup,find_packages


setup(
    name='mrc',
    version='0.1',
    py_modules=['open'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'mrc=open:open'

        ],
    }
)

