from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_13_async_autocommit(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_13)

    def run_test_13(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            # Turn autocommit ON
            result = await conn.set_autocommit(True)
            print("set_autocommit(True):", result)

            # Turn autocommit OFF
            result = await conn.set_autocommit(False)
            print("set_autocommit(False):", result)

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#set_autocommit(True): True
#set_autocommit(False): True
#__ZOS_EXPECTED__
#set_autocommit(True): True
#set_autocommit(False): True
#__SYSTEMI_EXPECTED__
#set_autocommit(True): True
#set_autocommit(False): True
#__IDS_EXPECTED__
#set_autocommit(True): True
#set_autocommit(False): True
