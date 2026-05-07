from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_03_async_connection_class(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_03)

    def run_test_03(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            print("Connected via AsyncConnection.connect():", conn)

            cursor = await conn.cursor()
            print("Cursor created:", cursor)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Connected via AsyncConnection.connect(): <ibm_db_dbi.AsyncConnection object at %s>
#Cursor created: <ibm_db_dbi.AsyncCursor object at %s>
#__ZOS_EXPECTED__
#Connected via AsyncConnection.connect(): <ibm_db_dbi.AsyncConnection object at %s>
#Cursor created: <ibm_db_dbi.AsyncCursor object at %s>
#__SYSTEMI_EXPECTED__
#Connected via AsyncConnection.connect(): <ibm_db_dbi.AsyncConnection object at %s>
#Cursor created: <ibm_db_dbi.AsyncCursor object at %s>
#__IDS_EXPECTED__
#Connected via AsyncConnection.connect(): <ibm_db_dbi.AsyncConnection object at %s>
#Cursor created: <ibm_db_dbi.AsyncCursor object at %s>
