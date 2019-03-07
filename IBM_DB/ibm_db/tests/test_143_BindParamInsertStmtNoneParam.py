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

    def test_143_BindParamInsertStmtNoneParam(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_143)

    def run_test_143(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        insert1 = "INSERT INTO animals (id, breed, name, weight) VALUES (NULL, 'ghost', NULL, ?)"
        select = 'SELECT id, breed, name, weight FROM animals WHERE weight IS NULL'

        if conn:
            stmt = ibm_db.prepare(conn, insert1)

            animal = None
            ibm_db.bind_param(stmt, 1, animal)

            if ibm_db.execute(stmt):
                stmt = ibm_db.exec_immediate(conn, select)
                row = ibm_db.fetch_tuple(stmt)
                while ( row ):
                    #row.each { |child| print child }
                    for i in row:
                        print(i)
                    row = ibm_db.fetch_tuple(stmt)

            ibm_db.rollback(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#None
#ghost
#None
#None
#__ZOS_EXPECTED__
#None
#ghost
#None
#None
#__SYSTEMI_EXPECTED__
#None
#ghost
#None
#None
#__IDS_EXPECTED__
#None
#ghost
#None
#None
