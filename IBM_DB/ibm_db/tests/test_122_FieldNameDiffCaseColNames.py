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

    def test_122_FieldNameDiffCaseColNames(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_122)

    def run_test_122(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            drop = "drop table ftest"
            try:
                ibm_db.exec_immediate( conn, drop )
            except:
                pass

            create = "create table ftest ( \"TEST\" integer, \"test\" integer, \"Test\" integer  )"
            ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO ftest values (1,2,3)"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM ftest")

            num1 = ibm_db.field_name(stmt, 0)
            num2 = ibm_db.field_name(stmt, 1)
            num3 = ibm_db.field_name(stmt, 2)

            num4 = ibm_db.field_name(stmt, "TEST")
            num5 = ibm_db.field_name(stmt, 'test')
            num6 = ibm_db.field_name(stmt, 'Test')

            print("string(%d) \"%s\"" % (len(num1), num1))
            print("string(%d) \"%s\"" % (len(num2), num2))
            print("string(%d) \"%s\"" % (len(num3), num3))

            print("string(%d) \"%s\"" % (len(num4), num4))
            print("string(%d) \"%s\"" % (len(num5), num5))
            print("string(%d) \"%s\"" % (len(num6), num6))

        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#__ZOS_EXPECTED__
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#__SYSTEMI_EXPECTED__
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#__IDS_EXPECTED__
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
#string(4) "TEST"
#string(4) "test"
#string(4) "Test"
