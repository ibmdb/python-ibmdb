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

    def test_153_FetchAssocSelect_04(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_153)

    def run_test_153(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        result = ibm_db.exec_immediate(conn, "select * from org")

        row = ibm_db.fetch_assoc(result)
        while ( row ):
            #printf("%4d ",row['DEPTNUMB'])
            #printf("%-14s ",row['DEPTNAME'])
            #printf("%4d ",row['MANAGER'])
            #printf("%-10s",row['DIVISION'])
            #printf("%-13s ",row['LOCATION'])
            #puts ""
            print("%4d %-14s %4d %-10s%-13s " % (row['DEPTNUMB'], row['DEPTNAME'], row['MANAGER'], row['DIVISION'], row['LOCATION']))
            row = ibm_db.fetch_assoc(result)

#__END__
#__LUW_EXPECTED__
#
#  10 Head Office     160 Corporate New York      
#  15 New England      50 Eastern   Boston        
#  20 Mid Atlantic     10 Eastern   Washington    
#  38 South Atlantic   30 Eastern   Atlanta       
#  42 Great Lakes     100 Midwest   Chicago       
#  51 Plains          140 Midwest   Dallas        
#  66 Pacific         270 Western   San Francisco 
#  84 Mountain        290 Western   Denver        
#__ZOS_EXPECTED__
#
#  10 Head Office     160 Corporate New York      
#  15 New England      50 Eastern   Boston        
#  20 Mid Atlantic     10 Eastern   Washington    
#  38 South Atlantic   30 Eastern   Atlanta       
#  42 Great Lakes     100 Midwest   Chicago       
#  51 Plains          140 Midwest   Dallas        
#  66 Pacific         270 Western   San Francisco 
#  84 Mountain        290 Western   Denver        
#__SYSTEMI_EXPECTED__
#
#  10 Head Office     160 Corporate New York      
#  15 New England      50 Eastern   Boston        
#  20 Mid Atlantic     10 Eastern   Washington    
#  38 South Atlantic   30 Eastern   Atlanta       
#  42 Great Lakes     100 Midwest   Chicago       
#  51 Plains          140 Midwest   Dallas        
#  66 Pacific         270 Western   San Francisco 
#  84 Mountain        290 Western   Denver        
#__IDS_EXPECTED__
#
#  10 Head Office     160 Corporate New York      
#  15 New England      50 Eastern   Boston        
#  20 Mid Atlantic     10 Eastern   Washington    
#  38 South Atlantic   30 Eastern   Atlanta       
#  42 Great Lakes     100 Midwest   Chicago       
#  51 Plains          140 Midwest   Dallas        
#  66 Pacific         270 Western   San Francisco 
#  84 Mountain        290 Western   Denver        
#
