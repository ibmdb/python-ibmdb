#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2025
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_320_EmptyFetchMethods_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_320)

    def run_test_320(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        dbi_conn = ibm_db_dbi.Connection(conn)

        # Drop the test table, if exists
        drop = 'DROP TABLE dbiEmployeesEmpty'
        try:
            cur = dbi_conn.cursor()
            cur.execute(drop)
        except:
            pass

        # Create the test table (empty)
        create = 'CREATE TABLE dbiEmployeesEmpty (id INT PRIMARY KEY NOT NULL, name VARCHAR(255), age INT)'
        cur = dbi_conn.cursor()
        cur.execute(create)

        dbi_conn.commit()

        # 1) fetchone example on empty table
        cur1 = dbi_conn.cursor()
        cur1.execute('SELECT * FROM dbiEmployeesEmpty ORDER BY id')
        row = cur1.fetchone()
        print("fetchone():", row)

        # 2) fetchmany example on empty table
        cur2 = dbi_conn.cursor()
        cur2.execute('SELECT * FROM dbiEmployeesEmpty ORDER BY id')
        rows = cur2.fetchmany(2)
        print("fetchmany(2):", rows)

        # 3) fetchall example on empty table
        cur3 = dbi_conn.cursor()
        cur3.execute('SELECT * FROM dbiEmployeesEmpty ORDER BY id')
        all_rows = cur3.fetchall()
        print("fetchall():", all_rows)

#__END__
#__LUW_EXPECTED__
#fetchone(): None
#fetchmany(2): []
#fetchall(): []
#__ZOS_EXPECTED__
#fetchone(): None
#fetchmany(2): []
#fetchall(): []
#__SYSTEMI_EXPECTED__
#fetchone(): None
#fetchmany(2): []
#fetchall(): []
#__IDS_EXPECTED__
#fetchone(): None
#fetchmany(2): []
#fetchall(): []
