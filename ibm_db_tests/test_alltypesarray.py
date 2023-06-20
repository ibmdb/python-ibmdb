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
    def test_alltypesarray(self):
        self.maxDiff = None
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_alltypesarray)

    def run_test_alltypesarray(self):
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
                rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_PARAM_BIND_TYPE : ibm_db.SQL_PARAM_BIND_BY_COLUMN}, 0)
                rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT : 10}, 0)
            rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_PARAMSET_SIZE : 10}, 0)

            arr1 = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 80000000, 9000000, 1000000]
            arr2 = [False, False, False, False, False, False, False, False, False, False]
            arr3 = [True, True, True, True, True, True, True, True, True, True]
            arr4 = [date(1981, 2, 12), date(1982, 2, 12), date(1983, 2, 12), date(1984, 2, 12), date(1985, 2, 12), date(1986, 2, 12), date(1987, 2, 12), date(1988, 2, 12), date(1989, 2, 12), date(1990, 2, 12)]
            arr5 = [Decimal('1000000'), Decimal('2000000'), Decimal('3000000'), Decimal('4000000'), Decimal('5000000'), Decimal('6000000'), Decimal('7000000'), Decimal('8000000'), Decimal('9000000'), Decimal('1000000')]
            arr6 = [Decimal('1000000'), Decimal('2000000'), Decimal('3000000'), Decimal('4000000'), Decimal('5000000'), Decimal('6000000'), Decimal('7000000'), Decimal('8000000'), Decimal('9000000'), Decimal('1000000')]
            arr7 = [Decimal('1000000'), Decimal('2000000'), Decimal('3000000'), Decimal('4000000'), Decimal('5000000'), Decimal('6000000'), Decimal('7000000'), Decimal('8000000'), Decimal('9000000'), Decimal('1000000')]
            arr8 = [123.23, 234.34, 345.45, 456.56, 567.67, 578.78, 789.89, 890.90, 901.01, 1234.23]
            arr9 = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 1000000]
            arr10 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            arr11 = [b'To Test Binary1', b'To Test Binary2', b'To Test Binary3', b'To Test Binary4', b'To Test Binary5', b'To Test Binary6', b'To Test Binary7', b'To Test Binary8', b'To Test Binary9', b'To Test Binary10']
            arr12 = [b'To Test Blob1', b'To Test Blob2', b'To Test Blob3', b'To Test Blob4', b'To Test Blob5', b'To Test Blob6', b'To Test Blob7', b'To Test Blob8', b'To Test Blob9', b'To Test Blob10']
            arr13 = [b'To Test Char1', b'To Test Char2', b'To Test Char3', b'To Test Char4', b'To Test Char5', b'To Test Char6', b'To Test Char7', b'To Test Char8', b'To Test Char9', b'To Test Char10']
            arr14 = [b'To Test Clob1', b'To Test Clob2', b'To Test Clob3', b'To Test Clob4', b'To Test Clob5', b'To Test Clob6', b'To Test Clob7', b'To Test Clob8', b'To Test Clob9', b'To Test Clob10']
            arr15 = [b'To Test DBClob1', b'To Test DBClob2', b'To Test DBClob3', b'To Test DBClob4', b'To Test DBClob5', b'To Test DBClob6', b'To Test DBClob7', b'To Test DBClob8', b'To Test DBClob9', b'To Test DBClob10']
            arr16 = [b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010', b'1983-07-08 10:42:34.000010', b'1984-07-08 10:42:34.000010', b'1985-07-08 10:42:34.000010', b'1986-07-08 10:42:34.000010', b'1987-07-08 10:42:34.000010', b'1988-07-08 10:42:34.000010', b'1989-07-08 10:42:34.000010', b'1990-07-08 10:42:34.000010']
            arr17 = [b'To Test VarBinary1', b'To Test VarBinary2', b'To Test VarBinary3', b'To Test VarBinary4', b'To Test VarBinary5', b'To Test VarBinary6', b'To Test VarBinary7', b'To Test VarBinary8', b'To Test VarBinary9', b'To Test VarBinary10']
            arr18 = [b'To Test VARChar1', b'To Test VARChar2', b'To Test VARChar3', b'To Test VARChar4', b'To Test VARChar5', b'To Test VARChar6', b'To Test VARChar7', b'To Test VARChar8', b'To Test VARChar9', b'To Test VARChar10']
            arr19 = [time(12, 20, 30), time(13, 30, 45), time(14, 2, 12), time(15, 42, 33), time(5, 29, 59), time(8, 2, 12), time(9, 52, 12), time(7, 2, 12), time(23, 2, 12), time(19, 59, 59)]
            arr20 = [datetime(1981, 2, 12, 23, 55, 59, 342380), datetime(1982, 2, 12, 23, 55, 59, 342380), datetime(1983, 2, 12, 23, 55, 59, 342380), datetime(1984, 2, 12, 23, 55, 59, 342380), datetime(1985, 2, 12, 23, 55, 59, 342380), datetime(1986, 2, 12, 23, 55, 59, 342380), datetime(1987, 2, 12, 23, 55, 59, 342380), datetime(1988, 2, 12, 23, 55, 59, 342380), datetime(1989, 2, 12, 23, 55, 59, 342380), datetime(1990, 2, 12, 23, 55, 59, 342380)]
            arr21 = ['To Test Binary1', 'To Test Binary2', 'To Test Binary3', 'To Test Binary4', 'To Test Binary5', 'To Test Binary6', 'To Test Binary7', 'To Test Binary8', 'To Test Binary9', 'To Test Binary10']
            arr22 = ['To Test Blob1', 'To Test Blob2', 'To Test Blob3', 'To Test Blob4', 'To Test Blob5', 'To Test Blob6', 'To Test Blob7', 'To Test Blob8', 'To Test Blob9', 'To Test Blob10']
            arr23 = ['To Test Char1', 'To Test Char2', 'To Test Char3', 'To Test Char4', 'To Test Char5', 'To Test Char6', 'To Test Char7', 'To Test Char8', 'To Test Char9', 'To Test Char10']
            arr24 = ['To Test Clob1', 'To Test Clob2', 'To Test Clob3', 'To Test Clob4', 'To Test Clob5', 'To Test Clob6', 'To Test Clob7', 'To Test Clob8', 'To Test Clob9', 'To Test Clob10']
            arr25 = ['To Test DBClob1', 'To Test DBClob2', 'To Test DBClob3', 'To Test DBClob4', 'To Test DBClob5', 'To Test DBClob6', 'To Test DBClob7', 'To Test DBClob8', 'To Test DBClob9', 'To Test DBClob10']
            arr26 = ['1981-07-08 10:42:34.000010', '1982-07-08 10:42:34.000010', '1983-07-08 10:42:34.000010', '1984-07-08 10:42:34.000010', '1985-07-08 10:42:34.000010', '1986-07-08 10:42:34.000010', '1987-07-08 10:42:34.000010', '1988-07-08 10:42:34.000010', '1989-07-08 10:42:34.000010', '1990-07-08 10:42:34.000010']
            arr27 = ['To Test VarBinary1', 'To Test VarBinary2', 'To Test VarBinary3', 'To Test VarBinary4', 'To Test VarBinary5', 'To Test VarBinary6', 'To Test VarBinary7', 'To Test VarBinary8', 'To Test VarBinary9', 'To Test VarBinary10']
            arr28 = ['To Test VARChar1', 'To Test VARChar2', 'To Test VARChar3', 'To Test VARChar4', 'To Test VARChar5', 'To Test VARChar6', 'To Test VARChar7', 'To Test VARChar8', 'To Test VARChar9', 'To Test VARChar10']

            try:
                if(not serverinfo.DBMS_NAME.startswith("DB2/")):
                    ibm_db.bind_param(stmt, 1,  arr1, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 2,  arr4, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 3,  arr5, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 4,  arr6, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 5,  arr7, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 6,  arr8, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 7,  arr9, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 8, arr10,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 9, arr11,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 10, arr12,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 11, arr13,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 12, arr14,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 13, arr16,ibm_db.SQL_PARAM_INPUT)		#String Timestamp
                    ibm_db.bind_param(stmt, 14, arr18,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 15, arr19,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 16, arr20,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 17, arr21,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 18, arr22,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 19, arr23,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 20, arr24,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 21, arr26,ibm_db.SQL_PARAM_INPUT)		#Unicode Timestamp
                    ibm_db.bind_param(stmt, 22, arr27,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 23, arr28,ibm_db.SQL_PARAM_INPUT)
                else:
                    ibm_db.bind_param(stmt, 1,  arr1, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 2,  arr2, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 3,  arr3, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 4,  arr4, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 5,  arr5, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 6,  arr6, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 7,  arr7, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 8,  arr8, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 9,  arr9, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 10, arr10,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 11, arr11,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 12, arr12,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 13, arr13,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 14, arr14,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 15, arr15,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 16, arr16,ibm_db.SQL_PARAM_INPUT)		#String Timestamp
                    ibm_db.bind_param(stmt, 17, arr17,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 18, arr18,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 19, arr19,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 20, arr20,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 21, arr21,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 22, arr22,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 23, arr23,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 24, arr24,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 25, arr25,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 26, arr26,ibm_db.SQL_PARAM_INPUT)		#Unicode Timestamp
                    ibm_db.bind_param(stmt, 27, arr27,ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 28, arr28,ibm_db.SQL_PARAM_INPUT)
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
                print("ROW:" + str(rcount))
                count = 1
                for col in row:
                    print("Column:" + str(count) + ' ' +  str(col))
                    count += 1
                print("-------------------")
                rcount += 1
                row = ibm_db.fetch_tuple(exe)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#ROW:1
#Column:1 1000000
#Column:2 False
#Column:3 True
#Column:4 1981-02-12
#Column:5 1000000
#Column:6 1000000
#Column:7 1000000.00
#Column:8 123.23
#Column:9 1000000.00
#Column:10 10
#Column:11 b'To Test Binary1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob1'
#Column:13 To Test Char1                 
#Column:14 To Test Clob1
#Column:15 To Test DBClob1
#Column:16 1981-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary1'
#Column:18 To Test VARChar1
#Column:19 12:20:30
#Column:20 1981-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x001\x00'
#Column:23 To Test Char1                           
#Column:24 To Test Clob1
#Column:25 To Test DBClob1
#Column:26 1981-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x001\x00'
#Column:28 To Test VARChar1
#-------------------
#ROW:2
#Column:1 2000000
#Column:2 False
#Column:3 True
#Column:4 1982-02-12
#Column:5 2000000
#Column:6 2000000
#Column:7 2000000.00
#Column:8 234.34
#Column:9 2000000.00
#Column:10 20
#Column:11 b'To Test Binary2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob2'
#Column:13 To Test Char2                 
#Column:14 To Test Clob2
#Column:15 To Test DBClob2
#Column:16 1982-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary2'
#Column:18 To Test VARChar2
#Column:19 13:30:45
#Column:20 1982-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x002\x00'
#Column:23 To Test Char2                           
#Column:24 To Test Clob2
#Column:25 To Test DBClob2
#Column:26 1982-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x002\x00'
#Column:28 To Test VARChar2
#-------------------
#ROW:3
#Column:1 3000000
#Column:2 False
#Column:3 True
#Column:4 1983-02-12
#Column:5 3000000
#Column:6 3000000
#Column:7 3000000.00
#Column:8 345.45
#Column:9 3000000.00
#Column:10 30
#Column:11 b'To Test Binary3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob3'
#Column:13 To Test Char3                 
#Column:14 To Test Clob3
#Column:15 To Test DBClob3
#Column:16 1983-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary3'
#Column:18 To Test VARChar3
#Column:19 14:02:12
#Column:20 1983-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x003\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x003\x00'
#Column:23 To Test Char3                           
#Column:24 To Test Clob3
#Column:25 To Test DBClob3
#Column:26 1983-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x003\x00'
#Column:28 To Test VARChar3
#-------------------
#ROW:4
#Column:1 4000000
#Column:2 False
#Column:3 True
#Column:4 1984-02-12
#Column:5 4000000
#Column:6 4000000
#Column:7 4000000.00
#Column:8 456.56
#Column:9 4000000.00
#Column:10 40
#Column:11 b'To Test Binary4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob4'
#Column:13 To Test Char4                 
#Column:14 To Test Clob4
#Column:15 To Test DBClob4
#Column:16 1984-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary4'
#Column:18 To Test VARChar4
#Column:19 15:42:33
#Column:20 1984-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x004\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x004\x00'
#Column:23 To Test Char4                           
#Column:24 To Test Clob4
#Column:25 To Test DBClob4
#Column:26 1984-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x004\x00'
#Column:28 To Test VARChar4
#-------------------
#ROW:5
#Column:1 5000000
#Column:2 False
#Column:3 True
#Column:4 1985-02-12
#Column:5 5000000
#Column:6 5000000
#Column:7 5000000.00
#Column:8 567.67
#Column:9 5000000.00
#Column:10 50
#Column:11 b'To Test Binary5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob5'
#Column:13 To Test Char5                 
#Column:14 To Test Clob5
#Column:15 To Test DBClob5
#Column:16 1985-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary5'
#Column:18 To Test VARChar5
#Column:19 05:29:59
#Column:20 1985-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x005\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x005\x00'
#Column:23 To Test Char5                           
#Column:24 To Test Clob5
#Column:25 To Test DBClob5
#Column:26 1985-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x005\x00'
#Column:28 To Test VARChar5
#-------------------
#ROW:6
#Column:1 6000000
#Column:2 False
#Column:3 True
#Column:4 1986-02-12
#Column:5 6000000
#Column:6 6000000
#Column:7 6000000.00
#Column:8 578.78
#Column:9 6000000.00
#Column:10 60
#Column:11 b'To Test Binary6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob6'
#Column:13 To Test Char6                 
#Column:14 To Test Clob6
#Column:15 To Test DBClob6
#Column:16 1986-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary6'
#Column:18 To Test VARChar6
#Column:19 08:02:12
#Column:20 1986-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x006\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x006\x00'
#Column:23 To Test Char6                           
#Column:24 To Test Clob6
#Column:25 To Test DBClob6
#Column:26 1986-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x006\x00'
#Column:28 To Test VARChar6
#-------------------
#ROW:7
#Column:1 7000000
#Column:2 False
#Column:3 True
#Column:4 1987-02-12
#Column:5 7000000
#Column:6 7000000
#Column:7 7000000.00
#Column:8 789.89
#Column:9 7000000.00
#Column:10 70
#Column:11 b'To Test Binary7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob7'
#Column:13 To Test Char7                 
#Column:14 To Test Clob7
#Column:15 To Test DBClob7
#Column:16 1987-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary7'
#Column:18 To Test VARChar7
#Column:19 09:52:12
#Column:20 1987-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x007\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x007\x00'
#Column:23 To Test Char7                           
#Column:24 To Test Clob7
#Column:25 To Test DBClob7
#Column:26 1987-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x007\x00'
#Column:28 To Test VARChar7
#-------------------
#ROW:8
#Column:1 80000000
#Column:2 False
#Column:3 True
#Column:4 1988-02-12
#Column:5 8000000
#Column:6 8000000
#Column:7 8000000.00
#Column:8 890.90
#Column:9 8000000.00
#Column:10 80
#Column:11 b'To Test Binary8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob8'
#Column:13 To Test Char8                 
#Column:14 To Test Clob8
#Column:15 To Test DBClob8
#Column:16 1988-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary8'
#Column:18 To Test VARChar8
#Column:19 07:02:12
#Column:20 1988-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x008\x00'
#Column:23 To Test Char8                           
#Column:24 To Test Clob8
#Column:25 To Test DBClob8
#Column:26 1988-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x008\x00'
#Column:28 To Test VARChar8
#-------------------
#ROW:9
#Column:1 9000000
#Column:2 False
#Column:3 True
#Column:4 1989-02-12
#Column:5 9000000
#Column:6 9000000
#Column:7 9000000.00
#Column:8 901.01
#Column:9 9000000.00
#Column:10 90
#Column:11 b'To Test Binary9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob9'
#Column:13 To Test Char9                 
#Column:14 To Test Clob9
#Column:15 To Test DBClob9
#Column:16 1989-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary9'
#Column:18 To Test VARChar9
#Column:19 23:02:12
#Column:20 1989-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x009\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x009\x00'
#Column:23 To Test Char9                           
#Column:24 To Test Clob9
#Column:25 To Test DBClob9
#Column:26 1989-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x009\x00'
#Column:28 To Test VARChar9
#-------------------
#ROW:10
#Column:1 1000000
#Column:2 False
#Column:3 True
#Column:4 1990-02-12
#Column:5 1000000
#Column:6 1000000
#Column:7 1000000.00
#Column:8 1234.23
#Column:9 1000000.00
#Column:10 100
#Column:11 b'To Test Binary10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:12 b'To Test Blob10'
#Column:13 To Test Char10                
#Column:14 To Test Clob10
#Column:15 To Test DBClob10
#Column:16 1990-07-08 10:42:34.000010
#Column:17 b'To Test VarBinary10'
#Column:18 To Test VARChar10
#Column:19 19:59:59
#Column:20 1990-02-12 23:55:59.342380
#Column:21 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x001\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x001\x000\x00'
#Column:23 To Test Char10                          
#Column:24 To Test Clob10
#Column:25 To Test DBClob10
#Column:26 1990-07-08 10:42:34.000010
#Column:27 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x001\x000\x00'
#Column:28 To Test VARChar10
#-------------------
#__ZOS_EXPECTED__
#ROW:1
#Column:1 1000000
#Column:2 1981-02-12
#Column:3 1000000
#Column:4 1000000
#Column:5 1000000.00
#Column:6 123.23
#Column:7 1000000.00
#Column:8 10
#Column:9 b'To Test Binary1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob1'
#Column:11 To Test Char1                 
#Column:12 To Test Clob1
#Column:13 1981-07-08 10:42:34.000010
#Column:14 To Test VARChar1
#Column:15 12:20:30
#Column:16 1981-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x001\x00'
#Column:19 To Test Char1                           
#Column:20 To Test Clob1
#Column:21 1981-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x001\x00'
#Column:23 To Test VARChar1
#-------------------
#ROW:2
#Column:1 2000000
#Column:2 1982-02-12
#Column:3 2000000
#Column:4 2000000
#Column:5 2000000.00
#Column:6 234.34
#Column:7 2000000.00
#Column:8 20
#Column:9 b'To Test Binary2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob2'
#Column:11 To Test Char2                 
#Column:12 To Test Clob2
#Column:13 1982-07-08 10:42:34.000010
#Column:14 To Test VARChar2
#Column:15 13:30:45
#Column:16 1982-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x002\x00'
#Column:19 To Test Char2                           
#Column:20 To Test Clob2
#Column:21 1982-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x002\x00'
#Column:23 To Test VARChar2
#-------------------
#ROW:3
#Column:1 3000000
#Column:2 1983-02-12
#Column:3 3000000
#Column:4 3000000
#Column:5 3000000.00
#Column:6 345.45
#Column:7 3000000.00
#Column:8 30
#Column:9 b'To Test Binary3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob3'
#Column:11 To Test Char3                 
#Column:12 To Test Clob3
#Column:13 1983-07-08 10:42:34.000010
#Column:14 To Test VARChar3
#Column:15 14:02:12
#Column:16 1983-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x003\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x003\x00'
#Column:19 To Test Char3                           
#Column:20 To Test Clob3
#Column:21 1983-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x003\x00'
#Column:23 To Test VARChar3
#-------------------
#ROW:4
#Column:1 4000000
#Column:2 1984-02-12
#Column:3 4000000
#Column:4 4000000
#Column:5 4000000.00
#Column:6 456.56
#Column:7 4000000.00
#Column:8 40
#Column:9 b'To Test Binary4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob4'
#Column:11 To Test Char4                 
#Column:12 To Test Clob4
#Column:13 1984-07-08 10:42:34.000010
#Column:14 To Test VARChar4
#Column:15 15:42:33
#Column:16 1984-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x004\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x004\x00'
#Column:19 To Test Char4                           
#Column:20 To Test Clob4
#Column:21 1984-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x004\x00'
#Column:23 To Test VARChar4
#-------------------
#ROW:5
#Column:1 5000000
#Column:2 1985-02-12
#Column:3 5000000
#Column:4 5000000
#Column:5 5000000.00
#Column:6 567.67
#Column:7 5000000.00
#Column:8 50
#Column:9 b'To Test Binary5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob5'
#Column:11 To Test Char5                 
#Column:12 To Test Clob5
#Column:13 1985-07-08 10:42:34.000010
#Column:14 To Test VARChar5
#Column:15 05:29:59
#Column:16 1985-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x005\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x005\x00'
#Column:19 To Test Char5                           
#Column:20 To Test Clob5
#Column:21 1985-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x005\x00'
#Column:23 To Test VARChar5
#-------------------
#ROW:6
#Column:1 6000000
#Column:2 1986-02-12
#Column:3 6000000
#Column:4 6000000
#Column:5 6000000.00
#Column:6 578.78
#Column:7 6000000.00
#Column:8 60
#Column:9 b'To Test Binary6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob6'
#Column:11 To Test Char6                 
#Column:12 To Test Clob6
#Column:13 1986-07-08 10:42:34.000010
#Column:14 To Test VARChar6
#Column:15 08:02:12
#Column:16 1986-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x006\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x006\x00'
#Column:19 To Test Char6                           
#Column:20 To Test Clob6
#Column:21 1986-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x006\x00'
#Column:23 To Test VARChar6
#-------------------
#ROW:7
#Column:1 7000000
#Column:2 1987-02-12
#Column:3 7000000
#Column:4 7000000
#Column:5 7000000.00
#Column:6 789.89
#Column:7 7000000.00
#Column:8 70
#Column:9 b'To Test Binary7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob7'
#Column:11 To Test Char7                 
#Column:12 To Test Clob7
#Column:13 1987-07-08 10:42:34.000010
#Column:14 To Test VARChar7
#Column:15 09:52:12
#Column:16 1987-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x007\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x007\x00'
#Column:19 To Test Char7                           
#Column:20 To Test Clob7
#Column:21 1987-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x007\x00'
#Column:23 To Test VARChar7
#-------------------
#ROW:8
#Column:1 80000000
#Column:2 1988-02-12
#Column:3 8000000
#Column:4 8000000
#Column:5 8000000.00
#Column:6 890.90
#Column:7 8000000.00
#Column:8 80
#Column:9 b'To Test Binary8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob8'
#Column:11 To Test Char8                 
#Column:12 To Test Clob8
#Column:13 1988-07-08 10:42:34.000010
#Column:14 To Test VARChar8
#Column:15 07:02:12
#Column:16 1988-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x008\x00'
#Column:19 To Test Char8                           
#Column:20 To Test Clob8
#Column:21 1988-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x008\x00'
#Column:23 To Test VARChar8
#-------------------
#ROW:9
#Column:1 9000000
#Column:2 1989-02-12
#Column:3 9000000
#Column:4 9000000
#Column:5 9000000.00
#Column:6 901.01
#Column:7 9000000.00
#Column:8 90
#Column:9 b'To Test Binary9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob9'
#Column:11 To Test Char9                 
#Column:12 To Test Clob9
#Column:13 1989-07-08 10:42:34.000010
#Column:14 To Test VARChar9
#Column:15 23:02:12
#Column:16 1989-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x009\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x009\x00'
#Column:19 To Test Char9                           
#Column:20 To Test Clob9
#Column:21 1989-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x009\x00'
#Column:23 To Test VARChar9
#-------------------
#ROW:10
#Column:1 1000000
#Column:2 1990-02-12
#Column:3 1000000
#Column:4 1000000
#Column:5 1000000.00
#Column:6 1234.23
#Column:7 1000000.00
#Column:8 100
#Column:9 b'To Test Binary10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:10 b'To Test Blob10'
#Column:11 To Test Char10                
#Column:12 To Test Clob10
#Column:13 1990-07-08 10:42:34.000010
#Column:14 To Test VARChar10
#Column:15 19:59:59
#Column:16 1990-02-12 23:55:59.342380
#Column:17 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00i\x00n\x00a\x00r\x00y\x001\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#Column:18 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00B\x00l\x00o\x00b\x001\x000\x00'
#Column:19 To Test Char10                          
#Column:20 To Test Clob10
#Column:21 1990-07-08 10:42:34.000010
#Column:22 b'T\x00o\x00 \x00T\x00e\x00s\x00t\x00 \x00V\x00a\x00r\x00B\x00i\x00n\x00a\x00r\x00y\x001\x000\x00'
#Column:23 To Test VARChar10
#-------------------
