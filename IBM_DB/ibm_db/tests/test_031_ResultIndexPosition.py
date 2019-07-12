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

    def test_031_ResultIndexPosition(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_031)

    def run_test_031(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            stmt = ibm_db.exec_immediate(conn, "SELECT id, breed, name, weight FROM animals WHERE id = 0")

            while (ibm_db.fetch_row(stmt)):
                id = ibm_db.result(stmt, 0)
                print("int(%d)" % id)
                breed = ibm_db.result(stmt, 1)
                print("string(%d) \"%s\"" % (len(breed), breed))
                name = ibm_db.result(stmt, 2)
                print("string(%d) \"%s\"" % (len(name), name))
                weight = ibm_db.result(stmt, 3)
                print("string(%d) \"%s\"" % (len(str(weight)), weight))
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__ZOS_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__SYSTEMI_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__IDS_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
