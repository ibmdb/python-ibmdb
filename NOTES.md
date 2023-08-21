## Notes

Please note that on z/OS, you can only have one active connection per thread.

## Installation from source code
```shell 
cd /u/pdharr/git/python-ibmdb
export IBM_DB_HOME='DSN.VC10'
python setup.py install
```

## Installation from Conda
```shell
conda install ibm-db --channel ODSP-TEST/labels/test
```

## Important environment variables to set before running Python Programs on z/OS
```
export IBM_DB_HOME='DSN.VC10'
export SUBSYSTEM=<SSID>
export STEPLIB=$SUBSYSTEM.SDSNEXIT:$IBM_DB_HOME.SDSNLOD2:$IBM_DB_HOME.SDSNLOAD
```

## Setting the ODBC INI File
 
DSNACLI is in SYSIBM.SYSPLAN on <SSID>

```shell
export DSNAOINI="$HOME/ODBC_${HOSTNAME}_${SUBSYSTEM}_CAF"

touch $DSNAOINI
chtag -t -c 1047 $DSNAOINI
cat <<EOF >$DSNAOINI
[COMMON]
MVSDEFAULTSSID=$SUBSYSTEM
CURRENTAPPENSCH=UNICODE
FLOAT=IEEE
[$SUBSYSTEM]
MVSATTACHTYPE=CAF
PLANNAME=DSNACLI
[$HOSTNAME$SUBSYSTEM]
AUTOCOMMIT=1
EOF
chtag -b $DSNAOINI # we have to tag as binary, so that ODBC can read it, since python's program ccsid is ascii

```

## A simple test for connecting to Db2

Running the sample code to test basic connection.

```python
import ibm_db
conn = ibm_db.connect('DSN=$HOSTNAME$SUBSYSTEM', None, None)
print('info=%r' % ibm_db.server_info(conn))
```

## TESTING

Before running the test suite make sure to perform the following

- rename the config.py.sample to config.py
- Replace the following in run_all_tests
```
export IBM_DB_HOME='XXXX.DSN'
export SUBSYSTEM=<SSID> # SSID if the zos machine
```

### To run single test case:

```shell
./run_individual_tests
```

### To run all the tests, with different settings:
```shell
./run_all_tests
```


Also, we will need to run some or all of the tests using MVSATTACHTYPE=RRSAF, which requires usernames and passwords
I suggest a file ~/.password, with "chmod 600 ~/.password", and a config.py that sets the password based on this file.

```
export DSNAOINI="$HOME/ODBC_${HOSTNAME}_${SUBSYSTEM}_RRSAF"
touch $DSNAOINI
chtag -t -c 1047 $DSNAOINI
cat <<EOF >$DSNAOINI
[COMMON]
MVSDEFAULTSSID=$SUBSYSTEM
FLOAT=IEEE
[$SUBSYSTEM]
MVSATTACHTYPE=RRSAF
PLANNAME=DSNACLI
[$HOSTNAME$SUBSYSTEM]
AUTOCOMMIT=1
EOF
chtag -b $DSNAOINI # we have to tag as binary, so that ODBC can read it, since python's program ccsid is ascii
```


## DEPRECATED API FOR ZOS

|API NAME      |Architecture    |Supported     |
| :---:        |  :---:         |  :---:       |
|execute_many  |  zos           |  No          |
|SQL_ATTR_CHANNING_BEING| ZOS   |  No          |
|SQL_ATTR_CHANNING_END  | ZOS   |  No          |
