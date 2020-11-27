_ **Installing IBM Python &amp; ODBC on z/OS** _

Below steps were followed for the same:

1. Pre-Requisite:
```

-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.8.3 64 bit
-- Install the ++APAR PH27502
-- In order for Python driver for Db2 to be installed smoothly on z/OS 2.3 make sure & NOTE of below:

	a.	Removing text tag from ibm_db.so resolves error with  "CEE3512S An HFS load of module ... failed." i.e. chtag -R <path to Python ibm-db egg file>/ibm_db.so
	b.	File, which is used in DSNAOINI should be tagged as binary, if it tagged as text - it can't be used for some reason by python/db2 code.
	c.	It is possible to connect to default DB2  subsystem (set in DSNAOINI file) by using empty connection string in python ibm_db.
	d.	You need to make sure all environment variables as mentioned below are set before running the installation script i.e. Install_z_ibm-db.

```

2. Set the desired Db2 for z/OS subsystem to connect to via ODBC as the same needs to be configured as part of ODBC installation in &quot;odbc.ini&quot; file. e.g.
```
[COMMON]
MVSDEFAULTSSID=XXXX
CONNECTTYPE=2
APPLTRACE=0
APPLTRACEFILENAME=./odbctrace.txt
DIAGTRACE=0
[XXXX]
MVSATTACHTYPE=RRSAF
PLANNAME=DSNACLI

```

1. Create a shell profile (i.e. &quot;. profile&quot; file in your home environment) which includes environment variables, needed for python and DB2 for z/OS ODBC(make sure all the below paths are changed based on your Python Home and other parameters and all the variables are configured with none missed).

**NOTE:** step 4 (create python venv) should be executed only after &quot;fresh&quot; login, where .profile from step 3 will be auto-executed.

e.g.

```
export PATH=$HOME/bin:/rsusr/pyz/bin:$PATH
export LIBPATH=$HOME/lib:/rsusr/pyz/lib:$PATH
export STEPLIB=RSREE.DSN.VC10.SDSNLOAD
export STEPLIB=RSREE.DSN.VC10.SDSNLOD2:$STEPLIB
export STEPLIB=XXXX.SDSNEXIT:$STEPLIB
export IBM_DB_HOME=RSREE.DSN.VC10
export DSNAOINI=$HOME/odbc_XXXX.ini
. $HOME/ibm_python_venv/bin/activate

```

1. Make sure when python is installed, you validate the same by typing &quot;python3 -V&quot; and it should return 3.8.3 or greater.

1. Make sure &quot;pip&quot; is installed and enabled as part of Python installation and is working.
2. ODBC installed connects and works with the DB2 for z/OS on the same subsytem or Sysplex with details configured in &quot;.ini&quot; file. No additional setting has to be done or credentials needs to be given during connection creation in python program. e.g.

```

import ibm_db
conn = ibm_db.connect('','','')


```

_ **Installing Python driver for DB2 i.e. ibm\_db &amp; Running a validation Program** _

Now that the Python and ODBC is ready, for connecting to DB2 you need a DB2 Python driver which we are going to install.

Follow the below steps for the same:

1. Open Putty tool and enter the subsystem address and login using your TSO ID and PWD.
4. Type bash so that you will feel more comfortable working on unix environment i.e. (ibm\_python\_venv) bash-4.3$ prompt.
5. Download the ibm\_db source from GIT i.e. zODBC\_support branch of python-ibmdb located at [git@github.com:ibmdb/python-ibmdb.git](mailto:git@github.com:ibmdb/python-ibmdb.git).
6. For performing step-1 make sure you have executed the below steps i.e.
  1. Clone the project in your own github repo from the source repo.
  2. Generate SSH key for your Z/OS system by following below steps:
    1. run ssh-keygen.

More detailed description can be found here:

[https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/)

  1. Then go to /u/\&lt;uid\&gt;/.ssh and copy the public key from id\_rsa.pub to BitBucket settings (open github in your browser and go to your profile).
1. Now go to the home directory of your USS in putty i.e. /u/\&lt;TSOID\&gt; or simply type $HOME.
2. Run the git checkout command i.e. git clone -b zODBC\_Support [git@github.com:ibmdb/python-ibmdb.git](mailto:git@github.com:ibmdb/python-ibmdb.git)
3. Now make sure you have &quot;ibmdb\_test&quot; directory in your $HOME directory.
4. Once conformed, go to $HOME/ibmdb\_test/python-ibmdb/IBM\_DB/ibm\_db/ directory and run below command:

```
(ibm\_python\_venv) bash-4.3$ ./Install_z_ibm-db

```

This will create the ibm\_db(Python driver&#39;s **.so** i.e. object file egg in your Python Virtual Environment for future usage by Python to install the driver).

1. If you face any issues make sure you clean the existing setup by doing below steps:

1. Uninstall current package. pip3 uninstall ibm-db
 2. Cleanup build directories. python3 setup.py clean -a
 3. Do a fresh build. python3 setup.py build
 4. Do a fresh install python3 setup.py install
 5. Check places where you have &quot;old&quot; ibm\_db.so files: find ~ -name &quot;ibm\_db.so&quot;
 You should have only 2 files: one in build dir and one in site-packages dir.
 6. Execute test once more to see that error has gone.

1. Now assuming everything went fine. You can run a test program i.e. **odbc\_test.py** with below content to validate if the setup has been done perfectly i.e. (ibm\_python\_venv) bash-4.3$ python3 odbc\_test.py:

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