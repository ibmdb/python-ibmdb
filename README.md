#Python support for IBM DB2 and IBM Informix 

##Python, DB-API, Django/Django_jython and SQLAlchemy components for IBM DB2 and Informix

Provides Python, Django and SQLAlchemy support for IBM DB2 and Informix 

###Components :

1. The *ibm_db* contains:
   * *ibm_db* driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix. 
   * *ibm_db_dbi*: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db) for getting started with ibm_db and ibm_db_dbi
 
2. The *ibm_db_django*: Django adapter for IBM DB2 databases. Supports latest Django versions and Django on Jython as well.
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db_django) for using DB2 with Django

3. The *ibm_db_sa*: SQLAlchemy adapter for IBM DB2 and IBM Informix databases. Supports SQLAlchemy 0.7.3 and above. 
   Checkout the [README](https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db_sa) to get you started

4. The *ibm_db_alembic*: Alembic adaptor for IBM DB2 databases. Supports Alembic-0.6.5 and above

Additional information is available in the README files provided in the Python Eggs and also the source repository. .

===Downloads===
Use following pypi web location for downloading source code and binaries
 # *ibm_db*: https://pypi.python.org/pypi/ibm_db .
 # *ibm_db_django*: https://pypi.python.org/pypi/ibm_db_django .
 # *ibm_db_sa*: https://pypi.python.org/pypi/ibm_db_sa .
 # *ibm_db_alembic*: https://pypi.python.org/pypi/ibm_db_alembic .

===Latest Updates===
*Support for Alembic*
  Oct 29th 2014: IBM DB2 backend support in Alembic application is now available to the community. Right now it is in beta stage.

*Support for Django*
  Nov 21th 2014: New Release of IBM_DB_DJANGO (1.0.7) with Django 1.7.x support made.

*Support for SQLAlchemy*
  Oct 20th 2014: New Release of IBM_DB_SA (0.3.2) made.

*Updated ibm_db*
  Jan 1st 2015: A new release 2.0.5.1 of ibm_db and ibm_db_dbi

*Support for Django on Jython*
  ibm_db_django supports Django on Jython (on Jython-Django v1.0.x and v1.1.x are supported).


===Support===
 * Google Group: http://groups.google.com/group/ibm_db
   
 * Development: opendev at us dot ibm dot com.

===Contributing to the ibm_db python project===
[Contributions Guidelines for Contributions]()

