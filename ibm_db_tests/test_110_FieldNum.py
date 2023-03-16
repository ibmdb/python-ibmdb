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

    def test_110_FieldNum(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_110)

    def run_test_110(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY breed")

            if (server.DBMS_NAME[0:3] == 'IDS'):
                num1 = ibm_db.field_num(stmt, "id")
                num2 = ibm_db.field_num(stmt, "breed")
                num3 = ibm_db.field_num(stmt, "name")
                num4 = ibm_db.field_num(stmt, "weight")
                num5 = ibm_db.field_num(stmt, "test")
                num6 = ibm_db.field_num(stmt, 8)
                num7 = ibm_db.field_num(stmt, 1)
                num8 = ibm_db.field_num(stmt, "WEIGHT")
            else:
                num1 = ibm_db.field_num(stmt, "ID")
                num2 = ibm_db.field_num(stmt, "BREED")
                num3 = ibm_db.field_num(stmt, "NAME")
                num4 = ibm_db.field_num(stmt, "WEIGHT")
                num5 = ibm_db.field_num(stmt, "TEST")
                num6 = ibm_db.field_num(stmt, 8)
                num7 = ibm_db.field_num(stmt, 1)
                num8 = ibm_db.field_num(stmt, "weight")

            print("int(%d)" % num1)
            print("int(%d)" % num2)
            print("int(%d)" % num3)
            print("int(%d)" % num4)

            print("%s" % num5)
            print("%s" % num6)
            print("int(%d)" % num7)
            print("%s" % num8)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(0)
#int(1)
#int(2)
#int(3)
#False
#False
#int(1)
#False
#__ZOS_EXPECTED__
#int(0)
#int(1)
#int(2)
#int(3)
#False
#False
#int(1)
#False
#__SYSTEMI_EXPECTED__
#int(0)
#int(1)
#int(2)
#int(3)
#False
#False
#int(1)
#False
#__IDS_EXPECTED__
#int(0)
#int(1)
#int(2)
#int(3)
#False
#False
#int(1)
#False
