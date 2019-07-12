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

    def test_115_NumericTest_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_115)

    def run_test_115(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        if conn:
            drop = "drop table numericliteral"
            try:
                ibm_db.exec_immediate( conn, drop )
            except:
                pass

            create = "create table numericliteral ( id INTEGER, data VARCHAR(50) )"
            ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO numericliteral (id, data) values (12, 'NUMERIC LITERAL TEST')"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.prepare(conn, "SELECT data FROM numericliteral")
            ibm_db.execute(stmt)

#      NOTE: This is a workaround
#      function fetch_object() to be implemented...
#      row = ibm_db.fetch_object(stmt, 0)

            class Row:
                pass

            row = Row()
            ibm_db.fetch_row(stmt, 0)
            if (server.DBMS_NAME[0:3] != 'IDS'):
                row.DATA = ibm_db.result(stmt, 'DATA')
            else:
                row.DATA = ibm_db.result(stmt, 'data')
            print(row.DATA)

            insert = "UPDATE numericliteral SET data = '@@@@@@@@@@' WHERE id = '12'"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.prepare(conn, "SELECT data FROM numericliteral")
            ibm_db.execute(stmt)

#      row = ibm_db.fetch_object(stmt, 0)
            ibm_db.fetch_row(stmt, 0)
            if (server.DBMS_NAME[0:3] != 'IDS'):
                row.DATA = ibm_db.result(stmt, 'DATA')
            else:
                row.DATA = ibm_db.result(stmt, 'data')
            print(row.DATA)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#NUMERIC LITERAL TEST
#@@@@@@@@@@
#__ZOS_EXPECTED__
#NUMERIC LITERAL TEST
#@@@@@@@@@@
#__SYSTEMI_EXPECTED__
#NUMERIC LITERAL TEST
#@@@@@@@@@@
#__IDS_EXPECTED__
#NUMERIC LITERAL TEST
#@@@@@@@@@@
