#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_unicodeTable(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_unicodeTable)

    def run_test_unicodeTable(self):
        try:
            connection = ibm_db.connect(config.database, config.user, config.password)
            print("=> Connected to Server ... SUCCESSFULL")
        except:
            print("=> Connection to server .... FAILED")
            print("Error Description = " + ibm_db.conn_errormsg())
            print("SQLSTATE = " + ibm_db.conn_error())
            return 0

        serverInfo = ibm_db.server_info(connection)

        if("IDS" in serverInfo.DBMS_NAME):
            print("No run for IDS")
            return 0

        print("=> Server Type = " + serverInfo.DBMS_NAME)

        print("=> Create table with unicode Column Name")

        table_create = "Create TABLE test_uni(\"åÅÕ\" int, \"ñéü\" int)"
        table_drop = "drop table test_uni"

        try:
            rc = ibm_db.exec_immediate(connection,table_create)
        except:
            rc = ibm_db.exec_immediate(connection,table_drop)
            rc = ibm_db.exec_immediate(connection,table_create)

        print("=> Table Created...")

        print("=> Getting field type of the table with unicode column")

        select = "select * from test_uni"

        rc = ibm_db.exec_immediate(connection,select)

        for i in range(0,ibm_db.num_fields(rc)):
            print("=> ROW : " + str(i) + "[" + str(ibm_db.field_type(rc,i)) + "]")
            print("=> COL NAME : " + str(i) + "[" + str(ibm_db.field_name(rc,i)) + "]")

        print("=> Insert data into table with unicode column")

        insert = "insert into test_uni(\"åÅÕ\",\"ñéü\") values(1,2)"

        rc = ibm_db.exec_immediate(connection,insert)

        print("=> Fetching data from table with unicode column")

        select = "select \"ñéü\" from test_uni"

        rc = ibm_db.exec_immediate(connection,select)
        row = ibm_db.fetch_tuple(rc)

        print("=> Using fetch_tuple")

        while row:
            print(row[0])
            row = ibm_db.fetch_tuple(rc)

        print("=> Using fetch_assoc")
        rc = ibm_db.exec_immediate(connection,select)
        row = ibm_db.fetch_assoc(rc)

        while row:
            print(row)
            row = ibm_db.fetch_assoc(rc)

        print("=> Create table with unicode character in table name")

        create2 = "create table \"ÆÈÊ\" (\"åÅÕ\" int, \"ñéü\" varchar(20))"
        drop2 = "drop table \"ÆÈÊ\""

        try:
            rc = ibm_db.exec_immediate(connection,create2)
        except:
            rc = ibm_db.exec_immediate(connection,drop2)
            rc = ibm_db.exec_immediate(connection,create2)

        print("=> Table created")

        print("=> Insert data into unicode named table")

        insert2 = "insert into \"ÆÈÊ\"(\"åÅÕ\",\"ñéü\") values(1,\'data1\')"

        rc = ibm_db.exec_immediate(connection,insert2)

        print("=> Getting field type of the unicode named table")

        select = "select * from \"ÆÈÊ\""

        rc = ibm_db.exec_immediate(connection,select)

        for i in range(0,ibm_db.num_fields(rc)):
            print("=> ROW : " + str(i) + "[" + str(ibm_db.field_type(rc,i)) + "]")
            print("=> COL NAME : " + str(i) + "[" + str(ibm_db.field_name(rc,i)) + "]")

        print("=> Fetching data from unicode named table")

        select = "select \"ñéü\" from \"ÆÈÊ\""

        rc = ibm_db.exec_immediate(connection,select)
        row = ibm_db.fetch_tuple(rc)

        print("=> Using Fetch Tuple")

        while row:
            print(row[0])
            row = ibm_db.fetch_tuple(rc)

        print("=> Using fetch_assoc")

        rc = ibm_db.exec_immediate(connection,select)
        row = ibm_db.fetch_assoc(rc)

        while row:
            print(row)
            row = ibm_db.fetch_assoc(rc)

#__END__
#__LUW_EXPECTED__
#=> Connected to Server ... SUCCESSFULL
#=> Server Type = DB2/LINUXX8664
#=> Create table with unicode Column Name
#=> Table Created...
#=> Getting field type of the table with unicode column
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[int]
#=> COL NAME : 1[ñéü]
#=> Insert data into table with unicode column
#=> Fetching data from table with unicode column
#=> Using fetch_tuple
#2
#=> Using fetch_assoc
#{'ñéü': 2}
#=> Create table with unicode character in table name
#=> Table created
#=> Insert data into unicode named table
#=> Getting field type of the unicode named table
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[string]
#=> COL NAME : 1[ñéü]
#=> Fetching data from unicode named table
#=> Using Fetch Tuple
#data1
#=> Using fetch_assoc
#{'ñéü': 'data1'}
#__ZOS_EXPECTED__
#=> Connected to Server ... SUCCESSFULL
#=> Server Type = DB2
#=> Create table with unicode Column Name
#=> Table Created...
#=> Getting field type of the table with unicode column
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[int]
#=> COL NAME : 1[ñéü]
#=> Insert data into table with unicode column
#=> Fetching data from table with unicode column
#=> Using fetch_tuple
#2
#=> Using fetch_assoc
#{'ñéü': 2}
#=> Create table with unicode character in table name
#=> Table created
#=> Insert data into unicode named table
#=> Getting field type of the unicode named table
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[string]
#=> COL NAME : 1[ñéü]
#=> Fetching data from unicode named table
#=> Using Fetch Tuple
#data1
#=> Using fetch_assoc
#{'ñéü': 'data1'}
#__SYSTEMI_EXPECTED__
#=> Connected to Server ... SUCCESSFULL
#=> Server Type = AS
#=> Create table with unicode Column Name
#=> Table Created...
#=> Getting field type of the table with unicode column
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[int]
#=> COL NAME : 1[ñéü]
#=> Insert data into table with unicode column
#=> Fetching data from table with unicode column
#=> Using fetch_tuple
#2
#=> Using fetch_assoc
#{'ñéü': 2}
#=> Create table with unicode character in table name
#=> Table created
#=> Insert data into unicode named table
#=> Getting field type of the unicode named table
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[string]
#=> COL NAME : 1[ñéü]
#=> Fetching data from unicode named table
#=> Using Fetch Tuple
#data1
#=> Using fetch_assoc
#{'ñéü': 'data1'}
#__IDS_EXPECTED__
#=> Connected to Server ... SUCCESSFULL
#No run for IDS
#__ZOS_ODBC_EXPECTED__
#=> Connected to Server ... SUCCESSFULL
#=> Server Type = DSN12015
#=> Create table with unicode Column Name
#=> Table Created...
#=> Getting field type of the table with unicode column
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[int]
#=> COL NAME : 1[ñéü]
#=> Insert data into table with unicode column
#=> Fetching data from table with unicode column
#=> Using fetch_tuple
#2
#=> Using fetch_assoc
#{'ñéü': 2}
#=> Create table with unicode character in table name
#=> Table created
#=> Insert data into unicode named table
#=> Getting field type of the unicode named table
#=> ROW : 0[int]
#=> COL NAME : 0[åÅÕ]
#=> ROW : 1[string]
#=> COL NAME : 1[ñéü]
#=> Fetching data from unicode named table
#=> Using Fetch Tuple
#data1
#=> Using fetch_assoc
#{'ñéü': 'data1'}