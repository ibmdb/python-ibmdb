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
import ibm_db_ctx

class IbmDbTestCase(unittest.TestCase):

    def test_context_ConnDb(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_context_ConnDb)

    def run_test_context_ConnDb(self):
        with ibm_db_ctx.Db2connect(config.database, config.user, config.password) as conn:
            print("Connection succeeded.")
		   

#__END__
#__LUW_EXPECTED__
#Connection succeeded.
#__ZOS_EXPECTED__
#Connection succeeded.
#__SYSTEMI_EXPECTED__
#Connection succeeded.
#__IDS_EXPECTED__
#Connection succeeded.