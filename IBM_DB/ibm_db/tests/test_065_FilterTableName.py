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

    def test_065_FilterTableName(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_065)

    def run_test_065(self):
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

        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.tables(conn, None, '%', "t3")
        else:
            result = ibm_db.tables(conn, None, '%', "T3")

        columns = ibm_db.num_fields(result)

        for i in range(0, columns):
            print("%s, " % ibm_db.field_name(result, i))
        print("\n\n")

        row = ibm_db.fetch_tuple(result)
        while ( row ):
            final = ", " + row[1] + ", " + row[2] + ", " + row[3] + ", , ";
            row = ibm_db.fetch_tuple(result)

        print(final)

        ibm_db.free_result(result)

        ibm_db.exec_immediate(conn, 'DROP TABLE t.t1')
        ibm_db.exec_immediate(conn, 'DROP TABLE t.t2')
        ibm_db.exec_immediate(conn, 'DROP TABLE t.t3')
        ibm_db.exec_immediate(conn, 'DROP TABLE t.t4')

#__END__
#__LUW_EXPECTED__
#TABLE_CAT, TABLE_SCHEM, TABLE_NAME, TABLE_TYPE, REMARKS, 
#
#, T, T3, TABLE, , 
#__ZOS_EXPECTED__
#TABLE_CAT, TABLE_SCHEM, TABLE_NAME, TABLE_TYPE, REMARKS, 
#
#, %sT, T3, TABLE, , 
#__SYSTEMI_EXPECTED__
#TABLE_CAT, TABLE_SCHEM, TABLE_NAME, TABLE_TYPE, REMARKS, 
#
#, T, T3, TABLE, , 
#__IDS_EXPECTED__
#table_cat, table_schem, table_name, table_type, remarks, 
#
#, t, t3, TABLE, ,
