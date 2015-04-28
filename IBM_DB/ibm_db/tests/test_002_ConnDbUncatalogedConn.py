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

  def test_002_ConnDbUncatalogedConn(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_002)

  def run_test_002(self):
    conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (config.database, config.hostname, config.port, config.user, config.password)
    
    try:
      conn = ibm_db.connect(conn_str, '', '')
      print("Connection succeeded.")
      ibm_db.close(conn)
    except:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Connection succeeded.
#__ZOS_EXPECTED__
#Connection succeeded.
#__SYSTEMI_EXPECTED__
#Connection succeeded.
#__IDS_EXPECTED__
#Connection succeeded.
