#!/usr/bin/env python

from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='pytdx',
    version='1.27',
    description='A Python Interface to TDX protocol',
    long_description=long_description,
    author='RainX<Jing Xu>',
    author_email='i@rainx.cc',
    url='https://github.com/rainx/pytdx',
    packages=find_packages(),
    install_requires=[
          'click',
          'pandas',
          'six'
    ],
    entry_points={
          'console_scripts': [
              'hqget=pytdx.bin.hqget:main',
              'hqreader=pytdx.bin.hqreader:main'

          ]
      }
    )

