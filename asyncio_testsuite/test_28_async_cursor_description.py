from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_28_async_cursor_description(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_28)

    def run_test_28(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            await cursor.execute("SELECT ID, NAME, JOB, SALARY FROM STAFF FETCH FIRST 1 ROWS ONLY")

            # Description is populated after execute
            desc = cursor.description
            print("cursor.description:")
            if desc:
                for col in desc:
                    print("  %s" % (col,))
            else:
                print("  description is None (may need async fetch of description)")

            row = await cursor.fetchone()
            print("First row:", row)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#cursor.description:
#  ['ID', DBAPITypeObject(%s), 6, 6, 5, 0, False]
#  ['NAME', DBAPITypeObject(%s), 9, 9, 9, 0, True]
#  ['JOB', DBAPITypeObject(%s), 5, 5, 5, 0, True]
#  ['SALARY', DBAPITypeObject(%s), 9, 9, 7, 2, True]
#First row: (10, 'Sanders', 'Mgr  ', Decimal('18357.50'))
#__ZOS_EXPECTED__
#cursor.description:
#  ['ID', DBAPITypeObject(%s), 6, 6, 5, 0, False]
#  ['NAME', DBAPITypeObject(%s), 9, 9, 9, 0, True]
#  ['JOB', DBAPITypeObject(%s), 5, 5, 5, 0, True]
#  ['SALARY', DBAPITypeObject(%s), 9, 9, 7, 2, True]
#First row: (10, 'Sanders', 'Mgr  ', Decimal('18357.50'))
#__SYSTEMI_EXPECTED__
#cursor.description:
#  ['ID', DBAPITypeObject(%s), 6, 6, 5, 0, False]
#  ['NAME', DBAPITypeObject(%s), 9, 9, 9, 0, True]
#  ['JOB', DBAPITypeObject(%s), 5, 5, 5, 0, True]
#  ['SALARY', DBAPITypeObject(%s), 9, 9, 7, 2, True]
#First row: (10, 'Sanders', 'Mgr  ', Decimal('18357.50'))
#__IDS_EXPECTED__
#cursor.description:
#  ['ID', DBAPITypeObject(%s), 6, 6, 5, 0, False]
#  ['NAME', DBAPITypeObject(%s), 9, 9, 9, 0, True]
#  ['JOB', DBAPITypeObject(%s), 5, 5, 5, 0, True]
#  ['SALARY', DBAPITypeObject(%s), 9, 9, 7, 2, True]
#First row: (10, 'Sanders', 'Mgr  ', Decimal('18357.50'))
