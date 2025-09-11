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

    def test_319_FetchMethods_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_319)

    def run_test_319(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        dbi_conn = ibm_db_dbi.Connection(conn)

        # Drop the test table, in case it exists
        drop = 'DROP TABLE dbiEmployees'
        try:
            cur = dbi_conn.cursor()
            cur.execute(drop)
        except:
            pass

        # Create the test table
        create = 'CREATE TABLE dbiEmployees (id INT PRIMARY KEY NOT NULL, name VARCHAR(255), age INT)'
        cur = dbi_conn.cursor()
        cur.execute(create)

        # Insert rows into the table
        insert_sql = 'INSERT INTO dbiEmployees (id, name, age) VALUES (?, ?, ?)'
        employees = [
            (1, 'Alice', 30),
            (2, 'Bob', 24),
            (3, 'Charlie', 29),
            (4, 'Diana', 35),
            (5, 'Eve', 40)
        ]
        for emp in employees:
            cur.execute(insert_sql, emp)

        dbi_conn.commit()

        # 1) fetchone example
        cur1 = dbi_conn.cursor()
        cur1.execute('SELECT * FROM dbiEmployees ORDER BY id')
        row = cur1.fetchone()
        print("fetchone():", row)

        # 2) fetchmany example
        cur2 = dbi_conn.cursor()
        cur2.execute('SELECT * FROM dbiEmployees ORDER BY id')
        rows = cur2.fetchmany(2)
        print("fetchmany(2):", rows)

        # 3) fetchall example
        cur3 = dbi_conn.cursor()
        cur3.execute('SELECT * FROM dbiEmployees ORDER BY id')
        all_rows = cur3.fetchall()
        print("fetchall():", all_rows)

#__END__
#__LUW_EXPECTED__
#fetchone(): (1, 'Alice', 30)
#fetchmany(2): [(1, 'Alice', 30), (2, 'Bob', 24)]
#fetchall(): [(1, 'Alice', 30), (2, 'Bob', 24), (3, 'Charlie', 29), (4, 'Diana', 35), (5, 'Eve', 40)]
#__ZOS_EXPECTED__
#fetchone(): (1, 'Alice', 30)
#fetchmany(2): [(1, 'Alice', 30), (2, 'Bob', 24)]
#fetchall(): [(1, 'Alice', 30), (2, 'Bob', 24), (3, 'Charlie', 29), (4, 'Diana', 35), (5, 'Eve', 40)]
#__SYSTEMI_EXPECTED__
#fetchone(): (1, 'Alice', 30)
#fetchmany(2): [(1, 'Alice', 30), (2, 'Bob', 24)]
#fetchall(): [(1, 'Alice', 30), (2, 'Bob', 24), (3, 'Charlie', 29), (4, 'Diana', 35), (5, 'Eve', 40)]
#__IDS_EXPECTED__
#fetchone(): (1, 'Alice', 30)
#fetchmany(2): [(1, 'Alice', 30), (2, 'Bob', 24)]
#fetchall(): [(1, 'Alice', 30), (2, 'Bob', 24), (3, 'Charlie', 29), (4, 'Diana', 35), (5, 'Eve', 40)]

