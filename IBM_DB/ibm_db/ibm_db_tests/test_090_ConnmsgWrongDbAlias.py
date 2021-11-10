#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import os
import sys
import unittest
import ibm_db
import config
import getpass
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    @unittest.skipIf(os.environ.get("CI", False), "Test fails in CI")
    # Gets this output instead:
    # [IBM][CLI Driver] SQL1531N  The connection failed because the name specified
    # with the DSN connection string keyword could not be found in either the
    # db2dsdriver.cfg configuration file or the db2cli.ini configuration file.
    # Data source name specified in the connection string: "X". SQLCODE=-1531
    def test_090_ConnmsgWrongDbAlias(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_090)

    def run_test_090(self):
        try:
            if sys.platform == 'zos':
                conn =  ibm_db.connect("x", getpass.getuser(), config.password)
            else:
                conn = ibm_db.connect("x", config.user, config.password)
            print("??? No way.")
        except:
            err = ibm_db.conn_errormsg()
            print(err)

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver] SQL1013N  The database alias name or database name "X" could not be found.  SQLSTATE=42705 SQLCODE=-1013
#__ZOS_EXPECTED__
#[IBM][CLI Driver] SQL1013N  The database alias name or database name "X" could not be found.  SQLSTATE=42705 SQLCODE=-1013
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver] SQL1013N  The database alias name or database name "X" could not be found.  SQLSTATE=42705 SQLCODE=-1013
#__IDS_EXPECTED__
#[IBM][CLI Driver] SQL1013N  The database alias name or database name "X" could not be found.  SQLSTATE=42705 SQLCODE=-1013
