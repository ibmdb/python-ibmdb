from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_09_async_callproc(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_09)

    def run_test_09(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # Create stored procedure (ignore error if already exists)
            try:
                await cursor.execute("""
                    CREATE PROCEDURE ASYNC_TEST_DOUBLE(IN val BIGINT, OUT result BIGINT)
                    LANGUAGE SQL
                    BEGIN
                        SET result = val * 2;
                    END
                """)
            except Exception:
                pass

            # Call procedure via callproc
            result = await cursor.callproc("ASYNC_TEST_DOUBLE", (42, 0))
            print("callproc result:", result)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#callproc result: (42, 84)
#__ZOS_EXPECTED__
#callproc result: (42, 84)
#__SYSTEMI_EXPECTED__
#callproc result: (42, 84)
#__IDS_EXPECTED__
#callproc result: (42, 84)
