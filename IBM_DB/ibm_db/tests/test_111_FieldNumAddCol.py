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

    def test_111_FieldNumAddCol(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_111)

    def run_test_111(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

            insert = "INSERT INTO animals values (7, 'cat', 'Benji', 5.1)"
            ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.exec_immediate(conn, "SELECT breed, COUNT(breed) AS number FROM animals GROUP BY breed ORDER BY breed")

            if (server.DBMS_NAME[0:3] == 'IDS'):
                num1 = ibm_db.field_num(stmt, "id")
                num2 = ibm_db.field_num(stmt, "breed")
                num3 = ibm_db.field_num(stmt, "number")
                num4 = ibm_db.field_num(stmt, "NUMBER")
                num5 = ibm_db.field_num(stmt, "bREED")
                num6 = ibm_db.field_num(stmt, 8)
                num7 = ibm_db.field_num(stmt, 1)
                num8 = ibm_db.field_num(stmt, "WEIGHT")
            else:
                num1 = ibm_db.field_num(stmt, "ID")
                num2 = ibm_db.field_num(stmt, "BREED")
                num3 = ibm_db.field_num(stmt, "NUMBER")
                num4 = ibm_db.field_num(stmt, "number")
                num5 = ibm_db.field_num(stmt, "Breed")
                num6 = ibm_db.field_num(stmt, 8)
                num7 = ibm_db.field_num(stmt, 1)
                num8 = ibm_db.field_num(stmt, "weight")

            print("%s" % num1)
            print("int(%d)" % num2)
            print("int(%d)" % num3)
            print("%s" % num4)

            print("%s" % num5)
            print("%s" % num6)
            print("int(%d)" % num7)
            print("%s" % num8)

            ibm_db.rollback(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#False
#int(0)
#int(1)
#False
#False
#False
#int(1)
#False
#__ZOS_EXPECTED__
#False
#int(0)
#int(1)
#False
#False
#False
#int(1)
#False
#__SYSTEMI_EXPECTED__
#False
#int(0)
#int(1)
#False
#False
#False
#int(1)
#False
#__IDS_EXPECTED__
#False
#int(0)
#int(1)
#False
#False
#False
#int(1)
#False
