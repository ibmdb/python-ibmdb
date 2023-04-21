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

    def test_6561_InsertNULLValues(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6561)

    def run_test_6561(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

            stmt = ibm_db.exec_immediate(conn, "INSERT INTO animals (id, breed, name, weight) VALUES (null, null, null, null)")
            statement = "SELECT count(id) FROM animals"
            result = ibm_db.exec_immediate(conn, statement)
            if ( (not result) and ibm_db.stmt_error() ):
                print("ERROR: %s" % (ibm_db.stmt_errormsg(), ))

            row = ibm_db.fetch_tuple(result)
            while ( row ):
                for i in row:
                    print(i)
                row = ibm_db.fetch_tuple(result)

            ibm_db.rollback(conn)
            ibm_db.close(conn)

        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#7
#__ZOS_EXPECTED__
#7
#__SYSTEMI_EXPECTED__
#7
#__IDS_EXPECTED__
#7
