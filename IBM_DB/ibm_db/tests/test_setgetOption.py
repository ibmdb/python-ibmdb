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
    def test_setgetOption(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_setgetOption)

    def run_test_setgetOption(self):
        if sys.platform == 'zos':
            options = {}
        else:
            options = { ibm_db.SQL_ATTR_INFO_PROGRAMNAME : 'TestProgram'}
        conn = ibm_db.connect(config.database, config.user, config.password, options)

        # Get the server type
        serverinfo = ibm_db.server_info( conn )

        if conn:
            if sys.platform != 'zos':
                value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_INFO_PROGRAMNAME, 1)
                print("Connection options:\nSQL_ATTR_INFO_PROGRAMNAME = ", end="")
                print(value)
            else:
                print("Connection options:\n", end="")

            returncode=ibm_db.set_option(conn, {ibm_db.SQL_ATTR_AUTOCOMMIT:0},1)
            value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_AUTOCOMMIT, 1)
            print("SQL_ATTR_AUTOCOMMIT = ", end="")
            print(str(value)+"\n")

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

            stmt = ibm_db.prepare(conn, "SELECT * FROM temp_test WHERE id > 1" )
            if sys.platform != 'zos':
                returnCode = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT : 20}, 0)
                value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_QUERY_TIMEOUT, 0)
                print("Statement options:\nSQL_ATTR_QUERY_TIMEOUT = ", end="")
                print(str(value)+"\n")

            ibm_db.execute(stmt)
            if result:
                ibm_db.free_result(stmt)
            else:
                print(ibm_db.stmt_errormsg())
            ibm_db.rollback(conn)
            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Connection options:
#SQL_ATTR_INFO_PROGRAMNAME = TestProgram
#SQL_ATTR_AUTOCOMMIT = 0
#Statement options:
#SQL_ATTR_QUERY_TIMEOUT = 20
#__ZOS_EXPECTED__
#Connection options:
#SQL_ATTR_INFO_PROGRAMNAME = TestProgram
#SQL_ATTR_AUTOCOMMIT = 0
#Statement options:
#SQL_ATTR_QUERY_TIMEOUT = 20
#__SYSTEMI_EXPECTED__
#Connection options:
#SQL_ATTR_INFO_PROGRAMNAME = TestProgram
#SQL_ATTR_AUTOCOMMIT = 0
#Statement options:
#SQL_ATTR_QUERY_TIMEOUT = 20
#__ZOS_ODBC_EXPECTED__
#Connection options:
#SQL_ATTR_AUTOCOMMIT = 0

