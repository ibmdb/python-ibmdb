# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2008.                                      |
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
# | Authors: Ambrish Bhargava                                                |
# | Version: 0.1.0                                                           |
# +--------------------------------------------------------------------------+

import sys

from distutils.core import setup

try:
    import ibm_db
    import ibm_db_dbi
except ImportError:
    print '''ibm_db/ibm_db_dbi module is not installed.
Install ibm_db (v0.7.0 or higher) from any one of the following: 
1. http://code.google.com/p/ibm-db.
2. http://pypi.python.org/pypi/ibm_db'''
    sys.exit()

PACKAGE = 'django.db.backends.db2'
VERSION = '0.1.0'
LICENSE = 'Apache License 2.0'

setup (
    name              = PACKAGE,
    version           = VERSION,
    license           = LICENSE,
    requires          = ['ibm_db     ( >= 0.7.0 )', 
                         'ibm_db_dbi ( >= 0.7.0 )', 
                         'django     ( >= 1.0 )'],
    description       = 'DB2 support for Django framework.',
    long_description  = 'DB2 support for Django framework.',
    download_url      = 'http://code.google.com/p/ibm-db',      
    author            = 'Ambrish Bhargava',
    author_email      = 'abhargav@in.ibm.com',
    maintainer        = 'Ambrish Bhargava',
    maintainer_email  = 'abhargav@in.ibm.com',
    url               = 'http://code.google.com/p/ibm-db',
    keywords          = 'django db2 backends adapter IBM Data Servers database',
    packages          = ['django.db.backends.db2', 'django.db.backends.db2'],
    platforms         = 'LinuxIA32, Win32',
    classifiers       = ['Development Status :: 4 - Beta',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: Apache Software License',
                         'Operating System :: Microsoft :: Windows :: Windows NT/2000',
                         'Operating System :: Unix',
                         'Operating System :: Linux',
                         'Topic :: Database :: Front-Ends'],
)