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

    def test_040_FetchTuple(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_040)

    def run_test_040(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        # Drop the test table, in case it exists
        drop = 'DROP TABLE animals'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass

        # Create the test table
        create = 'CREATE TABLE animals (id INTEGER, breed VARCHAR(32), name CHAR(16), weight DECIMAL(7,2))'
        result = ibm_db.exec_immediate(conn, create)

        insert = "INSERT INTO animals values (0, 'cat', 'Pook', 3.2)"

        ibm_db.exec_immediate(conn, insert)

        stmt = ibm_db.exec_immediate(conn, "select * from animals")

        onerow = ibm_db.fetch_tuple(stmt)

        for element in onerow:
            print(element)

        ibm_db.rollback(conn)

#__END__
#__LUW_EXPECTED__
#0
#cat
#Pook            
#3.20
#__ZOS_EXPECTED__
#0
#cat
#Pook            
#3.20
#__SYSTEMI_EXPECTED__
#0
#cat
#Pook            
#3.20
#__IDS_EXPECTED__
#0
#cat
#Pook            
#3.20
