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

    def test_147_PrepareWithWrongType(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_147)

    def run_test_147(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

            stmt = ibm_db.prepare(conn, "INSERT INTO animals (id, breed, name) VALUES (?, ?, ?)")

            id = "\"999\""
            breed = None
            name = 'PythonDS'
            try:
                ibm_db.bind_param(stmt, 1, id)
                ibm_db.bind_param(stmt, 2, breed)
                ibm_db.bind_param(stmt, 3, name)

                error = ibm_db.execute(stmt)
                print("Should not make it this far")
            except:
                excp = sys.exc_info()
                # slot 1 contains error message
                print(excp[1])
            finally:
                ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Statement Execute Failed: [IBM][CLI Driver] CLI0112E  Error in assignment. SQLSTATE=22005 SQLCODE=-99999
#__ZOS_EXPECTED__
#Statement Execute Failed: [IBM][CLI Driver] CLI0112E  Error in assignment. SQLSTATE=22005 SQLCODE=-99999
#__SYSTEMI_EXPECTED__
#Statement Execute Failed: [IBM][CLI Driver] CLI0112E  Error in assignment. SQLSTATE=22005 SQLCODE=-99999
#__IDS_EXPECTED__
#Statement Execute Failed: [IBM][CLI Driver] CLI0112E  Error in assignment. SQLSTATE=22005 SQLCODE=-99999
#__ZOS_ODBC_EXPECTED__
#Statement Execute Failed: {DB2 FOR OS/390}{ODBC DRIVER}  SQLSTATE=22005  ERRLOC=4:3:2 SQLCODE=-99999
