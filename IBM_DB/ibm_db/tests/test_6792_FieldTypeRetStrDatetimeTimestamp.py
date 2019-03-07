#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2013
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_6792_FieldTypeRetStrDatetimeTimestamp(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6792)

    def run_test_6792(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            drop = 'DROP TABLE table_6792'
            result = ''
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass

            t_val = '10:42:34'
            d_val = '1981-07-08'
            ts_val = '1981-07-08 10:42:34'
            ts_withT_val = '2013-06-06T15:30:39'

            server = ibm_db.server_info( conn )
            if (server.DBMS_NAME[0:3] == 'IDS'):
                statement = "CREATE TABLE table_6792 (col1 DATETIME HOUR TO SECOND, col2 DATE, col3 DATETIME YEAR TO SECOND, col4 DATETIME YEAR TO SECOND)"
                result = ibm_db.exec_immediate(conn, statement)
                statement = "INSERT INTO table_6792 (col1, col2, col3) values (?, ?, ?)"
                stmt = ibm_db.prepare(conn, statement)
                result = ibm_db.execute(stmt, (t_val, d_val, ts_val))
            else:
                statement = "CREATE TABLE table_6792 (col1 TIME, col2 DATE, col3 TIMESTAMP, col4 TIMESTAMP)"
                result = ibm_db.exec_immediate(conn, statement)
                statement = "INSERT INTO table_6792 (col1, col2, col3, col4) values (?, ?, ?, ?)"
                stmt = ibm_db.prepare(conn, statement)
                result = ibm_db.execute(stmt, (t_val, d_val, ts_val, ts_withT_val))

            statement = "SELECT * FROM table_6792"
            result = ibm_db.exec_immediate(conn, statement)

            for i in range(0, ibm_db.num_fields(result)):
                print(str(i) + ":" + ibm_db.field_type(result,i))

            statement = "SELECT * FROM table_6792"
            stmt = ibm_db.prepare(conn, statement)
            rc = ibm_db.execute(stmt)
            result = ibm_db.fetch_row(stmt)
            while ( result ):
                row0 = ibm_db.result(stmt, 0)
                row1 = ibm_db.result(stmt, 1)
                row2 = ibm_db.result(stmt, 2)
                row3 = ibm_db.result(stmt, 3)
                print(row0)
                print(row1)
                print(row2)
                print(row3)
                result = ibm_db.fetch_row(stmt)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#0:time
#1:date
#2:timestamp
#3:timestamp
#10:42:34
#1981-07-08
#1981-07-08 10:42:34
#2013-06-06 15:30:39
#__ZOS_EXPECTED__
#0:time
#1:date
#2:timestamp
#3:timestamp
#10:42:34
#1981-07-08
#1981-07-08 10:42:34
#2013-06-06 15:30:39
#__SYSTEMI_EXPECTED__
#0:time
#1:date
#2:timestamp
#3:timestamp
#10:42:34
#1981-07-08
#1981-07-08 10:42:34
#2013-06-06 15:30:39
#__IDS_EXPECTED__
#0:time
#1:date
#2:timestamp
#3:timestamp
#10:42:34
#1981-07-08
#1981-07-08 10:42:34
#2013-06-06 15:30:39
