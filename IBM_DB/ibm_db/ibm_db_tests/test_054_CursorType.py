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

    def test_054_CursorType(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_054)

    def run_test_054(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        serverinfo = ibm_db.server_info( conn )

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals")
        val = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
        print(val)

        op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_FORWARD_ONLY}
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals", op)
        val = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
        print(val)

        if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN}
        else:
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC}
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals", op)
        val = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
        print(val)

        op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC}
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals", op)
        val = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
        print(val)

#__END__
#__LUW_EXPECTED__
#0
#0
#1
#3
#__ZOS_EXPECTED__
#0
#0
#1
#3
#__SYSTEMI_EXPECTED__
#0
#0
#3
#3
#__IDS_EXPECTED__
#0
#0
#3
#3
#
#__ZOS_ODBC_EXPECTED__
#0
#0
#3
#3
#
