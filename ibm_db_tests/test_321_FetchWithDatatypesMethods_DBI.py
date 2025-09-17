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
import decimal
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_321_FetchWithDatatypesMethods_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_321)

    def _format_blob_rows(self, rows):
        """Convert memoryview BLOBs to strings for consistent output."""
        formatted = []
        for row in rows:
            id_, dec_val, blob_mv = row
            blob_bytes = bytes(blob_mv)
            blob_str = blob_bytes.decode('utf-8')
            formatted.append((id_, dec_val, blob_str))
        return formatted

    def run_test_321(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
        dbi_conn = ibm_db_dbi.Connection(conn)

        cur = dbi_conn.cursor()

        try:
            cur.execute("DROP TABLE dbiEmployeesDatatypes")
        except:
            pass

        create_sql = '''
            CREATE TABLE dbiEmployeesDatatypes (
                id INT PRIMARY KEY NOT NULL,
                SMTH DECIMAL(10,2),
                BDATA BLOB
            )
        '''
        cur.execute(create_sql)
        dbi_conn.commit()

        insert_sql = 'INSERT INTO dbiEmployeesDatatypes (id, SMTH, BDATA) VALUES (?, ?, ?)'
        for i in range(1, 6):
            dec_val = decimal.Decimal(f"{1000 + i * 0.5:.2f}")
            blob_val = f"Blob data {i}".encode("utf-8")
            cur.execute(insert_sql, (i, dec_val, blob_val))

        dbi_conn.commit()

        select_sql = "SELECT * FROM dbiEmployeesDatatypes ORDER BY id"

        # fetchall
        cur.execute(select_sql)
        all_rows = cur.fetchall()
        print(self._format_blob_rows(all_rows))

        # fetchmany(2)
        cur2 = dbi_conn.cursor()
        cur2.execute(select_sql)
        many_rows = cur2.fetchmany(2)
        print(self._format_blob_rows(many_rows))

        # fetchone
        cur3 = dbi_conn.cursor()
        cur3.execute(select_sql)
        one_row = cur3.fetchone()
        # format fetchone single row as tuple (id, decimal, string)
        id_, dec_val, blob_mv = one_row
        blob_str = bytes(blob_mv).decode('utf-8')
        print((id_, dec_val, blob_str))


#__END__
#__LUW_EXPECTED__
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2'), (3, Decimal('1001.50'), 'Blob data 3'), (4, Decimal('1002.00'), 'Blob data 4'), (5, Decimal('1002.50'), 'Blob data 5')]
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2')]
#(1, Decimal('1000.50'), 'Blob data 1')
#__ZOS_EXPECTED__
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2'), (3, Decimal('1001.50'), 'Blob data 3'), (4, Decimal('1002.00'), 'Blob data 4'), (5, Decimal('1002.50'), 'Blob data 5')]
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2')]
#(1, Decimal('1000.50'), 'Blob data 1')
#__SYSTEMI_EXPECTED__
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2'), (3, Decimal('1001.50'), 'Blob data 3'), (4, Decimal('1002.00'), 'Blob data 4'), (5, Decimal('1002.50'), 'Blob data 5')]
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2')]
#(1, Decimal('1000.50'), 'Blob data 1')
#__IDS_EXPECTED__
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2'), (3, Decimal('1001.50'), 'Blob data 3'), (4, Decimal('1002.00'), 'Blob data 4'), (5, Decimal('1002.50'), 'Blob data 5')]
#[(1, Decimal('1000.50'), 'Blob data 1'), (2, Decimal('1001.00'), 'Blob data 2')]
#(1, Decimal('1000.50'), 'Blob data 1')