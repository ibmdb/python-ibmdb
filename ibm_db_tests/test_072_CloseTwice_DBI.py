#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2026
#

from __future__ import print_function
import sys
import unittest
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_072_CloseTwice_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_072)

    def run_test_072(self):
        conn = ibm_db_dbi.connect(config.database, config.user, config.password)

        rc1 = conn.close()
        rc2 = conn.close()

        print(rc1)
        print(rc2)

#__END__
#__LUW_EXPECTED__
#True
#True
#__ZOS_EXPECTED__
#True
#True
#__SYSTEMI_EXPECTED__
#True
#True
#__IDS_EXPECTED__
#True
#True
