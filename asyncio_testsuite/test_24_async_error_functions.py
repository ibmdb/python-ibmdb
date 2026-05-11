from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_24_async_error_functions(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_24)

    def run_test_24(self):
        async def main():
            # Good connection first
            conn = await ibm_db_dbi.connect_async(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            # Check error functions on a good connection (pass raw conn_handler)
            err_msg = await ibm_db_dbi.conn_errormsg_async(conn.conn_handler)
            print("conn_errormsg_async (good conn):", repr(err_msg))

            err_code = await ibm_db_dbi.conn_error_async(conn.conn_handler)
            print("conn_error_async (good conn):", repr(err_code))

            sqlcode = await ibm_db_dbi.get_sqlcode_async()
            print("get_sqlcode_async:", repr(sqlcode))

            conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#__ZOS_EXPECTED__
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#__SYSTEMI_EXPECTED__
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#__IDS_EXPECTED__
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
