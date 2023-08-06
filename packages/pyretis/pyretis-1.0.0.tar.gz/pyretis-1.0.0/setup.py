# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
PyRETIS - A simulation package for rare event simulations.
Copyright (C) 2015  The PyRETIS team

This file is part of PyRETIS.

PyRETIS is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 2.1 of the License, or
(at your option) any later version.

PyRETIS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PyRETIS. If not, see <http://www.gnu.org/licenses/>
"""
from codecs import open as openc
import os
import shutil
from setuptools import setup, find_packages


def get_long_description():
    """Return the contents of README.rst"""
    here = os.path.abspath(os.path.dirname(__file__))
    # Get the long description from the README file
    long_description = ''
    with openc(os.path.join(here, 'README.rst'), encoding='utf-8') as fileh:
        long_description = fileh.read()
    return long_description


FULL_VERSION = '1.0.0'

# create copies of scripts:
try:
    shutil.copy('bin/pyretisrun.py', 'bin/pyretisrun')
    shutil.copy('bin/pyretisanalyse.py', 'bin/pyretisanalyse')
except FileNotFoundError:
    pass

setup(name='pyretis',
      version=FULL_VERSION,
      description='A simulation package for rare events',
      long_description=get_long_description(),
      url='http://www.pyretis.org',
      author='The PyRETIS team',
      author_email='pyretis@pyretis.org',
      license='LGPLv2.1+',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   ('License :: OSI Approved :: '
                    'GNU Lesser General Public License v2 or later (LGPLv2+)'),
                   'Natural Language :: English',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Physics'],
      keywords='rare-events md mc tps simulation tis retis',
      packages=find_packages(exclude=['docs']),
      package_data={'pyretis': ['pyretis.mplstyle', 'pyretis/inout/report/templates/*']},
      include_package_data=True,
      install_requires=['numpy>=1.13.1',
                        'scipy>=0.19.1',
                        'matplotlib>=2.0.2',
                        'jinja2>=2.9.6',
                        'docutils>=0.14',
                        'tqdm>=4.15.0',
                        'colorama>=0.3.9'],
      scripts=['bin/pyretisrun', 'bin/pyretisanalyse'])
