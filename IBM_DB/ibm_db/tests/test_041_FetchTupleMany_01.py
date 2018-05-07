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

    def test_041_FetchTupleMany_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_041)

    def run_test_041(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            stmt = ibm_db.exec_immediate(conn, "select * from animals order by breed")

            i = 0

            cols = ibm_db.fetch_tuple( stmt )
            while( cols ):
                print("%s %s %s %s " % (cols[0], cols[1], cols[2], cols[3]))
                i+=1
                cols = ibm_db.fetch_tuple( stmt )

            print("\nNumber of rows: %d" % i)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#4 budgerigar Gizmo            0.20 
#0 cat Pook             3.20 
#1 dog Peaches          12.30 
#5 goat Rickety Ride     9.70 
#3 gold fish Bubbles          0.10 
#2 horse Smarty           350.00 
#6 llama Sweater          150.00 
#
#Number of rows: 7
#__ZOS_EXPECTED__
#4 budgerigar Gizmo            0.20 
#0 cat Pook             3.20 
#1 dog Peaches          12.30 
#5 goat Rickety Ride     9.70 
#3 gold fish Bubbles          0.10 
#2 horse Smarty           350.00 
#6 llama Sweater          150.00 
#
#Number of rows: 7
#__SYSTEMI_EXPECTED__
#4 budgerigar Gizmo            0.20 
#0 cat Pook             3.20 
#1 dog Peaches          12.30 
#5 goat Rickety Ride     9.70 
#3 gold fish Bubbles          0.10 
#2 horse Smarty           350.00 
#6 llama Sweater          150.00 
#
#Number of rows: 7
#__IDS_EXPECTED__
#4 budgerigar Gizmo            0.20 
#0 cat Pook             3.20 
#1 dog Peaches          12.30 
#5 goat Rickety Ride     9.70 
#3 gold fish Bubbles          0.10 
#2 horse Smarty           350.00 
#6 llama Sweater          150.00 
#
#Number of rows: 7
