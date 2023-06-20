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

    def test_005_ConnBadUserBadPwd(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_005)

    def run_test_005(self):
        baduser = "non_user"
        badpass = "invalid_password"
        dsn = "DATABASE=" + config.database + ";UID=" + baduser + ";PWD=" + badpass + ";"
        try:
            conn = ibm_db.connect(dsn, "", "")
            print ("odd, ibm_db.connect succeeded with an invalid user / password")
            ibm_db.close(conn)
        except:
            print ("Ooops")

#__END__
#__LUW_EXPECTED__
#Ooops
#__ZOS_EXPECTED__
#Ooops
#__SYSTEMI_EXPECTED__
#Ooops
#__IDS_EXPECTED__
#Ooops
#__ZOS_ODBC_EXPECTED__
#Ooops
