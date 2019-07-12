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

    def test_063_Tables_04(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_063)

    def run_test_063(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.tables(conn, None, "SYSIBM", "", "VIEW")

        if (type(result) == ibm_db.IBM_DBStatement):
            print("Resource is a DB2 Statement")

        ibm_db.free_result(result)

#__END__
#__LUW_EXPECTED__
#Resource is a DB2 Statement
#__ZOS_EXPECTED__
#Resource is a DB2 Statement
#__SYSTEMI_EXPECTED__
#Resource is a DB2 Statement
#__IDS_EXPECTED__
#Resource is a DB2 Statement
