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

    def test_003_NumAffectedRows(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_003)

    def run_test_003(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
            sql = 'UPDATE animals SET id = 9'
            res = ibm_db.exec_immediate(conn, sql)
            print ("Number of affected rows: %d" % ibm_db.num_rows(res))
            ibm_db.rollback(conn)
            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Number of affected rows: 7
#__ZOS_EXPECTED__
#Number of affected rows: 7
#__SYSTEMI_EXPECTED__
#Number of affected rows: 7
#__IDS_EXPECTED__
#Number of affected rows: 7
