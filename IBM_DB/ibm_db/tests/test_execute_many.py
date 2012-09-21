# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    def test_execute_many(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_execute_many)

    def run_test_execute_many(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            # Drop the tabmany table, in case it exists
            drop = "DROP TABLE TABMANY"
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass

            #create table tabmany
            create = "CREATE TABLE TABMANY(id SMALLINT NOT NULL, name VARCHAR(32))"
            ibm_db.exec_immediate(conn, create)
            
            #Populate the tabmany table with execute_many
            insert = "INSERT INTO TABMANY (id, name) VALUES(?, ?)"
            params = ((10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi'), (40, 'OBrien'))
            stmt_insert = ibm_db.prepare(conn, insert)
            ibm_db.execute_many(stmt_insert, params)
            #check the number of rows inserted
            row_count = ibm_db.num_rows(stmt_insert)
            print row_count
            
            # chaeck the inserted columns
            select = "SELECT * FROM TABMANY"
            stmt_select = ibm_db.exec_immediate(conn, select)
            cols = ibm_db.fetch_tuple( stmt_select )
            while( cols ):
                print "%s, %s" % (cols[0], cols[1])
                cols = ibm_db.fetch_tuple( stmt_select )
            
            #populate the tabmany table 
            params = ((50, 'Hanes'), (55, ), (55.5, 'invalid row'), (60, 'Quigley'), (70, None) )
            try:
                ibm_db.execute_many(stmt_insert, params)
            except Exception, inst:
                #check the no. of inserted rows
                row_count = ibm_db.num_rows(stmt_insert)
                #check the exception raised by execute_many API
                print inst
                print row_count
            ibm_db.close(conn)

        else:
            print ibm_db.conn_errormsg()

#__END__
#__LUW_EXPECTED__
#4
#10, Sanders
#20, Pernal
#30, Marenghi
#40, OBrien
#Error 1: Value parameter tuple: 2 has less no of param 
#Error 2: Value parameters array 3 is not homogeneous with privious parameters array 
#3
#__ZOS_EXPECTED__
#4
#10, Sanders
#20, Pernal
#30, Marenghi
#40, OBrien
#Error 1: Value parameter tuple: 2 has less no of param 
#Error 2: Value parameters array 3 is not homogeneous with privious parameters array 
#3
