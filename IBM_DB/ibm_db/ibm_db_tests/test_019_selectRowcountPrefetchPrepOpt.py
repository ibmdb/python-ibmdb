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

    def test_019_selectRowcountPrefetchPrepOpt(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_019)

    def run_test_019(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_ON)
        if conn:
            if('zos' in sys.platform):
                stmt = ibm_db.prepare(conn, "SELECT * from animals WHERE weight < 10.0")
            else:
                stmt = ibm_db.prepare(conn, "SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_ON} )
            result = ibm_db.execute(stmt)
            if result:
                rows = ibm_db.num_rows(stmt)
                print("affected row:", rows)
                ibm_db.free_result(stmt)
            else:
                print(ibm_db.stmt_errormsg())

            ibm_db.close(conn)
        else:
            print("no connection:", ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#affected row: 4
#__ZOS_EXPECTED__
#affected row: 4
#__SYSTEMI_EXPECTED__
#affected row: 4
#__IDS_EXPECTED__
#affected row: 4
#__ZOS_ODBC_EXPECTED__
#affected row: -1
