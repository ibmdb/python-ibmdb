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

  def test_116_ConnActive(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_116)

  def run_test_116(self):
    conn = None
    is_alive = ibm_db.active(conn)
    if is_alive:
      print "Is active"
    else:
      print "Is not active"

    conn = ibm_db.connect(config.database, config.user, config.password)
    is_alive = ibm_db.active(conn)
    if is_alive:
      print "Is active"
    else:
      print "Is not active"

    ibm_db.close(conn)
    is_alive = ibm_db.active(conn)
    if is_alive:
      print "Is active"
    else:
      print "Is not active"

    # Executing active method multiple times to reproduce a customer reported defect
    print ibm_db.active(conn)
    print ibm_db.active(conn)
    print ibm_db.active(conn)
    conn = ibm_db.connect(config.database, config.user, config.password)
    print ibm_db.active(conn)
    print ibm_db.active(conn)
    print ibm_db.active(conn)

#__END__
#__LUW_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__ZOS_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__SYSTEMI_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__IDS_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
