#!/usr/bin/env python

# Copyright 2009 John Kleint
#
# This is free software, licensed under the Lesser Affero General 
# Public License, available in the accompanying LICENSE.txt file.


"""
Distutils setup script for googlemaps module.
"""


from distutils.core import setup
import sys

sys.path.insert(0, 'expressgui')
import expressgui


setup(name='expressgui',
      version='1.0.1',
      author='Bruno Steinmann',
      author_email='bruno.steinmann@gmx.com',
      url='http://www.brunosteinmann.com',
      download_url='http://www.brunosteinmann.com',
      description='ExpressVPN Gui',
      long_description='ExpressVPN Gui- & Tray-App',
      package_dir={'': 'expressgui'},
      py_modules=['expressgui'],
      provides=['expressgui'],
      requires=['PyQt5'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Scientific/Engineering :: GIS',
                  ],
      
     )
