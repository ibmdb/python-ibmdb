#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import os
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_144_BindParamInsertStmtPARAM_FILE(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_144)

    def run_test_144(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            # Drop the test table, in case it exists
            drop = 'DROP TABLE pictures'
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass

            # Create the test table
            create = 'CREATE TABLE pictures (id INTEGER, picture BLOB)'
            result = ibm_db.exec_immediate(conn, create)

            stmt = ibm_db.prepare(conn, "INSERT INTO pictures VALUES (0, ?)")

            picture = os.path.dirname(os.path.abspath(__file__)) + "/pic1.jpg"
            if sys.platform == 'zos':
                rc = ibm_db.bind_param(stmt, 1, picture, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            else:
                rc = ibm_db.bind_param(stmt, 1, picture, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BINARY)

            rc = ibm_db.execute(stmt)

            num = ibm_db.num_rows(stmt)

            print(num)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#1
#__ZOS_EXPECTED__
#1
#__SYSTEMI_EXPECTED__
#1
#__IDS_EXPECTED__
#1
