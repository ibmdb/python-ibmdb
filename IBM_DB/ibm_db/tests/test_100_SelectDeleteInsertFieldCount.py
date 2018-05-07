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

    def test_100_SelectDeleteInsertFieldCount(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_100)

    def run_test_100(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY breed")

            fields1 = ibm_db.num_fields(stmt)

            print("int(%d)" % fields1)

            stmt = ibm_db.exec_immediate(conn, "SELECT name, breed FROM animals ORDER BY breed")
            fields2 = ibm_db.num_fields(stmt)

            print("int(%d)" % fields2)

            stmt = ibm_db.exec_immediate(conn, "DELETE FROM animals")
            fields3 = ibm_db.num_fields(stmt)

            print("int(%d)" % fields3)

            stmt = ibm_db.exec_immediate(conn, "INSERT INTO animals values (0, 'cat', 'Pook', 3.2)")
            fields4 = ibm_db.num_fields(stmt)

            print("int(%d)" % fields4)

            stmt = ibm_db.exec_immediate(conn, "SELECT name, breed, 'TEST' FROM animals")
            fields5 = ibm_db.num_fields(stmt)

            print("int(%d)" % fields5)

            ibm_db.rollback(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(4)
#int(2)
#int(0)
#int(0)
#int(3)
#__ZOS_EXPECTED__
#int(4)
#int(2)
#int(0)
#int(0)
#int(3)
#__SYSTEMI_EXPECTED__
#int(4)
#int(2)
#int(0)
#int(0)
#int(3)
#__IDS_EXPECTED__
#int(4)
#int(2)
#int(0)
#int(0)
#int(3)
