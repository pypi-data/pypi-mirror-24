# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='midware',
    version='0.4.0',
    description='A simple general-purpose middleware library for Python',
    long_description=readme,
    author='Ivan Dmitrievsky',
    author_email='ivan.dmitrievsky+python@gmail.com',
    url='https://github.com/idmit/midware',
    install_requires=[],
    license=license_,
    packages=find_packages(exclude=('tests', 'docs')))
