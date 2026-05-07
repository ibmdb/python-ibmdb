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
    
    def test_313_FetchMany(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_313)

    def run_test_313(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        # ================================================================
        # Test 1: Basic types (INTEGER, VARCHAR, DECIMAL) - original test
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE animals')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE animals (id INTEGER, breed VARCHAR(32), name VARCHAR(16), weight DECIMAL(7,2))')
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (0, 'cat', 'Pook', 3.2)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (1, 'dog', 'Max', 12.5)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (2, 'parrot', 'Polly', 0.8)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (3, 'rabbit', 'Bunny', 2.3)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (4, 'hamster', 'Nibbles', 0.5)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (5, 'fish', 'Bubbles', 0.2)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (6, 'snake', 'Slither', 1.1)")
        ibm_db.exec_immediate(conn, "INSERT INTO animals VALUES (7, 'horse', 'Thunder', 450.7)")

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY id")
        rows = ibm_db.fetchmany(stmt, 2)
        print(rows)

        # ================================================================
        # Test 2: All numeric types (SMALLINT, INTEGER, BIGINT, REAL,
        #         DOUBLE, DECIMAL, NUMERIC)
        # Uses float values exact in binary to avoid precision issues
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_numeric')
        except:
            pass

        ibm_db.exec_immediate(conn, '''CREATE TABLE test_fm_numeric (
            c_si SMALLINT,
            c_int INTEGER,
            c_bi BIGINT,
            c_real REAL,
            c_double DOUBLE,
            c_dec DECIMAL(10,2),
            c_num NUMERIC(8,4)
        )''')
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_numeric VALUES (1, 100, 1000000, 1.5, 2.5, 10.55, 0.1234)")
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_numeric VALUES (2, 200, 2000000, 3.0, 5.0, 21.10, 0.2468)")
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_numeric VALUES (3, 300, 3000000, 4.5, 7.5, 31.65, 0.3702)")

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_numeric ORDER BY c_si")
        rows = ibm_db.fetchmany(stmt, 2)
        print(rows)

        # ================================================================
        # Test 3: DateTime types (DATE, TIME, TIMESTAMP)
        # Returns datetime.date, datetime.time, datetime.datetime objects
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_datetime')
        except:
            pass

        ibm_db.exec_immediate(conn, '''CREATE TABLE test_fm_datetime (
            c_id INTEGER,
            c_date DATE,
            c_time TIME,
            c_ts TIMESTAMP
        )''')
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_datetime VALUES (1, '2025-01-15', '10:30:00', '2025-01-15 10:30:00.000000')")
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_datetime VALUES (2, '2025-02-16', '11:45:00', '2025-02-16 11:45:00.000000')")
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_datetime VALUES (3, '2025-03-17', '12:00:30', '2025-03-17 12:00:30.123456')")

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_datetime ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print(rows)

        # ================================================================
        # Test 4: Binary types (VARCHAR FOR BIT DATA)
        # Returns Python bytes objects
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_binary')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_binary (c_id INTEGER, c_bin VARCHAR(10) FOR BIT DATA)')
        stmt_ins = ibm_db.prepare(conn, "INSERT INTO test_fm_binary VALUES (?, ?)")
        ibm_db.bind_param(stmt_ins, 1, 1)
        ibm_db.bind_param(stmt_ins, 2, b'\x01\x02\x03', ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_VARBINARY)
        ibm_db.execute(stmt_ins)
        ibm_db.bind_param(stmt_ins, 1, 2)
        ibm_db.bind_param(stmt_ins, 2, b'\x04\x05\x06', ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_VARBINARY)
        ibm_db.execute(stmt_ins)

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_binary ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print(rows)

        # ================================================================
        # Test 5: CLOB + BLOB (separate table for LOB types)
        # CLOB returns as Python str, BLOB returns as Python bytes
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_lob')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_lob (c_id INTEGER, c_clob CLOB(1024), c_blob BLOB(1024))')
        stmt_ins = ibm_db.prepare(conn, "INSERT INTO test_fm_lob VALUES (?, ?, ?)")
        for i in range(1, 4):
            ibm_db.bind_param(stmt_ins, 1, i)
            ibm_db.bind_param(stmt_ins, 2, 'CLOB_data_%d' % i, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_CLOB)
            ibm_db.bind_param(stmt_ins, 3, ('BLOB_%d' % i).encode('utf-8'), ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            ibm_db.execute(stmt_ins)

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_lob ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print("LOB: %d rows" % len(rows))
        for r in rows:
            print("id=%d clob=%s blob=%s" % (r[0], r[1], r[2].decode('utf-8')))

        # ================================================================
        # Test 5b: DBCLOB (separate table)
        # DBCLOB returns as Python str
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_dbclob')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_dbclob (c_id INTEGER, c_dbclob DBCLOB(1024))')
        stmt_ins = ibm_db.prepare(conn, "INSERT INTO test_fm_dbclob VALUES (?, ?)")
        for i in range(1, 3):
            ibm_db.bind_param(stmt_ins, 1, i)
            ibm_db.bind_param(stmt_ins, 2, 'DBCLOB_text_%d' % i, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_CLOB)
            ibm_db.execute(stmt_ins)

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_dbclob ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print("DBCLOB: %d rows, row0=%s" % (len(rows), rows[0][1]))

        # ================================================================
        # Test 5c: XML (separate table)
        # XML returns as Python str
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_xml')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_xml (c_id INTEGER, c_xml XML)')
        stmt_ins = ibm_db.prepare(conn, "INSERT INTO test_fm_xml VALUES (?, ?)")
        for i in range(1, 3):
            xml_val = '<root><id>%d</id><name>test_%d</name></root>' % (i, i)
            ibm_db.bind_param(stmt_ins, 1, i)
            ibm_db.bind_param(stmt_ins, 2, xml_val, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_XML)
            ibm_db.execute(stmt_ins)

        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_xml ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print("XML: %d rows, row0_has_id=%s" % (len(rows), str('<id>1</id>' in str(rows[0][1]))))

        # ================================================================
        # Test 6: fetchmany in batches (fetch 3 at a time from 8 rows)
        # ================================================================
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY id")
        total = 0
        batches = 0
        while True:
            chunk = ibm_db.fetchmany(stmt, 3)
            if not chunk:
                break
            batches += 1
            total += len(chunk)
        print("Batches: %d batches, %d total rows" % (batches, total))

        # ================================================================
        # Test 7: fetchmany all at once (fetch all 8 in one call)
        # ================================================================
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY id")
        rows = ibm_db.fetchmany(stmt, 8)
        print("AllAtOnce: %d rows, last=(%d, '%s')" % (len(rows), rows[-1][0], rows[-1][1]))

        # ================================================================
        # Test 8: Data integrity check on numeric table
        # Verify fetchmany returns correct values for each row
        # ================================================================
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_numeric ORDER BY c_si")
        rows = ibm_db.fetchmany(stmt, 3)
        errors = 0
        for idx, row in enumerate(rows):
            expected_si = idx + 1
            expected_int = (idx + 1) * 100
            expected_bi = (idx + 1) * 1000000
            if row[0] != expected_si:
                errors += 1
            if row[1] != expected_int:
                errors += 1
            if row[2] != expected_bi:
                errors += 1
        print("Integrity: %d rows checked, %d errors" % (len(rows), errors))

        # ================================================================
        # Test 9: SQL_ATTR_ROW_ARRAY_SIZE - set_option / get_option
        # Set custom rowset size, verify it, then fetch with it
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_rowset')
        except:
            pass

        ibm_db.exec_immediate(conn, '''CREATE TABLE test_fm_rowset (
            c_id INTEGER, c_name VARCHAR(30), c_val DECIMAL(8,2), c_ts TIMESTAMP
        )''')
        stmt_ins = ibm_db.prepare(conn, "INSERT INTO test_fm_rowset VALUES (?, ?, ?, ?)")
        for i in range(20):
            ibm_db.bind_param(stmt_ins, 1, i + 1)
            ibm_db.bind_param(stmt_ins, 2, "Row_%03d" % (i + 1))
            ibm_db.bind_param(stmt_ins, 3, str(round((i + 1) * 1.25, 2)))
            ibm_db.bind_param(stmt_ins, 4, "2025-07-%02d 08:00:00.000000" % ((i % 28) + 1))
            ibm_db.execute(stmt_ins)

        # 9a: set_option / get_option for SQL_ATTR_ROW_ARRAY_SIZE
        stmt2 = ibm_db.prepare(conn, "SELECT * FROM test_fm_rowset ORDER BY c_id")
        ibm_db.set_option(stmt2, {ibm_db.SQL_ATTR_ROW_ARRAY_SIZE: 5}, 0)
        value = ibm_db.get_option(stmt2, ibm_db.SQL_ATTR_ROW_ARRAY_SIZE, 0)
        print("RowsetSize: %s" % str(value))

        # 9b: fetchmany with custom SQL_ATTR_ROW_ARRAY_SIZE
        ibm_db.execute(stmt2)
        total = 0
        batches = 0
        while True:
            chunk = ibm_db.fetchmany(stmt2, 7)
            if not chunk:
                break
            batches += 1
            total += len(chunk)
        print("RowsetFetch: %d batches, %d total rows" % (batches, total))

        # 9c: Verify data integrity with custom rowset size
        stmt3 = ibm_db.prepare(conn, "SELECT * FROM test_fm_rowset ORDER BY c_id")
        ibm_db.set_option(stmt3, {ibm_db.SQL_ATTR_ROW_ARRAY_SIZE: 3}, 0)
        ibm_db.execute(stmt3)
        rows = ibm_db.fetchmany(stmt3, 5)
        rs_errors = 0
        for i, row in enumerate(rows):
            if row[0] != i + 1:
                rs_errors += 1
            if str(row[1]) != "Row_%03d" % (i + 1):
                rs_errors += 1
        print("RowsetIntegrity: %d rows, %d errors" % (len(rows), rs_errors))

        # ================================================================
        # Test 10: DECFLOAT type
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_decfloat')
        except:
            pass

        ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_decfloat (c_id INTEGER, c_df DECFLOAT)')
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_decfloat VALUES (1, 123.456)")
        ibm_db.exec_immediate(conn, "INSERT INTO test_fm_decfloat VALUES (2, 789.012)")
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_decfloat ORDER BY c_id")
        rows = ibm_db.fetchmany(stmt, 2)
        print("DECFLOAT: %d rows, r0=(%d, %s)" % (len(rows), rows[0][0], rows[0][1]))

        # ================================================================
        # Test 11: BOOLEAN type (LUW only, not z/OS)
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_bool')
        except:
            pass

        try:
            ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_bool (c_id INTEGER, c_bool BOOLEAN)')
            ibm_db.exec_immediate(conn, "INSERT INTO test_fm_bool VALUES (1, TRUE)")
            ibm_db.exec_immediate(conn, "INSERT INTO test_fm_bool VALUES (2, FALSE)")
            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_bool ORDER BY c_id")
            rows = ibm_db.fetchmany(stmt, 2)
            print("BOOLEAN: %d rows, r0_bool=%s, r1_bool=%s" % (len(rows), bool(rows[0][1]), bool(rows[1][1])))
        except:
            print("BOOLEAN: SKIP")

        # ================================================================
        # Test 12: GRAPHIC and VARGRAPHIC types
        # ================================================================
        try:
            ibm_db.exec_immediate(conn, 'DROP TABLE test_fm_graphic')
        except:
            pass

        try:
            ibm_db.exec_immediate(conn, 'CREATE TABLE test_fm_graphic (c_id INTEGER, c_gr GRAPHIC(10), c_vgr VARGRAPHIC(20))')
            ibm_db.exec_immediate(conn, "INSERT INTO test_fm_graphic VALUES (1, 'GR_0001', 'VGR_test_1')")
            ibm_db.exec_immediate(conn, "INSERT INTO test_fm_graphic VALUES (2, 'GR_0002', 'VGR_test_2')")
            stmt = ibm_db.exec_immediate(conn, "SELECT * FROM test_fm_graphic ORDER BY c_id")
            rows = ibm_db.fetchmany(stmt, 2)
            print("GRAPHIC: %d rows, r0_vgr=%s" % (len(rows), rows[0][2]))
        except:
            print("GRAPHIC: SKIP")

        # ================================================================
        # Test 13: DBI fetchmany (DB-API 2.0 interface)
        # ================================================================
        import ibm_db_dbi
        dbi_conn = ibm_db_dbi.Connection(conn)
        cursor = dbi_conn.cursor()
        cursor.execute("SELECT id, breed, name FROM animals ORDER BY id")
        rows = cursor.fetchmany(2)
        print("DBI: %d rows, row0=(%s, '%s', '%s')" % (len(rows), rows[0][0], rows[0][1], rows[0][2]))
        cursor.close()

        # ================================================================
        # Test 14: Empty result set - must return empty list, not None
        # ================================================================
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals WHERE id > 999")
        rows = ibm_db.fetchmany(stmt, 2)
        print("Empty: %d rows, is_list=%s" % (len(rows), isinstance(rows, list)))

        # ================================================================
        # Test 15: fetchmany after exhaustion - must return empty list, not None
        # ================================================================
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM animals ORDER BY id")
        rows1 = ibm_db.fetchmany(stmt, 8)  # fetch all 8 rows
        rows2 = ibm_db.fetchmany(stmt, 5)  # should return empty list
        print("Exhausted: %d rows, is_list=%s" % (len(rows2), isinstance(rows2, list)))

        ibm_db.rollback(conn)

#__END__
#__LUW_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50')]
#[(1, 100, 1000000, 1.5, 2.5, '10.55', '0.1234'), (2, 200, 2000000, 3.0, 5.0, '21.10', '0.2468')]
#[(1, datetime.date(2025, 1, 15), datetime.time(10, 30), datetime.datetime(2025, 1, 15, 10, 30)), (2, datetime.date(2025, 2, 16), datetime.time(11, 45), datetime.datetime(2025, 2, 16, 11, 45))]
#[(1, b'\x01\x02\x03'), (2, b'\x04\x05\x06')]
#LOB: 2 rows
#id=1 clob=CLOB_data_1 blob=BLOB_1
#id=2 clob=CLOB_data_2 blob=BLOB_2
#DBCLOB: 2 rows, row0=DBCLOB_text_1
#XML: 2 rows, row0_has_id=True
#Batches: 3 batches, 8 total rows
#AllAtOnce: 8 rows, last=(7, 'horse')
#Integrity: 3 rows checked, 0 errors
#RowsetSize: 5
#RowsetFetch: 3 batches, 20 total rows
#RowsetIntegrity: 5 rows, 0 errors
#DECFLOAT: 2 rows, r0=(1, 123.456)
#BOOLEAN: 2 rows, r0_bool=True, r1_bool=False
#GRAPHIC: 2 rows, r0_vgr=VGR_test_1
#DBI: 2 rows, row0=(0, 'cat', 'Pook')
#Empty: 0 rows, is_list=True
#Exhausted: 0 rows, is_list=True
#__ZOS_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50')]
#[(1, 100, 1000000, 1.5, 2.5, '10.55', '0.1234'), (2, 200, 2000000, 3.0, 5.0, '21.10', '0.2468')]
#[(1, datetime.date(2025, 1, 15), datetime.time(10, 30), datetime.datetime(2025, 1, 15, 10, 30)), (2, datetime.date(2025, 2, 16), datetime.time(11, 45), datetime.datetime(2025, 2, 16, 11, 45))]
#[(1, b'\x01\x02\x03'), (2, b'\x04\x05\x06')]
#LOB: 2 rows
#id=1 clob=CLOB_data_1 blob=BLOB_1
#id=2 clob=CLOB_data_2 blob=BLOB_2
#DBCLOB: 2 rows, row0=DBCLOB_text_1
#XML: 2 rows, row0_has_id=True
#Batches: 3 batches, 8 total rows
#AllAtOnce: 8 rows, last=(7, 'horse')
#Integrity: 3 rows checked, 0 errors
#RowsetSize: 5
#RowsetFetch: 3 batches, 20 total rows
#RowsetIntegrity: 5 rows, 0 errors
#DECFLOAT: 2 rows, r0=(1, 123.456)
#BOOLEAN: SKIP
#GRAPHIC: 2 rows, r0_vgr=VGR_test_1
#DBI: 2 rows, row0=(0, 'cat', 'Pook')
#Empty: 0 rows, is_list=True
#Exhausted: 0 rows, is_list=True
#__SYSTEMI_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50')]
#[(1, 100, 1000000, 1.5, 2.5, '10.55', '0.1234'), (2, 200, 2000000, 3.0, 5.0, '21.10', '0.2468')]
#[(1, datetime.date(2025, 1, 15), datetime.time(10, 30), datetime.datetime(2025, 1, 15, 10, 30)), (2, datetime.date(2025, 2, 16), datetime.time(11, 45), datetime.datetime(2025, 2, 16, 11, 45))]
#[(1, b'\x01\x02\x03'), (2, b'\x04\x05\x06')]
#LOB: 2 rows
#id=1 clob=CLOB_data_1 blob=BLOB_1
#id=2 clob=CLOB_data_2 blob=BLOB_2
#DBCLOB: 2 rows, row0=DBCLOB_text_1
#XML: 2 rows, row0_has_id=True
#Batches: 3 batches, 8 total rows
#AllAtOnce: 8 rows, last=(7, 'horse')
#Integrity: 3 rows checked, 0 errors
#RowsetSize: 5
#RowsetFetch: 3 batches, 20 total rows
#RowsetIntegrity: 5 rows, 0 errors
#DECFLOAT: 2 rows, r0=(1, 123.456)
#BOOLEAN: SKIP
#GRAPHIC: SKIP
#DBI: 2 rows, row0=(0, 'cat', 'Pook')
#Empty: 0 rows, is_list=True
#Exhausted: 0 rows, is_list=True
#__IDS_EXPECTED__
#[(0, 'cat', 'Pook', '3.20'), (1, 'dog', 'Max', '12.50')]
#[(1, 100, 1000000, 1.5, 2.5, '10.55', '0.1234'), (2, 200, 2000000, 3.0, 5.0, '21.10', '0.2468')]
#[(1, datetime.date(2025, 1, 15), datetime.time(10, 30), datetime.datetime(2025, 1, 15, 10, 30)), (2, datetime.date(2025, 2, 16), datetime.time(11, 45), datetime.datetime(2025, 2, 16, 11, 45))]
#[(1, b'\x01\x02\x03'), (2, b'\x04\x05\x06')]
#LOB: 2 rows
#id=1 clob=CLOB_data_1 blob=BLOB_1
#id=2 clob=CLOB_data_2 blob=BLOB_2
#DBCLOB: 2 rows, row0=DBCLOB_text_1
#XML: 2 rows, row0_has_id=True
#Batches: 3 batches, 8 total rows
#AllAtOnce: 8 rows, last=(7, 'horse')
#Integrity: 3 rows checked, 0 errors
#RowsetSize: 5
#RowsetFetch: 3 batches, 20 total rows
#RowsetIntegrity: 5 rows, 0 errors
#DECFLOAT: SKIP
#BOOLEAN: SKIP
#GRAPHIC: SKIP
#DBI: 2 rows, row0=(0, 'cat', 'Pook')
#Empty: 0 rows, is_list=True
#Exhausted: 0 rows, is_list=True
