from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_07_async_execute_params(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_07)

    def run_test_07(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # SELECT with positional parameter
            await cursor.execute(
                "SELECT ID, NAME, JOB, SALARY FROM STAFF WHERE ID = ?",
                (20,)
            )
            row = await cursor.fetchone()
            print("Staff ID 20:", row)

            # SELECT with multiple parameters
            await cursor.execute(
                "SELECT ID, NAME, JOB FROM STAFF WHERE DEPT = ? AND JOB = ?",
                (20, 'Sales')
            )
            rows = await cursor.fetchall()
            print("Dept 20 Sales (%d rows):" % len(rows))
            for r in rows:
                print("  ", r)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#Dept 20 Sales (1 rows):
#   (20, 'Pernal', 'Sales')
#__ZOS_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#Dept 20 Sales (1 rows):
#   (20, 'Pernal', 'Sales')
#__SYSTEMI_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#Dept 20 Sales (1 rows):
#   (20, 'Pernal', 'Sales')
#__IDS_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#Dept 20 Sales (1 rows):
#   (20, 'Pernal', 'Sales')
