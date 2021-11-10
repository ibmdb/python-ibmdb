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
    def test_warn(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_warn)

    def run_test_warn(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        # Get the server type
        serverinfo = ibm_db.server_info( conn )

        if conn:

            drop = "DROP TABLE WITH_CLOB"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the table with_clob

            if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
                create = "CREATE TABLE WITH_CLOB (id SMALLINT NOT NULL, clob_col CLOB(1k))"
            else:
                create = "CREATE TABLE WITH_CLOB (id SMALLINT NOT NULL, clob_col CLOB(smart))"
            result = ibm_db.exec_immediate(conn, create)

            # Select the result from the table. This is just to verify we get appropriate warning using
            # ibm_db.stmt_warn() API

            query = 'SELECT * FROM WITH_CLOB'
            if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
                stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            else:
                stmt = ibm_db.prepare(conn, query)

            ibm_db.execute(stmt)
            data = ibm_db.fetch_both( stmt )
            if data:
                print("Success")
            else:
                print("No Data")
                print(ibm_db.stmt_warn(stmt))
            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#No Data[IBM][CLI Driver][DB2/%s] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000 SQLCODE=100
#__ZOS_EXPECTED__
#No Data[IBM][CLI Driver][DB2]
# SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000 SQLCODE=100
#__SYSTEMI_EXPECTED__
#No Data
#__IDS_EXPECTED__
#No Data
#[IBM][CLI Driver][IDS/%s] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000 SQLCODE=100
#__ZOS_ODBC_EXPECTED__
#No Data









