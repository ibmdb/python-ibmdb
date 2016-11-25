# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009-2014.                                      |
# +--------------------------------------------------------------------------+
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
# +--------------------------------------------------------------------------+

import sys

_IS_JYTHON = sys.platform.startswith('java')
from setuptools import setup, find_packages
from distutils.core import setup, Extension

PACKAGE = 'ibm_db_django'
VERSION = __import__('ibm_db_django').__version__
LICENSE = 'Apache License 2.0'
extra = {}
if sys.version_info >= (3, ):
    extra['use_2to3'] = True
    
setup (
    name              = PACKAGE,
    version           = VERSION,
    license           = LICENSE,
    platforms         = 'All',
    install_requires  = _IS_JYTHON and ['django>=1.0.3'] or ['ibm_db>=1.0.3',
                          'django>=1.0.3'],
    dependency_links  = _IS_JYTHON and ['http://pypi.python.org/pypi/Django/'] or ['http://pypi.python.org/pypi/ibm_db/',
                          'http://pypi.python.org/pypi/Django/'],
    description       = 'DB2 support for Django framework.',
    long_description  = 'DB2 support for Django framework.',
    author            = 'Ambrish Bhargava, Tarun Pasrija, Rahul Priyadarshi',
    author_email      = 'opendev@us.ibm.com',
    maintainer        = 'IBM Application Development Team',
    maintainer_email  = 'opendev@us.ibm.com, ibm_db@googlegroups.com',
    url               = 'http://pypi.python.org/pypi/ibm_db_django/',
    keywords          = 'django ibm_db_django backends adapter IBM Data Servers database db2',
    packages          = ['ibm_db_django'],
    classifiers       = [ _IS_JYTHON and 'Development Status :: 4 - Beta' or 'Development Status :: 5 - Production/Stable',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: Apache Software License',
                         'Operating System :: Microsoft :: Windows :: Windows NT/2000',
                         'Operating System :: Unix',
                         'Operating System :: POSIX :: Linux',
                         'Operating System :: MacOS',
                         'Topic :: Database :: Front-Ends'],
    data_files        = [ ('', ['./README.md']),
                          ('', ['./CHANGES']),
                          ('', ['./LICENSE']) ],
    zip_safe          = False,
    include_package_data = True,
    entry_points = {
		'django.db.backends': ['ibm_db_django = ibm_db_django']
    },
    **extra
)
