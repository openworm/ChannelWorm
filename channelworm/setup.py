#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='ChannelWorm',
    # GETTING-STARTED: set your app name:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='OpenShift App',
    # GETTING-STARTED: set author name (your name):
    author='',
    # GETTING-STARTED: set author name (your name):
    author_email='',
    # GETTING-STARTED: set author name (your name):
    url='http://www.python.org/sigs/distutils-sig/',
    # GETTING-STARTED: define required django version:
    install_requires=['Django<=1.8','metapub','django-formtools'],
)
