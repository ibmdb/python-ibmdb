# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest, sys
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
      try:
        result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", { ibm_db.SQL_ATTR_CURSOR_TYPE : ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
        rows = ibm_db.num_rows(result)
        print("affected row: %d" % rows)
      except:
        print(ibm_db.stmt_errormsg())
      
      try:
        result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_CURSOR_TYPE : ibm_db.SQL_CURSOR_FORWARD_ONLY})
        rows = ibm_db.num_rows(result)
        print("affected row: %d" % rows)
      except:
        print(ibm_db.stmt_errormsg())
      
      try:
        result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_ON})
        rows = ibm_db.num_rows(result)
        print("affected row: %d" % rows)
      except:
        print(ibm_db.stmt_errormsg())
      
      try:
        result = ibm_db.exec_immediate(conn,"SELECT * from animals WHERE weight < 10.0", {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH : ibm_db.SQL_ROWCOUNT_PREFETCH_OFF})
        rows = ibm_db.num_rows(result)
        print("affected row: %d" % rows)
      except:
        print(ibm_db.stmt_errormsg())


      ibm_db.close(conn)
    else:
      print("no connection: %s" % ibm_db.conn_errormsg())

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
#__PASE_EXPECTED__
#affected row: -1
#affected row: -1
#Error occurred in SQL Call Level Interface SQLSTATE=HY009 SQLCODE=-99999
#Error occurred in SQL Call Level Interface SQLSTATE=HY009 SQLCODE=-99999
#__IDS_EXPECTED__
#affected row: 4
#affected row: -1
#affected row: 4
#affected row: -1
