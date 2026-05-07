from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_19_async_dml(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_19)

    def run_test_19(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            await conn.set_autocommit(True)
            cursor = await conn.cursor()

            # Setup
            try:
                await cursor.execute("DROP TABLE ASYNC_TEST_DML")
            except Exception:
                pass
            await cursor.execute("CREATE TABLE ASYNC_TEST_DML (ID INT, NAME VARCHAR(30))")

            # INSERT
            await cursor.execute("INSERT INTO ASYNC_TEST_DML VALUES (1, 'Alice')")
            print("Insert rowcount:", cursor.rowcount)

            await cursor.execute("INSERT INTO ASYNC_TEST_DML VALUES (2, 'Bob')")
            await cursor.execute("INSERT INTO ASYNC_TEST_DML VALUES (3, 'Charlie')")

            # UPDATE
            await cursor.execute("UPDATE ASYNC_TEST_DML SET NAME = 'ALICE_UPDATED' WHERE ID = 1")
            print("Update rowcount:", cursor.rowcount)

            # DELETE
            await cursor.execute("DELETE FROM ASYNC_TEST_DML WHERE ID = 2")
            print("Delete rowcount:", cursor.rowcount)

            # Verify
            await cursor.execute("SELECT * FROM ASYNC_TEST_DML ORDER BY ID")
            rows = await cursor.fetchall()
            print("Remaining rows:", rows)

            # Cleanup
            await cursor.execute("DROP TABLE ASYNC_TEST_DML")

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Insert rowcount: 1
#Update rowcount: 1
#Delete rowcount: 1
#Remaining rows: [(1, 'ALICE_UPDATED'), (3, 'Charlie')]
#__ZOS_EXPECTED__
#Insert rowcount: 1
#Update rowcount: 1
#Delete rowcount: 1
#Remaining rows: [(1, 'ALICE_UPDATED'), (3, 'Charlie')]
#__SYSTEMI_EXPECTED__
#Insert rowcount: 1
#Update rowcount: 1
#Delete rowcount: 1
#Remaining rows: [(1, 'ALICE_UPDATED'), (3, 'Charlie')]
#__IDS_EXPECTED__
#Insert rowcount: 1
#Update rowcount: 1
#Delete rowcount: 1
#Remaining rows: [(1, 'ALICE_UPDATED'), (3, 'Charlie')]
