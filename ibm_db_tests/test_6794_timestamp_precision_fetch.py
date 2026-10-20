#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2026
#

from __future__ import print_function
import datetime
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_6794_timestamp_precision_fetch(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6794)

    def run_test_6794(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            server = ibm_db.server_info(conn)
            if (server.DBMS_NAME[0:3] == 'IDS'):
                print("SKIPPED")
                ibm_db.close(conn)
                return

            for p in (6, 9, 10, 11, 12):
                sql = "VALUES CAST('2024-01-02 03:04:05.123456789012' AS TIMESTAMP(%d))" % p
                stmt = ibm_db.exec_immediate(conn, sql)
                row = ibm_db.fetch_tuple(stmt)

                print("%d %s %s" % (p, isinstance(row[0], datetime.datetime), row[0]))

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#6 True 2024-01-02 03:04:05.123456
#9 True 2024-01-02 03:04:05.123456
#10 True 2024-01-02 03:04:05.123456
#11 True 2024-01-02 03:04:05.123456
#12 True 2024-01-02 03:04:05.123456
#__ZOS_EXPECTED__
#6 True 2024-01-02 03:04:05.123456
#9 True 2024-01-02 03:04:05.123456
#10 True 2024-01-02 03:04:05.123456
#11 True 2024-01-02 03:04:05.123456
#12 True 2024-01-02 03:04:05.123456
#__SYSTEMI_EXPECTED__
#6 True 2024-01-02 03:04:05.123456
#9 True 2024-01-02 03:04:05.123456
#10 True 2024-01-02 03:04:05.123456
#11 True 2024-01-02 03:04:05.123456
#12 True 2024-01-02 03:04:05.123456
#__IDS_EXPECTED__
#SKIPPED
