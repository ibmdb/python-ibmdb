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

    def test_112_FieldNumDiffCaseColNames(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_112)

    def run_test_112(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            drop = "DROP TABLE ftest"
            try:
                ibm_db.exec_immediate( conn, drop )
            except:
                pass

            create = "CREATE TABLE ftest ( \"TEST\" INTEGER, \"test\" INTEGER, \"Test\" INTEGER  )"
            ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO ftest VALUES (1,2,3)"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM ftest")

            num1 = ibm_db.field_num(stmt, "TEST")
            num2 = ibm_db.field_num(stmt, 'test')
            num3 = ibm_db.field_num(stmt, 'Test')

            print("int(%d)" % num1)
            print("int(%d)" % num2)
            print("int(%d)" % num3)

        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(0)
#int(1)
#int(2)
#__ZOS_EXPECTED__
#int(0)
#int(1)
#int(2)
#__SYSTEMI_EXPECTED__
#int(0)
#int(1)
#int(2)
#__IDS_EXPECTED__
#int(0)
#int(1)
#int(2)
