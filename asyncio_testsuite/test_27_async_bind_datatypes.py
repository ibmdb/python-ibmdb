from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_27_async_bind_datatypes(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_27)

    def run_test_27(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            await conn.set_autocommit(True)
            cursor = await conn.cursor()

            # Create temp table with multiple types
            try:
                await cursor.execute("DROP TABLE ASYNC_TEST_TYPES")
            except Exception:
                pass
            await cursor.execute("""
                CREATE TABLE ASYNC_TEST_TYPES (
                    ID INTEGER,
                    NAME VARCHAR(50),
                    AMOUNT DECIMAL(10,2),
                    ACTIVE SMALLINT
                )
            """)

            # Prepare and bind different types
            await cursor.prepare("INSERT INTO ASYNC_TEST_TYPES VALUES (?, ?, ?, ?)")
            await cursor.bind_param(1, 1)
            await cursor.bind_param(2, 'Test Name')
            await cursor.bind_param(3, '99.95')
            await cursor.bind_param(4, 1)
            await cursor.execute()

            # Verify
            await cursor.execute("SELECT * FROM ASYNC_TEST_TYPES")
            row = await cursor.fetchone()
            print("Inserted row:", row)
            print("  ID type:", type(row[0]))
            print("  NAME type:", type(row[1]))
            print("  AMOUNT type:", type(row[2]))

            # Cleanup
            await cursor.execute("DROP TABLE ASYNC_TEST_TYPES")

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Inserted row: (1, 'Test Name', Decimal('99.95'), 1)
#  ID type: <class 'int'>
#  NAME type: <class 'str'>
#  AMOUNT type: <class 'decimal.Decimal'>
#__ZOS_EXPECTED__
#Inserted row: (1, 'Test Name', Decimal('99.95'), 1)
#  ID type: <class 'int'>
#  NAME type: <class 'str'>
#  AMOUNT type: <class 'decimal.Decimal'>
#__SYSTEMI_EXPECTED__
#Inserted row: (1, 'Test Name', Decimal('99.95'), 1)
#  ID type: <class 'int'>
#  NAME type: <class 'str'>
#  AMOUNT type: <class 'decimal.Decimal'>
#__IDS_EXPECTED__
#Inserted row: (1, 'Test Name', Decimal('99.95'), 1)
#  ID type: <class 'int'>
#  NAME type: <class 'str'>
#  AMOUNT type: <class 'decimal.Decimal'>
