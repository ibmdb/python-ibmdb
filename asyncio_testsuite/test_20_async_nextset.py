from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_20_async_nextset(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_20)

    def run_test_20(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # Create a procedure that returns two result sets
            try:
                await cursor.execute("DROP PROCEDURE ASYNC_TEST_MULTI_RS")
            except Exception:
                pass
            await cursor.execute("""
                CREATE PROCEDURE ASYNC_TEST_MULTI_RS()
                LANGUAGE SQL
                DYNAMIC RESULT SETS 2
                BEGIN
                    DECLARE c1 CURSOR WITH RETURN FOR
                        SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY;
                    DECLARE c2 CURSOR WITH RETURN FOR
                        SELECT DEPTNO, DEPTNAME FROM DEPARTMENT FETCH FIRST 3 ROWS ONLY;
                    OPEN c1;
                    OPEN c2;
                END
            """)

            # Call the stored procedure
            await cursor.callproc("ASYNC_TEST_MULTI_RS")

            # First result set
            print("Result set 1:")
            rows1 = await cursor.fetchall()
            for r in rows1:
                print("  ", r)

            # Move to next result set
            has_next = await cursor.nextset()
            print("nextset returned:", has_next)

            if has_next:
                print("Result set 2:")
                rows2 = await cursor.fetchall()
                for r in rows2:
                    print("  ", r)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Result set 1:
#   (10, 'Sanders')
#   (20, 'Pernal')
#   (30, 'Marenghi')
#nextset returned: True
#Result set 2:
#   ('A00', 'SPIFFY COMPUTER SERVICE DIV.')
#   ('B01', 'PLANNING')
#   ('C01', 'INFORMATION CENTER')
#__ZOS_EXPECTED__
#Result set 1:
#   (10, 'Sanders')
#   (20, 'Pernal')
#   (30, 'Marenghi')
#nextset returned: True
#Result set 2:
#   ('A00', 'SPIFFY COMPUTER SERVICE DIV.')
#   ('B01', 'PLANNING')
#   ('C01', 'INFORMATION CENTER')
#__SYSTEMI_EXPECTED__
#Result set 1:
#   (10, 'Sanders')
#   (20, 'Pernal')
#   (30, 'Marenghi')
#nextset returned: True
#Result set 2:
#   ('A00', 'SPIFFY COMPUTER SERVICE DIV.')
#   ('B01', 'PLANNING')
#   ('C01', 'INFORMATION CENTER')
#__IDS_EXPECTED__
#Result set 1:
#   (10, 'Sanders')
#   (20, 'Pernal')
#   (30, 'Marenghi')
#nextset returned: True
#Result set 2:
#   ('A00', 'SPIFFY COMPUTER SERVICE DIV.')
#   ('B01', 'PLANNING')
#   ('C01', 'INFORMATION CENTER')
