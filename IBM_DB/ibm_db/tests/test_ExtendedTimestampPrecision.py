# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2013
#

import unittest, sys, datetime
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

  def test_ExtendedTimestampPrecision(self):
    self.obj = IbmDbTestFunctions()
    
    if (not self.obj.isServerIBMi(self.obj.server)):
      raise unittest.SkipTest("Extended Timestamp Precision not supported")
    else:
      version = int(self.obj.server.DBMS_VER[0:2])
      release = int(self.obj.server.DBMS_VER[2:4])
      
      if version < 7 or (version == 7 and release < 2):
        raise unittest.SkipTest("Extended Timestamp Precision not supported prior to IBM i 7.2")
      
    self.obj.assert_expect(self.run_test_ExtendedTimestampPrecision)

  def run_test_ExtendedTimestampPrecision(self):
    conn = ibm_db.connect(config.database, config.user, config.password)
    
    if conn:
      drop = 'DROP TABLE tab_ts_precision'
      result = ''
      try:
        result = ibm_db.exec_immediate(conn, drop)
      except:
        pass
      
      statement = "CREATE TABLE tab_ts_precision (ts1 timestamp(0), ts2 timestamp(2), ts6 timestamp(6), ts9 timestamp(9), ts12 timestamp(12))"
      result = ibm_db.exec_immediate(conn, statement)
      
      statement = "INSERT INTO tab_ts_precision values ('1970-01-02-10.11.12', '1970-01-02-10.11.12.13', '1970-01-02-10.11.12.123456', '1970-01-02-10.11.12.987654321', '1970-01-02-10.11.12.162534435261')"
      stmt = ibm_db.exec_immediate(conn, statement)
      
      statement = "SELECT * FROM tab_ts_precision"
      stmt = ibm_db.prepare(conn, statement)
      
      num_fields = ibm_db.num_fields(result)
      
      rc = ibm_db.execute(stmt)
      result = ibm_db.fetch_tuple(stmt)
      while ( result ):
        for col in result:
          print(col)
        result = ibm_db.fetch_tuple(stmt)
      ibm_db.close(conn)
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Not implemented
#__ZOS_EXPECTED__
#Not implemented
#__SYSTEMI_EXPECTED__
#1970-01-02 10:11:12
#1970-01-02 10:11:12.130000
#1970-01-02 10:11:12.123456
#1970-01-02 10:11:12.987654
#1970-01-02 10:11:12.162534
#__IDS_EXPECTED__
#Not implemented
