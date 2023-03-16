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

    def test_142_BindParamSelectStmtMultipleParams_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_142)

    def run_test_142(self):
        sql = "SELECT id, breed, name, weight FROM animals WHERE weight < ? AND weight > ?"

        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            stmt = ibm_db.prepare(conn, sql)

            weight = 200.05
            mass = 2.0

            ibm_db.bind_param(stmt, 1, weight, ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt, 2, mass, ibm_db.SQL_PARAM_INPUT)

            result = ibm_db.execute(stmt)
            if ( result ):
                row = ibm_db.fetch_tuple(stmt)
                while ( row ):
                    #row.each { |child| print child }
                    for i in row:
                        print(i)
                    row = ibm_db.fetch_tuple(stmt)
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#0
#cat
#Pook            
#3.20
#1
#dog
#Peaches         
#12.30
#5
#goat
#Rickety Ride    
#9.70
#6
#llama
#Sweater         
#150.00
#__ZOS_EXPECTED__
#0
#cat
#Pook            
#3.20
#1
#dog
#Peaches         
#12.30
#5
#goat
#Rickety Ride    
#9.70
#6
#llama
#Sweater         
#150.00
#__SYSTEMI_EXPECTED__
#0
#cat
#Pook            
#3.20
#1
#dog
#Peaches         
#12.30
#5
#goat
#Rickety Ride    
#9.70
#6
#llama
#Sweater         
#150.00
#__IDS_EXPECTED__
#0
#cat
#Pook            
#3.20
#1
#dog
#Peaches         
#12.30
#5
#goat
#Rickety Ride    
#9.70
#6
#llama
#Sweater         
#150.00
