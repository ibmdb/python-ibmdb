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

    def test_booleanInsertSelect(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_booleanInsertSelect)

    def run_test_booleanInsertSelect(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if (not conn):
            print("Could not make a connection.")
            return 0
        server = ibm_db.server_info( conn )

        if( not server.DBMS_NAME.startswith('DB2/')):
            print("Boolean is not supported")
            return 0

        try:
            ibm_db.exec_immediate(conn,"DROP TABLE bool_test")
        except:
            pass

        try:
            ibm_db.exec_immediate(conn, "CREATE TABLE bool_test(col1 BOOLEAN, description varchar(50))")
        except Exception as e:
            print("Error : {}\n".format(str(e)))
            exit(-1)

        try:
            insert_sql = "INSERT INTO bool_test values(?, ?)"
            stmt = ibm_db.prepare(conn, insert_sql)

            rows = (
                (True, 'bindparam true'),
                (False, 'bindparam false'),
                (None, 'bindparam None')
            )

            for row in rows:
                ibm_db.bind_param(stmt, 1, row[0])
                ibm_db.bind_param(stmt, 2, row[1])
                ibm_db.execute(stmt)
            stmt = None

            select_sql = 'SELECT * FROM bool_test'
            stmt = ibm_db.exec_immediate(conn, select_sql)
            result = ibm_db.fetch_tuple(stmt)

            while result:
                for col in result:
                    print(col)
                result = ibm_db.fetch_tuple(stmt)

            ibm_db.close(conn)
        except Exception as e:
            print("Error:{}".format(str(e)))


#__END__
#__LUW_EXPECTED__
#True
#bindparam true
#False
#bindparam false
#None
#bindparam None
#__ZOS_EXPECTED__
#Boolean is not supported
#__SYSTEMI_EXPECTED__
#Boolean is not supported
#__IDS_EXPECTED__
#Boolean is not supported
