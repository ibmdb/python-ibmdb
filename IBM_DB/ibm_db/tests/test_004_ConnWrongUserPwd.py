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

  def test_004_ConnWrongUserPwd(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_004)

  def run_test_004(self):
    conn = ibm_db.connect("sample", "not_a_user", "inv_pass")
    if conn:
      ibm_db.close(conn)
      print("connect succeeded? Test failed")
    else:
      print("connect failed, test succeeded")

#__END__
#__LUW_EXPECTED__
#connect failed, test succeeded
#__ZOS_EXPECTED__
#connect failed, test succeeded
#__SYSTEMI_EXPECTED__
#connect failed, test succeeded
#__IDS_EXPECTED__
#connect failed, test succeeded
