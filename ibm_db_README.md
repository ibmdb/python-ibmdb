# Installing ibm\_db and ibm\_db\_dbi module #

We are assuming that you have Python already installed. In Linux you may need the python-dev package (you can install python-dev package through "$yum install python-devel" if yum doesn't work then you can also install it through "$apt-get install python-dev")


## Installation ##
```
  pip install ibm_db
```

This will install **ibm\_db** and **ibm\_db\_dbi** module.

> ## IBM\_DB and DB-API wrapper (ibm\_db\_dbi) sanity test ##

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

## Supported databases ##
  * **Minimum Supported version of IBM DB2 is V9fp2 for Linux, UNIX, and Windows
  ***Informix 11.10**(Cheetah)
  ***Remote connections to i5/OS (iSeries)*****Remote connections to z/OS (DB2 for z/OS)

## Feedback ##

Your feedback is very much appreciated and expected through project ibm-db:
  * **ibm-db project**:         http://code.google.com/p/ibm-db/
  * **ibm-db wiki**:            http://code.google.com/p/ibm-db/w/list
  * **ibm-db issues reports**:  http://code.google.com/p/ibm-db/issues/list
  * **ibm-db developers**:      opendev@us.ibm.com

note: since 2.5.0.1 (Jan 1 2015) the install process was simplified to a single 'pip install' command. Hence all no longer relevant comments on this page have been marked as deleted