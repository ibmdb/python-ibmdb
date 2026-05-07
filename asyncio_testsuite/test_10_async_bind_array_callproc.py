from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_10_async_bind_array_callproc(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_10)

    def run_test_10(self):
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
                    CREATE PROCEDURE CLIARRAY.ARRAY_BINT12(IN var1 bint_array, OUT var2 BIGINT)
                    LANGUAGE SQL
                    BEGIN
                        SET var2 = CARDINALITY(var1);
                    END
                """)
            except Exception:
                pass

            # Prepare, bind array IN + scalar OUT, execute
            await cursor.prepare("CALL CLIARRAY.ARRAY_BINT12(?,?)")

            input_array = [10, 20, 30, 40, 50, 60, 70]
            output = 0

            await cursor.bind_param(1, input_array, ibm_db.SQL_PARAM_INPUT)
            await cursor.bind_param(2, output, ibm_db.SQL_PARAM_OUTPUT)

            await cursor.execute()

            result = await cursor.fetch_callproc()
            print("Input array:", input_array)
            print("fetch_callproc result (cardinality):", result)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Input array: [10, 20, 30, 40, 50, 60, 70]
#fetch_callproc result (cardinality): (<ibm_db.IBM_DBStatement object at %s>, [10, 20, 30, 40, 50, 60, 70], 7)
#__ZOS_EXPECTED__
#Input array: [10, 20, 30, 40, 50, 60, 70]
#fetch_callproc result (cardinality): (<ibm_db.IBM_DBStatement object at %s>, [10, 20, 30, 40, 50, 60, 70], 7)
#__SYSTEMI_EXPECTED__
#Input array: [10, 20, 30, 40, 50, 60, 70]
#fetch_callproc result (cardinality): (<ibm_db.IBM_DBStatement object at %s>, [10, 20, 30, 40, 50, 60, 70], 7)
#__IDS_EXPECTED__
#Input array: [10, 20, 30, 40, 50, 60, 70]
#fetch_callproc result (cardinality): (<ibm_db.IBM_DBStatement object at %s>, [10, 20, 30, 40, 50, 60, 70], 7)
