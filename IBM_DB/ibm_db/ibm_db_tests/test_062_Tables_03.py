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

    def test_062_Tables_03(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_062)

    def run_test_062(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        create = 'CREATE SCHEMA AUTHORIZATION t'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass

        create = 'CREATE TABLE t.t1( c1 integer, c2 varchar(40))'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass

        create = 'CREATE TABLE t.t2( c1 integer, c2 varchar(40))'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass

        create = 'CREATE TABLE t.t3( c1 integer, c2 varchar(40))'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass

        create = 'CREATE TABLE t.t4( c1 integer, c2 varchar(40))'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass

        if conn:
            if (server.DBMS_NAME[0:3] == 'IDS'):
                schema = 't'
            else:
                schema = 'T'
            result = ibm_db.tables(conn,None,schema);
            i = 0
            row = ibm_db.fetch_both(result)
            while ( row ):
                str = row[1] + "/" + row[2] + "/" + row[3]
                if (i < 4):
                    print(str)
                i = i + 1
                row = ibm_db.fetch_both(result)

            ibm_db.exec_immediate(conn, 'DROP TABLE t.t1')
            ibm_db.exec_immediate(conn, 'DROP TABLE t.t2')
            ibm_db.exec_immediate(conn, 'DROP TABLE t.t3')
            ibm_db.exec_immediate(conn, 'DROP TABLE t.t4')

            print("done!")
        else:
            print("no connection: #{ibm_db.conn_errormsg}");

#__END__
#__LUW_EXPECTED__
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__ZOS_EXPECTED__
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__SYSTEMI_EXPECTED__
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__IDS_EXPECTED__
#t/t1/TABLE%s
#t/t2/TABLE%s
#t/t3/TABLE%s
#t/t4/TABLE%s
#done!
