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

    def test_211_FieldDisplaySize_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_211)

    def run_test_211(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")

        i = 1

        while (i <= ibm_db.num_fields(result)):
            #printf("%d size %d\n",i, ibm_db.field_display_size(result,i) || 0)
            print("%d size %d" % (i, ibm_db.field_display_size(result,i) or 0))
            i += 1

        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#1 size 15
#2 size 15
#3 size 11
#4 size 0
#__ZOS_EXPECTED__
#1 size 15
#2 size 15
#3 size 11
#4 size 0
#__SYSTEMI_EXPECTED__
#1 size 15
#2 size 15
#3 size 11
#4 size 0
#__IDS_EXPECTED__
#1 size 15
#2 size 15
#3 size 11
#4 size 0
