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

    def test_018_selectRowcountPrefetchSetOpt(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_018)

    def run_test_018(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_ON)
        if conn:
            stmt = ibm_db.prepare(conn, "SELECT * from animals WHERE weight < 10.0" )
            if('zos' not in sys.platform):
                ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_ON}, 2)
            result = ibm_db.execute(stmt)
            if result:
                rows = ibm_db.num_rows(stmt)
                print("affected row:", rows)
                ibm_db.free_result(stmt)
            else:
                print(ibm_db.stmt_errormsg())

            if('zos' not in sys.platform):
                ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_OFF}, 2)
            result = ibm_db.execute(stmt)
            if result:
                rows = ibm_db.num_rows(stmt)
                print("affected row:", rows)
                ibm_db.free_result(stmt)
            else:
                print(ibm_db.stmt_errormsg())

            if('zos' not in sys.platform):
                ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_ON}, 2)
            result = ibm_db.execute(stmt)
            if result:
                rows = ibm_db.num_rows(stmt)
                print("affected row:", rows)
            else:
                print(ibm_db.stmt_errormsg())

            ibm_db.close(conn)
        else:
            print("no connection:", ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#__ZOS_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#__SYSTEMI_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#__IDS_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#__ZOS_ODBC_EXPECTED__
#affected row: -1
#affected row: -1
#affected row: -1
