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

    def test_201_MultipleRsltsetsDiffColDefs(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_201)

    def run_test_201(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]
        if (server == 'IDS'):
            procedure = """CREATE FUNCTION multiResults ()
           RETURNING CHAR(16), INT, VARCHAR(32), NUMERIC(7,2);
           
           DEFINE p_name CHAR(16);
           DEFINE p_id INT;
           DEFINE p_breed VARCHAR(32);
           DEFINE p_weight NUMERIC(7,2);
           
           FOREACH c1 FOR
              SELECT name, id, breed, weight
              INTO p_name, p_id, p_breed, p_weight
              FROM animals
              ORDER BY name DESC
              RETURN p_name, p_id, p_breed, p_weight WITH RESUME;
           END FOREACH;
    
       END FUNCTION;"""
        else:
            procedure = """CREATE PROCEDURE multiResults ()
        RESULT SETS 3
        LANGUAGE SQL
        BEGIN
         DECLARE c1 CURSOR WITH RETURN FOR
          SELECT name, id
          FROM animals
          ORDER BY name;
    
         DECLARE c2 CURSOR WITH RETURN FOR
          SELECT name, id, breed, weight
          FROM animals
          ORDER BY name DESC;
    
         DECLARE c3 CURSOR WITH RETURN FOR
          SELECT name
          FROM animals
          ORDER BY name;
    
         OPEN c1;
         OPEN c2;
         OPEN c3;
        END"""

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

            print("Fetching first result set")
            row = ibm_db.fetch_tuple(stmt)
            while ( row ):
                for i in row:
                    print(str(i).strip())
                row = ibm_db.fetch_tuple(stmt)

            if (server == 'IDS') :
                print("Fetching second result set (should fail -- IDS does not support multiple result sets)")
            else:
                print("Fetching second result set")
            res = ibm_db.next_result(stmt)

            if res:
                row = ibm_db.fetch_tuple(res)
                while ( row ):
                    for i in row:
                        print(str(i).strip())
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
                        print(str(i).strip())
                    row = ibm_db.fetch_tuple(res2)

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
#Sweater
#6
#llama
#150.00
#Smarty
#2
#horse
#350.00
#Rickety Ride
#5
#goat
#9.70
#Pook
#0
#cat
#3.20
#Peaches
#1
#dog
#12.30
#Gizmo
#4
#budgerigar
#0.20
#Bubbles
#3
#gold fish
#0.10
#Fetching third result set
#Bubbles
#Gizmo
#Peaches
#Pook
#Rickety Ride
#Smarty
#Sweater
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
#Sweater
#6
#llama
#150.00
#Smarty
#2
#horse
#350.00
#Rickety Ride
#5
#goat
#9.70
#Pook
#0
#cat
#3.20
#Peaches
#1
#dog
#12.30
#Gizmo
#4
#budgerigar
#0.20
#Bubbles
#3
#gold fish
#0.10
#Fetching third result set
#Bubbles
#Gizmo
#Peaches
#Pook
#Rickety Ride
#Smarty
#Sweater
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
#Sweater
#6
#llama
#150.00
#Smarty
#2
#horse
#350.00
#Rickety Ride
#5
#goat
#9.70
#Pook
#0
#cat
#3.20
#Peaches
#1
#dog
#12.30
#Gizmo
#4
#budgerigar
#0.20
#Bubbles
#3
#gold fish
#0.10
#Fetching third result set
#Bubbles
#Gizmo
#Peaches
#Pook
#Rickety Ride
#Smarty
#Sweater
#__IDS_EXPECTED__
#Fetching first result set
#Sweater
#6
#llama
#150.00
#Smarty
#2
#horse
#350.00
#Rickety Ride
#5
#goat
#9.70
#Pook
#0
#cat
#3.20
#Peaches
#1
#dog
#12.30
#Gizmo
#4
#budgerigar
#0.20
#Bubbles
#3
#gold fish
#0.10
#Fetching second result set (should fail -- IDS does not support multiple result sets)
#Fetching third result set (should fail -- IDS does not support multiple result sets)
