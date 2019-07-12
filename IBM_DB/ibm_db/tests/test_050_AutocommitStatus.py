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

    def test_050_AutocommitStatus(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_050)

    def run_test_050(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ac = ibm_db.autocommit(conn)

        print(ac)

#__END__
#__LUW_EXPECTED__
#1
#__ZOS_EXPECTED__
#1
#__SYSTEMI_EXPECTED__
#1
#__IDS_EXPECTED__
#1
