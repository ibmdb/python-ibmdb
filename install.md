_ **Installing IBM Python &amp; ODBC on Z/OS** _

Below steps were followed for the same:

1. Make sure that the susbystem where the Python &amp; ODBC is getting installed has the latest version of Z/OS i.e. v2.4 or later. There are known issues in Z/OS v2.3 C compiler which prevents the Python driver for Db2 to be installed smoothly.
2. Select the Db2 which you want to connect to via ODBC as the same needs to be configured as part of ODBC installation in &quot;odbc.ini&quot; file. e.g.
```
[COMMON]

MVSDEFAULTSSID=LDS8

CONNECTTYPE=2

APPLTRACE=0

APPLTRACEFILENAME=./odbctrace.txt

DIAGTRACE=0

[LDS8]

MVSATTACHTYPE=RRSAF

PLANNAME=DSNACLI

```

1. Create a shell profile (i.e. &quot;. profile&quot; file in your home environment) which includes environment variables, needed for python and DB2 ODBC(make sure all the below paths are changed based on your Python Home and other parameters and all the variables are configured with none missed).

**NOTE:** step 4 (create python venv) should be executed only after &quot;fresh&quot; login, where .profile from step 3 will be auto-executed.

e.g.

```
export PATH=$HOME/bin:/rsusr/pyz/bin:$PATH

export LIBPATH=$HOME/lib:/rsusr/pyz/lib:$PATH

export \_BPXK\_AUTOCVT=&#39;ON&#39;

export \_CEE\_RUNOPTS=&#39;FILETAG(AUTOCVT,AUTOTAG) POSIX(ON) XPLINK(ON)&#39;

export \_CC\_ASUFFIX=so

export \_C89\_ASUFFIX=so

export \_CXX\_ASUFFIX=so

export \_CC\_CCMODE=1

export \_C89\_CCMODE=1

export \_CXX\_CCMODE=1

export \_TAG\_REDIR\_ERR=txt

export \_TAG\_REDIR\_IN=txt

export \_TAG\_REDIR\_OUT=txt

export STEPLIB=RSRTE.DSN.VC10.SDSNLOAD

export STEPLIB=RSRTE.DSN.VC10.SDSNLOD2:$STEPLIB

export STEPLIB=LDS8.SDSNEXIT:$STEPLIB

export DSNAOINI=$HOME/odbc\_LDS8.ini

export TMPDIR=$HOME/tmp

export IBM\_DB\_HOME=RSRTE.DSN.VC10

. $HOME/ibm\_python\_venv/bin/activate

```

1. Create python virtual environment, to be able install packages into own local repository:

```

mkdir $HOME/ibm\_python\_venv

python3 -m venv $HOME/ibm\_python\_venv --system-site-packages

```

1. Make sure when python is installed, you validate the same by typing &quot;python3 -V&quot; and it should return 3.8.3.
2. Now there are some changes that needs to be done to **ccompiler.py** file under $PYTHON\_HOME/pyz/usr/lpp/IBM/cyp/v3r8/pyz/lib/python3.8/distutils i.e.

**NOTE: The following lines should be pythonized and put into setup.py so that user doesn&#39;t need to do the same manually.(Work In Progress.)**

```

if [[-d sdsnc.h]]; then

rm -rf sdsnc.h

fi

mkdir sdsnc.h

cp &quot;//&#39;DSN.VC10.SDSNC.H&#39;&quot; sdsnc.h

echo &quot;Please add sdsnc.h to your .gitignore file&quot;

for f in sdsnc.h/\*; do

chtag -t -c 1047 $f

mv $f $f.h

done

cp &quot;//&#39;DSN.VC10.SDSNMACS(DSNAO64C)&#39;&quot; dsnao64c

chtag -t -c 1047 dsnao64c

cat dsnao64c \

| dd conv=block cbs=80 \

\&gt; libdsnao64c.x

chtag -t -c 1047 libdsnao64c.x

cp -X &quot;//&#39;DSN.VB10.SDSNLOD2(DSNAO64C)&#39;&quot; libdsnao64c.so

echo &#39;Please add \*dsnao64c\* to your .gitignore file&#39;

```

1. Make sure &quot;pip&quot; is installed and enabled as part of Python installation and is working.
2. ODBC installed connects and works with the DB2 on the same susbsytem or Sysplex with details configured in &quot;.ini&quot; file. No additional setting has to be done or credentials needs to be given during connection creation in python program. e.g.

```

import ibm\_db

conn = ibm\_db.connect(&#39;&#39;,&#39;&#39;,&#39;&#39;)

```

_ **Installing Python driver for DB2 i.e. ibm\_db &amp; Running a validation Program** _

Now that the Python and ODBC is ready, for connecting to DB2 you need a DB2 Python driver which we are going to install.

Follow the below steps for the same:

1. Open Putty tool and enter the subsystem address and login using your TSO ID and PWD.
2. Make directory for Python Virtual Environment i.e. $mkdir $HOME/ibm\_python\_venv
3. Make sure that as soon as you login, you are in ibm\_python\_venv if you have already created $HOME/ibm\_python\_venv i.e. Python&#39;s virtual environment i.e. (ibm\_python\_venv)$ prompt else logoff and login post the directory creation. This will happen only when the &quot;.profile&quot; file is there in your $HOME directory. Make sure it doesn&#39;t collide with .bashrc file, so either merge the .profile and .bashrc or disable the .bashrc i.e. $mv .bashrc .bashrc\_temp
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

(ibm\_python\_venv) bash-4.3$ python3 setup.py install --home $HOME/ibm\_python\_venv/

This will create the ibm\_db(Python driver&#39;s **.so** i.e. object file egg in your Python Virtual Environment for future usage by Python to install the driver).

1. Or you can simply build i.e. (ibm\_python\_venv) bash-4.3$ python3 setup.py build --home $HOME/ibm\_python\_venv and later install the same using pip3 i.e. (ibm\_python\_venv) bash-4.3$ pip3 install
2. If you face any issues make sure you clean the existing setup by doing below steps:

1. Uninstall current package. pip3 uninstall ibm-db
 2. Cleanup build directories. python3 setup.py clean -a
 3. Do a fresh build. python3 setup.py build
 4. Do a fresh install python3 setup.py install
 5. Check places where you have &quot;old&quot; ibm\_db.so files: find ~ -name &quot;ibm\_db.so&quot;
 You should have only 2 files: one in build dir and one in site-packages dir.
 6. Execute test once more to see that error has gone.

1. Now assuming everything went fine. You can run a test program i.e. **odbc\_test.py** with below content to validate if the setup has been done perfectly i.e. (ibm\_python\_venv) bash-4.3$ python3 odbc\_test.py:

```

from \_\_future\_\_ import print\_function

import sys

import ibm\_db

print(&#39;ODBC Test start&#39;)

conn = ibm\_db.connect(&#39;&#39;,&#39;&#39;,&#39;&#39;)

if conn:

stmt = ibm\_db.exec\_immediate(conn,&quot;SELECT CURRENT DATE FROM SYSIBM.SYSDUMMY1&quot;)

if stmt:

while (ibm\_db.fetch\_row(stmt)):

date = ibm\_db.result(stmt, 0)

print(&quot;Current date is :&quot;,date)

else:

print(ibm\_db.stmt\_errormsg())

ibm\_db.close(conn)

else:

print(&quot;No connection:&quot;, ibm\_db.conn\_errormsg())

print(&#39;ODBC Test end&#39;)

```