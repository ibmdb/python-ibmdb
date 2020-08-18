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

    def test_017_selectRowcountPrefetchSTMTOpt(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_017)

    def run_test_017(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if conn:
            if ('zos' in sys.platform):
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0")
            else:
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", { ibm_db.SQL_ATTR_CURSOR_TYPE : ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            if result:
                rows = ibm_db.num_rows(result)
                print("affected row:", rows)
            else:
                print(ibm_db.stmt_errormsg())
            if('zos' in sys.platform):
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0")
            else:
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_CURSOR_TYPE : ibm_db.SQL_CURSOR_FORWARD_ONLY})
            if result:
                rows = ibm_db.num_rows(result)
                print("affected row:", rows)
            else:
                print(ibm_db.stmt_errormsg())
            if ('zos' in sys.platform):
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0")
            else:
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_ON})
            if result:
                rows = ibm_db.num_rows(result)
                print("affected row:", rows)
            else:
                print(ibm_db.stmt_errormsg())
            if('zos' in sys.platform):
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0")
            else:
                result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_OFF})
            if result:
                rows = ibm_db.num_rows(result)
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
#affected row: -1
#__ZOS_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#affected row: -1
#__SYSTEMI_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#affected row: -1
#__IDS_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#affected row: -1
#__ZOS_ODBC_EXPECTED__
#affected row: -1
#affected row: -1
#affected row: -1
#affected row: -1
