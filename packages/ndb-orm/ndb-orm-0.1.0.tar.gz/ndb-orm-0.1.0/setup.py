#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('pandoc -o README.rst README.md')
    os.system('python setup.py sdist upload')
    sys.exit()

README = open('README.md').read()
HISTORY = open('CHANGES.txt').read().replace('.. :changelog:', '')

setup(
    name='ndb-orm',
    version='0.1.0',
    description="google datatstore ndb orm which might be used with google-cloud-datastore (python3 compatible)",
    long_description=README + '\n\n' + HISTORY,
    author='Ulf Bartel',
    author_email='elastic.code@gmail.com',
    url='https://github.com/berlincode/ndb-orm',
    packages=[
        'ndb-orm',
    ],
    package_dir={'ndb-orm': 'ndb_orm'},
    include_package_data=True,
    install_requires=['six', 'google-cloud-datastore', 'proto-google-cloud-datastore-v1', 'protorpc'],
    license='Apache 2.0',
    zip_safe=False,
    keywords='ndb, model, orm, app engine standard, flexible, datastore, python3, migrate',
    entry_points={
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
    ],
    test_suite='tests',
)
