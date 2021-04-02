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

    def test_091_ConnmsgWrongUser(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_091)

    def run_test_091(self):
        try:
            conn = ibm_db.connect(config.database, "y", config.password)
            print("??? No way.")
        except:
            err = ibm_db.conn_errormsg()
            print(err)

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#__ZOS_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#__IDS_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#__ZOS_ODBC_EXPECTED__
#??? No way.
