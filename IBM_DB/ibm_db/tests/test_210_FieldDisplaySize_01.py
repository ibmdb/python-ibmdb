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

    def test_210_FieldDisplaySize_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_210)

    def run_test_210(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from staff")
        cols = ibm_db.num_fields(result)

        for i in range(0, cols):
            size = ibm_db.field_display_size(result,i)
            print("col:%d and size: %d" % (i, size))

        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#col:0 and size: 6
#col:1 and size: 9
#col:2 and size: 6
#col:3 and size: 5
#col:4 and size: 6
#col:5 and size: 9
#col:6 and size: 9
#__ZOS_EXPECTED__
#col:0 and size: 6
#col:1 and size: 9
#col:2 and size: 6
#col:3 and size: 5
#col:4 and size: 6
#col:5 and size: 9
#col:6 and size: 9
#__SYSTEMI_EXPECTED__
#col:0 and size: 6
#col:1 and size: 9
#col:2 and size: 6
#col:3 and size: 5
#col:4 and size: 6
#col:5 and size: 9
#col:6 and size: 9
#__IDS_EXPECTED__
#col:0 and size: 6
#col:1 and size: 9
#col:2 and size: 6
#col:3 and size: 5
#col:4 and size: 6
#col:5 and size: 9
#col:6 and size: 9
