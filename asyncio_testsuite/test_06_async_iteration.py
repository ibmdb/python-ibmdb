from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_06_async_iteration(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_06)

    def run_test_06(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 5 ROWS ONLY")

            count = 0
            async for row in cursor:
                print(row)
                count += 1
            print("Iterated over %d rows" % count)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#(40, 'OBrien')
#(50, 'Hanes')
#Iterated over 5 rows
#__ZOS_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#(40, 'OBrien')
#(50, 'Hanes')
#Iterated over 5 rows
#__SYSTEMI_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#(40, 'OBrien')
#(50, 'Hanes')
#Iterated over 5 rows
#__IDS_EXPECTED__
#(10, 'Sanders')
#(20, 'Pernal')
#(30, 'Marenghi')
#(40, 'OBrien')
#(50, 'Hanes')
#Iterated over 5 rows
