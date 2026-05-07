from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_05_async_fetch(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_05)

    def run_test_05(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            await cursor.execute("SELECT ID, NAME, JOB FROM STAFF FETCH FIRST 10 ROWS ONLY")

            # fetchone
            row = await cursor.fetchone()
            print("fetchone:", row)

            # fetchmany
            rows = await cursor.fetchmany(size=3)
            print("fetchmany(3):", rows)

            # fetchall (remaining)
            remaining = await cursor.fetchall()
            print("fetchall remaining:", remaining)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#fetchone: (10, 'Sanders', 'Mgr  ')
#fetchmany(3): [(20, 'Pernal', 'Sales'), (30, 'Marenghi', 'Mgr  '), (40, 'OBrien', 'Sales')]
#fetchall remaining: [(50, 'Hanes', 'Mgr  '), (60, 'Quigley', 'Sales'), (70, 'Rothman', 'Sales'), (80, 'James', 'Clerk'), (90, 'Koonitz', 'Sales'), (100, 'Plotz', 'Mgr  ')]
#__ZOS_EXPECTED__
#fetchone: (10, 'Sanders', 'Mgr  ')
#fetchmany(3): [(20, 'Pernal', 'Sales'), (30, 'Marenghi', 'Mgr  '), (40, 'OBrien', 'Sales')]
#fetchall remaining: [(50, 'Hanes', 'Mgr  '), (60, 'Quigley', 'Sales'), (70, 'Rothman', 'Sales'), (80, 'James', 'Clerk'), (90, 'Koonitz', 'Sales'), (100, 'Plotz', 'Mgr  ')]
#__SYSTEMI_EXPECTED__
#fetchone: (10, 'Sanders', 'Mgr  ')
#fetchmany(3): [(20, 'Pernal', 'Sales'), (30, 'Marenghi', 'Mgr  '), (40, 'OBrien', 'Sales')]
#fetchall remaining: [(50, 'Hanes', 'Mgr  '), (60, 'Quigley', 'Sales'), (70, 'Rothman', 'Sales'), (80, 'James', 'Clerk'), (90, 'Koonitz', 'Sales'), (100, 'Plotz', 'Mgr  ')]
#__IDS_EXPECTED__
#fetchone: (10, 'Sanders', 'Mgr  ')
#fetchmany(3): [(20, 'Pernal', 'Sales'), (30, 'Marenghi', 'Mgr  '), (40, 'OBrien', 'Sales')]
#fetchall remaining: [(50, 'Hanes', 'Mgr  '), (60, 'Quigley', 'Sales'), (70, 'Rothman', 'Sales'), (80, 'James', 'Clerk'), (90, 'Koonitz', 'Sales'), (100, 'Plotz', 'Mgr  ')]
