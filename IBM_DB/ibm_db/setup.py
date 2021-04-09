import os
import sys
import os.path
import sys
import ssl
import struct
import warnings
import tarfile
import zipfile
import shutil
import glob
import subprocess

if sys.version_info >= (3, ):
    from urllib import request
    from io import BytesIO
else:
    import urllib2 as request
    from cStringIO import StringIO as BytesIO

from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_python_lib
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

PACKAGE = 'ibm_db'
VERSION = '3.0.4'
LICENSE = 'Apache License 2.0'

if 'zos' != sys.platform:
    context = ssl.create_default_context()
    context.load_verify_locations('certs/ibm_certs.pem')

machine_bits =  8 * struct.calcsize("P")
is64Bit = True
libDir = ''
ibm_db_home = ''
ibm_db_dir = ''
ibm_db_lib = ''
ibm_db_lib_runtime = ''
license_agreement = False
prebuildIbmdbPYD = False
cmd_class = dict()

if machine_bits == 64:
    is64Bit = True
    libDir = 'lib64'
    sys.stdout.write("Detected 64-bit Python\n")
else:
    is64Bit = False
    libDir = 'lib32'
    sys.stdout.write("Detected 32-bit Python\n")

# define post-build-ext and post-install operation for mac OS
if('darwin' in sys.platform):
    class PostInstall(install):
        """ Post installation - run install_name_tool on Darwin """
        def run(self):
            install.run(self)
            clipath = os.getenv('IBM_DB_HOME')
            if not clipath:
                # no IBM_DB_HOME during install, keep current value
                return

            for so in glob.glob(get_python_lib()+r'/ibm_db*.so'):
                os.system("install_name_tool -change @loader_path/clidriver/lib/libdb2.dylib {}/lib/libdb2.dylib {}".format(clipath, so))

    class PostBuildExt(build_ext):
        """ Post build_ext - update db2 dynamic lib to use loader_path on Darwin """
        def run(self):
            build_ext.run(self)
            clipath = os.getenv('IBM_DB_HOME', '@loader_path/clidriver')
            for so in glob.glob(self.build_lib+r'/ibm_db*.so'):
                os.system("install_name_tool -change libdb2.dylib {}/lib/libdb2.dylib {}".format(clipath, so))

    cmd_class = dict(install = PostInstall, build_ext = PostBuildExt)

# define post-build-ext and post-install operation for ZOS platform   
if('zos' in sys.platform):
    class PostInstall(install):
        def run(self):
            install.run(self)
            for so in glob.glob(get_python_lib()+r'/ibm_db*.egg/ibm_db*.so'):
                os.system("chtag -r " + get_python_lib() + r"/ibm_db*.egg/ibm_db*.so")
            for so in glob.glob(get_python_lib()+r'/ibm_db*.so'):
                try:
                    os.system("chtag -r " + get_python_lib() + r"/ibm_db*.so")
                except:
                    print("Could not change file tag information")
            
    class PostBuildExt(build_ext):
        def run(self):
            build_ext.run(self)
            for so in glob.glob(self.build_lib+r'/ibm_db*.so'):
                try:
                    os.system("chtag -r " + self.build_lib + r"/ibm_db*.so")
                except:
                    print("Could not change file tag information")
                    
    cmd_class = dict(install = PostInstall, build_ext = PostBuildExt)

# defining extension
def _ext_modules(include_dir, library, lib_dir, runtime_dir=None):
    ext_args = dict(include_dirs = [include_dir],
                    libraries = library if library else [],
                    library_dirs = [lib_dir] if lib_dir else [],
                    sources = ['ibm_db.c'])
    if sys.platform == 'zos':
        ext_args['extra_objects'] = [os.path.join(os.getcwd(), "libdsnao64c.x")]
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

# add add_dll_directory to ibm_db.py for python 3.8. refer https://bugs.python.org/issue36085 for details
def _setDllPath():
    pyFile = open('ibm_db.py', 'r+')
    old = pyFile.read()
    if "add_dll_directory" not in old:
        pyFile.seek(0)
        add_dll_directory = "import os\n" + '''if 'IBM_DB_HOME' not in os.environ:\n    os.add_dll_directory(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'clidriver', 'bin'))\nelse:\n    ibm_db_home = os.environ['IBM_DB_HOME'].strip('"')\n    os.add_dll_directory(os.path.join(ibm_db_home, 'bin'))'''

        pyFile.write( add_dll_directory + "\n" + old )
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
    if ('zos' == sys.platform):
        sys.stdout.write("You must set the environment variable IBM_DB_HOME to the HLQ of a DB2 installation\n")
        sys.stdout.flush()
        sys.exit()
    elif ('aix' in sys.platform):
        os_ = 'aix'
        arch_ = '*'
        if is64Bit:
            cliFileName = 'aix64_odbc_cli.tar.gz'
        else:
            cliFileName = 'aix32_odbc_cli.tar.gz'
    elif ('linux' in sys.platform):
        os_ = 'linux'
        if ('ppc64le' in os.uname()[4]):
            os_ = 'ppc64le'
            if is64Bit:
                cliFileName = 'ppc64le_odbc_cli.tar.gz'
                arch_ = 'ppc64le'
        elif ('ppc' in os.uname()[4]):
            os_ = 'ppc'
            if is64Bit:
                cliFileName = 'ppc64_odbc_cli.tar.gz'
                arch_ = 'ppc64'
            else:
                cliFileName = 'ppc32_odbc_cli.tar.gz'
                arch_ = 'ppc*'
        elif ('86' in os.uname()[4]): # todo needs to search in list
            if is64Bit:
                cliFileName = 'linuxx64_odbc_cli.tar.gz'
                arch_ = 'x86_64'
            else:
                cliFileName = 'linuxia32_odbc_cli.tar.gz'
                arch_ = 'i686'
        elif ('390' in os.uname()[4]):
            if is64Bit:
                cliFileName = 's390x64_odbc_cli.tar.gz'
                arch_ = 's390x'
            else:
                cliFileName = 's390_odbc_cli.tar.gz'
                arch_ = 's390'
    elif ('sunos' in sys.platform):
        os_ = 'solaris*'
        if ('i86pc' in os.uname()[4]):
            arch_ = 'i86pc'
            if is64Bit:
                cliFileName = 'sunamd64_odbc_cli.tar.gz'
            else:
                cliFileName = 'sunamd32_odbc_cli.tar.gz'
        elif ('sun4' in os.uname()[4]):
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
        sys.stdout.write("Not a known platform for python ibm_db.\n")
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
        file_stream = BytesIO(request.urlopen(url, context=context).read())
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
        if (sys.version_info >= (3, 8,)):
            _setDllPath()

    license_agreement = '''\n****************************************\nYou are downloading a package which includes the Python module for IBM DB2/Informix.  The module is licensed under the Apache License 2.0. The package also includes IBM ODBC and CLI Driver from IBM, which is automatically downloaded as the python module is installed on your system/device. The license agreement to the IBM ODBC and CLI Driver is available in %s or %s.   Check for additional dependencies, which may come with their own license agreement(s). Your use of the components of the package and dependencies constitutes your acceptance of their respective license agreements. If you do not accept the terms of any license agreement(s), then delete the relevant component(s) from your device.\n****************************************\n''' % (pip_cli_path, easy_cli_path)
else:
    if ('zos' == sys.platform):
        os.environ['_BPXK_AUTOCVT']='ON'
        os.environ['_CEE_RUNOPTS']='FILETAG(AUTOCVT,AUTOTAG) POSIX(ON) XPLINK(ON)'
        os.environ['_CC_ASUFFIX']='so'
        os.environ['_C89_ASUFFIX']='so'
        os.environ['_CXX_ASUFFIX']='so'
        os.environ['_CC_CCMODE']='1'
        os.environ['_C89_CCMODE']='1'
        os.environ['_CXX_CCMODE']='1'
        os.environ['_TAG_REDIR_ERR']='txt'
        os.environ['_TAG_REDIR_IN']='txt'
        os.environ['_TAG_REDIR_OUT']='txt'

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

if not os.path.isdir(ibm_db_lib) and 'zos' != sys.platform:
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
if not prebuildIbmdbPYD and not os.path.isdir(ibm_db_include) and 'zos' != sys.platform:
    sys.stdout.write(" %s/include folder not found. Check if you have set the IBM_DB_HOME environment variable's value correctly\n " %(ibm_db_dir))
    sys.exit()

if 'zos' == sys.platform:
    #ibm_db_include = "//'%s.SDSNC.H'" % ibm_db_home
    #dataset_include = "//'%s.SDSNC.H'" % ibm_db_home
    if(('DB2_INC' not in os.environ)):
        dataset_include = "//'%s.SDSNC.H'" % ibm_db_home
    else:
        sdsnc_h = os.environ['DB2_INC']
        dataset_include = "//'%s'" % sdsnc_h
    include_dir = 'sdsnc.h'
    #library = ['dsnao64c'] 
    library = []
    library_x = "libdsnao64c.x"
    library_so = "libdsnao64c.so" # fake, but helpful for gen_lib_options in cpython/Lib/distutils/ccompiler.py
    ibm_db_lib = '.'
    if not os.path.isfile(library_x):
        #with open("//'%s.SDSNMACS(DSNAO64C)'" % ibm_db_home, "rt", encoding='cp1047_oe') as x_in:
            #with open(library_x, "wt", encoding='cp1047_oe') as x_out:
                #x_out.write(''.join(["%-80s" % x for x in x_in.read().split('\n')]))
        #command = ['tso', "oput '{}.SDSNMACS(DSNAO64C)' '{}'".format(ibm_db_home, os.path.join(os.getcwd(), library_x))]
        if (('DB2_MACS' not in os.environ)):
            subprocess.run(['tso', "oput '{}.SDSNMACS(DSNAO64C)' '{}'".format(ibm_db_home, os.path.join(os.getcwd(), library_x))])
        else:
            sdsn_macs = os.environ['DB2_MACS']
            subprocess.run(['tso', "oput '{}(DSNAO64C)' '{}'".format(sdsn_macs, os.path.join(os.getcwd(), library_x))])
    if not os.path.isdir(include_dir):
        os.mkdir(include_dir)
        subprocess.run(['cp', dataset_include, include_dir])
        for f in glob.glob(os.path.join(include_dir, '*')):
            subprocess.run(['chtag', '-tc', '1047', f])
            os.rename(f, '{}.h'.format(f))
    if not os.path.isfile(library_so):
        with open(library_so, "wb") as x_out:
            pass
else:
    library = ['db2']
    
package_data = { 'ibm_db_tests': [ 'run_individual_tests', '*.png', '*.jpg', 'config.py.sample']}

data_files = [ (get_python_lib(), ['./README.md']),
               (get_python_lib(), ['./CHANGES.md']),
               (get_python_lib(), ['./LICENSE']),
               (get_python_lib(), ['./config.py.sample'])]

modules = ['ibm_db_dbi', 'testfunctions', 'tests']

if 'zos' == sys.platform:
    ext_modules = _ext_modules(os.path.join(os.getcwd(), include_dir), library, ibm_db_lib, ibm_db_lib_runtime)
else:
    ext_modules = _ext_modules(ibm_db_include, library, ibm_db_lib, ibm_db_lib_runtime)

if (sys.platform[0:3] == 'win'):
    library = ['db2cli64']
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
                      'Operating System :: Microsoft :: Windows :: Windows 10',
                      'Operating System :: Unix',
                      'Programming Language :: Python',
                      'Programming Language :: Python :: 2',
                      'Programming Language :: Python :: 2.7',
                      'Programming Language :: Python :: 3',
                      'Programming Language :: Python :: 3.5',
                      'Programming Language :: Python :: 3.6',
                      'Programming Language :: Python :: 3.7',
                      'Programming Language :: Python :: 3.8',
                      'Programming Language :: Python :: 3.9',
                      'Topic :: Database :: Front-Ends'],

       long_description = '''
                      This extension is the implementation of Python Database API Specification v2.0
                      The extension supports DB2 (LUW, zOS, i5) and IDS (Informix Dynamic Server)''',
       platforms = 'Linux32/64, Win32/64, aix32/64, ppc32/64, sunamd32/64, sun32/64, ppc64le, Z/OS',
       ext_modules  = ext_modules,
       py_modules   = modules,
       packages     = find_packages(),
       package_data = package_data,
       data_files   = data_files,
       include_package_data = True,
       cmdclass = cmd_class,
       **extra
     )

if license_agreement:
    sys.stdout.write(license_agreement)
