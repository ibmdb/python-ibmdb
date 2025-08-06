#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2025
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_317_connErrormsg_connError_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_317)

    def run_test_317(self):
        try:
            # Intentionally wrong credentials to trigger connection failure
            conn = ibm_db_dbi.connect(config.database, "wrongUser", "wrongPassword")
            print(conn)  # Should not get here
        except Exception:
            print(ibm_db_dbi.conn_errormsg())
            print(ibm_db_dbi.conn_error())

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001  SQLCODE=-30082
#08001
#__ZOS_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001  SQLCODE=-30082
#08001
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001  SQLCODE=-30082
#08001
#__IDS_EXPECTED__
#[IBM][CLI Driver] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001  SQLCODE=-30082
#08001
