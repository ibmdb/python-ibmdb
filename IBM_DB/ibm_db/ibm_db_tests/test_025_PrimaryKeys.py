#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#
# NOTE: IDS requires that you pass the schema name (cannot pass None)

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_025_PrimaryKeys(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_025)

    def run_test_025(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if (conn != 0):
            drop = 'DROP TABLE test_primary_keys'
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass
            drop = 'DROP TABLE test_foreign_keys'
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass
            statement = 'CREATE TABLE test_primary_keys (id INTEGER NOT NULL, PRIMARY KEY(id))'
            result = ibm_db.exec_immediate(conn, statement)
            statement = "INSERT INTO test_primary_keys VALUES (1)"
            result = ibm_db.exec_immediate(conn, statement)
            statement = 'CREATE TABLE test_foreign_keys (idf INTEGER NOT NULL, FOREIGN KEY(idf) REFERENCES test_primary_keys(id))'
            result = ibm_db.exec_immediate(conn, statement)
            statement = "INSERT INTO test_foreign_keys VALUES (1)"
            result = ibm_db.exec_immediate(conn, statement)

            if (server.DBMS_NAME[0:3] == 'IDS'):
                stmt = ibm_db.primary_keys(conn, None, config.user, 'test_primary_keys')
            elif ( 'zos' in sys.platform):
                stmt = ibm_db.primary_keys(conn, None, config.user, 'TEST_PRIMARY_KEYS')
            else:
                stmt = ibm_db.primary_keys(conn, None, None, 'TEST_PRIMARY_KEYS')
            row = ibm_db.fetch_tuple(stmt)
            print(row[2])
            print(row[3])
            print(row[4])
            ibm_db.close(conn)
        else:
            print(ibm_db.conn_errormsg())
            print("Connection failed\n")

#__END__
#__LUW_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#1
#__ZOS_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#1
#__SYSTEMI_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#1
#__IDS_EXPECTED__
#test_primary_keys
#id
#1
