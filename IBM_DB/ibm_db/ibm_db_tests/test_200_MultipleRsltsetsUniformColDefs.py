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
from unittest import TestCase
TestCase.maxDiff=None
class IbmDbTestCase(unittest.TestCase):

    def test_200_MultipleRsltsetsUniformColDefs(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_200)
        self.maxDiff = None

    def run_test_200(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]
        if (server == 'IDS'):
            procedure = """
        CREATE FUNCTION multiResults()
         RETURNING CHAR(16), INT;
                
         DEFINE p_name CHAR(16);
         DEFINE p_id INT;
               
         FOREACH c1 FOR
             SELECT name, id
              INTO p_name, p_id
               FROM animals
               ORDER BY name
              RETURN p_name, p_id WITH RESUME;
         END FOREACH;
                
       END FUNCTION;
       """
        else:
            procedure = """
        CREATE PROCEDURE multiResults ()
        RESULT SETS 3
        LANGUAGE SQL
        BEGIN
         DECLARE c1 CURSOR WITH RETURN FOR
          SELECT name, id
          FROM animals
          ORDER BY name;
    
         DECLARE c2 CURSOR WITH RETURN FOR
          SELECT name, id
          FROM animals
          WHERE id < 4
          ORDER BY name DESC;
    
         DECLARE c3 CURSOR WITH RETURN FOR
          SELECT name, id
          FROM animals
          WHERE weight < 5.0
          ORDER BY name;
    
         OPEN c1;
         OPEN c2;
         OPEN c3;
        END
       """

        if conn:
            try:
                ibm_db.exec_immediate(conn, 'DROP PROCEDURE multiResults')
            except:
                pass
            ibm_db.exec_immediate(conn, procedure)
            if sys.platform == 'zos':
                stmt = ibm_db.exec_immediate(conn, 'CALL MULTIRESULTS()')
            else:
                stmt = ibm_db.exec_immediate(conn, 'CALL multiresults()')
            #print(stmt)
            print("Fetching first result set")
            row = ibm_db.fetch_tuple(stmt)
            while ( row ):
                for i in row:
                    print(i)
                row = ibm_db.fetch_tuple(stmt)

            if (server == 'IDS'):
                print("Fetching second result set (should fail -- IDS does not support multiple result sets)")
            else:
                print("Fetching second result set")
            #print(stmt)
            res = ibm_db.next_result (stmt)
            if res:
                row = ibm_db.fetch_tuple(res)
                while ( row ):
                    for i in row:
                        print(i)
                    row = ibm_db.fetch_tuple(res)

            if (server == 'IDS'):
                print("Fetching third result set (should fail -- IDS does not support multiple result sets)")
            else:
                print("Fetching third result set")
            res2 = ibm_db.next_result(stmt)
            if res2:
                row = ibm_db.fetch_tuple(res2)
                while ( row ):
                    for i in row:
                        print(i)
                    row = ibm_db.fetch_tuple(res2)

            print("Fetching fourth result set (should fail)")
            res3 = ibm_db.next_result(stmt)
            if res3:
                row = ibm_db.fetch_tuple(res3)
                while ( row ):
                    for i in row:
                        print(i)
                    row = ibm_db.fetch_tuple(res3)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Fetching first result set
#Bubbles         
#3
#Gizmo           
#4
#Peaches         
#1
#Pook            
#0
#Rickety Ride    
#5
#Smarty          
#2
#Sweater         
#6
#Fetching second result set
#Smarty          
#2
#Pook            
#0
#Peaches         
#1
#Bubbles         
#3
#Fetching third result set
#Bubbles         
#3
#Gizmo           
#4
#Pook            
#0
#Fetching fourth result set (should fail)
#__ZOS_EXPECTED__
#Fetching first result set
#Bubbles         
#3
#Gizmo           
#4
#Peaches         
#1
#Pook            
#0
#Rickety Ride    
#5
#Smarty          
#2
#Sweater         
#6
#Fetching second result set
#Smarty          
#2
#Pook            
#0
#Peaches         
#1
#Bubbles         
#3
#Fetching third result set
#Bubbles         
#3
#Gizmo           
#4
#Pook            
#0
#Fetching fourth result set (should fail)
#__SYSTEMI_EXPECTED__
#Fetching first result set
#Bubbles         
#3
#Gizmo           
#4
#Peaches         
#1
#Pook            
#0
#Rickety Ride    
#5
#Smarty          
#2
#Sweater         
#6
#Fetching second result set
#Smarty          
#2
#Pook            
#0
#Peaches         
#1
#Bubbles         
#3
#Fetching third result set
#Bubbles         
#3
#Gizmo           
#4
#Pook            
#0
#Fetching fourth result set (should fail)
#__IDS_EXPECTED__
#Fetching first result set
#Bubbles         
#3
#Gizmo           
#4
#Peaches         
#1
#Pook            
#0
#Rickety Ride    
#5
#Smarty          
#2
#Sweater         
#6
#Fetching second result set (should fail -- IDS does not support multiple result sets)
#Fetching third result set (should fail -- IDS does not support multiple result sets)
#Fetching fourth result set (should fail)
