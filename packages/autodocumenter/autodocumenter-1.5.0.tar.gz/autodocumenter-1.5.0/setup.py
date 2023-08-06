# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='autodocumenter',
    version='1.5.0',
    description='Python package for generating empty documentation templates',
    long_description=readme,
    author='Nick Janetos',
    author_email='njanetos@wharton.upenn.edu',
    url='https://github.com/njanetos',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'autodocumenter': 'autodocumenter'},
    package_data={'autodocumenter': ['autodocumenter/*.css', 'autodocumenter/*.html']}
)
