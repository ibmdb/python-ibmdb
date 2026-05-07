from __future__ import print_function
import asyncio
import time
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_async_concurrent_mixed(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_misc)

    def run_test_misc(self):
        async def slow_query(conn):
            label = "slow_query"
            print("  [%s] started" % label)
            t0 = time.perf_counter()

            cursor = await conn.cursor()
            await cursor.execute("""
                SELECT COUNT(*) AS cnt, AVG(a.SALARY) AS avg_salary
                FROM STAFF a, STAFF b, STAFF c
            """)
            row = await cursor.fetchone()
            await cursor.close()

            elapsed = time.perf_counter() - t0
            print("  [%s] finished in %.3fs  =>  %s" % (label, elapsed, row))
            return row

        async def fast_query_1(conn):
            label = "fast_query_1"
            print("  [%s] started" % label)
            t0 = time.perf_counter()

            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT ID, NAME, DEPT, JOB FROM STAFF WHERE ID = ?",
                (10,)
            )
            row = await cursor.fetchone()
            await cursor.close()

            elapsed = time.perf_counter() - t0
            print("  [%s] finished in %.3fs  =>  %s" % (label, elapsed, row))
            return row

        async def fast_query_2(conn):
            label = "fast_query_2"
            print("  [%s] started" % label)
            t0 = time.perf_counter()

            cursor = await conn.cursor()
            await cursor.execute("SELECT COUNT(*) AS total FROM STAFF")
            row = await cursor.fetchone()
            await cursor.close()

            elapsed = time.perf_counter() - t0
            print("  [%s] finished in %.3fs  =>  %s" % (label, elapsed, row))
            return row

        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            overall_start = time.perf_counter()

            slow_result, fast1_result, fast2_result = await asyncio.gather(
                slow_query(conn),
                fast_query_1(conn),
                fast_query_2(conn),
            )

            overall_elapsed = time.perf_counter() - overall_start

            print("\n--- Results ---")
            print("  Slow  query : %s" % (slow_result,))
            print("  Fast query 1: %s" % (fast1_result,))
            print("  Fast query 2: %s" % (fast2_result,))
            print("\n  Total wall-clock time: %.3fs" % overall_elapsed)
            print("  (Should be close to the slow query time, not the sum of all three)")

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#%s
#__ZOS_EXPECTED__
#%s
#__SYSTEMI_EXPECTED__
#%s
#__IDS_EXPECTED__
#%s
