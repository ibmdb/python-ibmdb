from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_11_async_executemany(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_11)

    def run_test_11(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            await conn.set_autocommit(True)
            cursor = await conn.cursor()

            # Create temp table
            try:
                await cursor.execute("DROP TABLE ASYNC_TEST_BATCH")
            except Exception:
                pass
            await cursor.execute("CREATE TABLE ASYNC_TEST_BATCH (ID INT, NAME VARCHAR(30))")

            # Insert multiple rows
            data = [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
            await cursor.executemany("INSERT INTO ASYNC_TEST_BATCH (ID, NAME) VALUES (?, ?)", data)
            print("Inserted %d rows" % len(data))

            # Verify
            await cursor.execute("SELECT * FROM ASYNC_TEST_BATCH ORDER BY ID")
            rows = await cursor.fetchall()
            print("Rows:", rows)

            # Cleanup
            await cursor.execute("DROP TABLE ASYNC_TEST_BATCH")

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Inserted 4 rows
#Rows: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
#__ZOS_EXPECTED__
#Inserted 4 rows
#Rows: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
#__SYSTEMI_EXPECTED__
#Inserted 4 rows
#Rows: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
#__IDS_EXPECTED__
#Inserted 4 rows
#Rows: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
