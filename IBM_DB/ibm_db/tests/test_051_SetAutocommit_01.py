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

    def test_051_SetAutocommit_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_051)

    def run_test_051(self):
        options = { ibm_db.SQL_ATTR_AUTOCOMMIT:  ibm_db.SQL_AUTOCOMMIT_OFF }

        conn = ibm_db.connect(config.database, config.user, config.password, options)

        ac = ibm_db.autocommit(conn)

        print(ac)

#__END__
#__LUW_EXPECTED__
#0
#__ZOS_EXPECTED__
#0
#__SYSTEMI_EXPECTED__
#0
#__IDS_EXPECTED__
#0
