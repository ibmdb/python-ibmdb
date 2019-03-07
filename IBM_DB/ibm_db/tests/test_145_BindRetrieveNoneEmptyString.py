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

    def test_145_BindRetrieveNoneEmptyString(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_145)

    def run_test_145(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

            stmt = ibm_db.prepare(conn, "INSERT INTO animals (id, breed, name) VALUES (?, ?, ?)")

            id = 999
            breed = None
            name = 'PythonDS'
            ibm_db.bind_param(stmt, 1, id)
            ibm_db.bind_param(stmt, 2, breed)
            ibm_db.bind_param(stmt, 3, name)

            # After this statement, we expect that the BREED column will contain
            # an SQL NULL value, while the NAME column contains an empty string

            ibm_db.execute(stmt)

            # After this statement, we expect that the BREED column will contain
            # an SQL NULL value, while the NAME column contains an empty string.
            # Use the dynamically bound parameters to ensure that the code paths
            # for both ibm_db.bind_param and ibm_db.execute treat Python Nones and empty
            # strings the right way.

            ibm_db.execute(stmt, (1000, None, 'PythonDS'))

            result = ibm_db.exec_immediate(conn, "SELECT id, breed, name FROM animals WHERE breed IS NULL")
            row = ibm_db.fetch_tuple(result)
            while ( row ):
                for i in row:
                    print(i)
                row = ibm_db.fetch_tuple(result)

            ibm_db.rollback(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#999
#None
#PythonDS        
#1000
#None
#PythonDS        
#__ZOS_EXPECTED__
#999
#None
#PythonDS        
#1000
#None
#PythonDS        
#__SYSTEMI_EXPECTED__
#999
#None
#PythonDS        
#1000
#None
#PythonDS        
#__IDS_EXPECTED__
#999
#None
#PythonDS        
#1000
#None
#PythonDS        
