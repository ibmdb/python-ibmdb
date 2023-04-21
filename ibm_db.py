import os
import sys
if 'clidriver' not in os.environ['PATH']:
    os.environ['PATH'] = os.environ['PATH'] + ";" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'clidriver', 'bin')
if sys.version_info >= (3,8,):
    if 'IBM_DB_HOME' not in os.environ:
        os.add_dll_directory(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'clidriver', 'bin'))
    else:
        ibm_db_home = os.environ['IBM_DB_HOME'].strip('"')
        os.add_dll_directory(os.path.join(ibm_db_home, 'bin'))

def __bootstrap__():
   global __bootstrap__, __loader__, __file__
   import sys, pkg_resources, imp
   __file__ = pkg_resources.resource_filename(__name__,'ibm_db.cp311-win_amd64.pyd')
   __loader__ = None; del __bootstrap__, __loader__
   imp.load_dynamic(__name__,__file__)
__bootstrap__()


