## Python, DB-API, Django/Django\_jython and SQLAlchemy components for IBM DB2 and Informix ##

Provides Python, Django and SQLAlchemy support for IBM DB2 and Informix

### Components (Python Eggs): ###

1. The **ibm\_db** Python Egg contains:
  * **ibm\_db** driver: Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.
  * **ibm\_db\_dbi**: Python driver for IBM DB2 and IBM Informix databases that complies to the DB-API 2.0 specification.
> Checkout the [README](http://code.google.com/p/ibm-db/wiki/ibm_db_README) for getting started with ibm\_db and ibm\_db\_dbi

2. The **ibm\_db\_django**: Django adapter for IBM DB2 databases. Supports latest Django versions and Django on Jython as well.
> Checkout the [README](http://code.google.com/p/ibm-db/wiki/ibm_db_django_README) for using DB2 with Django

3. The **ibm\_db\_sa**: SQLAlchemy adapter for IBM DB2 and IBM Informix databases. Supports SQLAlchemy 0.7.3 and above.
> Checkout the [README](http://code.google.com/p/ibm-db/wiki/README) to get you started

4. The **ibm\_db\_alembic**: Alembic adaptor for IBM DB2 databases. Supports Alembic-0.6.5 and above

Additional information is available in the README files provided in the Python Eggs and also the source repository. .

### Downloads ###
Use following pypi web location for downloading source code and binaries
  1. **ibm\_db**: https://pypi.python.org/pypi/ibm_db .
  1. **ibm\_db\_django**: https://pypi.python.org/pypi/ibm_db_django .
  1. **ibm\_db\_sa**: https://pypi.python.org/pypi/ibm_db_sa .
  1. **ibm\_db\_alembic**: https://pypi.python.org/pypi/ibm_db_alembic .

### Latest Updates ###
**Support for Alembic**
> Oct 29th 2014: IBM DB2 backend support in Alembic application is now available to the community. Right now it is in beta stage.

**Support for Django**
> Nov 21th 2014: New Release of IBM\_DB\_DJANGO (1.0.7) with Django 1.7.x support made.

**Support for SQLAlchemy**
> Oct 20th 2014: New Release of IBM\_DB\_SA (0.3.2) made.

**Updated ibm\_db**
> Jan 1st 2015: A new release 2.0.5.1 of ibm\_db and ibm\_db\_dbi

**Support for Django on Jython**
> ibm\_db\_django supports Django on Jython (on Jython-Django v1.0.x and v1.1.x are supported).


### Support ###
  * Google Group: http://groups.google.com/group/ibm_db

  * Development: opendev at us dot ibm dot com.

### Contributing to the ibm\_db python project ###
[Guidelines for Contributions](Contributions.md)
