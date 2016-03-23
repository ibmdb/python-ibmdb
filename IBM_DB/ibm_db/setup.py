import os
import sys
import struct
import warnings
import tarfile
import zipfile
import shutil

if sys.version_info >= (3, ):
    from urllib import request
    from io import BytesIO
else:
    import urllib2 as request
    from cStringIO import StringIO as BytesIO
    
from setuptools import setup, find_packages
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib

PACKAGE = 'ibm_db'
VERSION = '2.0.7'
LICENSE = 'Apache License 2.0'

machine_bits =  8 * struct.calcsize("P")
is64Bit = True
libDir = ''
ibm_db_home = ''
ibm_db_dir = ''
ibm_db_lib = ''
ibm_db_lib_runtime = ''
license_agreement = False
prebuildIbmdbPYD = False
    
if machine_bits == 64:
    is64Bit = True
    libDir = 'lib64'
    sys.stdout.write("Detected 64-bit Python\n")
else:
    is64Bit = False
    libDir = 'lib32'
    sys.stdout.write("Detected 32-bit Python\n")

# check if val exists in list
def _checkOSList(list, val):
    for s in list:
        if ( val in s):
            return True
    return False

# defining extension    
def _ext_modules(include_dir, library, lib_dir, runtime_dir=None):
    ext_args = dict(include_dirs = [include_dir],
                    libraries = library,
                    library_dirs = [lib_dir],
                    sources = ['ibm_db.c'])
    if runtime_dir:
        ext_args['runtime_library_dirs'] = [runtime_dir]
    ibm_db = Extension('ibm_db', **ext_args)
    return [ibm_db]

# set the win32 env, if not present    
def _setWinEnv(name, value):
    pyFile = open('ibm_db.py', 'r+')
    old = pyFile.read()
    if name not in old:
        pyFile.seek(0)
        envVal = "import os\n" + \
                '''if 'clidriver' not in os.environ['%(name)s']:\n    os.environ['%(name)s'] = os.environ['%(name)s']''' % {'name': name}
        envVal = envVal + ''' + ";" + os.path.join(os.path.abspath(os.path.dirname(__file__)), '%(val)s', 'bin')''' % {'val': value}
        pyFile.write( envVal + "\n" + old )
    pyFile.close()

if('win32' in sys.platform):
    prebuildPYDname = ''
    if is64Bit:
        prebuildPYDname = "ibm_db64_py%i%i.pyd" % (sys.version_info[0], sys.version_info[1])
    else:
        prebuildPYDname = "ibm_db32_py%i%i.pyd" % (sys.version_info[0], sys.version_info[1])
        
    if os.path.isfile(prebuildPYDname):
        # creating ibm_db_dlls package to put ibm_db.dll
        dllDir = 'ibm_db_dlls'
        try:
            os.stat(dllDir)
        except:
            os.mkdir(dllDir)
        open(os.path.join(dllDir, '__init__.py'), 'w').close()
        shutil.copy(prebuildPYDname, os.path.join(dllDir, 'ibm_db.dll'))
        prebuildIbmdbPYD = True
        
if (('IBM_DB_HOME' not in os.environ) and ('IBM_DB_DIR' not in os.environ) and ('IBM_DB_LIB' not in os.environ)):
    if ('aix' in sys.platform):
        os_ = 'aix'
        arch_ = '*'
        if is64Bit:
            cliFileName = 'aix64_odbc_cli.tar.gz'
        else:
            cliFileName = 'aix32_odbc_cli.tar.gz'
    elif ('linux' in sys.platform):
        os_ = 'linux'
        if (_checkOSList(os.uname(),'ppc')):	
            os_ = 'ppc'
            if is64Bit:
                cliFileName = 'ppc64_odbc_cli.tar.gz'
                arch_ = 'ppc64'
            else:
                cliFileName = 'ppc32_odbc_cli.tar.gz'
                arch_ = 'ppc*'
        elif (_checkOSList(os.uname(),'86')): # todo needs to search in list
            if is64Bit:
                cliFileName = 'linuxx64_odbc_cli.tar.gz'
                arch_ = 'x86_64'    
            else:
                cliFileName = 'linuxia32_odbc_cli.tar.gz'
                arch_ = 'i686'
    elif ('sunos' in sys.platform):
        os_ = 'solaris*'
        if ('i86pc' in os.uname()):
            arch_ = 'i86pc'
            if is64Bit:
                cliFileName = 'sunamd64_odbc_cli.tar.gz'
            else:
                cliFileName = 'sunamd32_odbc_cli.tar.gz'
        elif ('SPARC' in os.uname()):
            arch_ = 'SUNW'
            if is64Bit:
                cliFileName = 'sun64_odbc_cli.tar.gz'
            else:
                cliFileName = 'sun32_odbc_cli.tar.gz'
    elif('win32' in sys.platform):
        os_ = 'win'
        if is64Bit:
            cliFileName = 'ntx64_odbc_cli.zip'
            arch_ = 'amd64'
        else:
            cliFileName = 'nt32_odbc_cli.zip'
            arch_ = '32'

    elif('darwin' in sys.platform and is64Bit): 
        os_ = 'mac' 
        cliFileName = 'macos64_odbc_cli.tar.gz' 
        arch_ = 'x86_64' 
    else:
        sys.stdout.write("Not a known platform for python ibm_db . Contact opendev@us.ibm.com")
        sys.stdout.flush()
        sys.exit()
        
    tmp_path = get_python_lib()
    easy_cli_path = os.path.join(tmp_path, 'ibm_db-%s.egg' % ("-".join([VERSION, "py"+sys.version.split(" ")[0][0:3]]) if('win32' in sys.platform) else "-".join([VERSION, "py"+sys.version.split(" ")[0][0:3], os_, arch_])), 'clidriver')
    pip_cli_path = os.path.join(tmp_path, 'clidriver')
    ibm_db_lib_runtime = os.path.join('$ORIGIN', 'clidriver', 'lib')
    ibm_db_dir = 'clidriver'
    ibm_db_lib = os.path.join(ibm_db_dir, 'lib')
    
    if not os.path.isdir('clidriver'):
        url = 'https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/' + cliFileName
        sys.stdout.write("Downloading %s\n" % (url))
        sys.stdout.flush();
        file_stream = BytesIO(request.urlopen(url).read())
        if (os_ == 'win'):
            if sys.version_info[0:2] <= (2, 5):
                sys.stdout.write("Auto installation of clidriver for Python Version %i.%i on Window platform is currently not supported \n" % (sys.version_info[0:2]))
                sys.stdout.write("Environment variable IBM_DB_HOME is not set. Set it to your DB2/IBM_Data_Server_Driver installation directory and retry ibm_db module install.\n")
                sys.stdout.flush()
                sys.exit()
            cliDriver_zip =  zipfile.ZipFile(file_stream)
            cliDriver_zip.extractall()
        else:
            cliDriver_tar = tarfile.open(fileobj=file_stream)
            cliDriver_tar.extractall()
        open(os.path.join(ibm_db_dir, '__init__.py'), 'w').close()
        if os.path.isfile('ibm_db.dll'):
            shutil.copy('ibm_db.dll', 'clidriver')
        
    if prebuildIbmdbPYD:
        _setWinEnv("PATH", "clidriver")
        
    license_agreement = '''\n****************************************\nYou are downloading a package which includes the Python module for IBM DB2/Informix.  The module is licensed under the Apache License 2.0. The package also includes IBM ODBC and CLI Driver from IBM, which is automatically downloaded as the python module is installed on your system/device. The license agreement to the IBM ODBC and CLI Driver is available in %s or %s.   Check for additional dependencies, which may come with their own license agreement(s). Your use of the components of the package and dependencies constitutes your acceptance of their respective license agreements. If you do not accept the terms of any license agreement(s), then delete the relevant component(s) from your device.\n****************************************\n''' % (pip_cli_path, easy_cli_path)

if ('win32' not in sys.platform):
    if os.path.isfile('ibm_db.py'):
        os.rename("ibm_db.py","ibm_db_win.py")

if ibm_db_dir == '':
    try:
        ibm_db_home = os.environ['IBM_DB_HOME']
        ibm_db_dir = ibm_db_home
        ibm_db_lib = os.path.join(ibm_db_dir, libDir)
    except (KeyError):   
        try:
            ibm_db_dir = os.environ['IBM_DB_DIR']
            ibm_db_lib = os.path.join(ibm_db_dir, libDir)
        except (KeyError):
            sys.stdout.write("Environment variable IBM_DB_HOME is not set. Set it to your DB2/IBM_Data_Server_Driver installation directory and retry ibm_db module install.\n")
            sys.exit()

if not os.path.isdir(ibm_db_lib):
    ibm_db_lib = os.path.join(ibm_db_dir, 'lib')
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
ibm_db_include = os.path.join(ibm_db_dir, 'include')
if not prebuildIbmdbPYD and not os.path.isdir(ibm_db_include):
    sys.stdout.write(" %s/include folder not found. Check if you have set the IBM_DB_HOME environment variable's value correctly\n " %(ibm_db_dir))
    sys.exit()
    
library = ['db2']
package_data = { 'tests': [ '*.png', '*.jpg']}
data_files = [ ('', ['./README.md']),
               ('', ['./CHANGES']),
               ('', ['./LICENSE']) ]

modules = ['config', 'ibm_db_dbi', 'testfunctions', 'tests']
ext_modules = _ext_modules(ibm_db_include, library, ibm_db_lib, ibm_db_lib_runtime)

if (sys.platform[0:3] == 'win'):
    library = ['db2cli']
    if prebuildIbmdbPYD:
        ext_modules = None
        modules.append('ibm_db')
    else:
        ext_modules = _ext_modules(ibm_db_include, library, ibm_db_lib)

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
       platforms = 'Linux32/64, Win32/64, aix32/64, ppc32/64, sunamd32/64, sun32/64',
       ext_modules  = ext_modules,
       py_modules   = modules,
       packages     = find_packages(),
       package_data = package_data,
       data_files   = data_files,
       include_package_data = True,
       **extra
     )

if license_agreement:
    sys.stdout.write(license_agreement)
