#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import sys


version = __import__('pygnutools').VERSION

scripts = ['bin/pyfind.py']

if sys.platform == "win":
    scripts.append('bin/pyfind.bat')
else:
    scripts.append('bin/pyfind')

setup(name='pygnutools',
    version=version,
    description='Pure python implementation of GNU tools',
    author='Meitham Jamaa',
    author_email='meitham@meitham.com',
    url='http://meitham.com/pygnutools/',
    packages=find_packages(),
    scripts = scripts,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Shell Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
 )
