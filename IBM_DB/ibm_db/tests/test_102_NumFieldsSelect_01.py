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

  def test_102_NumFieldsSelect_01(self):
    self.obj = IbmDbTestFunctions()
    self.obj.assert_expect(self.run_test_102)

  def run_test_102(self):
    conn = ibm_db.connect(config.database, config.user, config.password)
    
    if (not conn):
      print(ibm_db.conn_errormsg())
    
    server = ibm_db.server_info( conn )
    if (self.obj.isServerLUW(server) or self.obj.isServerIBMi(server)):
      result = ibm_db.exec_immediate(conn, "VALUES(1)")
      print(ibm_db.num_fields(result))
    else:
      print('Not Supported')
    ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#1
#__ZOS_EXPECTED__
#Not Supported
#__SYSTEMI_EXPECTED__
#1
#__IDS_EXPECTED__
#Not Supported
