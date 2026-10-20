from __future__ import print_function
import asyncio
import datetime
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_37_async_timestamp_precision_fetch(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_37)

    def run_test_37(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            for p in (6, 9, 10, 11, 12):
                ts = "CAST('2024-01-02 03:04:05.123456789012' AS TIMESTAMP(%d))" % p

                await cursor.execute("VALUES " + ts)
                row = await cursor.fetchone()
                print("%d fetchone %s %s" % (p, isinstance(row[0], datetime.datetime), row[0]))

                await cursor.execute("VALUES (%s), (%s)" % (ts, ts))
                rows = await cursor.fetchall()
                print("%d fetchall %d %s" % (p, len(rows), all(r[0] == row[0] for r in rows)))

            await cursor.close()
            await conn.close()

        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#6 fetchone True 2024-01-02 03:04:05.123456
#6 fetchall 2 True
#9 fetchone True 2024-01-02 03:04:05.123456
#9 fetchall 2 True
#10 fetchone True 2024-01-02 03:04:05.123456
#10 fetchall 2 True
#11 fetchone True 2024-01-02 03:04:05.123456
#11 fetchall 2 True
#12 fetchone True 2024-01-02 03:04:05.123456
#12 fetchall 2 True
#__ZOS_EXPECTED__
#6 fetchone True 2024-01-02 03:04:05.123456
#6 fetchall 2 True
#9 fetchone True 2024-01-02 03:04:05.123456
#9 fetchall 2 True
#10 fetchone True 2024-01-02 03:04:05.123456
#10 fetchall 2 True
#11 fetchone True 2024-01-02 03:04:05.123456
#11 fetchall 2 True
#12 fetchone True 2024-01-02 03:04:05.123456
#12 fetchall 2 True
#__SYSTEMI_EXPECTED__
#6 fetchone True 2024-01-02 03:04:05.123456
#6 fetchall 2 True
#9 fetchone True 2024-01-02 03:04:05.123456
#9 fetchall 2 True
#10 fetchone True 2024-01-02 03:04:05.123456
#10 fetchall 2 True
#11 fetchone True 2024-01-02 03:04:05.123456
#11 fetchall 2 True
#12 fetchone True 2024-01-02 03:04:05.123456
#12 fetchall 2 True
#__IDS_EXPECTED__
#6 fetchone True 2024-01-02 03:04:05.123456
#6 fetchall 2 True
#9 fetchone True 2024-01-02 03:04:05.123456
#9 fetchall 2 True
#10 fetchone True 2024-01-02 03:04:05.123456
#10 fetchall 2 True
#11 fetchone True 2024-01-02 03:04:05.123456
#11 fetchall 2 True
#12 fetchone True 2024-01-02 03:04:05.123456
#12 fetchall 2 True
