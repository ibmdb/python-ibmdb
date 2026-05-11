from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_18_async_fix_return_type(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_18)

    def run_test_18(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            await conn.set_autocommit(True)

            # Enable FIX_RETURN_TYPE
            await conn.set_fix_return_type(True)
            cursor = await conn.cursor()

            await cursor.execute("SELECT SALARY, COMM FROM STAFF WHERE ID = 20")
            row = await cursor.fetchone()
            print("With FIX_RETURN_TYPE=True:", row)
            print("  SALARY type:", type(row[0]))

            # Disable FIX_RETURN_TYPE
            await conn.set_fix_return_type(False)
            cursor2 = await conn.cursor()
            await cursor2.execute("SELECT SALARY, COMM FROM STAFF WHERE ID = 20")
            row2 = await cursor2.fetchone()
            print("With FIX_RETURN_TYPE=False:", row2)
            print("  SALARY type:", type(row2[0]))

            await cursor.close()
            await cursor2.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#With FIX_RETURN_TYPE=True: (Decimal('18171.25'), Decimal('612.45'))
#  SALARY type: <class 'decimal.Decimal'>
#With FIX_RETURN_TYPE=False: ('18171.25', '612.45')
#  SALARY type: <class 'str'>
#__ZOS_EXPECTED__
#With FIX_RETURN_TYPE=True: (Decimal('18171.25'), Decimal('612.45'))
#  SALARY type: <class 'decimal.Decimal'>
#With FIX_RETURN_TYPE=False: ('18171.25', '612.45')
#  SALARY type: <class 'str'>
#__SYSTEMI_EXPECTED__
#With FIX_RETURN_TYPE=True: (Decimal('18171.25'), Decimal('612.45'))
#  SALARY type: <class 'decimal.Decimal'>
#With FIX_RETURN_TYPE=False: ('18171.25', '612.45')
#  SALARY type: <class 'str'>
#__IDS_EXPECTED__
#With FIX_RETURN_TYPE=True: (Decimal('18171.25'), Decimal('612.45'))
#  SALARY type: <class 'decimal.Decimal'>
#With FIX_RETURN_TYPE=False: ('18171.25', '612.45')
#  SALARY type: <class 'str'>
