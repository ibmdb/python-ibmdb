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

    def test_6755_ExtraNULLChar_ResultCLOBCol(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6755)

    def run_test_6755(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            drop = 'DROP TABLE table_6755'
            result = ''
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass

            if (server.DBMS_NAME[0:3] == 'IDS'):
                create = 'CREATE TABLE table_6755 (col1 VARCHAR(20), col2 CLOB)'
                insert = "INSERT INTO table_6755 VALUES ('database', 'database')"
            else:
                create = 'CREATE TABLE table_6755 (col1 VARCHAR(20), col2 CLOB(20))'
                insert = "INSERT INTO table_6755 VALUES ('database', 'database')"
            result = ibm_db.exec_immediate(conn, create)
            result = ibm_db.exec_immediate(conn, insert)
            statement = "SELECT col1, col2 FROM table_6755"

            result = ibm_db.prepare(conn, statement)
            ibm_db.execute(result)

            row = ibm_db.fetch_tuple(result)
            while ( row ):
                #printf("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n",
                #    row[0], row[0].length,
                #    row[1], row[1].length)
                print("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long." % (row[0], len(row[0]), row[1], len(row[1])))
                row = ibm_db.fetch_tuple(result)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__ZOS_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__SYSTEMI_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__IDS_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
