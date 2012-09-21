import os
import sys
import struct
import warnings

from setuptools import setup, find_packages
from distutils.core import setup, Extension

PACKAGE = 'ibm_db'
VERSION = '2.0.0'
LICENSE = 'Apache License 2.0'

machine_bits =  8 * struct.calcsize("P")
is64Bit = True
libDir = ''
ibm_db_home = ''
ibm_db_dir = ''
ibm_db_lib = ''

if machine_bits == 64:
    is64Bit = True
    libDir = 'lib64'
    sys.stdout.write("Detected 64-bit Python\n")
else:
    is64Bit = False
    libDir = 'lib32'
    sys.stdout.write("Detected 32-bit Python\m")
    
try:
    ibm_db_home = os.environ['IBM_DB_HOME']
    ibm_db_dir = ibm_db_home
    ibm_db_lib = ibm_db_dir + '/' + libDir
except (KeyError):   
    try:
        ibm_db_dir = os.environ['IBM_DB_DIR']
        ibm_db_lib = ibm_db_dir + '/' + libDir
    except (KeyError):
        sys.stdout.write("Environment variable IBM_DB_HOME is not set. Set it to your DB2/IBM_Data_Server_Driver installation directory and retry ibm_db module install.\n")
        sys.exit()

if not os.path.isdir(ibm_db_lib):
    ibm_db_lib = ibm_db_dir + '/lib'
    if not os.path.isdir(ibm_db_lib):
        sys.stdout.write("Cannot find %s directory. Check if you have set the IBM_DB_HOME environment variable's value correctly\n " %(ibm_db_lib))
        sys.exit()
    notifyString  = "Detected usage of IBM Data Server Driver package. Ensure you have downloaded "
    if is64Bit:
        notifyString = notifyString + "64-bit package "
    else:
        notifyString = notifyString + "32-bit package "
    notifyString = notifyString + "of IBM_Data_Server_Driver and retry the ibm_db module install\n "
    warnings.warn(notifyString)
if not os.path.isdir(ibm_db_dir + '/include'):
    sys.stdout.write(" %s/include folder not found. Check if you have set the IBM_DB_HOME environment variable's value correctly\n " %(ibm_db_dir))
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
extra = {}
if sys.version_info >= (3, ):
    extra['use_2to3'] = True

setup( name    = PACKAGE, 
       version = VERSION,
       license = LICENSE,
       description      = 'Python DBI driver for DB2 (LUW, zOS, i5) and IDS',
       author           = 'IBM Application Development Team',
       author_email     = 'opendev@us.ibm.com',
       url              = 'http://pypi.python.org/pypi/ibm_db/',
       download_url     = 'http://code.google.com/p/ibm-db/downloads/list',
       keywords         = 'database DB-API interface IBM Data Servers DB2 Informix IDS',
       classifiers  = [(sys.version_info >= (3, )) and 'Development Status :: 4 - Beta' or 'Development Status :: 5 - Production/Stable',
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
       include_package_data = True,
       **extra
     )
