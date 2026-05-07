from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_04_async_context_manager(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_04)

    def run_test_04(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            async with conn:
                cursor = await conn.cursor()
                async with cursor:
                    await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
                    rows = await cursor.fetchall()
                    for row in rows:
                        print(row)
                print("Cursor auto-closed via __aexit__")
            print("Connection auto-closed via __aexit__")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#Cursor auto-closed via __aexit__
#Connection auto-closed via __aexit__
#__ZOS_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#Cursor auto-closed via __aexit__
#Connection auto-closed via __aexit__
#__SYSTEMI_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#Cursor auto-closed via __aexit__
#Connection auto-closed via __aexit__
#__IDS_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#Cursor auto-closed via __aexit__
#Connection auto-closed via __aexit__
