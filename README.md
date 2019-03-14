Python support for IBM DB2 and IBM Informix
=========

[![Build Status](https://travis-ci.org/ibmdb/python-ibmdb.svg?branch=master)](https://travis-ci.org/ibmdb/python-ibmdb)

## Python, DB-API, Django/Django_jython and SQLAlchemy components for IBM DB2 and Informix

Provides Python, Django and SQLAlchemy support for IBM DB2 and Informix

### Table of contents

[Components](#components)

[Downloads](#downloads)

[Latest Updates](#latest-updates)

[Support](#support)

[Contributing to the ibm_db python project](#contributing-to-the-ibm_db-python-project)

<a name='components'></a>
## Components (Python Eggs)

1. The **ibm_db** Python Egg contains:
   * **ibm_db** driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.
   * **ibm_db_dbi**: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db) for getting started with ibm_db and ibm_db_dbi

2. The **ibm_db_django**: Django adapter for IBM DB2 databases. Supports latest Django versions and Django on Jython as well.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db_django) for using DB2 with Django

3. The **ibm_db_sa**: SQLAlchemy adapter for IBM DB2 and IBM Informix databases. Supports SQLAlchemy 0.7.3 and above.
   Checkout the [README](https://github.com/ibmdb/python-ibmdbsa/tree/master/ibm_db_sa) to get you started

4. The **ibm_db_alembic**: Alembic adaptor for IBM DB2 databases. Supports Alembic-0.6.5 and above

Additional information is available in the README files provided in the Python Eggs and also the source repository. .

<a name='downloads'></a>
## Downloads

Use following pypi web location for downloading source code and binaries
 1. **ibm_db**: https://pypi.python.org/pypi/ibm_db .
 2. **ibm_db_django**: https://pypi.python.org/pypi/ibm_db_django .
 3. **ibm_db_sa**: https://pypi.python.org/pypi/ibm_db_sa .
 4. **ibm_db_alembic**: https://pypi.python.org/pypi/ibm_db_alembic .

<a name='latest-updates'></a>
## Latest Updates

### *Support for Alembic*
  Oct 29th 2014: IBM DB2 backend support in Alembic application is now available to the community. Right now it is in beta stage.

### *Support for Django*
  Mar 23th 2017: New Release of IBM_DB_DJANGO (1.1.1.0) with Python3.x support made.

### *Support for SQLAlchemy*
  Aug 30th 2016: New Release of IBM_DB_SA (0.3.3) made.

### *Updated ibm_db*
  Mar 14th 2019: A new release 3.0.1 of ibm_db and ibm_db_dbi available.

### *Support for Django on Jython*
  ibm_db_django supports Django on Jython (on Jython-Django v1.0.x and v1.1.x are supported).


<a name='support'></a>
## Support

 * Google Group: http://groups.google.com/group/ibm_db


<a name='contributing-to-the-ibm_db-python-project'></a>
## Contributing to the ibm_db python project

See [CONTRIBUTING](https://github.com/ibmdb/python-ibmdb/blob/master/contributing/CONTRIBUTING.md)

```
The developer sign-off should include the reference to the DCO in remarks(example below):
DCO 1.1 Signed-off-by: Random J Developer <random@developer.org>
```

