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

    def test_011_DeleteRowCount(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_011)

    def run_test_011(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
            stmt = ibm_db.exec_immediate(conn, "DELETE FROM animals WHERE weight > 10.0")
            print ("Number of affected rows: %d" % ibm_db.num_rows( stmt ))
            ibm_db.rollback(conn)
            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Number of affected rows: 3
#__ZOS_EXPECTED__
#Number of affected rows: 3
#__SYSTEMI_EXPECTED__
#Number of affected rows: 3
#__IDS_EXPECTED__
#Number of affected rows: 3
