#!/usr/bin/env python

from setuptools import setup

setup(name='flair-client',
      version='0.2.0',
      description='Flair API Client',
      author='Edward Paget',
      author_email='ed@flair.co',
      url='https://api.flair.co',
      packages=['flair_api'],
      install_requires=['requests']
)
