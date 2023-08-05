#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'tweepy',
    'geojson'
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(SiggyF): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='ttf',
    version='0.1.0',
    description="Ask people for information, through twitter, during a humanitarian response effort.",
    long_description=readme + '\n\n' + history,
    author="Fedor Baart",
    author_email='fedor.baart@deltares.nl',
    url='https://github.com/SiggyF/ttf',
    packages=find_packages(include=['ttf']),
    entry_points={
        'console_scripts': [
            'ttf=ttf.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='ttf',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
