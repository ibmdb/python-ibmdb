Python support for IBM DB2 and IBM Informix
=========

[![Build Status](https://travis-ci.org/ibmdb/python-ibmdb.svg?branch=master)](https://travis-ci.org/ibmdb/python-ibmdb)

## Python, DB-API components for IBM DB2 and Informix

Provides Python interface for connecting to IBM DB2 and Informix

### Table of contents

[Components](#components)

[Pre-requisites](#prereq)

[Installation](#inst)

[Quick Example](#eg)

[Downloads](#downloads)

[Latest Updates](#latest-updates)

[Support](#support)

[Contributing to the ibm_db python project](#contributing-to-the-ibm_db-python-project)

<a name='components'></a>
## Components

1. The **ibm_db** contains:
   * **ibm_db** driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.
   * **ibm_db_dbi**: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db) for getting started with ibm_db and ibm_db_dbi

## <a name="prereq"></a> Pre-requisites
Install Python 2.7 or newer versions except python 3.3. Python ibm_db driver does not include support python 3.3 as it has reached end-of-life.
You might need zlib, openssl, pip installations if not already available in your setup. 

## <a name="inst"></a> Installation
You can install the driver using pip as:
```
pip install ibm_db
```
This will install ibm_db and ibm_db_dbi module. 

* Environment Variables:
  `IBM_DB_HOME :`

  Set this environment variable to avoid automatic downloading of the clidriver during installation. You could set this to the installation path of ODBC and CLI driver in your environment. The ODBC and CLI driver is available for download at [Db2 LUW ODBC and CLI Driver](https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/).
Refer to ([License requirements](#Licenserequirements)) for more details on the CLI driver for manual download and installation.
  
If you face any problems due to missing dependencies while installing the ibm_db module, you can refer to section [Installing Dependencies](#Insdepen).

### <a name="Insdepen"></a> Installing Dependencies

#### Linux/Unix:
* If you face problems due to missing python header files, you would need to install python developer package before installing python ibm_db driver. e.g:

```
    zypper install python-devel
     or
    yum install python-devel
```
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
>>> conn_str='database=pydev;hostname=host.test.com;port=portno;protocol=tcpip;uid=db2inst1;pwd=secret'
>>> ibm_db_conn = ibm_db.connect(conn_str,'','')
>>> import ibm_db_dbi
>>> conn = ibm_db_dbi.Connection(ibm_db_conn)
>>> conn.tables('SYSCAT', '%')
```
More examples can be found under ['tests'](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db/tests) folder.

### <a name="Licenserequirements"></a> License requirements for connecting to databases

Python ibm_db driver can connect to DB2 on Linux Unix and Windows without any additional license/s, however, connecting to databases on DB2 for z/OS or DB2 for i(AS400) Servers require either client side or server side license/s. The client side license would need to be copied under `license` folder of your `cidriver` installation directory and for activating server side license, you would need to purchase DB2 Connect Unlimited for System z® and DB2 Connect Unlimited Edition for System i®.

To know more about license and purchasing cost, please contact [IBM Customer Support](http://www-05.ibm.com/support/operations/zz/en/selectcountrylang.html).

To know more about server based licensing viz db2connectactivate, follow below links:
* [Activating the license certificate file for DB2 Connect Unlimited Edition](https://www.ibm.com/developerworks/community/blogs/96960515-2ea1-4391-8170-b0515d08e4da/entry/unlimited_licensing_in_non_java_drivers_using_db2connectactivate_utlility1?lang=en).
* [Unlimited licensing using db2connectactivate utility](https://www.ibm.com/developerworks/community/blogs/96960515-2ea1-4391-8170-b0515d08e4da/entry/unlimited_licensing_in_non_java_drivers_using_db2connectactivate_utlility1?lang=en.)

Following are the details of the client license versions that you need to be able to connect to databases on non-LUW servers:

#### <a name="LicenseDetails"></a> Client license for Specific Platform and Architecture

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
  Mar 14th 2019: A new release 3.0.1 of ibm_db and ibm_db_dbi available.


<a name='support'></a>
## Support

 * Google Group: http://groups.google.com/group/ibm_db
 * Github issues tracker: https://github.com/ibmdb/python-ibmdb/issues


<a name='contributing-to-the-ibm_db-python-project'></a>
## Contributing to the ibm_db python project

See [CONTRIBUTING](https://github.com/ibmdb/python-ibmdb/blob/master/contributing/CONTRIBUTING.md)

```
The developer sign-off should include the reference to the DCO in remarks(example below):
DCO 1.1 Signed-off-by: Random J Developer <random@developer.org>
```
