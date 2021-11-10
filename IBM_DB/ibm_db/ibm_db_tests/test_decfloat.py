#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2014
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    def test_decfloat(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_decfloat)

    def run_test_decfloat(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            serverinfo = ibm_db.server_info( conn )

            drop = "DROP TABLE STOCKPRICE"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the table stockprice
            if (serverinfo.DBMS_NAME[0:3] == 'IDS'):
                create = "CREATE TABLE STOCKPRICE (id SMALLINT NOT NULL, company VARCHAR(30), stockshare DECIMAL(7,2), stockprice DECIMAL(16))"
            else:
                create = "CREATE TABLE STOCKPRICE (id SMALLINT NOT NULL, company VARCHAR(30), stockshare DECIMAL(7,2), stockprice DECFLOAT(16))"
            result = ibm_db.exec_immediate(conn, create)

            # Insert Directly
            insert = "INSERT INTO STOCKPRICE (id, company, stockshare, stockprice) VALUES (10,'Megadeth', 100.002, 990.356736488388374888532323)"
            result = ibm_db.exec_immediate(conn, insert)

            # Prepare and Insert in the stockprice table
            stockprice = (\
                    (20, "Zaral", 102.205, "100.234"),\
                    (30, "Megabyte", 98.65, "1002.112"),\
                    (40, "Visarsoft", 123.34, "1652.345"),\
                    (50, "Mailersoft", 134.22, "1643.126"),\
                    (60, "Kaerci", 100.97, "9876.765")\
                )
            insert = 'INSERT INTO STOCKPRICE (id, company, stockshare,stockprice) VALUES (?,?,?,?)'
            stmt = ibm_db.prepare(conn,insert)
            if stmt:
                for company in stockprice:
                    result = ibm_db.execute(stmt,company)

            id = 70
            company = 'Nirvana'
            stockshare = 100.1234
            stockprice = "100.567"
            try:
                ibm_db.bind_param(stmt, 1, id)
                ibm_db.bind_param(stmt, 2, company)
                ibm_db.bind_param(stmt, 3, stockshare)
                ibm_db.bind_param(stmt, 4, stockprice)
                error = ibm_db.execute(stmt);
            except:
                excp = sys.exc_info()
                # slot 1 contains error message
                print(excp[1])

            # Select the result from the table and
            query = 'SELECT * FROM STOCKPRICE ORDER BY id'
            if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
                stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            else:
                stmt = ibm_db.prepare(conn, query)
            ibm_db.execute(stmt)
            data = ibm_db.fetch_both( stmt )
            while ( data ):
                print("%s : %s : %s : %s\n" % (data[0], data[1], data[2], data[3]))
                data = ibm_db.fetch_both( stmt )
            try:
                stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE:  ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
                ibm_db.execute(stmt)
                rc = ibm_db.fetch_row(stmt, -1)
                print("Fetch Row -1:%s " %str(rc))
            except:
                print("Requested row number must be a positive value")
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#10 : Megadeth : 100.00 : 990.3567364883884
#20 : Zaral : 102.20 : 100.234
#30 : Megabyte : 98.65 : 1002.112
#40 : Visarsoft : 123.34 : 1652.345
#50 : Mailersoft : 134.22 : 1643.126
#60 : Kaerci : 100.97 : 9876.765
#70 : Nirvana : 100.12 : 100.567
#Requested row number must be a positive value
#__ZOS_EXPECTED__
#10 : Megadeth : 100.00 : 990.3567364883884
#20 : Zaral : 102.20 : 100.234
#30 : Megabyte : 98.65 : 1002.112
#40 : Visarsoft : 123.34 : 1652.345
#50 : Mailersoft : 134.22 : 1643.126
#60 : Kaerci : 100.97 : 9876.765
#70 : Nirvana : 100.12 : 100.567
#Requested row number must be a positive value
#__SYSTEMI_EXPECTED__
#NA
#__IDS_EXPECTED__
#10 : Megadeth : 100.00 : 990.356736488
#20 : Zaral : 102.20 : 100.234
#30 : Megabyte : 98.65 : 1002.112
#40 : Visarsoft : 123.34 : 1652.345
#50 : Mailersoft : 134.22 : 1643.126
#60 : Kaerci : 100.97 : 9876.765
#70 : Nirvana : 100.12 : 100.567
#Requested row number must be a positive value
#__ZOS_ODBC_EXPECTED__
#10 : Megadeth : 100.00 : 990.3567364883884
#20 : Zaral : 102.20 : 100.234
#30 : Megabyte : 98.65 : 1002.112
#40 : Visarsoft : 123.34 : 1652.345
#50 : Mailersoft : 134.22 : 1643.126
#60 : Kaerci : 100.97 : 9876.765
#70 : Nirvana : 100.12 : 100.567
#Requested row number must be a positive value
