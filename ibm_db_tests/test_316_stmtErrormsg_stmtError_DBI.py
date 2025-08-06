#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2025
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_316_stmtErrormsg_stmtError_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_316)

    def run_test_316(self):
        conn = ibm_db_dbi.connect(config.database, config.user, config.password)
        cursor = conn.cursor()

        try:
            cursor.execute("INVALID SQL")
        except Exception:
            print(cursor.stmt_errormsg())
            print(cursor.stmt_error())

        cursor.close()
        conn.close()

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver][DB2/LINUXX8664] SQL0104N  An unexpected token "END-OF-STATEMENT" was found following "INVALID SQL".  Expected tokens may include:  "JOIN <joined_table>".  SQLSTATE=42601  SQLCODE=-104
#42601
#__ZOS_EXPECTED__
#[IBM][CLI Driver][DB2/LINUXX8664] SQL0104N  An unexpected token "END-OF-STATEMENT" was found following "INVALID SQL".  Expected tokens may include:  "JOIN <joined_table>".  SQLSTATE=42601  SQLCODE=-104
#42601
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver][AS] SQL0104N  An unexpected token "END-OF-STATEMENT" was found following "INVALID SQL".  Expected tokens may include:  "JOIN <joined_table>".  SQLSTATE=42601  SQLCODE=-104
#42601
#__IDS_EXPECTED__
#[IBM][CLI Driver][IDS/LINUXX8664] SQL0104N  An unexpected token "END-OF-STATEMENT" was found following "INVALID SQL".  Expected tokens may include:  "JOIN <joined_table>".  SQLSTATE=42601  SQLCODE=-104
#42601
