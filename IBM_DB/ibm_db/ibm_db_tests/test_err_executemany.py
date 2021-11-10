#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2020
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
import os
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf(((os.environ.get("CI", False)) or (sys.platform == 'zos')), "Test fails in CI")
    def test_err_executemany(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_err_executemany)

    def run_test_err_executemany(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        serverinfo = ibm_db.server_info( conn )
        server = serverinfo.DBMS_NAME[0:3]

        if conn:
            try:
                ibm_db.exec_immediate(conn, 'DROP TABLE CLI0126E')
            except:
                pass
            create_ddl = "create table CLI0126E \
                (\
                    offer_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\
                    position_id int NOT NULL,\
                    title VARCHAR(5000) NOT NULL,\
                    type VARCHAR(5000),\
                    quantity decimal(10, 3) NOT NULL,\
                    price_btc decimal(10, 8) NOT NULL,\
                    city VARCHAR(5000),\
                    country VARCHAR(500)\
                )"

            try:           
                ibm_db.exec_immediate(conn, create_ddl)
            except:
                pass

            insert_statement = "INSERT INTO CLI0126E (position_id, title, type, quantity, price_btc, city, country)\
                                VALUES (?, ?, ?, ?, ?, ?, ?)"

            stmt = ibm_db.prepare(conn, insert_statement)

            # deliberately use wrong size decimal values to trigger CLI0111E (hidden by execute_many()).
            parms1= (15628, 'correct value in row1 column4', '', 1999999.0, 0.0067762, 'Belarus', 'Belarus1')
            parms2= (15629, 'incorrect value in row2 column4', '', 99999999.0, 0.0067762, 'Belarus', 'Belarus2')
            parms3= (15630, 'correct value in row3 column4', '', 1999999.0, 0.0067762, 'Belarus', 'Belarus3')

            parms=( parms1 , parms2, parms3)

            try:
               ibm_db.execute_many(stmt, parms)
               print(str(ibm_db.num_rows(stmt)) +" - Rows inserted successfully")
            except:
               print("Failed to insert multiple-rows with ibm_db.execute_many()")
               print(ibm_db.stmt_errormsg())
               print("Number of rows inserted: "+ str(ibm_db.num_rows(stmt)) )


            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Failed to insert multiple-rows with ibm_db.execute_many()
#[IBM][CLI Driver] CLI0111E  Numeric value out of range. SQLSTATE=22003 SQLCODE=-99999
#Number of rows inserted: 1
#__ZOS_EXPECTED__
#Failed to insert multiple-rows with ibm_db.execute_many()
#[IBM][CLI Driver] CLI0111E  Numeric value out of range. SQLSTATE=22003 SQLCODE=-99999
#Number of rows inserted: 1
#__SYSTEMI_EXPECTED__
#Failed to insert multiple-rows with ibm_db.execute_many()
#[IBM][CLI Driver] CLI0111E  Numeric value out of range. SQLSTATE=22003 SQLCODE=-99999
#Number of rows inserted: 1
#__IDS_EXPECTED__
#Failed to insert multiple-rows with ibm_db.execute_many()
#[IBM][CLI Driver] CLI0111E  Numeric value out of range. SQLSTATE=22003 SQLCODE=-99999
#Number of rows inserted: 1
