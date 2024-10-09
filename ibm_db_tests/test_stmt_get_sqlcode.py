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

    def test_stmt_get_sqlcode(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_stmt_get_sqlcode)

    @unittest.skipIf(sys.platform == 'zos',"Test fails with z/OS ODBC driver")
    def run_test_stmt_get_sqlcode(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if conn:
            result = ''
            result2 = ''
            try:
                result = ibm_db.exec_immediate(conn,"insert int0 t_string values(123,1.222333,'one to one')")
            except:
                pass
            if result:
                cols = ibm_db.num_fields(result)
                print("col:", cols,", ")
                rows = ibm_db.num_rows(result)
                print("affected row:", rows)
            else:
                print(ibm_db.get_sqlcode())
            try:
                result = ibm_db.exec_immediate(conn,"delete from t_string where a=123")
            except:
                pass
            if result:
                cols = ibm_db.num_fields(result)
                print("col:", cols,", ")
                rows = ibm_db.num_rows(result)
                print("affected row:", rows)
            else:
                print(ibm_db.get_sqlcode())

        else:
            print("no connection")

#__END__
#__LUW_EXPECTED__
#SQLCODE=-104
#__ZOS_EXPECTED__
#SQLCODE=-104
#__SYSTEMI_EXPECTED__
#SQLCODE=-104
#__IDS_EXPECTED__
#SQLCODE=-201
