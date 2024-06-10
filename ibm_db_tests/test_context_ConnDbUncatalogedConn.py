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
import ibm_db_ctx

class IbmDbTestCase(unittest.TestCase):

    def test_context_ConnDbUncatalogedConn(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_context_ConnDbUncatalogedConn)

    def run_test_context_ConnDbUncatalogedConn(self):
        conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (config.database, config.hostname, config.port, config.user, config.password)
        with ibm_db_ctx.Db2connect(conn_str,'','') as conn:
            print("Connection succeeded.")
		
                

#__END__
#__LUW_EXPECTED__
#Connection succeeded.
#__ZOS_EXPECTED__
#Connection succeeded.
#__SYSTEMI_EXPECTED__
#Connection succeeded.
#__IDS_EXPECTED__
#Connection succeeded.