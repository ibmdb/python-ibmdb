from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_29_async_reprepare(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_29)

    def run_test_29(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # First query
            await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 2 ROWS ONLY")
            rows1 = await cursor.fetchall()
            print("Query 1:", rows1)

            # Re-execute with different SQL on same cursor
            await cursor.execute("SELECT DEPTNO, DEPTNAME FROM DEPARTMENT FETCH FIRST 2 ROWS ONLY")
            rows2 = await cursor.fetchall()
            print("Query 2:", rows2)

            # Re-prepare with bind_param
            await cursor.prepare("SELECT ID, NAME FROM STAFF WHERE ID = ?")
            await cursor.bind_param(1, 30)
            await cursor.execute()
            row = await cursor.fetchone()
            print("Query 3 (prepared):", row)

            await cursor.close()
            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Query 1: [(10, 'Sanders'), (20, 'Pernal')]
#Query 2: [('A00', 'SPIFFY COMPUTER SERVICE DIV.'), ('B01', 'PLANNING')]
#Query 3 (prepared): (30, 'Marenghi')
#__ZOS_EXPECTED__
#Query 1: [(10, 'Sanders'), (20, 'Pernal')]
#Query 2: [('A00', 'SPIFFY COMPUTER SERVICE DIV.'), ('B01', 'PLANNING')]
#Query 3 (prepared): (30, 'Marenghi')
#__SYSTEMI_EXPECTED__
#Query 1: [(10, 'Sanders'), (20, 'Pernal')]
#Query 2: [('A00', 'SPIFFY COMPUTER SERVICE DIV.'), ('B01', 'PLANNING')]
#Query 3 (prepared): (30, 'Marenghi')
#__IDS_EXPECTED__
#Query 1: [(10, 'Sanders'), (20, 'Pernal')]
#Query 2: [('A00', 'SPIFFY COMPUTER SERVICE DIV.'), ('B01', 'PLANNING')]
#Query 3 (prepared): (30, 'Marenghi')
