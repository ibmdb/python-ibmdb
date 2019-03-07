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

    def test_250_FreeResult_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_250)

    def run_test_250(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")
        result2 = ibm_db.exec_immediate(conn, "select * from staff")
        result3 = ibm_db.exec_immediate(conn, "select * from emp_photo")

        r1 = ibm_db.free_result(result)
        r2 = ibm_db.free_result(result2)
        r3 = ibm_db.free_result(result3)

        print(r1)
        print(r2)
        print(r3)

#__END__
#__LUW_EXPECTED__
#True
#True
#True
#__ZOS_EXPECTED__
#True
#True
#True
#__SYSTEMI_EXPECTED__
#True
#True
#True
#__IDS_EXPECTED__
#True
#True
#True
