from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_22_async_scalar_bind_callproc(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_22)

    def run_test_22(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # Create stored procedure
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

            # Prepare + bind + execute
            await cursor.prepare("CALL ASYNC_TEST_DOUBLE(?,?)")
            await cursor.bind_param(1, 123456, ibm_db.SQL_PARAM_INPUT)
            await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
            await cursor.execute()

            result = await cursor.fetch_callproc()
            print("Input: 123456")
            print("fetch_callproc result:", result)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Input: 123456
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 123456, 246912)
#__ZOS_EXPECTED__
#Input: 123456
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 123456, 246912)
#__SYSTEMI_EXPECTED__
#Input: 123456
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 123456, 246912)
#__IDS_EXPECTED__
#Input: 123456
#fetch_callproc result: (<ibm_db.IBM_DBStatement object at %s>, 123456, 246912)
