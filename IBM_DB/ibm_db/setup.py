import os
import sys

from setuptools import setup, find_packages
from distutils.core import setup, Extension

PACKAGE = 'ibm_db'
VERSION = '1.0.5'
LICENSE = 'Apache License 2.0'

try:
	ibm_db_dir = os.environ['IBM_DB_DIR']
	ibm_db_lib = os.environ['IBM_DB_LIB']
except (KeyError):
	print '''IBM DataServer environment not set. 
Please set IBM_DB_DIR to path to sqllib,
and set IBM_DB_LIB to lib directory under sqllib
e.g. export IBM_DB_DIR=/home/db2inst1/sqllib
     export IBM_DB_LIB=/home/db2inst1/sqllib/lib
'''
	sys.exit()

library = ['db2']
if (sys.platform[0:3] == 'win'):
  library = ['db2cli']

ibm_db = Extension('ibm_db',
                    include_dirs = [ibm_db_dir + '/include'],
                    libraries = library,
                    library_dirs = [ibm_db_lib],
                    sources = ['ibm_db.c'])

modules = ['config', 'ibm_db_dbi', 'testfunctions', 'tests']

setup( name    = PACKAGE, 
       version = VERSION,
       license = LICENSE,
       description      = 'Python DBI driver for DB2 (LUW, zOS, i5) and IDS',
       author           = 'IBM Application Development Team',
       author_email     = 'opendev@us.ibm.com',
       url              = 'http://pypi.python.org/pypi/ibm_db/',
       download_url     = 'http://code.google.com/p/ibm-db/downloads/list',
       keywords         = 'database DB-API interface IBM Data Servers DB2 Informix IDS',
       classifiers  = ['Development Status :: 5 - Production/Stable',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: Apache Software License',
                      'Operating System :: Microsoft :: Windows :: Windows NT/2000/XP',
                      'Operating System :: Unix',
                      'Topic :: Database :: Front-Ends'],

       long_description = '''
                      This extension is the implementation of Python Database API Specification v2.0
                      The extension supports DB2 (LUW, zOS, i5) and IDS (Informix Dynamic Server)''',
       platforms = 'LinuxIA32, Win32',
       ext_modules  = [ibm_db],
       py_modules   = modules,
       packages     = find_packages(),
       package_data = { 'tests': [ '*.png', '*.jpg']},
       data_files=[ ('', ['./README']),
                    ('', ['./CHANGES']),
                    ('', ['./LICENSE']) ],
       include_package_data = True
     )
