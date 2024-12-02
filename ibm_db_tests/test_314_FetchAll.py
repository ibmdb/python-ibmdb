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
    
    def test_314_FetchAll(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_314)

    def run_test_314(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        # Drop the test table, in case it exists
        drop = 'DROP TABLE animals'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass

        # Create the test table
        create = 'CREATE TABLE animals (id INTEGER, breed VARCHAR(32), name VARCHAR(16), weight DECIMAL(7,2))'
        result = ibm_db.exec_immediate(conn, create)
        
        insert = "INSERT INTO animals values (0, 'cat', 'Pook', 3.2)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (1, 'dog', 'Max', 12.5)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (2, 'parrot', 'Polly', 0.8)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (3, 'rabbit', 'Bunny', 2.3)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (4, 'hamster', 'Nibbles', 0.5)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (5, 'fish', 'Bubbles', 0.2)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (6, 'snake', 'Slither', 1.1)"
        ibm_db.exec_immediate(conn, insert)
        
        insert = "INSERT INTO animals values (7, 'horse', 'Thunder', 450.7)"
        ibm_db.exec_immediate(conn, insert)

        stmt = ibm_db.exec_immediate(conn, "select * from animals")

        allRows = ibm_db.fetchall(stmt)

        print(allRows)

        ibm_db.rollback(conn)

#__END__
#__LUW_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50'), (2, 'parrot', 'Polly', '0.80'), (3, 'rabbit', 'Bunny', '2.30'), (4, 'hamster', 'Nibbles', '0.50'), (5, 'fish', 'Bubbles', '0.20'), (6, 'snake', 'Slither', '1.10'), (7, 'horse', 'Thunder', '450.70')]
#__ZOS_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50'), (2, 'parrot', 'Polly', '0.80'), (3, 'rabbit', 'Bunny', '2.30'), (4, 'hamster', 'Nibbles', '0.50'), (5, 'fish', 'Bubbles', '0.20'), (6, 'snake', 'Slither', '1.10'), (7, 'horse', 'Thunder', '450.70')]
#__SYSTEMI_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50'), (2, 'parrot', 'Polly', '0.80'), (3, 'rabbit', 'Bunny', '2.30'), (4, 'hamster', 'Nibbles', '0.50'), (5, 'fish', 'Bubbles', '0.20'), (6, 'snake', 'Slither', '1.10'), (7, 'horse', 'Thunder', '450.70')]
#__IDS_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50'), (2, 'parrot', 'Polly', '0.80'), (3, 'rabbit', 'Bunny', '2.30'), (4, 'hamster', 'Nibbles', '0.50'), (5, 'fish', 'Bubbles', '0.20'), (6, 'snake', 'Slither', '1.10'), (7, 'horse', 'Thunder', '450.70')]
