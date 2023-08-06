#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2015/06/13
# copy: (C) Copyright 2015-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
]

dependencies = [
  'pyramid              >= 1.4.2',
  'FormEncode           >= 1.2.5',
  'asset                >= 0.6.3',
  'globre               >= 0.1.3',
  'aadict               >= 0.2.2',
  'morph                >= 0.1.2',
  'six                  >= 1.6.0',
]

extras_dependencies = {
  'yaml':  'PyYAML      >= 3.10',
}

classifiers = [
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Framework :: Pyramid',
  'Environment :: Console',
  'Environment :: Web Environment',
  'Operating System :: OS Independent',
  'Topic :: Internet',
  'Topic :: Software Development',
  'Topic :: Internet :: WWW/HTTP',
  'Topic :: Internet :: WWW/HTTP :: WSGI',
  'Topic :: Software Development :: Libraries :: Application Frameworks',
  'Natural Language :: English',
  'License :: OSI Approved :: MIT License',
  'License :: Public Domain',
]

setup(
  name                  = 'pyramid_input',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'A Pyramid tween that normalizes HTTP request input data.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'Philip J Grabner, Canary Health Inc',
  author_email          = 'oss-pypi@canary.md',
  url                   = 'http://github.com/canaryhealth/pyramid_input',
  keywords              = 'web wsgi pyramid http input data normalize get post json yaml xml',
  packages              = find_packages(),
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  extras_require        = extras_dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'pyramid_input',
  entry_points          = '',
  license               = 'MIT (http://opensource.org/licenses/MIT)',
)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
