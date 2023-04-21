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

    def test_SPInOutBlob(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_SPInOutBlob)

    def run_test_SPInOutBlob(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]

        if (server == 'IDS'):
            procedure = """CREATE PROCEDURE TEST_OUT_BLOB(IN P1 BLOB(100),OUT P2 BLOB(100)); LET P2 = P1;END PROCEDURE;"""
        else:
            procedure = """CREATE PROCEDURE TEST_OUT_BLOB(IN P1 BLOB(100),OUT P2 BLOB(100)) 
                           LANGUAGE SQL
                           DYNAMIC RESULT SETS 0
                           BEGIN
                           SET P2 = P1;
                           END"""

        if conn:
            try:
                ibm_db.exec_immediate(conn, 'DROP PROCEDURE TEST_OUT_BLOB')
            except:
                pass
            ibm_db.exec_immediate(conn, procedure)

            stmt, inparam, outparam = ibm_db.callproc(conn, "TEST_OUT_BLOB",(b'12345678901234567890', b'0'))

            if stmt is not None:
                print("Values of bound parameters _after_ CALL:")
                print("  1: %s  2: %s\n" % (inparam, outparam))
            else:
                print("Error\n")
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Values of bound parameters _after_ CALL:
#  1: 12345678901234567890  2: 12345678901234567890
#__ZOS_EXPECTED__
#Values of bound parameters _after_ CALL:
#  1: 12345678901234567890  2: 12345678901234567890
#__SYSTEMI_EXPECTED__
#Values of bound parameters _after_ CALL:
#  1: 12345678901234567890  2: 12345678901234567890
#__IDS_EXPECTED__
#Values of bound parameters _after_ CALL:
#  1: 12345678901234567890  2: 12345678901234567890
