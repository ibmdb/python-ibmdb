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

    def test_024_ForeignKeys(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_024)

    def run_test_024(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn != 0:
            drop = 'DROP TABLE test_primary_keys'
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass
            drop = 'DROP TABLE test_keys'
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
            statement = 'CREATE TABLE test_keys (name VARCHAR(30) NOT NULL, idf INTEGER NOT NULL, FOREIGN KEY(idf) REFERENCES test_primary_keys(id), \
                   PRIMARY KEY(name))'
            result = ibm_db.exec_immediate(conn, statement)
            statement = "INSERT INTO test_keys VALUES ('vince', 1)"
            result = ibm_db.exec_immediate(conn, statement)
            statement = 'CREATE TABLE test_foreign_keys (namef VARCHAR(30) NOT NULL, id INTEGER NOT NULL, FOREIGN KEY(namef) REFERENCES test_keys(name))'
            result = ibm_db.exec_immediate(conn, statement)
            statement = "INSERT INTO test_foreign_keys VALUES ('vince', 1)"
            result = ibm_db.exec_immediate(conn, statement)

            if (server.DBMS_NAME[0:3] == 'IDS' ):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'test_primary_keys')
            elif ('zos' in sys.platform):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'TEST_PRIMARY_KEYS')
            else:
                stmt = ibm_db.foreign_keys(conn, None, None, 'TEST_PRIMARY_KEYS')
            row = ibm_db.fetch_tuple(stmt)
            print(row[2])
            print(row[3])
            print(row[6])
            print(row[7])

            if (server.DBMS_NAME[0:3] == 'IDS'):
                stmt = ibm_db.foreign_keys(conn, None, None, None, None, config.user, 'test_keys')
            elif ( 'zos' in sys.platform):
                stmt = ibm_db.foreign_keys(conn, None, None, None, None, config.user,'TEST_KEYS')
            else:
                stmt = ibm_db.foreign_keys(conn, None, None, None, None, None, 'TEST_KEYS')
            row = ibm_db.fetch_tuple(stmt)
            print(row[2])
            print(row[3])
            print(row[6])
            print(row[7])

            if (server.DBMS_NAME[0:3] == 'IDS'):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'test_keys', None, None, None)
            elif ( 'zos' in sys.platform):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'TEST_KEYS', None, None, None)
            else:
                stmt = ibm_db.foreign_keys(conn, None, None, 'TEST_KEYS', None, None, None)
            row = ibm_db.fetch_tuple(stmt)
            print(row[2])
            print(row[3])
            print(row[6])
            print(row[7])

            if (server.DBMS_NAME[0:3] == 'IDS'):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'test_keys', None, config.user, 'test_foreign_keys')
            elif ( 'zos' in sys.platform):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'TEST_KEYS', None, config.user, 'TEST_FOREIGN_KEYS')
            else:
                stmt = ibm_db.foreign_keys(conn, None, None, 'TEST_KEYS', None, None, 'TEST_FOREIGN_KEYS')
            row = ibm_db.fetch_tuple(stmt)
            print(row[2])
            print(row[3])
            print(row[6])
            print(row[7])

            try:
                stmt = ibm_db.foreign_keys(conn, None, None, None, None, None, None)
                row = ibm_db.fetch_tuple(stmt)
            except:
                if (not stmt):
                    print(ibm_db.stmt_errormsg())

            if (server.DBMS_NAME[0:3] == 'IDS'):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'test_keys', None, 'dummy_schema')
            elif ( 'zos' in sys.platform):
                stmt = ibm_db.foreign_keys(conn, None, config.user, 'TEST_KEYS', None, 'dummy_schema')
            else:
                stmt = ibm_db.foreign_keys(conn, None, None, 'TEST_KEYS', None, 'dummy_schema')
            row = ibm_db.fetch_tuple(stmt)
            if(not row):
                print("No Data Found")
            else:
                print(row)
            ibm_db.close(conn)
        else:
            print(ibm_db.conn_errormsg())
            print("Connection failed\n")

#__END__
#__LUW_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#[IBM][CLI Driver] CLI0124E  Invalid argument value. SQLSTATE=HY009 SQLCODE=-99999
#No Data Found
#__ZOS_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#[IBM][CLI Driver] CLI0124E  Invalid argument value. SQLSTATE=HY009 SQLCODE=-99999
#No Data Found
#__SYSTEMI_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#[IBM][CLI Driver] CLI0124E  Invalid argument value. SQLSTATE=HY009 SQLCODE=-99999
#__IDS_EXPECTED__
#test_primary_keys
#id
#test_keys
#idf
#test_primary_keys
#id
#test_keys
#idf
#test_keys
#name
#test_foreign_keys
#namef
#test_keys
#name
#test_foreign_keys
#namef
#[IBM][CLI Driver] CLI0124E  Invalid argument value. SQLSTATE=HY009 SQLCODE=-99999
#No Data Found
#__ZOS_ODBC_EXPECTED__
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_PRIMARY_KEYS
#ID
#TEST_KEYS
#IDF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#TEST_KEYS
#NAME
#TEST_FOREIGN_KEYS
#NAMEF
#{DB2 FOR OS/390}{ODBC DRIVER}  SQLSTATE=HY009  ERRLOC=10:17:6 SQLCODE=-99999
#No Data Found