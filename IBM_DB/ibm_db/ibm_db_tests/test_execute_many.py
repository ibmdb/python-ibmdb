#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import os
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf((sys.platform == 'zos'), "Test fails in zOS")
    def test_execute_many(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_execute_many)

    def run_test_execute_many(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )

        if( not server.DBMS_NAME.startswith('DB2/')):
            print("Boolean is not supported")
            return 0

        if conn:
            # Drop the tabmany table, in case it exists
            drop = "DROP TABLE TABMANY"
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass

            #create table tabmany
            create = "CREATE TABLE TABMANY(id SMALLINT NOT NULL, name VARCHAR(32), bflag boolean)"
            ibm_db.exec_immediate(conn, create)

            #Populate the tabmany table with execute_many
            insert = "INSERT INTO TABMANY (id, name, bflag) VALUES(?, ?, ?)"
            params = ((10, 'Sanders', True), (20, 'Pernal', False), (30, 'Marenghi', True), (40, 'OBrien', False))
            stmt_insert = ibm_db.prepare(conn, insert)
            ibm_db.execute_many(stmt_insert, params)
            #check the number of rows inserted
            row_count = ibm_db.num_rows(stmt_insert)
            print(row_count)

            # check the inserted columns
            select = "SELECT * FROM TABMANY"
            stmt_select = ibm_db.exec_immediate(conn, select)
            cols = ibm_db.fetch_tuple( stmt_select )
            while( cols ):
                print("%s, %s, %s" % (cols[0], cols[1], cols[2]))
                cols = ibm_db.fetch_tuple( stmt_select )

            #populate the tabmany table
            params = ((50, 'Hanes', False), (55, 'Mike', False, 'Extra'), (55.5, 'invalid row','not a bool'), (60, 'Quigley'), (70, None, None), [75, 'List', True] )
            try:
                ibm_db.execute_many(stmt_insert, params)
            except Exception as inst:
                #check the no. of inserted rows
                row_count = ibm_db.num_rows(stmt_insert)
                #check the exception raised by execute_many API
                print(inst)
                print(row_count)
            ibm_db.close(conn)

        else:
            print(ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#4
#10, Sanders, True
#20, Pernal, False
#30, Marenghi, True
#40, OBrien, False
#Error 1: Value parameter tuple 2 has more parameters than previous tuple
#Error 2: Value parameter tuple 3 has types that are not homogeneous with previous tuple
#Error 3: Value parameter tuple 4 has fewer parameters than previous tuple
#Error 4: Value parameter 6 is not a tuple
#2
#__ZOS_EXPECTED__
#Boolean is not supported
#__SYSTEMI_EXPECTED__
#NA
#__IDS_EXPECTED__
#4
#10, Sanders, True
#20, Pernal, False
#30, Marenghi, True
#40, OBrien, False
#Error 1: Value parameter tuple 2 has more parameters than previous tuple
#Error 2: Value parameter tuple 3 has types that are not homogeneous with previous tuple
#Error 3: Value parameter tuple 4 has fewer parameters than previous tuple
#Error 4: Value parameter 6 is not a tuple
#2
