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

    def test_070_Close(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_070)

    def run_test_070(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            if (type(conn) == ibm_db.IBM_DBConnection):
                print("Resource is a DB2 Connection")

            rc = ibm_db.close(conn)

            print(rc)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Resource is a DB2 Connection
#True
#__ZOS_EXPECTED__
#Resource is a DB2 Connection
#True
#__SYSTEMI_EXPECTED__
#Resource is a DB2 Connection
#True
#__IDS_EXPECTED__
#Resource is a DB2 Connection
#True
