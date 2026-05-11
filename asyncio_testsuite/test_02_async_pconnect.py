from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_02_async_pconnect(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_02)

    def run_test_02(self):
        async def main():
            conn = await ibm_db_dbi.pconnect_async(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            print("Persistent connection:", conn)
            info = conn.server_info()
            print("Server info:", info)
            conn.close()
            print("Connection closed.")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Persistent connection: <ibm_db_dbi.Connection object at %s>
#Server info: (%s)
#Connection closed.
#__ZOS_EXPECTED__
#Persistent connection: <ibm_db_dbi.Connection object at %s>
#Server info: (%s)
#Connection closed.
#__SYSTEMI_EXPECTED__
#Persistent connection: <ibm_db_dbi.Connection object at %s>
#Server info: (%s)
#Connection closed.
#__IDS_EXPECTED__
#Persistent connection: <ibm_db_dbi.Connection object at %s>
#Server info: (%s)
#Connection closed.
