```
Please note that on z/OS, you can only have one active connection per thread.

### for me ###

cd /u/pdharr/git/python-ibmdb/IBM_DB/ibm_db
export IBM_DB_HOME='DSN.VC10'
python setup.py build
python setup.py install

### for others ###

conda install ibm-db --channel ODSP-TEST/labels/test

### ###

export IBM_DB_HOME='DSN.VC10'
export SUBSYSTEM=LC1A
export STEPLIB=$SUBSYSTEM.SDSNEXIT:$IBM_DB_HOME.SDSNLOD2:$IBM_DB_HOME.SDSNLOAD

# I checked that DSNACLI is in SYSIBM.SYSPLAN on LC1A

cd ibm_db_tests

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
chtag -r $DSNAOINI # we have to remove the tag, so that ODBC can read it, since python's program ccsid is ascii



# A simple test of connecting to DB2
python -c "import ibm_db; conn = ibm_db.connect('DSN=$HOSTNAME$SUBSYSTEM', None, None); print('connection=%r' % conn);"

# To run all the tests except for the ones that cause problems for the other tests:
python tests.py

# To run the tests that cause problems:
./run_single_tests


# Also, we will need to run some or all of the tests using MVSATTACHTYPE=RRSAF, which requires usernames and passwords
# I suggest a file ~/.password, with "chmod 600 ~/.password", and a config.py that sets the password based on this file.

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
chtag -r $DSNAOINI # we have to remove the tag, so that ODBC can read it, since python's program ccsid is ascii

```
