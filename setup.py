#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

test_requirements = ['pytest', ]

setup(
    author="Riccardo Magliocchetti",
    author_email='riccardo.magliocchetti@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="uWSGI log parser to find memory hogs",
    entry_points={
        'console_scripts': [
            'pyuwsgimemhog=pyuwsgimemhog.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyuwsgimemhog',
    name='pyuwsgimemhog',
    packages=find_packages(include=['pyuwsgimemhog']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/xrmx/pyuwsgimemhog',
    version='0.3.0',
    zip_safe=False,
)
