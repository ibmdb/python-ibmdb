# Installatin steps for python ibm_db driver

_Copyright (c) 2023 IBM Corporation and/or its affiliates. All rights reserved._

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

1. [ibm_db Installation on Linux, AIX, zLinux, Widnows and MacOS.](#inslnx)
2. [ibm_db Installation on z/OS](#inszos)
3. [ibm_db installation on MacOS M1/M2 Chip System](#m1chip)
4. [Troubleshooting Post Install Errors on MacOS](#troubleshooting)
   - [SQL30081N Error](#41-sql30081n-error)
   - [Symbol not found error or malloc error](#42-symbol-not-found-error-or-malloc-error)

## <a name="inslnx"></a> 1. python-ibmdb Installation on Linux, AIX, zLinux, Windows and MacOS.

### Install python-ibmdb

Below are the steps to install [_python-ibmdb_](https://github.com/ibmdb/python-ibmdb) from github or pip.

#### 1.1 Direct Installation using pip.

To install ibm_db and ibm_db_dbi module.

```
pip install ibm_db
```

or

```
pip install git+https://git@github.com/ibmdb/python-ibmdb.git
```

- `pip install ibm_db` installs python wheel images on Linux, Windows and MacOS(x64) for python v>=3.7
- MacOS(arm64) support python wheel images from python version 3.9 onwards.
- If wheel image is not available or for AIX and zLiux, native C++ code of ibm_db requires in-system compilation. For such case,
  you should have a C++ compiler installed in the system. Make sure the commands `gcc --version` and `make --version` works
  fine on Linux and MacOS system.
- For AIX and zLinux, you should have xLC Compiler intalled in the system. Also, `make` should be installed.
- For other pre-requisite and non-wheel installation, please check [here](https://github.com/ibmdb/python-ibmdb?tab=readme-ov-file#installation).

**Note:**
When we install ibm_db package on Linux, MacOS and Windows, `pip install ibm_db` command install
prebuilt Wheel package that includes clidriver too and ignores `IBM_DB_HOME` or `IBM_DB_INSTALLER_URL`
environment variables if set. Also, auto downloading of clidriver does not happen as clidriver is
already present inside wheel package.

To inforce auto downloading of clidriver or to make setting of environment variable `IBM_DB_HOME`
effective, install ibm_db from source distribution using below command:

```
pip install ibm_db --no-binary :all: --no-cache-dir
```

If you have to use your own URL for clidriver.tar.gz/.zip please set environment variable

```
IBM_DB_INSTALLER_URL=full_path_of_clidriver.tar.gz/.zip
```

When ibm_db get installed from wheel package, you can find clidriver under site_packages directory
of Python. You need to copy license file under `site_packages/clidriver/license` to be effective, if any.

**Note:** For windows after installing ibm_db, recieves the below error when we try to import ibm_db :

```>python
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import ibm_db
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: DLL load failed while importing ibm_db: The specified module could not be found.
>>>
```

We need to make sure to set dll path of dependent library of clidriver before importing the module as:

```
import os
os.add_dll_directory('path to clidriver installation until bin')
import ibm_db

e.g:
os.add_dll_directory('C:\\Program Files\\IBM\\CLIDRIVER\\bin')
import ibm_db
```

Refer https://bugs.python.org/issue36085 for more details.

#### 1.2 Manual Installation

```
git clone https://github.com/ibmdb/python-ibmdb/
cd python-ibmdb
python -m build
pip install dist/ibm_db-3.2.8-cp313-cp313-win_amd64.whl
pip list
```

- You can find .whl file under dist directory after `python -m build` command.
- `pip install dist/ibm_db-3.2.8-cp313-cp313-win_amd64.whl` command, installs `ibm_db` under site_packages.

#### 1.3 Manual Installation by using setup.py and .egg file [not recommended]

```
git clone https://github.com/ibmdb/python-ibmdb/
cd python-ibmdb
python setup.py bdist_egg => It generates egg file under dist directory.
python setup.py install
pip list
```

- `python setup.py install` command, installs python egg under site_packages.
- `python setup.py bdist_wheel` command generates .whl file under dist directory.
- `python setup.py bdist_egg bdist_wheel` command generates both .egg file and .whl file under dist directory.
- If you are still using .egg file for installation, please move using .whl file for installation. setuptools has removed easy_install that was used to install .egg file: https://github.com/pypa/setuptools/issues/917
- Details about .whl vs .egg is discussed here: https://packaging.python.org/en/latest/discussions/package-formats/

#### 1.4 Manual Installation using python wheel (Only Linux, Windows and MacOS)

To install ibm_db as python wheel, use below commands(recommended):

```
git clone https://github.com/ibmdb/python-ibmdb/
cd python-ibmdb
python -m build  => Note down the path of generated *.whl file to use below
pip install dist/ibm_db-3.2.8-cp313-cp313-win_amd64.whl
pip list  => You can see ibm_db in the output
```

## <a name="inszos"></a> 2. ibm_db Installation on z/OS

### 2.1 Install Python for z/OS

Below steps were followed for the same:

1. Tested under below:

```
-- zODBC(64 bit) installed with z/OS 2.3
-- IBM Python 3.13.0 64 bit
-- Install the below PTFs(If not installed):
    -- UI72588 (v11)
    -- UI72589 (v12)
```

### 2.2 Configure ODBC driver on z/OS

Please refer to the [ODBC Guide and References](https://www.ibm.com/support/knowledgecenter/SSEPEK/pdf/db2z_12_odbcbook.pdf) cookbook for how to configure your ODBC driver. Specifically, you need to ensure you have:

1.  Binded the ODBC packages. A sample JCL is provided in the `SDSNSAMP` dataset in member `DSNTIJCL`. Customize the JCL with specifics to your system.

2.  Ensure users that should be authorized have authority to execute the DSNACLI plan. Included are samples granting authority to public (all users), or specific groups via SQL GRANT statements, or alternately via RACF. The security administrator can use these samples as a model and customize/translate to your installation security standards as appropriate.

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

3.  Set the `IBM_DB_HOME` environment variable to the High Level Qualifier (HLQ) of your Db2 datasets. For example, if your Db2 datasets are located as `DSNC10.SDSNC.H` and `DSNC10.SDSNMACS`, you need to set `IBM_DB_HOME` environment variable to `DSNC10` with the following statement (can be saved in `~/.profile`):

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

### 2.3 Verify python installation

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

### 2.4 Installing Python driver for Db2 i.e. ibm_db &amp; Running a validation Program

Now that the Python and ODBC is ready, for connecting to Db2 you need a Db2 Python driver which we are going to install.

Follow the standard steps for the same i.e. pip3 install ibm_db

### 2.5 Install python-ibmdb

#### 2.5.1 Install ibm_db from IBM Python AI Toolkit for z/OS

IBM provides a precompiled version of ibm_db as part of IBM Python AI Toolkit for z/OS, see https://ibm-z-oss-oda.github.io/python_ai_toolkit_zos/.

Install command:

```
pip3 install --index-url https://downloads.pyaitoolkit.ibm.net/repository/python_ai_toolkit_zos/simple --trusted-host downloads.pyaitoolkit.ibm.net --only-binary :all: ibm_db
```

#### 2.5.2 Direct Installation: Using pip from pypi or github

```
pip install ibm_db
```

or

```
pip install --no-build-isolation ibm_db
```

or

```
pip install git+https://git@github.com/ibmdb/python-ibmdb.git
```

In case you encounter the following error during the installation process:

```
error: command '/usr/lpp/IBM/oelcpp/v2r0/bin/clang' failed: EDC5129I No such file or directory.
```

This issue may arise due to the absence of the required clang compiler. To resolve this, you can use the following alternative commands:

```
CC="ibm-clang64" pip install ibm_db
```

or

```
CC="ibm-clang64" pip install --no-build-isolation ibm_db
```

#### 2.5.3 Manual Installation by using git clone.

Before starting the manual installation, ensure you have the latest versions of the required modules installed. Run the following command to install them:

```
pip install setuptools build wheel
```

Next, clone the python-ibmdb repository from GitHub:

```
git clone https://github.com/ibmdb/python-ibmdb.git
```

After cloning the repository, navigate to the python-ibmdb directory and tag all the files with the ASCII tag:

```
cd python-ibmdb
chtag -Rtc 819 .
```

Now, you can build the package using the following command:

```
python -m build
```

In case you encounter the following error during the installation process:

```
error: command '/usr/lpp/IBM/oelcpp/v2r0/bin/clang' failed: EDC5129I No such file or directory.
```

This issue occurs due to the absence of the required clang compiler. To resolve it, use the following alternative command to build the package with the ibm-clang64 compiler:

```
CC="ibm-clang64" python -m build
```

After building the package, navigate to the dist directory where the .whl file is generated:

```
cd dist
```

Now, install the .whl file (the wheel file) using pip. Replace nameofwheelfile.whl with the actual name of the wheel file generated:

```
pip install nameofwheelfile.whl

for example:
pip install ibm_db-3.2.5-cp313-cp313-os390_29_00_3931.whl
```

Finally, verify that the installation was successful by running:

```
pip list
```

This will show the installed packages, and you should see ibm_db listed among them.

Now assuming everything went fine. You can run a test program i.e. **odbc_test.py** with below content to validate if the setup has been done perfectly i.e. bash-4.3$ python3 odbc_test.py:

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

#### Troubleshooting

**Important:** When working with `ibm_db` or `ibm_db_dbi` on z/OS environments such as USS and BPXBATCH, always use the provided APIs — `conn_errormsg()`, `conn_error()`, `stmt_errormsg()`, `stmt_error()`, and `get_sqlcode()` — to retrieve error messages, SQLSTATE and SQLCODE values for connection or statement failures.
Avoid using direct `print()` statements or relying on raw exception output, as this may result in missing or unreadable error messages, or `UnicodeDecodeError` due to encoding limitations on these platforms.
These APIs ensure consistent and reliable error handling across all supported environments.

## <a name="m1chip"></a> 3. ibm_db installation on MacOS M1/M2 Chip System (arm64 architecture)

\*\*Important:

> ibm_db@3.2.5 onwards supports native installation on MacOS ARM64(M\* Chip/Apple Silicon Chip) system using clidriver/dsdriver version 12.1.0.
> You need **db2connect v12.1 license** to connect to z/OS or iSeries server from M1 Chip system.

### Installation:

    Follow same steps as documented for [ibm_db Installation on Linux, AIX, zLinux, Widnows and MacOS.](#inslnx)

## <a name="troubleshooting"></a> 4. Troubleshooting Post Install Errors on MacOS

### 4.1 SQL30081N Error

- If connection fails with SQL30081N error: means `ibm_db` installation is correct and you need to provide correct connection string.

### 4.2 Symbol not found error or malloc error

- If `import ibm_db` fails with `Symbol not found: ___cxa_throw_bad_array_new_length` error or `malloc` error:
  You need to find the correct location of lib/gcc/12 directory and add it to DYLD_LIBRARY_PATH environment variable.
  Also, execute below commands from terminal with correct location of `lib/gcc/12/libstdc++.6.dylib` library.
  ```
  cd ..../site_packages/clidriverd/lib
  install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib <full path of libstdc++.6.dylib> libdb2.dylib
  f.e.
  install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib /usr/local/homebrew/lib/gcc/12/libstdc++.6.dylib libdb2.dylib
  ```
- Suppose, you have installed gcc v13.1.0 and libstdc++ is available under `/usr/local/Homebrew/Cellar/gcc/13.1.0/lib/gcc/13`, then you need to run below two commands from terminal to fix this issue:

```
cd  .../lib/python3.11/site-packages/clidriver/lib
install_name_tool -change /usr/local/lib/gcc/8/libstdc++.6.dylib /usr/local/Homebrew/Cellar/gcc/13.1.0/lib/gcc/13/libstdc++.6.dylib libdb2.dylib
```

i.e. change current path of `libstdc++.6.dylib` in `libdb2.dylib` library to the corrent path in your system. You can find the path of `libstdc++.6.dylib` in libdb2.dylib using the command : `otool -L libdb2.dylib`. Once you have the path of libstdc++.6.dylib, you need to change it using the commond: `install_name_tool -change <current path in libdb2.dylib>  <actual path in your system>  libdb2.dylib`
Now run your test program and verify.
