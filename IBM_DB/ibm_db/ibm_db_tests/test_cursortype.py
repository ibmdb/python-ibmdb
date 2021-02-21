#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2016
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    def test_cursortype(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_cursortype)

    def run_test_cursortype(self):
        if sys.platform == 'zos':
            options = {}
        else:
            options = { ibm_db.SQL_ATTR_INFO_PROGRAMNAME : 'TestProgram'}
        conn = ibm_db.connect(config.database, config.user, config.password, options)

        if conn:
            drop = "DROP TABLE TEMP_TEST"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the table temp_test

            create = "CREATE TABLE TEMP_TEST (id INTEGER, name CHAR(16))"
            result = ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO temp_test values (1, 'cat')"
            ibm_db.exec_immediate(conn, insert)

            print("Setting cursor type to SQL_CURSOR_FORWARD_ONLY")
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_FORWARD_ONLY}
            stmt = ibm_db.prepare(conn, "SELECT * FROM temp_test WHERE id > 1",op )
            val = ibm_db.cursor_type(stmt)
            print("statement cursor type = ", end="")
            print(val, end="\n")
            value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
            print(value)
            print()

            print("Setting cursor type to SQL_CURSOR_KEYSET_DRIVEN")
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN}
            stmt = ibm_db.prepare(conn, "SELECT * FROM temp_test", op)
            val = ibm_db.cursor_type(stmt)
            print("statement cursor type = ", end="")
            print(val,end="\n")
            value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
            print(value)
            print()

            print("Setting cursor type to SQL_CURSOR_STATIC")
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC}
            stmt = ibm_db.prepare(conn, "SELECT * FROM temp_test", op)
            val = ibm_db.cursor_type(stmt)
            print("statement cursor type = ", end="")
            print(val)
            value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
            print(value)
            print()

            print("Setting cursor type to SQL_CURSOR_DYNAMIC - zOS only")
            op = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_DYNAMIC}
            stmt = ibm_db.prepare(conn, "SELECT * FROM temp_test", op)
            val = ibm_db.cursor_type(stmt)
            print("statement cursor type = ", end="")
            print(val)
            value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_CURSOR_TYPE, 0)
            print(value)
            print()

            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Setting cursor type to SQL_CURSOR_FORWARD_ONLY
#statement cursor type = 0
#0
#Setting cursor type to SQL_CURSOR_KEYSET_DRIVEN
#statement cursor type = 1
#1
#Setting cursor type to SQL_CURSOR_STATIC
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_DYNAMIC - zOS only
#statement cursor type = 1
#1
#__ZOS_EXPECTED__
#Setting cursor type to SQL_CURSOR_FORWARD_ONLY
#statement cursor type = 0
#0
#Setting cursor type to SQL_CURSOR_KEYSET_DRIVEN
#statement cursor type = 1
#1
#Setting cursor type to SQL_CURSOR_STATIC
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_DYNAMIC - zOS only
#statement cursor type = 1
#2
#__SYSTEMI_EXPECTED__
#Setting cursor type to SQL_CURSOR_FORWARD_ONLY
#statement cursor type = 0
#0
#Setting cursor type to SQL_CURSOR_KEYSET_DRIVEN
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_STATIC
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_DYNAMIC - zOS only
#statement cursor type = 1
#3
#__ZOS_ODBC_EXPECTED__
#Setting cursor type to SQL_CURSOR_FORWARD_ONLY
#statement cursor type = 0
#0
#Setting cursor type to SQL_CURSOR_KEYSET_DRIVEN
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_STATIC
#statement cursor type = 1
#3
#Setting cursor type to SQL_CURSOR_DYNAMIC - zOS only
#statement cursor type = 1
#2
