_ **Installing IBM Python &amp; ODBC on z/OS** _

Below steps were followed for the same:

1. Tested under below:
```

-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.8.3 64 bit
-- Install the ++APAR PH27502(If not installed)
```

2. Configure below environment variables or create a shell profile (i.e. &quot;. profile&quot; file in your home environment) which includes environment variables, needed for Python and DB2 for z/OS ODBC(make sure all the below paths are changed based on your system and DB setting and all the variables are configured with none missed).

e.g.

```
export _BPXK_AUTOCVT='ON'
export _CEE_RUNOPTS='FILETAG(AUTOCVT,AUTOTAG) POSIX(ON) XPLINK(ON)
export PATH=$HOME/bin:/rsusr/pyz/bin:$PATH
export LIBPATH=$HOME/lib:/rsusr/pyz/lib:$PATH
export STEPLIB=RSREE.DSN.VC10.SDSNLOAD
export STEPLIB=RSREE.DSN.VC10.SDSNLOD2:$STEPLIB
export STEPLIB=XXXX.SDSNEXIT:$STEPLIB
export IBM_DB_HOME=RSREE.DSN.VC10
export DSNAOINI=$HOME/odbc_XXXX.ini

```

3. Make sure when python is installed, you validate the same by typing &quot;python3 -V&quot; and it should return 3.8.3 or greater.

4. Make sure &quot;pip3&quot; is installed and enabled as part of Python installation and is working.
5. ODBC installed connects and works with the DB2 for z/OS on the same subsytem or Sysplex with details configured in &quot;.ini&quot; file. No additional setting has to be done or credentials needs to be given during connection creation in python program. e.g.

```

import ibm_db
conn = ibm_db.connect('','','')


```

_ **Installing Python driver for DB2 i.e. ibm\_db &amp; Running a validation Program** _

Now that the Python and ODBC is ready, for connecting to DB2 you need a DB2 Python driver which we are going to install.

Follow the standard steps for the same i.e. pip3 install ibm_db

Now assuming everything went fine. You can run a test program i.e. **odbc\_test.py** with below content to validate if the setup has been done perfectly i.e. bash-4.3$ python3 odbc\_test.py:

```


from __future__ import print_function
import sys
import ibm_db
print('ODBC Test start')
conn = ibm_db.connect('','','')
if conn:
    stmt = ibm_db.exec_immediate(conn,"SELECT CURRENT DATE FROM SYSIBM.SYSDUMMY1")
    if stmt:
        while (ibm_db.fetch_row(stmt)):
            date = ibm_db.result(stmt, 0)
            print("Current date is :",date)
    else:
        print(ibm_db.stmt_errormsg())
    ibm_db.close(conn)
else:
    print("No connection:", ibm_db.conn_errormsg())
print('ODBC Test end')


```