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

    def test_conn_get_sqlcode(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_conn_get_sqlcode)

    def run_test_conn_get_sqlcode(self):
        try:
            conn = ibm_db.connect(config.database, "y", config.password)
            print("??? No way.")
        except:
            print(ibm_db.get_sqlcode())

#__END__
#__LUW_EXPECTED__
#SQLCODE=-30082
#__ZOS_EXPECTED__
#SQLCODE=-30082
#__SYSTEMI_EXPECTED__
#SQLCODE=-30082
#__IDS_EXPECTED__
#SQLCODE=-30082
#__ZOS_ODBC_EXPECTED__
#??? No way.
