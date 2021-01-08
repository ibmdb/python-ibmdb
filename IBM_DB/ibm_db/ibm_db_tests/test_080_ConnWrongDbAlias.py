#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import os
import sys
import unittest
import ibm_db
import config
import getpass
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    # Fails with AssertionError: '     ' != '08001'
    @unittest.skipIf(os.environ.get("CI", False), "Test fails in CI")
    def test_080_ConnWrongDbAlias(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_080)

    def run_test_080(self):
        try:
            if sys.platform == 'zos':
                conn =  ibm_db.connect("x", getpass.getuser(), config.password)
            else:
                conn = ibm_db.connect("x", config.user, config.password)
            print("??? No way.")
        except:
            print(ibm_db.conn_error())

        #if conn:
        #  print "??? No way."
        #else:
        #  print ibm_db.conn_error()

#__END__
#__LUW_EXPECTED__
#08001
#__ZOS_EXPECTED__
#08001
#__SYSTEMI_EXPECTED__
#08001
#__IDS_EXPECTED__
#08001
#__ZOS_ODBC_EXPECTED__
#42505
