#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
from rszio import version

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')  # noqa
except ImportError:
    read_md = lambda f: open(f, 'r').read()  # noqa

setup(
    name='django-rszio',
    author='Chad Shryock',
    author_email='chad@keystone.works',
    description='Django wrapper for RSZ.IO',
    long_description=read_md('README.md'),
    license='MIT',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/g3rd/django-rszio',
    zip_safe=True,
    install_requires=[
        'django>=1.10',
        'requests>=2.14.2',
    ],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django resize image',
)
