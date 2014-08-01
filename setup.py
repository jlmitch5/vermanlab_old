#!/usr/bin/env python

from setuptools import setup

setup(
    name='vml',
    version='1.0',
    description='OpenShift App',
    author='John Mitchell',
    author_email='jmitchel@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=[
	'Django>=1.7c2,<1.8',
	'django-widget-tweaks>=1.3,<1.4',
    'djangorestframework>=2.3,<2.4',
    'requests>=2.3,<2.4',
    'coverage>=3.7,<3.8',
    ]
)
