#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.core import setup

PACKAGE = 'ibm_db_sa'
VERSION = '0.1.5'
LICENSE = 'Apache License 2.0'

setup( name    = PACKAGE, 
       version = VERSION,
       license = LICENSE,
       description  = 'SQLAlchemy support for IBM Data Servers',
       author       = 'IBM Application Development Team',
       author_email = 'opendev@us.ibm.com',
       url          = 'http://pypi.python.org/pypi/ibm_db/',
       download_url = 'http://code.google.com/p/ibm-db/downloads/list',
       keywords     = 'sqlalchemy database interface IBM Data Servers DB2 Informix IDS',
       classifiers  = ['Development Status :: 3 - Alpha',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: Apache License 2.0',
                      'Operating Systtem :: OS Independent',
                      'Topic :: Databases :: Front-end, middle-tier'],
       long_description = '''
                      IBM_DB_SA implementats the SQLAlchemy version 0.4.0 specification
                      in support of IBM Data Servers: DB2 8 and 9, Informix IDS 11''',
       platforms        = 'All',
       install_requires = [ 'ibm_db>=0.2.5',
                            'sqlalchemy>=0.4' ],
       dependency_links = [ 'http://pypi.python.org/pypi/ibm_db/',
                            'http://pypi.python.org/pypi/SQLAlchemy/'],
       packages     = find_packages(), 
       data_files   = [ ('', ['./README']),
                        ('', ['./CHANGES']),
                        ('', ['./LICENSE']),
                        ('ibm_db_sa', ['./ibm_db_sa/ibm_db_reserved']) ],
       entry_points = {
         'sqlalchemy.databases': ['ibm_db_sa = ibm_db_sa.ibm_db_sa:dialect',]
       },
       include_package_data = True,
       zip_safe             = False,
     )
