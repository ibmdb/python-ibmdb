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

    def test_221_100PersistentConns(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_221)

    def run_test_221(self):
        pconn = list(range(100))

        for i in range(100):
            pconn[i] = ibm_db.pconnect(config.database, config.user, config.password)

        if pconn[33]:
            conn = pconn[22]
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
            stmt = ibm_db.exec_immediate(pconn[33], "UPDATE animals SET name = 'flyweight' WHERE weight < 10.0")
            print("Number of affected rows:", ibm_db.num_rows( stmt ))
            ibm_db.rollback(conn)
            ibm_db.close(pconn[33])
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Number of affected rows: 4
#__ZOS_EXPECTED__
#Number of affected rows: 4
#__SYSTEMI_EXPECTED__
#Number of affected rows: 4
#__IDS_EXPECTED__
#Number of affected rows: 4
