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

    def test_015_InsertDeleteRowCount_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_015)

    def run_test_015(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if conn:
            result = ibm_db.exec_immediate(conn,"insert into t_string values(123,1.222333,'one to one')")
            if result:
                cols = ibm_db.num_fields(result)
                # NOTE: Removed '\n' from the following and a few more prints here (refer to ruby test_015.rb)
                print ("col:", cols)
                rows = ibm_db.num_rows(result)
                print ("affected row:", rows)
            else:
                print (ibm_db.stmt_errormsg())
            result = ibm_db.exec_immediate(conn,"delete from t_string where a=123")
            if result:
                cols = ibm_db.num_fields(result)
                print ("col:", cols)
                rows = ibm_db.num_rows(result)
                print ("affected row:", rows)
            else:
                print (ibm_db.stmt_errormsg())
            ibm_db.close(conn)
        else:
            print ("no connection:", ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#col: 0
#affected row: 1
#col: 0
#affected row: 1
#__ZOS_EXPECTED__
#col: 0
#affected row: 1
#col: 0
#affected row: 1
#__SYSTEMI_EXPECTED__
#col: 0
#affected row: 1
#col: 0
#affected row: 1
#__IDS_EXPECTED__
#col: 0
#affected row: 1
#col: 0
#affected row: 1
