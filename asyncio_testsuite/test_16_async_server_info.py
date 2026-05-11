from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_16_async_server_info(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_16)

    def run_test_16(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            info = await conn.server_info()
            print("Server info (DBMS_NAME, DBMS_VER):", info)

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Server info (DBMS_NAME, DBMS_VER): (%s)
#__ZOS_EXPECTED__
#Server info (DBMS_NAME, DBMS_VER): (%s)
#__SYSTEMI_EXPECTED__
#Server info (DBMS_NAME, DBMS_VER): (%s)
#__IDS_EXPECTED__
#Server info (DBMS_NAME, DBMS_VER): (%s)
