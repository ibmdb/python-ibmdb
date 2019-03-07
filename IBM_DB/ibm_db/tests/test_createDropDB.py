#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import os
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf(os.environ.get("CI", False), "Test fails in CI")
    # Fails with
    # [IBM][CLI Driver][DB2/LINUXX8664] SQL0001N  Binding or precompilation
    # did not complete successfully. SQLCODE=-1
    def test_createDropDB(self):
        obj = IbmDbTestFunctions()
        if ((obj.server.DBMS_NAME == "DB2") or (obj.server.DBMS_NAME[0:3] != "DB2")):
            raise unittest.SkipTest("createdb, dropdb not Supported")
        obj.assert_expect(self.run_test_createDropDB)

    def run_test_createDropDB(self):
        database = 'test001'
        conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (database, config.hostname, config.port, config.user, config.password)
        conn_str_attach = "attach=true;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (config.hostname, config.port, config.user, config.password) #for create db or drop db API it is nessesory that connection only attach to the DB server not to any existing database of DB server
        conn_attach = ibm_db.connect(conn_str_attach, '', '')

        if conn_attach:
            conn = False
            try:
                conn = ibm_db.connect(conn_str, '', '')
            except:
                pass

            if conn:
                ibm_db.close(conn)
                conn = False
                try:
                    ibm_db.dropdb(conn_attach, database)
                except:
                    print('Errors occurred during drop database')
            try:
                #create databse
                rc = ibm_db.createdb(conn_attach, database)
                if rc:
                    conn = ibm_db.connect(conn_str, '', '')
                    if conn:
                        print('database created sucessfully')
                        ibm_db.close(conn)
                        conn = False
                    else:
                        print('database is not created')
                else:
                    print('Errors occurred during create database')

                #drop databse
                rc = ibm_db.dropdb(conn_attach, database)
                if rc:
                    try:
                        conn = ibm_db.connect(conn_str, '', '')
                    except:
                        print('datbase droped sucessfully')
                    if conn:
                        print('Errors occurred during drop database')
                        ibm_db.close(conn)
                        conn = False
                else:
                    print('Errors occurred during delete database')

                #create database with codeset option
                rc = ibm_db.createdb(conn_attach, database, 'iso88591')
                if rc:
                    conn = ibm_db.connect(conn_str, '', '')
                    server_info = ibm_db.server_info( conn )
                    if conn and (server_info.DB_CODEPAGE == 819):
                        print('database with codeset created sucessfully')
                        ibm_db.close(conn)
                        conn = False
                    else:
                        print('database is not created')
                else:
                    print('Errors occurred during create database')

                #drop database
                rc = ibm_db.dropdb(conn_attach, database)
                if rc:
                    try:
                        conn = ibm_db.connect(conn_str, '', '')
                    except:
                        print('datbase droped sucessfully')
                    if conn:
                        print('Errors occurred during drop database')
                        ibm_db.close(conn)
                        conn = False
                else:
                    print('Errors occurred during drop database')
            except:
                print(ibm_db.conn_errormsg())
                pass
            ibm_db.close(conn_attach)
        else:
            print(ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#database created sucessfully
#datbase droped sucessfully
#database with codeset created sucessfully
#datbase droped sucessfully
