from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_12_async_commit_rollback(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_12)

    def run_test_12(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            await conn.set_autocommit(False)
            cursor = await conn.cursor()

            # Create temp table
            try:
                await cursor.execute("DROP TABLE ASYNC_TEST_TXN")
            except Exception:
                pass
            await conn.commit()
            await cursor.execute("CREATE TABLE ASYNC_TEST_TXN (ID INT, VAL VARCHAR(20))")
            await conn.commit()

            # Insert and rollback
            await cursor.execute("INSERT INTO ASYNC_TEST_TXN VALUES (1, 'should_disappear')")
            await conn.rollback()
            await cursor.execute("SELECT COUNT(*) FROM ASYNC_TEST_TXN")
            row = await cursor.fetchone()
            print("After rollback, count:", row[0])
            assert row[0] == 0, "Rollback failed"

            # Insert and commit
            await cursor.execute("INSERT INTO ASYNC_TEST_TXN VALUES (2, 'should_stay')")
            await conn.commit()
            await cursor.execute("SELECT * FROM ASYNC_TEST_TXN")
            row = await cursor.fetchone()
            print("After commit:", row)
            assert row is not None, "Commit failed"

            # Cleanup
            await cursor.execute("DROP TABLE ASYNC_TEST_TXN")
            await conn.commit()

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#After rollback, count: 0
#After commit: (2, 'should_stay')
#__ZOS_EXPECTED__
#After rollback, count: 0
#After commit: (2, 'should_stay')
#__SYSTEMI_EXPECTED__
#After rollback, count: 0
#After commit: (2, 'should_stay')
#__IDS_EXPECTED__
#After rollback, count: 0
#After commit: (2, 'should_stay')
