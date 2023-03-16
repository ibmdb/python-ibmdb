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

    def test_113_DateTest(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_113)

    def run_test_113(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            drop = "DROP TABLE datetest"
            try:
                ibm_db.exec_immediate( conn, drop )
            except:
                pass

            create = "CREATE TABLE datetest ( id INTEGER, mydate DATE )"
            ibm_db.exec_immediate(conn, create)

            server = ibm_db.server_info( conn )
            if (server.DBMS_NAME[0:3] == 'IDS'):
                insert = "INSERT INTO datetest (id, mydate) VALUES (1,'1982-03-27')"
                ibm_db.exec_immediate(conn, insert)
                insert = "INSERT INTO datetest (id, mydate) VALUES (2,'1981-07-08')"
                ibm_db.exec_immediate(conn, insert)
            else:
                insert = "INSERT INTO datetest (id, mydate) VALUES (1,'1982-03-27')"
                ibm_db.exec_immediate(conn, insert)
                insert = "INSERT INTO datetest (id, mydate) VALUES (2,'1981-07-08')"
                ibm_db.exec_immediate(conn, insert)

            stmt = ibm_db.prepare(conn, "SELECT * FROM datetest")
            ibm_db.execute(stmt)

            result = ibm_db.fetch_row( stmt )
            while ( result ):
                row0 = ibm_db.result(stmt, 0)
                row1 = ibm_db.result(stmt, 1)
                print(row0)
                print(row1)
                result = ibm_db.fetch_row( stmt )
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#1
#1982-03-27
#2
#1981-07-08
#__ZOS_EXPECTED__
#1
#1982-03-27
#2
#1981-07-08
#__SYSTEMI_EXPECTED__
#1
#1982-03-27
#2
#1981-07-08
#__IDS_EXPECTED__
#1
#1982-03-27
#2
#1981-07-08
