#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_148_CallSPDiffBindPattern_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_148)

    def run_test_148(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ##### Set up #####
            serverinfo = ibm_db.server_info( conn )
            server = serverinfo.DBMS_NAME[0:3]
            try:
                sql = "DROP TABLE sptb"
                ibm_db.exec_immediate(conn, sql)
            except:
                pass

            try:
                sql = "DROP PROCEDURE sp"
                ibm_db.exec_immediate(conn, sql)
            except:
                pass

            if (server == 'IDS'):
                sql = "CREATE TABLE sptb (c1 INTEGER, c2 FLOAT, c3 VARCHAR(10), c4 INT8, c5 CLOB)"
            else:
                sql = "CREATE TABLE sptb (c1 INTEGER, c2 FLOAT, c3 VARCHAR(10), c4 BIGINT, c5 CLOB)"

            ibm_db.exec_immediate(conn, sql)

            sql = "INSERT INTO sptb (c1, c2, c3, c4, c5) VALUES (1, 5.01, 'varchar', 3271982, 'clob data clob data')"
            ibm_db.exec_immediate(conn, sql)

            if (server == 'IDS'):
                sql = """CREATE PROCEDURE sp(OUT out1 INTEGER, OUT out2 FLOAT, OUT out3 VARCHAR(10), OUT out4 INT8, OUT out5 CLOB);
                 SELECT c1, c2, c3, c4, c5 INTO out1, out2, out3, out4, out5 FROM sptb; END PROCEDURE;"""
            else:
                sql = """CREATE PROCEDURE sp(OUT out1 INTEGER, OUT out2 FLOAT, OUT out3 VARCHAR(10), OUT out4 BIGINT, OUT out5 CLOB)
                 DYNAMIC RESULT SETS 1 LANGUAGE SQL BEGIN
                 SELECT c1, c2, c3, c4, c5 INTO out1, out2, out3, out4, out5 FROM sptb; END"""
            ibm_db.exec_immediate(conn, sql)
            #############################

            ##### Run the test #####

            out1 = 0
            out2 = 0.00
            out3 = ""
            out4 = 0
            out5 = ""

            if 'zos' == sys.platform:
                stmt, out1, out2, out3, out4, out5 = ibm_db.callproc(conn, 'SP', (out1, out2, out3, out4, out5))
            else:
                stmt, out1, out2, out3, out4, out5 = ibm_db.callproc(conn, 'sp', (out1, out2, out3, out4, out5))

            print("out 1:")
            print(out1)
            print("out 2:")
            print(out2)
            print("out 3:")
            print(out3)
            print("out 4:")
            print(out4)
            print("out 5:")
            print(out5)
            #############################
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#out 1:
#1
#out 2:
#5.01
#out 3:
#varchar
#out 4:
#3271982
#out 5:
#clob data clob data
#__ZOS_EXPECTED__
#out 1:
#1
#out 2:
#5.01
#out 3:
#varchar
#out 4:
#3271982
#out 5:
#clob data clob data
#__SYSTEMI_EXPECTED__
#out 1:
#1
#out 2:
#5.01
#out 3:
#varchar
#out 4:
#3271982
#out 5:
#clob data clob data
#__IDS_EXPECTED__
#out 1:
#1
#out 2:
#5.01
#out 3:
#varchar
#out 4:
#3271982
#out 5:
#clob data clob data
