#!/usr/bin/env python

from setuptools import setup

setup(
    name='ChannelWorm',
    version='1.0',
    description='Modeling Ion Channels in C. Elegans',
    author='OpenWorm Community',
    author_email='vahidghayoomi@gmail.com, milad.jafary@gmail.com, trav221@gmail.com',
    url='https://github.com/openworm/ChannelWorm',
    install_requires=['Django','metapub','django-formtools', 'django-sql-explorer', 'python-unicodecsv'],
)