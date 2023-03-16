#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2021
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions
from datetime import date, time, datetime
from decimal import Decimal


class IbmDbTestCase(unittest.TestCase):
    def test_alltypes(self):
        self.maxDiff = None
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_alltypes)

    def run_test_alltypes(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            serverinfo = ibm_db.server_info( conn )

            drop = "DROP TABLE TESTTYPES"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the table of all data types
            if (serverinfo.DBMS_NAME[0:3] == 'IDS'):
                create = "CREATE TABLE TESTTYPES(C1 BIGINT, C2 BOOLEAN, C3 BOOLEAN, C4 DATE, C5 DECIMAL(16), C6 DECIMAL(34), C7 DECIMAL(16,2), C8 DECIMAL(16,2), C9 DECIMAL(16,2), C10 INTEGER, C11 BINARY(30), C12 BLOB(30), C13 Char(30), C14 CLOB(30), C15 DBCLOB(30), C16 TIMESTAMP, C17 VARBINARY(30), C18 VARChar(30), C19 TIME, C20 TIMESTAMP, C21 BINARY(40), C22 BLOB(40), C23 Char(40), C24 CLOB(40), C25 DBCLOB(40), C26 TIMESTAMP, C27 VARBINARY(40), C28 VARChar(40))"
            elif (serverinfo.DBMS_NAME =="DB2" or serverinfo.DBMS_NAME =="DSN12015"):
                create = "CREATE TABLE TESTTYPES(C1 BIGINT, C2 DATE, C3 DECFLOAT(16), C4 DECFLOAT(34), C5 DECIMAL(16,2), C6 DECIMAL(16,2), C7 DECIMAL(16,2), C8 INTEGER, C9 BINARY(30), C10 BLOB(30), C11 Char(30), C12 CLOB(30), C13 TIMESTAMP, C14 VARChar(30), C15 TIME, C16 TIMESTAMP, C17 BINARY(40), C18 BLOB(40), C19 Char(40), C20 CLOB(40), C21 TIMESTAMP, C22 VARBINARY(40), C23 VARChar(40))"
            else:
                create = "CREATE TABLE TESTTYPES(C1 BIGINT, C2 BOOLEAN, C3 BOOLEAN, C4 DATE, C5 DECFLOAT(16), C6 DECFLOAT(34), C7 DECIMAL(16,2), C8 DECIMAL(16,2), C9 DECIMAL(16,2), C10 INTEGER, C11 BINARY(30), C12 BLOB(30), C13 Char(30), C14 CLOB(30), C15 DBCLOB(30), C16 TIMESTAMP, C17 VARBINARY(30), C18 VARChar(30), C19 TIME, C20 TIMESTAMP, C21 BINARY(40), C22 BLOB(40), C23 Char(40), C24 CLOB(40), C25 DBCLOB(40), C26 TIMESTAMP, C27 VARBINARY(40), C28 VARChar(40))"

            result = ibm_db.exec_immediate(conn, create)

            if(not serverinfo.DBMS_NAME.startswith("DB2/")):
                insert = "insert into TESTTYPES values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            else:
                insert = "insert into TESTTYPES values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            stmt = ibm_db.prepare(conn,insert)

            if(serverinfo.DBMS_NAME != "DSN12015"):
                rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT : 10}, 0)

            try:
                if(not serverinfo.DBMS_NAME.startswith("DB2/")):
                    ibm_db.bind_param(stmt, 1,  870000, 				ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 2,  date(1982, 2, 12), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 3,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 4,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 5,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 6,  8723.45, 				ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 7,  8723, 					ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 8, 87, 					    ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 9, b'To Test BINARY', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 10, b'To Test Blob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 11, b'To Test Char', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 12, b'To Test Clob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 13, b'1981-07-08 10:42:34.000010', ibm_db.SQL_PARAM_INPUT)	#String Timestamp
                    ibm_db.bind_param(stmt, 14, b'To Test VARChar', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 15, time(12, 35, 45), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 16, datetime(2017, 11, 28, 23, 55, 59, 342380), ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 17, 'To Test UniBINARY', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 18, 'To Test UniBlob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 19, 'To Test UniChar', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 20, 'To Test UniClob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 21, '1981-07-08 10:42:34.000010', ibm_db.SQL_PARAM_INPUT)	#Unicode Timestamp
                    ibm_db.bind_param(stmt, 22, 'To Test UniVARBINARY', ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 23, 'To Test UniVARChar', 	ibm_db.SQL_PARAM_INPUT)
                else:
                    ibm_db.bind_param(stmt, 1,  870000, 				ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 2,  True, 					ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 3,  False, 					ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 4,  date(1982, 2, 12), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 5,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 6,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 7,  Decimal('8723'), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 8,  8723.45, 				ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 9,  8723, 					ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 10, 87, 					ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 11, b'To Test BINARY', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 12, b'To Test Blob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 13, b'To Test Char', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 14, b'To Test Clob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 15, b'To Test DBClob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 16, b'1981-07-08 10:42:34.000010', ibm_db.SQL_PARAM_INPUT)	#String Timestamp
                    ibm_db.bind_param(stmt, 17, b'To Test VARBINARY', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 18, b'To Test VARChar', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 19, time(12, 35, 45), 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 20, datetime(2017, 11, 28, 23, 55, 59, 342380), ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 21, 'To Test UniBINARY', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 22, 'To Test UniBlob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 23, 'To Test UniChar', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 24, 'To Test UniClob', 		ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 25, 'To Test UniDBClob', 	ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 26, '1981-07-08 10:42:34.000010', ibm_db.SQL_PARAM_INPUT)	#Unicode Timestamp
                    ibm_db.bind_param(stmt, 27, 'To Test UniVARBINARY', ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 28, 'To Test UniVARChar', 	ibm_db.SQL_PARAM_INPUT)
                error = ibm_db.execute(stmt)
            except:
                excp = sys.exc_info()
                # slot 1 contains error message
                print(excp[1])

            # Select the result from the table and
            query = "select * from TESTTYPES"
            exe = ibm_db.exec_immediate(conn,query)

            row = ibm_db.fetch_tuple(exe)
            rcount = 1
            while row:
                count = 1
                for col in row:
                    print("Column:" + str(count) + ' ' +  str(col))
                    count += 1
                print("-------------------")
                row = ibm_db.fetch_tuple(exe)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Column:1 870000
#Column:2 True
#Column:3 False
#Column:4 1982-02-12
#Column:5 8723
#Column:6 8723
#Column:7 8723.00
#Column:8 8723.45
#Column:9 8723.00
#Column:10 87
#Column:11 b'To Test BINARY\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob'
#Column:13 To Test Char                  
#Column:14 To Test Clob
#Column:15 To Test DBClob
#Column:16 1981-07-08 10:42:34.000010
#Column:17 b'To Test VARBINARY'
#Column:18 To Test VARChar
#Column:19 12:35:45
#Column:20 2017-11-28 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00B\x00I\x00N\x00A\x00R\x00Y\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00B\x00l\x00o\x00b\x00'
#Column:23 To Test UniChar                         
#Column:24 To Test UniClob
#Column:25 To Test UniDBClob
#Column:26 1981-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00V\x00A\x00R\x00B\x00I\x00N\x00A\x00R\x00Y\x00'
#Column:28 To Test UniVARChar
#-------------------
#__ZOS_EXPECTED__
#Column:1 870000
#Column:2 1982-02-12
#Column:3 8723
#Column:4 8723
#Column:5 8723.00
#Column:6 8723.45
#Column:7 8723.00
#Column:8 87
#Column:9 b'To Test BINARY\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob'
#Column:11 To Test Char                  
#Column:12 To Test Clob
#Column:13 1981-07-08 10:42:34.000010
#Column:14 To Test VARChar
#Column:15 12:35:45
#Column:16 2017-11-28 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00B\x00I\x00N\x00A\x00R\x00Y\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00B\x00l\x00o\x00b\x00'
#Column:19 To Test UniChar                         
#Column:20 To Test UniClob
#Column:21 1981-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00U\x00n\x00i\x00V\x00A\x00R\x00B\x00I\x00N\x00A\x00R\x00Y\x00'
#Column:23 To Test UniVARChar
#-------------------
#__SYSTEMI_EXPECTED__
#Boolean is not supported
#__IDS_EXPECTED__
#Boolean is not supported
