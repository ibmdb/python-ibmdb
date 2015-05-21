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

  def test_157a_FetchAssocWithoutScrollableCursorErr(self):
    self.obj = IbmDbTestFunctions()
    if self.obj.isClientIBMi():
        self.obj.assert_expectf(self.run_test_157a)
    else:
        self.obj.assert_expect(self.run_test_157a)

  def run_test_157a(self):
    conn = ibm_db.connect(config.database, config.user, config.password)
    server = ibm_db.server_info( conn )

    print("Starting...")
    if conn:
      sql = "SELECT id, name, breed, weight FROM animals ORDER BY breed"
      result = ibm_db.exec_immediate(conn, sql)

      try:
          i = 2
          row = ibm_db.fetch_assoc(result, i)
          while ( row ):
              if (self.obj.isServerInformix(server)):
                print("%-5d %-16s %-32s %10s" % (row['id'], row['name'], row['breed'], row['weight']))
              else:
                print("%-5d %-16s %-32s %10s" % (row['ID'], row['NAME'], row['BREED'], row['WEIGHT']))
              i = i + 2
          row = ibm_db.fetch_assoc(result, i)
      except:
          print("SQLSTATE: %s" % ibm_db.stmt_error(result))
          print("Message: %s" % ibm_db.stmt_errormsg(result))
	
      print("DONE")

#__END__
#__LUW_EXPECTED__
#Starting...
#SQLSTATE: HY106
#Message: [IBM][CLI Driver] CLI0145E  Fetch type out of range. SQLSTATE=HY106 SQLCODE=-99999
#DONE
#__ZOS_EXPECTED__
#Starting...
#SQLSTATE: HY106
#Message: [IBM][CLI Driver] CLI0145E  Fetch type out of range. SQLSTATE=HY106 SQLCODE=-99999
#DONE
#__SYSTEMI_EXPECTED__
#Starting...
#SQLSTATE: HY106
#Message: [IBM][CLI Driver] CLI0145E  Fetch type out of range. SQLSTATE=HY106 SQLCODE=-99999
#DONE
#__PASE_EXPECTED__
#Starting...
#SQLSTATE: 42872
#Message: FETCH not valid; cursor %s not scrollable. SQLSTATE=42872 SQLCODE=-225
#DONE
#__IDS_EXPECTED__
#Starting...
#SQLSTATE: HY106
#Message: [IBM][CLI Driver] CLI0145E  Fetch type out of range. SQLSTATE=HY106 SQLCODE=-99999
#DONE
