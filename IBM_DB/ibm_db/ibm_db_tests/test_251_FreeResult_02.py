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

    def test_251_FreeResult_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_251)

    def run_test_251(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")

        r1 = ibm_db.free_result(result)
        r2 = ibm_db.free_result(result)
        r3 = ''
        try:
            r3 = ibm_db.free_result(result99)  # noqa: F821
        except:
            r3 = None

        print(r1)
        print(r2)
        print(r3)

#__END__
#__LUW_EXPECTED__
#True
#True
#None
#__ZOS_EXPECTED__
#True
#True
#None
#__SYSTEMI_EXPECTED__
#True
#True
#None
#__IDS_EXPECTED__
#True
#True
#None
