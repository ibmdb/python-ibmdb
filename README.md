# Quick Getting Started Steps (README) #

## Install **IBM\_DB** support for **SQLAlchemy** ##


The **IBM\_DB\_SA adapter** provides the [Python](http://www.python.org/)/[SQLAlchemy](http://www.sqlalchemy.org) interface to IBM DB2.

The **IBM\_DB\_SA adapter** is packaged as a [Python Egg](http://peak.telecommunity.com/DevCenter/PythonEggs) component and is dependent on:
  * **SQLAlchemy** 0.7.3 and above


We are assuming that you have DB2 or Informix 11.10 and SQLAlchemy already installed.

> If you need to connect from SQLAlchemy to a DB2 server on the same local machine, just proceed to the **Installation** section below.
> If you need to connect from SQLAlchemy to either a DB2 server on different machine or to Informix (local or remote) then you will need to at minimum install the [IBM Data Server Driver Package](https://www-304.ibm.com/support/docview.wss?uid=swg27016878) (DS Driver) on the machine where you installed SQLAlchemy.

## Installation and configuration ##

To install the IBM\_DB\_SA Python egg component (.egg), use the standard
setuptools provided by the Python Easy Install, which is available through
the [Python Enterprise Application Kit](http://peak.telecommunity.com/DevCenter/EasyInstall) community portal.

After installing Easy Install, perform these additional steps to install
the IBM\_DB\_SA egg component:

  * To install the IBM\_DB\_SA egg component available in the [remote](http://code.google.com/p/ibm-db/downloads/list) [repository](http://pypi.python.org/pypi/ibm_db):
> > Windows:
```
 > easy_install ibm_db_sa
```
> > Linux or UNIX:
```
 $ sudo easy_install ibm_db_sa
```

  * To install the IBM\_DB\_SA egg component from the downloaded .egg file:
> > Windows:
```
 > easy_install ibm_db_sa-x.x.x-py2.x.egg
```
> > Linux or UNIX:
```
 $ sudo easy_install ibm_db_sa-x.x.x-py2.x.egg
```

  * To uninstall the IBM\_DB\_SA egg component:
> > Windows:
```
 > easy_install -m ibm_db_sa==x.x.x
 > rmdir Python25\Lib\site-packages\ibm_db_sa-x.x.x-py2.x.egg
```
> > Linux or UNIX:
```
 $ sudo easy_install -m ibm_db_sa==x.x.x   
 $ sudo rm -rf /usr/lib/python2.5/site-packages/ibm_db_sa-x.x.x-py2.x.egg
```



## Quick Sanity Test Example ##

Before you open a Python prompt, you need to ensure that IBM CLI  (which the Python driver uses to connect to DB2/Informix) is accessible to SQLAlchemy. On Linux, set the LD\_LIBRARY\_PATH variable (for the user executing Python) to include the folder where the IBM CLI shared library (libdb2.so) resides

> For local DB2 access: export LD\_LIBRARY\_PATH=`<`DB2\_HOME`>`/sqllib/lib:$LD\_LIBRARY\_PATH .For remote DB2 or any Informix access with DS Driver: export LD\_LIBRARY\_PATH=`<`DS\_DRIVER\_FOLDER`>`/odbc\_cli\_driver/linux/clidriver/lib:$LD\_LIBRARY\_PATH


### IBM\_DB SA adapter sanity test ###
```
$ python
Python 2.5.1 (r251:54863, Oct  5 2007, 13:36:32)
[GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlalchemy
>>> from sqlalchemy import *
>>> db2 = sqlalchemy.create_engine('ibm_db_sa://db2inst1:secret@host.name.com:50000/pydev')
>>> metadata = MetaData()
>>> users = Table('users', metadata, 
    Column('user_id', Integer, primary_key = True),
    Column('user_name', String(16), nullable = False),
    Column('email_address', String(60), key='email'),
    Column('password', String(20), nullable = False)
)
>>> metadata.bind = db2
>>> metadata.create_all()
>>> users_table = Table('users', metadata, autoload=True, autoload_with=db2)
>>> users_table
```


### IBM\_DB DB-API wrapper sanity test ###
```
$ python
Python 2.5.1 (r251:54863, Oct  5 2007, 13:36:32)
[GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import ibm_db
>>> ibm_db_conn = ibm_db.connect('pydev', 'db2inst1', 'secret')
>>> import ibm_db_dbi
>>> conn = ibm_db_dbi.Connection(ibm_db_conn)
>>> conn.tables('SYSCAT', '%')
```


### Example: Using the Data Source Name (DSN) through CLI configuration ###
```
$ cat ./clidriver/db2cli.ini
...
[pydb]
Database=pydev
Protocol=tcpip
Hostname=host.name.com
Servicename=50000
uid=db2inst1
pwd=secret
```


```
$ python
Python 2.5.1 (r251:54863, Oct  5 2007, 13:36:32)
[GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlalchemy
>>> from sqlalchemy import *
>>> db2 = sqlalchemy.create_engine('ibm_db_sa://db2inst1:secret@/pydb')
>>> ...
```




## Tested operating systems ##
  * **SuSE Linux Server** 9 32-bit
  * **Ubuntu Linux 7.04** 32-bit
  * **MS Windows** 32-bit


## Supported databases ##
  * **Minimum Supported version of IBM DB2 is V9fp2** for Linux, UNIX, and Windows
  * **IBM DB2 Version 9.5** for Linux, UNIX, and Windows
  * **IBM DB2 Version 9.1** for Linux, UNIX, and Windows



## Feedback ##

Your feedback is very much appreciated and expected through project ibm-db:
  * **ibm-db project**:         http://code.google.com/p/ibm-db/
  * **ibm-db wiki**:            http://code.google.com/p/ibm-db/w/list
  * **ibm-db issues reports**:  http://code.google.com/p/ibm-db/issues/list
  * **ibm-db developers**:      opendev@us.ibm.com