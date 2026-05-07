from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_15_async_schema(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_15)

    def run_test_15(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            schema = await conn.get_current_schema()
            print("Current schema:", schema.upper())

            await conn.set_current_schema("TESTSCHEMA")
            schema = await conn.get_current_schema()
            print("After set schema:", schema)

            # Reset back to original
            await conn.set_current_schema(config.user.upper())
            schema = await conn.get_current_schema()
            print("After reset schema:", schema.upper())

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Current schema: %s
#After set schema: TESTSCHEMA
#After reset schema: %s
#__ZOS_EXPECTED__
#Current schema: %s
#After set schema: TESTSCHEMA
#After reset schema: %s
#__SYSTEMI_EXPECTED__
#Current schema: %s
#After set schema: TESTSCHEMA
#After reset schema: %s
#__IDS_EXPECTED__
#Current schema: %s
#After set schema: TESTSCHEMA
#After reset schema: %s
