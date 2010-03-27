# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009.                                      |
# +--------------------------------------------------------------------------+
# | This module complies with Django 1.0 and is                              |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Ambrish Bhargava, Tarun Pasrija, Rahul Priyadarshi              |
# | Version: 0.2.0                                                           |
# +--------------------------------------------------------------------------+

import sys

from setuptools import setup, find_packages
from distutils.core import setup, Extension

PACKAGE = 'ibm_db_django'
VERSION = '0.2.0'
LICENSE = 'Apache License 2.0'

setup (
    name              = PACKAGE,
    version           = VERSION,
    license           = LICENSE,
    platforms         = 'All',
    install_requires  = [ 'ibm_db>=1.0.1',
                          'django>=1.0.3'],
    dependency_links  = [ 'http://pypi.python.org/pypi/ibm_db/',
                          'http://pypi.python.org/pypi/Django/'],
    description       = 'DB2 support for Django framework.',
    long_description  = 'DB2 support for Django framework.',
    download_url      = 'http://code.google.com/p/ibm-db/downloads/list',
    author            = 'Ambrish Bhargava, Tarun Pasrija',
    author_email      = 'abhargav@in.ibm.com, tarun.pasrija@in.ibm.com',
    maintainer        = 'Ambrish Bhargava, Tarun Pasrija',
    maintainer_email  = 'abhargav@in.ibm.com, tarun.pasrija@in.ibm.com',
    url               = 'http://pypi.python.org/pypi/ibm_db_django/',
    keywords          = 'django ibm_db_django backends adapter IBM Data Servers database db2',
    packages          = ['ibm_db_django'],
    classifiers       = ['Development Status :: 4 - Beta',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: Apache Software License',
                         'Operating System :: Microsoft :: Windows :: Windows NT/2000',
                         'Operating System :: Unix',
			 'Operating System :: POSIX :: Linux',
			 'Operating System :: MacOS',
                         'Topic :: Database :: Front-Ends'],
    data_files        = [ ('', ['./README']),
                          ('', ['./CHANGES']),
                          ('', ['./LICENSE']) ],
    zip_safe          = False,
    include_package_data = True,
    entry_points = {
		'django.db.backends': ['ibm_db_django = ibm_db_django']
    },
)
