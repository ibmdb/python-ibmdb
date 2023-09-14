# Installatin steps for python ibm_db driver

*Copyright (c) 2023 IBM Corporation and/or its affiliates. All rights reserved.*

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

## Contents

1. [ibm_db Installation on Linux](#inslnx)
2. [ibm_db Installation on AIX on Power Systems](#insaix_p)
3. [ibm_db Installation on Linux on System z](#inslnx_z)
4. [ibm_db Installation on Windows](#inswin)
5. [ibm_db Installation on MacOS](#insmac)
6. [ibm_db Installation on z/OS](#inszos)
7. [ibm_db installation on MacOS M1/M2 Chip System](#m1chip)
8. [Troubleshooting Post Install Errors](#troubleshooting)
 -  [SQL30081N Error](#sql30081n)
 -  [Symbol not found error or malloc error](#symbolerror)


## <a name="inslnx"></a> 1. Python-ibm_db Installation on Linux.

### Install python-ibm_db

Below are the steps to install [*python-ibm_db*](https://github.com/ibmdb/python-ibm_db) from github or pip.

#### 1.1 Direct Installation.
```
pip install ibm_db
```
or
```
pip install git+https://git@github.com/ibmdb/python-ibm_db.git
```

#### 1.2 Manual Installation by using git clone.

```
git clone https://github.com/ibmdb/python-ibm_db/
cd python-ibmdb
python setup.py build
python setup.py install
````

## <a name="insaix_p"></a> 2. Python-ibm_db Installation on AIX on Power Systems.

### 2.1 Install python-ibm_db

Follow the same steps mentioned in [Python-ibm_db Installation on Linux](#inslnx).


## <a name="inslnx_z"></a> 3. Python-ibm_db Installation on Linux on System z.

### 3.1 Install python-ibm_db

Follow the same steps mentioned in [Python-ibm_db Installation on Linux](#inslnx).


## <a name="inswin"></a> 4. Python-ibm_db Installation on Windows.

Below are the steps to install [*python-ibm_db*](https://github.com/ibmdb/python-ibm_db) from github or pip.

#### 4.1 Direct Installation.
```
pip install ibm_db
```
or
```
pip install git+https://github.com/ibmdb/python-ibmdb.git
```

#### 4.2 Manual Installation by using git clone.

```
git clone https://github.com/ibmdb/python-ibm_db/
cd python-ibmdb
python setup.py build
python setup.py install
````

## <a name="insmac"></a> 5. Python-ibm_db Installation on MacOS.

### 5.1 Install python-ibm_db

Follow the same steps mentioned in [python-ibm_db Installation on Linux](#inslnx).

## <a name="inszos"></a> 6. ibm_db Installation on z/OS

### 6.1 Install Python for z/OS

Below steps were followed for the same:

1. Tested under below:
```
-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.11.3 64 bit
-- Install the below PTFs(If not installed):
    -- UI72588 (v11)
    -- UI72589 (v12)
```

### 6.2 Configure ODBC driver on z/OS
Please refer to the [ODBC Guide and References](https://www.ibm.com/support/knowledgecenter/SSEPEK/pdf/db2z_12_odbcbook.pdf) cookbook for how to configure your ODBC driver. Specifically, you need to ensure you have:

1. Binded the ODBC packages.  A sample JCL is provided in the `SDSNSAMP` dataset in member `DSNTIJCL`.  Customize the JCL with specifics to your system.

2. Ensure users that should be authorized have authority to execute the DSNACLI plan.  Included are samples granting authority to public (all users), or specific groups via SQL GRANT statements, or alternately via RACF.  The security administrator can use these samples as a model and customize/translate to your installation security standards as appropriate.

    **Examples using SQL GRANT statement**:

    _Example 1:_ Grant the privilege to execute plan DSNACLI to RACF group, DBCLIGRP.

        GRANT EXECUTE ON PLAN DSNACLI TO DBCLIGRP;

    _Example 2:_ Grant the privilege to execute plan DSNACLI to all users at the current server.

        GRANT EXECUTE ON PLAN DSNACLI TO PUBLIC;

    **Examples using Access Control Authorization Exit for Db2 authorization**:

    Define profile for plan DSNACLI execute privilege check

        RDEFINE MDSNPN DB2A.DSNACLI.EXECUTE UACC(NONE) OWNER(DB2OWNER)

    _Example 1:_ PERMIT the privilege to execute plan DSNACLI to RACF group, DBCLIGRP

        PERMIT DB2A.DSNACLI.EXECUTE ID(DBCLIGRP) ACCESS(READ) CLASS(MDSNPN)

    _Example 2:_ PERMIT the privilege to execute plan DSNACLI to all users at the current server

        PERMIT DB2A.DSNACLI.EXECUTE ID(*) ACCESS(READ) CLASS(MDSNPN)

    Issue SETROPTS command to refresh in-storage profile lists

         SETR RACLIST(MDSNPN) REFRESH

3. Set the `IBM_DB_HOME` environment variable to the High Level Qualifier (HLQ) of your Db2 datasets.  For example, if your Db2 datasets are located as `DSNC10.SDSNC.H` and `DSNC10.SDSNMACS`, you need to set `IBM_DB_HOME` environment variable to `DSNC10` with the following statement (can be saved in `~/.profile`):

- NOTE(Default behaviour): 
	- IBM_DB_HOME is the HLQ for your Db2 libraries(SDSNMACS, SDSNC.H)

    ```sh
    # Set HLQ to Db2 datasets.
    export IBM_DB_HOME="DSNC10"
    ```

4. Update the `STEPLIB` environment variable to include the Db2 SDSNEXIT, SDSNLOAD and SDSNLOD2 data sets. You can set the `STEPLIB` environment variable with the following statement, after defining `IBM_DB_HOME` to the high level qualifier of your Db2 datasets as instructed above:

    ```sh
    # Assumes IBM_DB_HOME specifies the HLQ of the Db2 datasets.
    export STEPLIB=$STEPLIB:$IBM_DB_HOME.SDSNEXIT:$IBM_DB_HOME.SDSNLOAD:$IBM_DB_HOME.SDSNLOD2
    ```
5. Configure below environment variables for install/compilation or create a shell profile (i.e. &quot;. profile&quot; file in your home environment) which includes environment variables, needed for Python and Db2 for z/OS ODBC(make sure all the below paths are changed based on your system and DB setting and all the variables are configured with none missed).

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

6. In case you have data Set named anything other than SDSNC.H i.e. non default behaviour, you need to configure following variable. IGNORE OTHERWISE.
```shell
export DB2_INC=$IBM_DB_HOME.XXXX.H
```

7. In case you have SDSNMACS data Set named anything other than SDSNMACS i.e. non default behaviour, you need to configure following variable. IGNORE OTHERWISE.
```shell
export DB2_MACS=$IBM_DB_HOME.XXXX
```
8. Configured an appropriate _Db2 ODBC initialization file_ that can be read at application time. You can specify the file by using either a DSNAOINI data definition statement or by defining a `DSNAOINI` z/OS UNIX environment variable.

 - For compatibility with ibm_db, the following properties must be set:

    In COMMON section:

    ```
    MULTICONTEXT=2
    CURRENTAPPENSCH=ASCII
    FLOAT=IEEE
    ```

    In SUBSYSTEM section:

    ```
    MVSATTACHTYPE=RRSAF
    ```

    Here is a sample of a complete initialization file:

    ```
    ; This is a comment line...
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

9. The odbc.ini file must be encoded in IBM-1047 and cannot have the "text" tag on. Use chtag -p $DSNAOINI to verify that the file have T=off (text tag off) and is either tagged "binary" or mixed IBM-1047.
    ```
    chtag -b $DSNAOINI
    or
    chtag -m -c IBM-1047 $DSNAOINI
    ```
    If file is tagged text (chtag -t -c IBM1047 $DSNAOINI) the S0C4 abend occurs.

Reference Chapter 3 in the [ODBC Guide and References](https://www.ibm.com/support/knowledgecenter/SSEPEK/pdf/db2z_12_odbcbook.pdf) for more instructions.

### 6.3 Verify python installation
1. Make sure when python is installed, you validate the same by typing &quot;python3 -V&quot; and it should return 3.8.3 or greater.
- Unless you are a sysprog you'll likely not have authority to create the site-package so consider using a python virtual environment as following:
```
python3 -m venv $HOME/ibm_python_venv
source $HOME/ibm_python_venv/bin/activate
```

2. Make sure &quot;pip3&quot; is installed and enabled as part of Python installation and is working.

3. Make sure the installed ODBC connects and works with the Db2 for z/OS on the same subsytem or Sysplex with details configured in &quot;.ini&quot; file. No additional setting has to be done or credentials needs to be given during connection creation in python program using ibm_db after installation. e.g.

```python
import ibm_db
conn = ibm_db.connect('','','')
```

### 6.4 Installing Python driver for Db2 i.e. ibm\_db &amp; Running a validation Program

Now that the Python and ODBC is ready, for connecting to Db2 you need a Db2 Python driver which we are going to install.

Follow the standard steps for the same i.e. pip3 install ibm_db

### 6.5 Install python-ibm_db

Below are the steps to install [*python-ibm_db*](https://github.com/ibmdb/python-ibm_db) from github or pip.

#### 6.5.1 Direct Installation.
```
pip install ibm_db
```
or
```
pip install git+https://git@github.com/ibmdb/python-ibm_db.git
```

#### 6.5.2 Manual Installation by using git clone.

```
git clone https://github.com/ibmdb/python-ibm_db/
cd python-ibmdb
python setup.py build
python setup.py install
````

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

## <a name="m1chip"></a> 7. ibm_db installation on MacOS M1/M2 Chip System (arm64 architecture)

### 7.1 Install GCC using Homebrew

**Warning:** If you use the ARM version of homebrew (as recommended for M1/M2 chip systems) you will get the following error message:
```
$ brew install gcc-12
Error: Cannot install in Homebrew on ARM processor in Intel default prefix (/usr/local)!
Please create a new installation in /opt/homebrew using one of the
"Alternative Installs" from:
  https://docs.brew.sh/Installation
You can migrate your previously installed formula list with:
  brew bundle dump
```
Install `gcc@12` using homebrew `(note: the x86_64 version of homebrew is needed for this, not the recommended ARM based homebrew)`. The clearest instructions on how to install and use the `x86_64` version of `homebrew` is by following below steps:
*	My arm64/M1 brew is installed here:
```
	$ which brew
	/opt/homebrew/bin/brew
```
*	Step 1. Install x86_64 brew under /usr/local/bin/brew
	`arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
*	Step 2. Create an alias for the x86_64 brew
	I added this to my ~/.bashrc as below:
```
	# brew hack for x86_64
	alias brew64='arch -x86_64 /usr/local/bin/brew'
```
* Then install gcc@12 using the x86_64 homebrew:
```
	brew64 install gcc@12
```
* Now find location of `lib/gcc/12/libstdc++.6.dylib` file in your system. It should be inside `/usr/local/homebrew/lib/gcc/12` or `/usr/local/lib/gcc/12` or `/usr/local/homebrew/Cellar/gcc@12/12.2.0/lib/gcc/12` or something similar. You need to find the correct path.
Suppose path of gcc lib is `/usr/local/homebrew/lib/gcc/12`. Then update your .bashrc/.zshrc file with below line
```
export DYLD_LIBRARY_PATH=/usr/local/homebrew/lib/gcc/12:$DYLD_LIBRARY_PATH
```

### 7.2 Steps to Install Intel Python after verifying setup

Several things might be necessary to get `ibm_db` working on the Apple Silicon architecture:

1. Open new terminal and run command `arch -x86_64 /bin/bash    or arch -x86_64 /bin/zsh`.

2. Verify the output of  `gcc -v` command. It should show `Target: x86_64-apple-darwin21` in output.

3. Install Intel/x64 version of python for `ibm_db` as `ibm_db` do not work with `arm64` version of python. Example, you may install [this version](https://www.python.org/ftp/python/3.9.11/python-3.9.11-macosx10.9.pkg) of python on M1 Chip system and then install `ibm_db`.

4. When using pyenv to manage your Python installations, make sure you have pyenv installed as x86-compatible and run it in x86 mode (ie prepending all your command with `arch -x86_64`). If you are using Homebrew to install `pyenv`, Homebrew will itself also have to be installed as x86-compatible:

   ```bash
   # If you are using Homebrew to manage your pyenv installation, make sure Homebrew is installed as x86-compatible
   arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   # Make sure you are using Homebrew's x86-compatible version (especially important if you have installed Homebrew for Apple Silicon as well)
   eval "$(/usr/local/bin/brew shellenv)"
   arch -x86_64 brew install pyenv
   # Any time we want to use pyenv, we should first run `eval "$(/usr/local/bin/brew shellenv)"`
   arch -x86_64 pyenv install <YOUR_PYTHON_VERSION>
   ```

5. Check output of commands `python --version` , `which python` and `file /usr/local/bin/python` commands. It should show `/usr/local/bin/python: Mach-O 64-bit executable x86_64`

6. When regular installation does not work, it might help to preface your installation command with `ARCHFLAGS="-arch x86_64"`. Be sure to have uninstalled `ibm_db` before installing again, otherwise this fix won't help.

7. You might need zlib, openssl, pip installations if not already available in your setup.

* Open new terminal and run command `arch -x86_64 /bin/bash    or arch -x86_64 /bin/zsh`.
*  Verify the output of  `gcc -v` command. It should show `Target: x86_64-apple-darwin21` in output.
* Install Intel Version of Python like: https://www.python.org/ftp/python/3.9.11/python-3.9.11-macosx10.9.pkg

### 7.3 Install ibm_db with x86_64 version of gcc12 and Python on M1/M2 Chip System

* Open a new terminal and run below commands:
```
gcc -v   => Output should have x86_64
python --version   or python3 --version
file `which python` or file `which python3`   => Output should have x86_64
pip3 install ibm_db
```
Now, run your test program to verify.

## <a name="troubleshooting"></a> 8. Troubleshooting Post Install Errors

<a name="sql30081n"></a> 8.1 SQL30081N Error

* If connection fails with SQL30081N error: means `ibm_db` installation is correct and you need to provide correct connection string.

<a name="symbolerror"></a> 8.2 Symbol not found error or malloc error

* If `import ibm_db` fails with `Symbol not found: ___cxa_throw_bad_array_new_length` error or `malloc` error:
  You need to find the correct location of lib/gcc/12 directory and add it to DYLD_LIBRARY_PATH environment variable.
  Also, execute below commands from terminal with correct location of `lib/gcc/12/libstdc++.6.dylib` library.
  ```
  cd ..../site_packages/clidriverd/lib
  install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib <full path of libstdc++.6.dylib> libdb2.dylib
  f.e.
  install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib /usr/local/homebrew/lib/gcc/12/libstdc++.6.dylib libdb2.dylib
  ```
* Suppose, you have installed gcc v13.1.0 and libstdc++ is available under `/usr/local/Homebrew/Cellar/gcc/13.1.0/lib/gcc/13`, then you need to run below two commands from terminal to fix this issue:
```
cd  .../lib/python3.11/site-packages/clidriver/lib
install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib /usr/local/Homebrew/Cellar/gcc/13.1.0/lib/gcc/13/libstdc++.6.dylib libdb2.dylib
```
i.e. change current path of `libstdc++.6.dylib` in `libdb2.dylib` library to the corrent path in your system. You can find the path of `libstdc++.6.dylib` in libdb2.dylib using the command : `otool -L libdb2.dylib`. Once you have the path of libstdc++.6.dylib, you need to change it using the commond: `install_name_tool -change <current path in libdb2.dylib>  <actual path in your system>  libdb2.dylib`

Now run your test program and verify.

