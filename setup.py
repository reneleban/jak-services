# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='jak-services',
    version='0.0.1',
    description='Just-Another-Kanban Services',
    long_description=readme,
    author='René Leban',
    author_email='leban.rene@gmail.com',
    url='https://github.com/reneleban/jak-services',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'bottle>=0.12'
    ]
)
