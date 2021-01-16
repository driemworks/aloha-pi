#!/usr/bin/env python
from distutils.core import setup

setup(name='aloha',
      version='1.0.0',
      description='',
      author='driemworks',
      author_email='tonyrriemer@gmail.com',
      url='#',
      packages=['aloha'],
      install_requires=[
          'python3-nmap',
          'pyyaml',
          'pyvizio',
          'requests'
      ]

)