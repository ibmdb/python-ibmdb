**_Installing IBM Python &amp; ODBC on z/OS_**

Below steps were to be followed for the same:

1. Tested under below versions:
```
-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.8.3 64 bit_
```

**_Installing IBM Python & ODBC on z/OS_**

Below steps were followed for the same:

1. Tested under below:
```
-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.8.3 64 bit
-- Install the below PTFs(If not installed):
    -- UI72588 (v11)
    -- UI72589 (v12)
```

2. Configure below environment variables for install/compilation or create a shell profile (i.e. &quot;. profile&quot; file in your home environment) which includes environment variables, needed for Python and Db2 for z/OS ODBC(make sure all the below paths are changed based on your system and DB setting and all the variables are configured with none missed).

- NOTE(Default behaviour): 
	- IBM_DB_HOME is the HLQ for your Db2 libraries(SDSNMACS, SDSNC.H)
   
 - For compatibility with python ibm_db the following parameters must be set in the ODBC ini file
   CURRENTAPPENSCH=ASCII or CURRENTAPPENSCH=UNICODE (CURRENTAPPENSCH=EBCDIC is not supported)
   MULTICONTEXT=2
   FLOAT=IEEE
   e.g.
     ```; This is a comment line...
        ; Example COMMON stanza
        [COMMON]
        MVSDEFAULTSSID=VC1A
        CONNECTTYPE=1
        MULTICONTEXT=2
        CURRENTAPPENSCH=ASCII
        FLOAT=IEEE
        ; Example SUBSYSTEM stanza for VC1A subsystem
        [VC1A]
        MVSATTACHTYPE=RRSAF
        PLANNAME=DSNACLI
        ; Example DATA SOURCE stanza for STLEC1 data source
        [STLEC1]
        AUTOCOMMIT=1
        CURSORHOLD=1
     ```
 - The ODBC ini file must be encoded in IBM-1047 and cannot have the text tag on, e.g.,
   chtag -b $DSNAOINI or chtag -m -c IBM-1047 $DSNAOINI.
   Use chtag -p $DSNAOINI to verify that the file have T=off (text tag off) and is either tagged binary or mixed IBM-1047.

e.g.

```shell
#Code page autoconversion i.e. USS will automatically convert between ASCII and EBCDIC where needed.
export _BPXK_AUTOCVT='ON'
export _CEE_RUNOPTS='FILETAG(AUTOCVT,AUTOTAG) POSIX(ON) XPLINK(ON)'
export PATH=$HOME/bin:/user/python_install/bin:$PATH
export LIBPATH=$HOME/lib:/user/python_install/lib:$PATH
export STEPLIB=XXXX.DSN.VC10.SDSNLOAD
export STEPLIB=XXXX.DSN.VC10.SDSNLOD2:$STEPLIB
export STEPLIB=XXXX.SDSNEXIT:$STEPLIB
export IBM_DB_HOME=XXXX.DSN.VC10
export DSNAOINI=$HOME/odbc_XXXX.ini
```

In case you have data Set named anything other than SDSNC.H i.e. non default behaviour, you need to configure following variable. IGNORE OTHERWISE.
```shell
export DB2_INC=$IBM_DB_HOME.XXXX.H
```

In case you have SDSNMACS data Set named anything other than SDSNMACS i.e. non default behaviour, you need to configure following variable. IGNORE OTHERWISE.
```shell
export DB2_MACS=$IBM_DB_HOME.XXXX
```

3. Make sure when python is installed, you validate the same by typing &quot;python3 -V&quot; and it should return 3.8.3 or greater.
- Unless you are a sysprog you'll likely not have authority to create the site-package so consider using a python virtual environment as following:
```
python3 -m venv $HOME/ibm_python_venv
source $HOME/ibm_python_venv/bin/activate
```

4. Make sure &quot;pip3&quot; is installed and enabled as part of Python installation and is working.

5. ODBC installed connects and works with the Db2 for z/OS on the same subsytem or Sysplex with details configured in &quot;.ini&quot; file. No additional setting has to be done or credentials needs to be given during connection creation in python program. e.g.

```python
import ibm_db
conn = ibm_db.connect('','','')
```

**_Installing Python driver for Db2 i.e. ibm\_db &amp; Running a validation Program_**

Now that the Python and ODBC is ready, for connecting to Db2 you need a Db2 Python driver which we are going to install.

Follow the standard steps for the same i.e. pip3 install ibm_db

Now assuming everything went fine. You can run a test program i.e. **odbc\_test.py** with below content to validate if the setup has been done perfectly i.e. bash-4.3$ python3 odbc\_test.py:

```python
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
