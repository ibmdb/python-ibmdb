from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_26_async_inout_param(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_26)

    def run_test_26(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # Create stored procedure with INOUT
            try:
                await cursor.execute("""
                    CREATE PROCEDURE ASYNC_TEST_INOUT(INOUT val INTEGER)
                    LANGUAGE SQL
                    BEGIN
                        SET val = val + 100;
                    END
                """)
            except Exception:
                pass

            await cursor.prepare("CALL ASYNC_TEST_INOUT(?)")
            await cursor.bind_param(1, 42, ibm_db.SQL_PARAM_INPUT_OUTPUT)
            await cursor.execute()

            result = await cursor.fetch_callproc()
            print("Input: 42, Expected output: 142")
            print("fetch_callproc result:", result)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Input: 42, Expected output: 142
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 142)
#__ZOS_EXPECTED__
#Input: 42, Expected output: 142
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 142)
#__SYSTEMI_EXPECTED__
#Input: 42, Expected output: 142
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 142)
#__IDS_EXPECTED__
#Input: 42, Expected output: 142
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 142)
