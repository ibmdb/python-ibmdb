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

    def test_071_CloseSuccess(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_071)

    def run_test_071(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            rc = ibm_db.close(conn)
            if (rc == True):
                print("ibm_db.close succeeded")
            else:
                print("ibm_db.close FAILED\n")
        else:
            print("%s" % ibm_db.conn_errormsg())
            print(",sqlstate=%s" % ibm_db.conn_error())
            print("%s" % ibm_db.conn_errormsg())
            print("%s" % ibm_db.conn_errormsg())
            print("%s" % ibm_db.conn_errormsg())
            print("%s" % ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#ibm_db.close succeeded
#__ZOS_EXPECTED__
#ibm_db.close succeeded
#__SYSTEMI_EXPECTED__
#ibm_db.close succeeded
#__IDS_EXPECTED__
#ibm_db.close succeeded
