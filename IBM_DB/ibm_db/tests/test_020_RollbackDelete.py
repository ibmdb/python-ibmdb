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

    def test_020_RollbackDelete(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_020)

    def run_test_020(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:

            stmt = ibm_db.exec_immediate(conn, "SELECT count(*) FROM animals")
            res = ibm_db.fetch_tuple(stmt)
            rows = res[0]
            print(rows)

            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
            ac = ibm_db.autocommit(conn)
            if ac != 0:
                print("Cannot set ibm_db.SQL_AUTOCOMMIT_OFF\nCannot run test")
                #continue

            ibm_db.exec_immediate(conn, "DELETE FROM animals")

            stmt = ibm_db.exec_immediate(conn, "SELECT count(*) FROM animals")
            res = ibm_db.fetch_tuple(stmt)
            rows = res[0]
            print(rows)

            ibm_db.rollback(conn)

            stmt = ibm_db.exec_immediate(conn, "SELECT count(*) FROM animals")
            res = ibm_db.fetch_tuple(stmt)
            rows = res[0]
            print(rows)
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#7
#0
#7
#__ZOS_EXPECTED__
#7
#0
#7
#__SYSTEMI_EXPECTED__
#7
#0
#7
#__IDS_EXPECTED__
#7
#0
#7
