#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
from decimal import Decimal
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    def test_decimal(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_decimal)

    def run_test_decimal(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            serverinfo = ibm_db.server_info( conn )

            drop = "DROP TABLE STOCKSHARE"
            try:
                result = ibm_db.exec_immediate(conn,drop)
            except:
                pass

            # Create the table stockprice
            create = "CREATE TABLE STOCKSHARE (id SMALLINT NOT NULL, company VARCHAR(30), stockshare DECIMAL(7, 2))"
            result = ibm_db.exec_immediate(conn, create)

            # Insert Directly
            insert = "INSERT INTO STOCKSHARE (id, company, stockshare) VALUES (10, 'Megadeth', 100.002)"
            result = ibm_db.exec_immediate(conn, insert)

            # Prepare and Insert in the stockprice table
            stockprice = (\
                    (20, "Zaral", 102.205),\
                    (30, "Megabyte", "98.65"),\
                    (40, "Visarsoft", Decimal("123.34")),\
                    (50, "Mailersoft", Decimal("134.222")),\
                    (60, "Kaerci", Decimal("100.976"))\
                    )
            insert = 'INSERT INTO STOCKSHARE (id, company, stockshare) VALUES (?,?,?)'
            stmt = ibm_db.prepare(conn,insert)
            if stmt:
                for company in stockprice:
                    result = ibm_db.execute(stmt,company)

            id = 70
            company = 'Nirvana'
            stockshare = Decimal("100.1234")
            try:
                ibm_db.bind_param(stmt, 1, id)
                ibm_db.bind_param(stmt, 2, company)
                ibm_db.bind_param(stmt, 3, stockshare)
                error = ibm_db.execute(stmt);
            except:
                excp = sys.exc_info()
                # slot 1 contains error message
                print(excp[1])

            # Select the result from the table and
            query = 'SELECT * FROM STOCKSHARE ORDER BY id'
            if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
                stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            else:
                stmt = ibm_db.prepare(conn, query)
            ibm_db.execute(stmt)
            data = ibm_db.fetch_both( stmt )
            while ( data ):
                print("%s : %s : %s\n" % (data[0], data[1], data[2]))
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
#10 : Megadeth : 100.00
#20 : Zaral : 102.20
#30 : Megabyte : 98.65
#40 : Visarsoft : 123.34
#50 : Mailersoft : 134.22
#60 : Kaerci : 100.97
#70 : Nirvana : 100.12
#Requested row number must be a positive value
#__ZOS_EXPECTED__
#10 : Megadeth : 100.00
#20 : Zaral : 102.20
#30 : Megabyte : 98.65
#40 : Visarsoft : 123.34
#50 : Mailersoft : 134.22
#60 : Kaerci : 100.97
#70 : Nirvana : 100.12
#Requested row number must be a positive value
#__SYSTEMI_EXPECTED__
#NA
#__IDS_EXPECTED__
#10 : Megadeth : 100.00
#20 : Zaral : 102.20
#30 : Megabyte : 98.65
#40 : Visarsoft : 123.34
#50 : Mailersoft : 134.22
#60 : Kaerci : 100.97
#70 : Nirvana : 100.12
#Requested row number must be a positive value
#__ZOS_ODBC_EXPECTED__
#NA
