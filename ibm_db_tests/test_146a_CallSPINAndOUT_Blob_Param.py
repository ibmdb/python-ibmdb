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

    def test_146a_CallSPINAndOUT_Blob_Param(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_146a)

    def run_test_146a(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if(not server.DBMS_NAME.startswith('DB2/')):
            print("SKIPPED")
            return 0

        if conn:
            p1 = bytes('1234', 'utf8')

            print("Values of bound parameters _before_ CALL:")
            print("  1: %s\n" % (p1.decode('utf8')))

            stmt, blob1 = ibm_db.callproc(conn, 'out_blob', (p1,))

            if stmt is not None:
                print("Values of bound parameters _after_ CALL:")
                print("  1: %s \n" % (blob1))


#__END__
#__LUW_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: 1234
#
#Values of bound parameters _after_ CALL:
#  1: 1234567801234567890 
#
#__ZOS_EXPECTED__
#SKIPPED
#__SYSTEMI_EXPECTED__
#SKIPPED
#__IDS_EXPECTED__
#SKIPPED