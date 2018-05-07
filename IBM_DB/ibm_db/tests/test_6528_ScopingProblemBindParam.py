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

    def test_6528_ScopingProblemBindParam(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6528)

    def checked_db2_execute(self, stmt):
        ibm_db.execute(stmt)
        row = ibm_db.fetch_tuple(stmt)
        for i in row:
            print(i)

    def run_test_6528(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            if (server.DBMS_NAME[0:3] == 'IDS'):
                sql = "SELECT TRIM(TRAILING FROM name) FROM animals WHERE breed = ?"
            else:
                sql = "SELECT RTRIM(name) FROM animals WHERE breed = ?"
            stmt = ibm_db.prepare(conn, sql)
            var = "cat"
            ibm_db.bind_param(stmt, 1, var, ibm_db.SQL_PARAM_INPUT)
            self.checked_db2_execute(stmt)
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Pook
#__ZOS_EXPECTED__
#Pook
#__SYSTEMI_EXPECTED__
#Pook
#__IDS_EXPECTED__
#Pook
