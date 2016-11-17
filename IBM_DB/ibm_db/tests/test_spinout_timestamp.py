#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2016
#

import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    def test_spinout_timestamp(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_spinout_timestamp)

    def run_test_spinout_timestamp(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        # Get the server type
        serverinfo = ibm_db.server_info( conn )

        if conn:

            drop = "DROP PROCEDURE PROC_TIMESTAMP"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the SP with timestamp parameters

            if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
                create = "CREATE PROCEDURE PROC_TIMESTAMP ( IN PAR1 TIMESTAMP, OUT PAR2 TIMESTAMP) BEGIN SET PAR2 = PAR1; END"
            else:
                create = "CREATE PROCEDURE PROC_TIMESTAMP ( IN PAR1 TIMESTAMP, OUT PAR2 TIMESTAMP) BEGIN SET PAR2 = PAR1; END"
            result = ibm_db.exec_immediate(conn, create)

            # call the SP. Expect PAR2 to contain value passed to PAR1
            par1 = "2016-11-14-22.47.29.872688"
            par2 = ""

            print "Values of bound parameters _before_ CALL:"
            print "  1: %s 2: %s\n" % (par1, par2)

            stmt, par1, par2 = ibm_db.callproc(conn, 'proc_timestamp', (par1, par2))
            if stmt is not None:
                print "Values of bound parameters _after_ CALL:"
                print "  1: %s 2: %s\n" % (par1, par2)

            ibm_db.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: 2016-11-14-22.47.29.872688 2: 
#
#Values of bound parameters _after_ CALL:
#  1: 2016-11-14-22.47.29.872688 2: 2016-11-14 22:47:29.872688
#__ZOS_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: 2016-11-14-22.47.29.872688 2: 
#
#Values of bound parameters _after_ CALL:
#  1: 2016-11-14-22.47.29.872688 2: 2016-11-14 22:47:29.872688
#__SYSTEMI_EXPECTED__
#  This will be updated later
#__IDS_EXPECTED__
#  This will be updated later
