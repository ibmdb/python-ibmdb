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

    def test_318_get_sqlcode_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_318)

    def run_test_318(self):
        try:
            # Intentionally wrong credentials to trigger connection failure
            conn = ibm_db_dbi.connect(config.database, "wrongUser", "wrongPassword")
            print(conn)  # Should not get here
        except Exception:
            print(ibm_db_dbi.get_sqlcode())

        try:
            conn1 = ibm_db_dbi.connect(config.database, config.user, config.password)
            cursor = conn1.cursor()
            cursor.execute("create table index_test(id int, data VARCHAR(50)")
        except Exception:
            print(ibm_db_dbi.get_sqlcode())

#__END__
#__LUW_EXPECTED__
#SQLCODE=-30082
#SQLCODE=-104
#__ZOS_EXPECTED__
#SQLCODE=-30082
#SQLCODE=-104
#__SYSTEMI_EXPECTED__
#SQLCODE=-30082
#SQLCODE=-104
#__IDS_EXPECTED__
#SQLCODE=-30082
#SQLCODE=-104
