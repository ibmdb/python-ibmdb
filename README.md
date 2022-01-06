Python support for IBM DB2 and IBM Informix
=========

[![Build Status](https://travis-ci.com/ibmdb/python-ibmdb.svg?branch=master)](https://travis-ci.com/ibmdb/python-ibmdb)

## Python, DB-API components for IBM DB2 and Informix

Provides Python interface for connecting to IBM DB2 and Informix

### Table of contents

[Components](#components)

[Pre-requisites](#pre-requisites)

[Installation](#inst)

[Quick Example](#eg)

[API Documentation](#api)

[Downloads](#downloads)

[Latest Updates](#latest-updates)

[Support & Feedback](#support)

[Contributing to the ibm_db python project](#contributing-to-the-ibm_db-python-project)

[Some common issues](#KnownIssues)

[Testing](#testing)

<a name='components'></a>
## Components

1. The **ibm_db** contains:
   * **ibm_db** driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.
   * **ibm_db_dbi**: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db) for getting started with ibm_db and ibm_db_dbi

<a name="prereq"></a>
## Pre-requisites
Install Python 2.7 or Python 3 <= 3.9. The minimum python version supported by driver is python 2.7 and the latest version supported is python 3.9 except version 3.3 as it has reached end-of-life.

The pre-built 32-bit and 64-bit binaries on windows are available for the following versions:
```
python 2.7
python 3.4
python 3.5
python 3.6
python 3.7
python 3.8
python 3.9
python 3.10
```

You might need zlib, openssl, pip installations if not already available in your setup.

* Z/OS:
  In case of any issues using Python on zO/S, refer to this [file](install.md) and also refer to this [doc](https://github.com/ibmdb/node-ibm_db#configure-odbc-driver-on-zos).

* Linux/Unix:
  If you face problems due to missing python header files while installing the driver, you would need to install python developer package and retry install. e.g:

```
    zypper install python-devel
     or
    yum install python-devel
```

* MAC OS:
  Db2 V11.5.4 clidriver is built with GCC version 8.4.0 and hence you may need to upgrade to this version if you face problems due to old version of the GCC compiler in your environment while loading the ibm_db library.

* For installing ibm_db on **Docker Linux container**, you may need to install **gcc, python, pip, python-devel, libxml2 and pam** if not already installed. Refer to [Installation](#docker) for more details.

<a name="installation"></a> 
## Installation

You can install the driver using pip as:

```
pip install ibm_db
```
This will install ibm_db and ibm_db_dbi module.

If you are using python 3.8 or 3.9 on windows and building the source manually, you will need to set dll path of dependent library of clidriver before importing the module as:
```
import os
os.add_dll_directory('path to clidriver installation until bin')

e.g:
os.add_dll_directory('C:\Program Files\IBM\CLIDRIVER\\bin')
```
Refer https://bugs.python.org/issue36085 for more details.

* <a name="docker"></a>For installing ibm_db on docker Linux container, you can refer as below:
```
yum install python gcc pam wget python-devel.x86_64 libxml2
use, `yum install python3` to install python 3.x

if pip or pip3 does not exist, install it as:
wget https://bootstrap.pypa.io/get-pip.py
docker cp get-pip.py /root:<containerid>
cd root
python2 get-pip.py or python3 get-pip.py

Install python ibm_db as:
pip install ibm_db
or
pip3 install ibm_db

```

* Uninstalling the ibm_db driver :
```python
pip uninstall ibm_db
```

The ODBC and CLI Driver(clidriver) is automatically downloaded at the time of installation and it is recommended to use this driver. However, if you wish to use an existing installation of clidriver or install the clidriver manually and use it, you can set IBM_DB_HOME environment variable. For more information on how to set this variable, refer [Environment Variables](#envvar) section.

* <a name="environment variables"></a>Environment Variables:
  `IBM_DB_HOME :`

  Set this environment variable to avoid automatic downloading of the clidriver during installation. You could set this to the installation path of ODBC and CLI driver in your environment.<br>
  e.g:
  ```
  Windows :
  set IBM_DB_HOME=c:/Users/skauser/clidriver

  Other platforms:
  export IBM_DB_HOME=/home/skauser/clidriver
  ```

  You are required to set the library path to the clidriver under IBM_DB_HOME to pick this version of the ODBC and CLI Driver.<br>
  e.g:
  ```
  Windows:
  set LIB=%IBM_DB_HOME%/lib;%LIB%

  AIX:
  export LIBPATH=$IBM_DB_HOME/lib:$LIBPATH

  MAC:
  export DYLD_LIBRARY_PATH=$IBM_DB_HOME/lib:$DYLD_LIBRARY_PATH

  Other platforms:
  export LD_LIBRARY_PATH=$IBM_DB_HOME/lib:$LD_LIBRARY_PATH
  ```

  The ODBC and CLI driver is available for download at [Db2 LUW ODBC and CLI Driver](https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/).
Refer to ([License requirements](#Licenserequirements)) for more details on the CLI driver for manual download and installation.

* Installing using Anaconda distribution of python
```
conda install -c conda-forge ibm_db
```

* Supported Platform for Anaconda Installation

|Platform      |Architecture    |Supported     |Version      |
| :---:        |  :---:         |  :---:       | :--:
|Linux         |  amd64 (x86_64)|  Yes         | Latest    |
|Linux         |  ppc64le       |  Yes         | Latest    |
|Darwin        |  Mac OS        |  Yes         | Latest    |
|Windows       |  x64           |  Yes         | Latest    |
|Windows       |  x32           |  Yes         | Latest    |


## <a name="quick example"></a> Quick Example
```python
$ python
Python 3.6.5 (default, May 10 2018, 00:54:55)
[GCC 4.3.4 [gcc-4_3-branch revision 152973]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ibm_db
>>> #For connecting to local database named pydev for user db2inst1 and password secret, use below example
>>> #ibm_db_conn = ibm_db.connect('pydev', 'db2inst1', 'secret')
>>> #For connecting to remote database named pydev for uid db2inst and pwd secret on host host.test.com, use below example
>>> # Connect using ibm_db
>>> conn_str='database=pydev;hostname=host.test.com;port=portno;protocol=tcpip;uid=db2inst1;pwd=secret'
>>> ibm_db_conn = ibm_db.connect(conn_str,'','')
>>>
>>> # Connect using ibm_db_dbi
>>> import ibm_db_dbi
>>> conn = ibm_db_dbi.Connection(ibm_db_conn)
>>> # create table using ibm_db
>>> create="create table mytable(id int, name varchar(50))"
>>> ibm_db.exec_immediate(ibm_db_conn, create)
<ibm_db.IBM_DBStatement object at 0x7fcc5f44f650>
>>>
>>> # Execute tables API
>>> conn.tables('DB2INST1', '%')
[{'TABLE_CAT': None, 'TABLE_SCHEM': 'DB2INST1', 'TABLE_NAME': 'MYTABLE', 'TABLE_TYPE': 'TABLE', 'REMARKS': None}]
>>>
>>> # Insert 3 rows into the table
>>> insert = "insert into mytable values(?,?)"
>>> params=((1,'Sanders'),(2,'Pernal'),(3,'OBrien'))
>>> stmt_insert = ibm_db.prepare(ibm_db_conn, insert)
>>> ibm_db.execute_many(stmt_insert,params)
3
>>> # Fetch data using ibm_db_dbi
>>> select="select id, name from mytable"
>>> cur = conn.cursor()
>>> cur.execute(select)
True
>>> row=cur.fetchall()
>>> print("{} \t {} \t {}".format(row[0],row[1],row[2]),end="\n")
(1, 'Sanders')   (2, 'Pernal')   (3, 'OBrien')
>>> row=cur.fetchall()
>>> print(row)
[]
>>>
>>> # Fetch data using ibm_db
>>> stmt_select = ibm_db.exec_immediate(ibm_db_conn, select)
>>> cols = ibm_db.fetch_tuple( stmt_select )
>>> print("%s, %s" % (cols[0], cols[1]))
1, Sanders
>>> cols = ibm_db.fetch_tuple( stmt_select )
>>> print("%s, %s" % (cols[0], cols[1]))
2, Pernal
>>> cols = ibm_db.fetch_tuple( stmt_select )
>>> print("%s, %s" % (cols[0], cols[1]))
3, OBrien
>>> cols = ibm_db.fetch_tuple( stmt_select )
>>> print(cols)
False
>>>
>>> # Close connections
>>> cur.close()
True
>>> # Dropping the table created
>>> drop = "drop table mytable"
>>> stmt_delete = ibm_db.exec_immediate(ibm_db_conn,drop)
>>> conn1.tables('DB2INST1','MY%')
[]
>>>
>>> ibm_db.close(ibm_db_conn)
True
```

## Example of SSL Connection String
 
```
Using SSLServerCertificate keyword
 
conn = ibm_db.connect("DATABASE=<DATABASE_NAME>;HOSTNAME=<HOSTNAME>;PORT=<SSL_PORT>;SECURITY=SSL;SSLServerCertificate=<FULL_PATH_TO_SERVER_CERTIFICATE>;UID=<USER_ID>;PWD=<PASSWORD>",'','')
```
 
```
Using SSLClientKeyStoreDB and SSLClientKeyStoreDBPassword keyword
 
conn = ibm_db.connect("DATABASE=<DATABASE_NAME>;HOSTNAME=<HOSTNAME>;PORT=<SSL_PORT>;SECURITY=SSL;SSLClientKeyStoreDB=<FULL_PATH_TO_CLIENT_KEY_STORE_DB>;SSLClientKeyStoreDBPassword=<KEYSTORE_PASSWORD>;UID=<USER_ID>;PWD=<PASSWORD>",'','')
```
 
```
Using SSLClientKeyStoreDB and SSLClientKeyStash keyword
 
conn = ibm_db.connect("DATABASE=<DATABASE_NAME>;HOSTNAME=<HOSTNAME>;PORT=<SSL_PORT>;SECURITY=SSL;SSLClientKeyStoreDB=<FULL_PATH_TO_CLIENT_KEY_STORE_DB>;SSLClientKeyStash=<FULL_PATH_TO_CLIENT_KEY_STASH>;UID=<USER_ID>;PWD=<PASSWORD>",'','')
```
More examples can be found under ['tests'](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db/tests) folder.

[API Documentation](https://github.com/ibmdb/python-ibmdb/wiki/APIs) has examples for each API.

Jupyter Notebook examples can be found here -> [Other Examples](https://github.com/IBM/db2-python/tree/master/Jupyter_Notebooks)

## <a name="api"></a> API Documentation
For more information on the APIs supported by ibm_db, please refer to below link:

https://github.com/ibmdb/python-ibmdb/wiki/APIs

### <a name="Licenserequirements"></a> License requirements for connecting to databases

Python ibm_db driver can connect to DB2 on Linux Unix and Windows without any additional license/s, however, connecting to databases on DB2 for z/OS or DB2 for i(AS400) Servers require either client side or server side license/s. The client side license would need to be copied under `license` folder of your `cidriver` installation directory and for activating server side license, you would need to purchase DB2 Connect Unlimited for System z® and DB2 Connect Unlimited Edition for System i®.

To know more about license and purchasing cost, please contact [IBM Customer Support](http://www-05.ibm.com/support/operations/zz/en/selectcountrylang.html).

To know more about server based licensing viz db2connectactivate, follow below links:
* [Activating the license certificate file for DB2 Connect Unlimited Edition](https://www.ibm.com/developerworks/community/blogs/96960515-2ea1-4391-8170-b0515d08e4da/entry/unlimited_licensing_in_non_java_drivers_using_db2connectactivate_utlility1?lang=en).
* [Unlimited licensing using db2connectactivate utility](https://www.ibm.com/developerworks/community/blogs/96960515-2ea1-4391-8170-b0515d08e4da/entry/unlimited_licensing_in_non_java_drivers_using_db2connectactivate_utlility1?lang=en.)

If you intend to install the clidriver manually, Following are the details of the client driver versions that you can download from [CLIDRIVER](https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/) to be able to connect to databases on non-LUW servers. You would need the client side license file as per Version for corresponding installation.:

#### <a name="LicenseDetails"></a> CLIDriver and Client license versions for Specific Platform and Architecture

|Platform      |Architecture    |Cli Driver               |Supported     |Version      |
| :---:        |  :---:         |  :---:                  |  :---:       | :--:
|AIX           |  ppc           |aix32_odbc_cli.tar.gz    |  Yes         | V11.5.5     |
|              |  others        |aix64_odbc_cli.tar.gz    |  Yes         | V11.5.5     |
|Darwin        |  x64           |macos64_odbc_cli.tar.gz  |  Yes         | V11.5.5     |
|Linux         |  x64           |linuxx64_odbc_cli.tar.gz |  Yes         | V11.5.5     |
|              |  s390x         |s390x64_odbc_cli.tar.gz  |  Yes         | V11.5.5     |
|              |  s390          |s390_odbc_cli.tar.gz     |  Yes         | V11.1       |
|              |  ppc64  (LE)   |ppc64le_odbc_cli.tar.gz  |  Yes         | V11.5.5     |
|              |  ppc64         |ppc64_odbc_cli.tar.gz    |  Yes         | V10.5       |
|              |  ppc32         |ppc32_odbc_cli.tar.gz    |  Yes         | V10.5       |
|              |  others        |linuxia32_odbc_cli.tar.gz|  Yes         | V11.5.5     |
|Windows       |  x64           |ntx64_odbc_cli.zip       |  Yes         | V11.5.5     |
|              |  x32           |nt32_odbc_cli.zip        |  Yes         | V11.5.5     |
|Sun           | i86pc          |sunamd64_odbc_cli.tar.gz |  Yes         | V10.5       |
|              |                |sunamd32_odbc_cli.tar.gz |  Yes         | V10.5       |
|              | sparc          |sun64_odbc_cli.tar.gz    |  Yes         | V11.1       |
|              | sparc          |sun32_odbc_cli.tar.gz    |  Yes         | V11.1       |

You can refer to [ODBC and CLI Driver installation](http://www-01.ibm.com/support/docview.wss?uid=swg21418043) for details on how to install the driver manually.


<a name='downloads'></a>
## Downloads

Use following pypi web location for downloading source code and binaries
**ibm_db**: https://pypi.python.org/pypi/ibm_db .
You can also get the source code by cloning the ibm_db github repository as :
```
git clone git@github.com:ibmdb/python-ibmdb.git
```

<a name='latest-updates'></a>
## Latest Updates

### *Updated ibm_db*
  Apr 12, 2021: A new release 3.0.4 of ibm_db and ibm_db_dbi available.


<a name='support'></a>
## Support & feedback
**Your feedback is very much appreciated and expected through project ibm-db:**
  * ibm-db issues reports: **https://github.com/ibmdb/python-ibmdb/issues**
  * ibm_db discuss: **http://groups.google.com/group/ibm_db**


<a name='contributing-to-the-ibm_db-python-project'></a>
## Contributing to the ibm_db python project

See [CONTRIBUTING](https://github.com/ibmdb/python-ibmdb/blob/master/contributing/CONTRIBUTING.md)

```
The developer sign-off should include the reference to the DCO in remarks(example below):
DCO 1.1 Signed-off-by: Random J Developer <random@developer.org>
```

<a name='KnownIssues'></a>
## Some common issues

## 1. Installation Issues for missing python.h file

### Always use the latest pip
```python3 -m pip install --upgrade pip```

### Install the package python3-dev that delivers the python.h header file
```
For RHEL use
yum install python3-dev
```
```
For Ubuntu use
apt-get install python3-dev
```

### Once the above steps goes through fine, try re-installing ibm_db.

### Issues with MAC OS X
* If you run into errors for libdb2.dylib as below:

```python
>>> import ibm_db
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: dlopen(/usr/local/lib/python3.5/site-packages/ibm_db.cpython-35m-darwin.so, 2): Library not loaded: libdb2.dylib
  Referenced from: /usr/local/lib/python3.5/site-packages/ibm_db.cpython-35m-darwin.so
  Reason: image not found

```

You would need to set DYLD_LIBRARY_PATH to point to lib folder as per the installation location of clidriver in your environment. Assuming the driver is installed at /usr/local/lib/python3.5/site-packages/clidriver, you can set the path as:

```
export DYLD_LIBRARY_PATH=/usr/local/lib/python3.5/site-packages/clidriver/lib:$DYLD_LIBRARY_PATH

```
If the issue is not resolved even after setting DYLD_LIBRARY_PATH, you could refer:
[MAC OS Hints and Tips](https://www.ibm.com/developerworks/community/blogs/96960515-2ea1-4391-8170-b0515d08e4da/entry/ibm_db_on_MAC_OS_Hints_and_Tips?lang=en)

* Resolving SQL1042C error

If you hit following error while attempting to connect to a database:

```python
>>> import ibm_db
>>> ibm_db.connect("my_connection_string", "", "")
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
 Exception: [IBM][CLI Driver] SQL1042C An unexpected system error occurred. SQLSTATE=58004 SQLCODE=-1042
```
Set DYLD_LIBRARY_PATH to point to icc folder as per the installation location of clidriver in your environment.

```
export DYLD_LIBRARY_PATH=/usr/local/lib/python3.5/site-packages/clidriver/lib/icc:$DYLD_LIBRARY_PATH
```

In case of similar issue in windows platform

```
set PATH=<clidriver_folder_path>\bin\amd64.VC12.CRT;%PATH%
```

<a name='testing'></a>
# Testing

Tests displaying Python ibm_db driver code examples are located in the ibm_db_tests
directory. A valid config.py will need to be created to configure your DB2
settings. A config.py.sample exists that can be copied and modified for your
environment.

The config.py should look like this:

```python
test_dir =      'ibm_db_tests'         # Location of testsuite file (relative to current directory)

database =      'test'          # Database to connect to
user     =      'db2inst1'      # User ID to connect with
password =      'password'      # Password for given User ID
hostname =      'localhost'     # Hostname
port     =      50000           # Port Number
```

Point the database to mydatabase as created by the following command.

The tests that ibm_db driver uses depends on a UTF-8 database.  This can be
created by running:
```
  CREATE DATABASE mydatabase USING CODESET UTF-8 TERRITORY US
```
Some of the tests utilize XML functionality only available in version 9 or
later of DB2.  While DB2 v8.x is fully supported, two of the tests
(test_195.py and test_52949.py) utilize XML functionality.  These tests will
fail on version 8.x of DB2.

## Running the driver testsuite on Linux
  In order to run the entire python driver testsuite on Linux, run this
  command at the command prompt:
  ```
    python tests.py
  ```
  To run a single test, set the environment variable, **SINGLE_PYTHON_TEST**, to
  the test filename you would like to run, followed by the previous command.

## Running the driver testsuite on Windows
  In order to run the entire python driver testsuite on Windows, run this
  command at the command prompt:
  ```
    tests.py
  ```
  To run a single test, set the environment variable, **SINGLE_PYTHON_TEST**, to
  the test filename you would like to run, followed by the previous command.


## Known Limitations for the Python driver

If trusted context is not set up, there will be two failures related to trusted context. When thick client has been used then additional three failures related to create, recreate DB.


## Known Limitations for the Python wrapper

1. The rowcount for select statements can not be generated.
2. Some warnings from the drivers are not caught by the wrapper.
   As such these might go unnoticed.