#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2024
#

from __future__ import print_function
import sys
import unittest
import os
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sp_return(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_sp_return)

    def run_test_sp_return(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]

        if (server == 'IDS'):
            procedure = """CREATE PROCEDURE TEST_SP_RETURN( ); declare retval integer;set retval = 100;return retval;END PROCEDURE;"""
        else:
            procedure = """CREATE PROCEDURE TEST_SP_RETURN( )
                           LANGUAGE SQL
                           BEGIN
                           declare retval integer;
                           set retval = 100;
                           return retval;
                           End
                        """

        if conn:
            try:
                ibm_db.exec_immediate(conn, 'DROP PROCEDURE TEST_SP_RETURN')
            except:
                pass
            ibm_db.exec_immediate(conn, procedure)

            stmt = ibm_db.callproc(conn, "TEST_SP_RETURN",( ))
            value =ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CALL_RETURN,0)
            print(value)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#100
#__ZOS_EXPECTED__
#100
#__SYSTEMI_EXPECTED__
#100
#__IDS_EXPECTED__
#100