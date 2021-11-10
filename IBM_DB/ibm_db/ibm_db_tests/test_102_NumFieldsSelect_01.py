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

    def test_102_NumFieldsSelect_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_102)

    def run_test_102(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if (not conn):
            print(ibm_db.conn_errormsg())

        server = ibm_db.server_info( conn )
        if ((server.DBMS_NAME[0:2] != "AS") and (server.DBMS_NAME != "DB2") and (server.DBMS_NAME[0:3] != "IDS") and (server.DBMS_NAME[0:3] != "DSN")):
            result = ibm_db.exec_immediate(conn, "VALUES(1)")
            #throw :unsupported unless result
            if (not result):
                raise Exception('Unsupported')
            print(ibm_db.num_fields(result))
        else:
            print('1')
        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#1
#__ZOS_EXPECTED__
#1
#__SYSTEMI_EXPECTED__
#1
#__IDS_EXPECTED__
#1
