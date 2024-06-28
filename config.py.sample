test_dir    =    'ibm_db_tests'        # Location of testsuite file (relative to current directory) (Don't change this.)

# database    =    'sample'    # Database to connect to. Please use an empty database for best results.

import sys, os, platform
import warnings
import json
if sys.platform != 'zos':
    file_path = 'config.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    database = data['database']               # Database to connect to
    hostname = data['hostname']               # Hostname
    port = data['port']                       # Port Number

    env_not_set = False
    if 'DB2_USER' in os.environ:
        user = os.getenv('DB2_USER')          # User ID to connect with (must be secadm for trusted-context testcases)
    else:
        user = data['user']
        env_not_set = True
    if 'DB2_PASSWD' in os.environ:
        password = os.getenv('DB2_PASSWD')    # Password for given User ID
    else:
        password = data['password']
        env_not_set = True

    if env_not_set == True:
        warnings.warn("Warning: Environment variable DB2_USER or DB2_PASSWD is not set.")
        print("Please set it before running test file and avoid")
        print("hardcoded password in config.json file." )
        exit
else:
    database = "DSN=%s%s" % (platform.node(), os.getenv("SUBSYSTEM"))
    user	=	os.getenv('USER')	# User ID to connect with
    try:
        with open("%s/.password" % os.getenv('HOME'), "r") as pwd:
            password=	pwd.read().rstrip()	# Password for given User ID
    except Exception:
        if os.getenv("DSNAOINI").endswith("RRSAF"):
            print("If you use RRSAF, please create the file ~/.password, and tag it, and run: chmod 600 ~/.password")
            print("Also, consider deleting ~/.password after testing is completed.")
        else:
            user     = None
            password = None
    hostname	=	None   #'localhost'	# Hostname
    port	=	None   #50000		# Port Number

auth_user   =    'auth_user'    # Authentic user of Database
auth_pass   =    'auth_pass'    # Password for Authentic user
tc_user     =    'tc_user'    # Trusted user
tc_pass     =    'tc_pass'    # Password to trusted user
tc_appserver_address = '' # optional. Hostname/IP-address, where trusted-context testcases run, defaults to local hostname

