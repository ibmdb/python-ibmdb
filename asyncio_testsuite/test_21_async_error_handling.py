from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_21_async_error_handling(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_21)

    def run_test_21(self):
        async def main():
            conn = None
            try:
                # Attempt connection
                conn = await ibm_db_dbi.connect_async(
                    "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                        config.database, config.hostname, config.port,
                        config.user, config.password),
                    '', '')
                print("Connected:", conn)

                # Run error APIs on a good connection
                err_msg = await ibm_db_dbi.conn_errormsg_async(conn.conn_handler)
                print("conn_errormsg_async (good conn):", repr(err_msg))

                err_code = await ibm_db_dbi.conn_error_async(conn.conn_handler)
                print("conn_error_async (good conn):", repr(err_code))

                sqlcode = await ibm_db_dbi.get_sqlcode_async()
                print("get_sqlcode_async:", repr(sqlcode))

            except Exception as e:
                # Connection itself failed
                print("Connection failed:", e)

                # Run error APIs without a valid conn_handler
                try:
                    err_msg = await ibm_db_dbi.conn_errormsg_async(None)
                    print("conn_errormsg_async (failed conn):", repr(err_msg))
                except Exception as e2:
                    print("conn_errormsg_async raised:", e2)

                try:
                    err_code = await ibm_db_dbi.conn_error_async(None)
                    print("conn_error_async (failed conn):", repr(err_code))
                except Exception as e2:
                    print("conn_error_async raised:", e2)

                try:
                    sqlcode = await ibm_db_dbi.get_sqlcode_async()
                    print("get_sqlcode_async (failed conn):", repr(sqlcode))
                except Exception as e2:
                    print("get_sqlcode_async raised:", e2)

            finally:
                if conn:
                    conn.close()
                    print("Connection closed.")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Connected: <ibm_db_dbi.Connection object at %s>
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#Connection closed.
#__ZOS_EXPECTED__
#Connected: <ibm_db_dbi.Connection object at %s>
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#Connection closed.
#__SYSTEMI_EXPECTED__
#Connected: <ibm_db_dbi.Connection object at %s>
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#Connection closed.
#__IDS_EXPECTED__
#Connected: <ibm_db_dbi.Connection object at %s>
#conn_errormsg_async (good conn): ''
#conn_error_async (good conn): ''
#get_sqlcode_async: ''
#Connection closed.
