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
import platform
import ibm_db_ctx

from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf(platform.system() == 'z/OS',"Test fails with z/OS ODBC driver")
    def test_context_ConnActive(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_context_ConnActive)

    def run_test_context_ConnActive(self):
        conn = None
        is_alive = ibm_db.active(conn)
        if is_alive:
            print("Is active")
        else:
            print("Is not active")

        with ibm_db_ctx.Db2connect(config.database, config.user, config.password) as conn:
            is_alive = ibm_db.active(conn)
            if is_alive:
                print("Is active")
            else:
                print("Is not active")

        is_alive = ibm_db.active(conn)
        if is_alive:
            print("Is active")
        else:
            print("Is not active")


#__END__
#__LUW_EXPECTED__
#Is not active
#Is active
#Is not active
#__ZOS_EXPECTED__
#Is not active
#Is active
#Is not active
#__SYSTEMI_EXPECTED__
#Is not active
#Is active
#Is not active
#__IDS_EXPECTED__
#Is not active
#Is active
#Is not active