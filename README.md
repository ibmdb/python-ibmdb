Python support for IBM DB2 and IBM Informix
=========

[![Build Status](https://travis-ci.org/ibmdb/python-ibmdb.svg?branch=master)](https://travis-ci.org/ibmdb/python-ibmdb)

## Python, DB-API components for IBM DB2 and Informix

Provides Python interface for connecting to IBM DB2 and Informix

### Pre-requisites
Install Python 2.7 or newer versions except python 3.3. Python ibm_db driver does not include support python 3.3 as it has reached end-of-life.
You might need zlib, openssl, pip installations if not already available in your setup. 

### Installation
You can install the driver using pip as:
```
pip install ibm_db
```
This will install ibm_db and ibm_db_dbi module. 

* Environment Variables:
  `IBM_DB_HOME :`

  Set this environment variable to avoid automatic downloading of the clidriver during installation. You could set this to the installation path of ODBC and CLI driver in your environment. 
  
If you face any problems due to missing dependencies while installing the ibm_db module, you can refer to following section Installing Dependencies.

#### <a name="Insdepen"></a> Installing Dependencies

##### Linux/Unix/MAC OS:
* If you face problems due to missing python header files, you would need to install python developer package before installing python ibm_db driver. e.g:

```
    zypper install python-devel
     or
    yum install python-devel
```
  
### Table of contents

[Components](#components)

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


<a name='downloads'></a>
## Downloads

Use following pypi web location for downloading source code and binaries
  **ibm_db**: https://pypi.python.org/pypi/ibm_db .

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

