#!/usr/bin/env python
"""
sentry-s3-nodestore
==============
An extension for Sentry which implements an Minio NodeStorage backend
"""
from setuptools import setup

install_requires = [
    'minio',
    'simplejson',
    'sentry>=7.4.0',
]

tests_requires = [
    'moto>=0.4.10'
]

setup(
    name='sentry-s3-nodestore',
    version='1.0.9',
    author='Negashev Alexandr',
    author_email='i@negash.ru',
    url='http://github.com/negashev/sentry-s3-nodestore',
    description='A Sentry extension to add Minio as a NodeStore backend.',
    long_description=__doc__,
    packages=['sentry_s3_nodestore'],
    license='BSD',
    zip_safe=False,
    install_requires=install_requires,
    tests_requires=tests_requires,
    test_suite='tests',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
