from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_08_async_prepare_bind_execute(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_08)

    def run_test_08(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            await cursor.prepare("SELECT ID, NAME, JOB, SALARY FROM STAFF WHERE ID = ?")
            await cursor.bind_param(1, 20)
            await cursor.execute()

            row = await cursor.fetchone()
            print("Staff ID 20:", row)

            while row:
                row = await cursor.fetchone()
                if row:
                    print(row)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#__ZOS_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#__SYSTEMI_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
#__IDS_EXPECTED__
#Staff ID 20: (20, 'Pernal', 'Sales', Decimal('18171.25'))
