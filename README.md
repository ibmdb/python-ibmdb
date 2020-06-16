Python support for IBM DB2 and IBM Informix
=========

[![Build Status](https://travis-ci.com/ibmdb/python-ibmdb.svg?branch=master)](https://travis-ci.com/ibmdb/python-ibmdb)

## Python, DB-API components for IBM DB2 and Informix

Provides Python interface for connecting to IBM DB2 and Informix

### Table of contents

[Components](#components)

[Pre-requisites](#prereq)

[Installation](#inst)

[Quick Example](#eg)

[API Documentation](#api)

[Downloads](#downloads)

[Latest Updates](#latest-updates)

[Support & Feedback](#support)

[Contributing to the ibm_db python project](#contributing-to-the-ibm_db-python-project)

<a name='components'></a>
## Components

1. The **ibm_db** contains:
   * **ibm_db** driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.
   * **ibm_db_dbi**: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db) for getting started with ibm_db and ibm_db_dbi

## <a name="prereq"></a> Pre-requisites
Install Python 2.7 or Python 3 <= 3.8. The minimum python version supported by driver is python 2.7 and the latest version supported is python 3.8 except version 3.3 as it has reached end-of-life.

The pre-built 32-bit and 64-bit binaries on windows are available for the following versions:
```
python 2.7
python 3.4
python 3.5
python 3.6
python 3.7
python 3.8
```

You might need zlib, openssl, pip installations if not already available in your setup.

* Linux/Unix:
  If you face problems due to missing python header files while installing the driver, you would need to install python developer package and retry install. e.g:

```
    zypper install python-devel
     or
    yum install python-devel
```

* For installing ibm_db on **Docker Linux container**, you may need to install **gcc, python, pip, python-devel and pam** if not already installed. Refer to [Installation](#docker) for more details.

## <a name="inst"></a> Installation
* MAC OS:
You can install the driver using pip as:
```
pip install --no-binary "ibm_db" ibm_db
```
* All other platforms:
You can install the driver using pip as:
```
pip install ibm_db
```
This will install ibm_db and ibm_db_dbi module.

* <a name="docker"></a>For installing ibm_db on docker Linux container, you can refer as below:
```
yum install python gcc pam wget python-devel.x86_64
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

* <a name="envvar"></a>Environment Variables:
  `IBM_DB_HOME :`

  Set this environment variable to avoid automatic downloading of the clidriver during installation. You could set this to the installation path of ODBC and CLI driver in your environment.
  e.g:
  ```
  Windows :
  set IBM_DB_HOME=c:/Users/skauser/clidriver

  Other platforms:
  export IBM_DB_HOME=/home/skauser/clidriver
  ```

  You are required to set the library path to the clidriver under IBM_DB_HOME to pick this version of the ODBC and CLI Driver.
  e.g:
  ```
  Windows:
  set LIB = %IBM_DB_HOME%/lib;%LIB%

  AIX:
  export LIBPATH = $IBM_DB_HOME/lib:$LIBPATH

  MAC:
  export DYLD_LIBRARY_PATH = $IBM_DB_HOME/lib:$DYLD_LIBRARY_PATH

  Other platforms:
  export LD_LIBRARY_PATH = $IBM_DB_HOME/lib:$LD_LIBRARY_PATH
  ```

  The ODBC and CLI driver is available for download at [Db2 LUW ODBC and CLI Driver](https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/).
Refer to ([License requirements](#Licenserequirements)) for more details on the CLI driver for manual download and installation.


## <a name="eg"></a> Quick Example
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
>>> # Execute tables API
>>> conn.tables('DB2ADMIN', '%')
[{'TABLE_CAT': None, 'TABLE_SCHEM': 'DB2ADMIN', 'TABLE_NAME': 'MYTABLE', 'TABLE_TYPE': 'TABLE', 'REMARKS': None}]
>>>
>>> # create table using ibm_db
>>> create="create table mytable(id int, name varchar(50))"
>>> ibm_db.exec_immediate(ibm_db_conn, create)
<ibm_db.IBM_DBStatement object at 0x7fcc5f44f650>
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
>>> ibm_db.close(ibm_db_conn)
True
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
|AIX           |  ppc           |aix32_odbc_cli.tar.gz    |  Yes         | V11.1       |
|              |  others        |aix64_odbc_cli.tar.gz    |  Yes         | V11.1       |
|Darwin        |  x64           |macos64_odbc_cli.tar.gz  |  Yes         | V10.5       |
|Linux         |  x64           |linuxx64_odbc_cli.tar.gz |  Yes         | V11.1       |
|              |  s390x         |s390x64_odbc_cli.tar.gz  |  Yes         | V11.1       |
|              |  s390          |s390_odbc_cli.tar.gz     |  Yes         | V11.1       |
|              |  ppc64  (LE)   |ppc64le_odbc_cli.tar.gz  |  Yes         | V11.1       |
|              |  ppc64         |ppc64_odbc_cli.tar.gz    |  Yes         | V10.5       |
|              |  ppc32         |ppc32_odbc_cli.tar.gz    |  Yes         | V10.5       |
|              |  others        |linuxia32_odbc_cli.tar.gz|  Yes         | V11.1       |
|Windows       |  x64           |ntx64_odbc_cli.zip       |  Yes         | V11.1       |
|              |  x32           |nt32_odbc_cli.zip        |  Deprecated  | NA          |
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
  June 16, 2019: A new release 3.0.2 of ibm_db and ibm_db_dbi available.


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
