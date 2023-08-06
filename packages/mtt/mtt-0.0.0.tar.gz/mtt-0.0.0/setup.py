#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
from textwrap import dedent
import os
import sys
from setuptools import setup, find_packages, Command


info_dict = dict(
    name='mtt',
    description='Maastricht Tractography Toolbox',
    author='Robbert Harms',
    author_email='robbert.harms@maastrichtuniversity.nl',
    maintainer='Robbert Harms',
    maintainer_email='robbert.harms@maastrichtuniversity.nl',
    url='https://github.com/cbclab/MTT',
    packages=find_packages(),
    include_package_data=True,
    license="LGPL v3",
    zip_safe=False,
    keywords='',
    classifiers=[
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ],
)
setup(**info_dict)
