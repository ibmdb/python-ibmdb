from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_23_async_concurrent_queries(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_23)

    def run_test_23(self):
        async def query_staff(conn, staff_id):
            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT ID, NAME, JOB FROM STAFF WHERE ID = ?",
                (staff_id,)
            )
            row = await cursor.fetchone()
            await cursor.close()
            return row

        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            # Run 3 queries concurrently
            results = await asyncio.gather(
                query_staff(conn, 10),
                query_staff(conn, 20),
                query_staff(conn, 30),
            )

            for r in results:
                print(r)

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#(10, 'Sanders', 'Mgr  ')
#(20, 'Pernal', 'Sales')
#(30, 'Marenghi', 'Mgr  ')
#__ZOS_EXPECTED__
#(10, 'Sanders', 'Mgr  ')
#(20, 'Pernal', 'Sales')
#(30, 'Marenghi', 'Mgr  ')
#__SYSTEMI_EXPECTED__
#(10, 'Sanders', 'Mgr  ')
#(20, 'Pernal', 'Sales')
#(30, 'Marenghi', 'Mgr  ')
#__IDS_EXPECTED__
#(10, 'Sanders', 'Mgr  ')
#(20, 'Pernal', 'Sales')
#(30, 'Marenghi', 'Mgr  ')
