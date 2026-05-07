from __future__ import print_function
import asyncio
import sys
import os
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf(os.environ.get("CI", False), "Test fails in CI")
    def test_25_async_createdb_dropdb(self):
        obj = IbmDbTestFunctions()
        if ((obj.server.DBMS_NAME == "DB2") or (obj.server.DBMS_NAME[0:3] != "DB2")):
            raise unittest.SkipTest("createdb, dropdb not Supported")
        obj.assert_expect(self.run_test_25)

    def run_test_25(self):
        async def main():
            database = 'test001'
            conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (database, config.hostname, config.port, config.user, config.password)
            dsn_attach = "attach=true;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;" % (config.hostname, config.port)

            # Clean up if test database already exists
            conn = None
            try:
                conn = ibm_db.connect(conn_str, '', '')
            except:
                pass
            if conn:
                ibm_db.close(conn)
                conn = None
                try:
                    await ibm_db_dbi.dropdb_async(database, dsn_attach, config.user, config.password)
                except:
                    print('Errors occurred during drop database')

            try:
                # create database
                rc = await ibm_db_dbi.createdb_async(database, dsn_attach, config.user, config.password)
                if rc:
                    conn = ibm_db.connect(conn_str, '', '')
                    if conn:
                        print('database created sucessfully')
                        ibm_db.close(conn)
                        conn = None
                    else:
                        print('database is not created')
                else:
                    print('Errors occurred during create database')

                # drop database
                rc = await ibm_db_dbi.dropdb_async(database, dsn_attach, config.user, config.password)
                if rc:
                    try:
                        conn = ibm_db.connect(conn_str, '', '')
                    except:
                        print('datbase droped sucessfully')
                    if conn:
                        print('Errors occurred during drop database')
                        ibm_db.close(conn)
                        conn = None
                else:
                    print('Errors occurred during delete database')

                # create database with codeset option
                rc = await ibm_db_dbi.createdb_async(database, dsn_attach, config.user, config.password, codeset='iso88591')
                if rc:
                    conn = ibm_db.connect(conn_str, '', '')
                    server_info = ibm_db.server_info(conn)
                    if conn and (server_info.DB_CODEPAGE == 819):
                        print('database with codeset created sucessfully')
                        ibm_db.close(conn)
                        conn = None
                    else:
                        print('database is not created')
                else:
                    print('Errors occurred during create database')

                # drop database
                rc = await ibm_db_dbi.dropdb_async(database, dsn_attach, config.user, config.password)
                if rc:
                    try:
                        conn = ibm_db.connect(conn_str, '', '')
                    except:
                        print('datbase droped sucessfully')
                    if conn:
                        print('Errors occurred during drop database')
                        ibm_db.close(conn)
                        conn = None
                else:
                    print('Errors occurred during drop database')
            except:
                print(ibm_db.conn_errormsg())
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#database created sucessfully
#datbase droped sucessfully
#database with codeset created sucessfully
#datbase droped sucessfully
