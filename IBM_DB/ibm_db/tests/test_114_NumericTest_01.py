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

    def test_114_NumericTest_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_114)

    def run_test_114(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            drop = "drop table numericliteral"

            try:
                ibm_db.exec_immediate( conn, drop )
            except:
                pass

            create = "create table numericliteral ( id INTEGER, num INTEGER )"
            ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO numericliteral (id, num) values (1,5)"
            ibm_db.exec_immediate(conn, insert)

            insert = "UPDATE numericliteral SET num = '10' WHERE num = '5'"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.prepare(conn, "SELECT * FROM numericliteral")
            ibm_db.execute(stmt)

            result = ibm_db.fetch_row( stmt )
            while ( result ):
                row0 = ibm_db.result(stmt, 0)
                row1 = ibm_db.result(stmt, 1)
                print(row0)
                print(row1)
                result = ibm_db.fetch_row( stmt )
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#1
#10
#__ZOS_EXPECTED__
#1
#10
#__SYSTEMI_EXPECTED__
#1
#10
#__IDS_EXPECTED__
#1
#10
