#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2020
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_SPInOutZero(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_SPInOutZero)

    def run_test_SPInOutZero(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]

        if (server == 'IDS'):
            procedure = """CREATE PROCEDURE TEST_OUT_ZERO_INT(OUT O_RETURN INTEGER); LET O_RETURN = 0;END PROCEDURE;"""
        else:
            procedure = """CREATE PROCEDURE TEST_OUT_ZERO_INT(OUT O_RETURN SMALLINT) BEGIN DECLARE C_RET_OK SMALLINT CONSTANT 0; DECLARE C_RET_EXCEPT  SMALLINT CONSTANT -1; SET O_RETURN = C_RET_OK; RETURN; END"""

        if conn:
            try:
                ibm_db.exec_immediate(conn, 'DROP PROCEDURE TEST_OUT_ZERO_INT')
            except:
                pass
            ibm_db.exec_immediate(conn, procedure)
            stmt, ret = ibm_db.callproc(conn, "TEST_OUT_ZERO_INT",(99,))

            if ret is not None:
                print("{}".format(ret))
            else:
                print("ret is None")
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#0
#__ZOS_EXPECTED__
#0
#__SYSTEMI_EXPECTED__
#0
#__IDS_EXPECTED__
#0

