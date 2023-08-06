#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Docunit - A package to conveniently hook doctests and unit tests together.

Authors:
    - Joe Flack, joeflack4@gmail.com
"""
from setuptools import setup, find_packages


setup(
    name='docunit',
    version='0.1.0',
    author='Joe Flack',
    author_email='joeflack4@gmail.com',
    description=('Docunit - A package to conveniently hook doctests and unit '
                 'tests together.'),
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[],
    tests_require=[],
    url='http://www.joeflack.net/',
    download_url='https://github.com/joeflack4/docunit/archive/0.1.0.tar.gz',
    keywords=['joeflack4', 'docunit', 'doctest', 'unittest'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Environment :: Other Environment',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Environment :: Plugins',
    ]
)
