#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2026
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_322_EmojiNonBMPRoundtrip(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_322)

    def run_test_322(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        # Drop the test table, in case it exists
        drop = 'DROP TABLE test_emoji_nonbmp'
        try:
            ibm_db.exec_immediate(conn, drop)
        except:
            pass

        # Create a table with VARCHAR and CLOB columns
        create = 'CREATE TABLE test_emoji_nonbmp (id INTEGER, c_varchar VARCHAR(200), c_clob CLOB(1M))'
        ibm_db.exec_immediate(conn, create)

        # Test strings: BMP-only and strings with non-BMP (supplementary) characters
        emoji = "\U0001f60a"          # U+1F60A SMILING FACE WITH SMILING EYES
        musical = "\U0001d11e"        # U+1D11E MUSICAL SYMBOL G CLEF
        flag = "\U0001f1fa\U0001f1f8" # Regional indicators U+S U+A (flag)

        cases = [
            (1, "plain ascii text"),
            (2, "BMP unicode: \u00e9\u00f1\u00fc\u00c5"),
            (3, "trailing emoji " + emoji),
            (4, "middle " + emoji + " emoji"),
            (5, emoji + " leading emoji"),
            (6, "musical clef: " + musical),
            (7, "multiple non-BMP: " + emoji + musical + flag),
            (8, emoji * 10),
        ]

        # Insert using prepared statements with parameter markers
        insert_sql = "INSERT INTO test_emoji_nonbmp (id, c_varchar, c_clob) VALUES (?, ?, ?)"
        for id_val, text in cases:
            stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.execute(stmt, (id_val, text, text))

        # Read back and verify round-trip
        select_sql = "SELECT id, c_varchar, c_clob FROM test_emoji_nonbmp ORDER BY id"
        stmt = ibm_db.exec_immediate(conn, select_sql)

        row = ibm_db.fetch_tuple(stmt)
        idx = 0
        while row:
            expected = cases[idx][1]
            id_val = row[0]
            varchar_val = row[1]
            clob_val = row[2]

            # Check VARCHAR round-trip
            if varchar_val == expected:
                print("id %d VARCHAR: OK" % id_val)
            else:
                print("id %d VARCHAR: FAIL (expected %r, got %r)" % (id_val, expected, varchar_val))

            # Check CLOB round-trip
            if clob_val == expected:
                print("id %d CLOB: OK" % id_val)
            else:
                print("id %d CLOB: FAIL (expected %r, got %r)" % (id_val, expected, clob_val))

            row = ibm_db.fetch_tuple(stmt)
            idx += 1

        ibm_db.rollback(conn)

#__END__
#__LUW_EXPECTED__
#id 1 VARCHAR: OK
#id 1 CLOB: OK
#id 2 VARCHAR: OK
#id 2 CLOB: OK
#id 3 VARCHAR: OK
#id 3 CLOB: OK
#id 4 VARCHAR: OK
#id 4 CLOB: OK
#id 5 VARCHAR: OK
#id 5 CLOB: OK
#id 6 VARCHAR: OK
#id 6 CLOB: OK
#id 7 VARCHAR: OK
#id 7 CLOB: OK
#id 8 VARCHAR: OK
#id 8 CLOB: OK
#__ZOS_EXPECTED__
#id 1 VARCHAR: OK
#id 1 CLOB: OK
#id 2 VARCHAR: OK
#id 2 CLOB: OK
#id 3 VARCHAR: OK
#id 3 CLOB: OK
#id 4 VARCHAR: OK
#id 4 CLOB: OK
#id 5 VARCHAR: OK
#id 5 CLOB: OK
#id 6 VARCHAR: OK
#id 6 CLOB: OK
#id 7 VARCHAR: OK
#id 7 CLOB: OK
#id 8 VARCHAR: OK
#id 8 CLOB: OK
#__SYSTEMI_EXPECTED__
#id 1 VARCHAR: OK
#id 1 CLOB: OK
#id 2 VARCHAR: OK
#id 2 CLOB: OK
#id 3 VARCHAR: OK
#id 3 CLOB: OK
#id 4 VARCHAR: OK
#id 4 CLOB: OK
#id 5 VARCHAR: OK
#id 5 CLOB: OK
#id 6 VARCHAR: OK
#id 6 CLOB: OK
#id 7 VARCHAR: OK
#id 7 CLOB: OK
#id 8 VARCHAR: OK
#id 8 CLOB: OK
#__IDS_EXPECTED__
#id 1 VARCHAR: OK
#id 1 CLOB: OK
#id 2 VARCHAR: OK
#id 2 CLOB: OK
#id 3 VARCHAR: OK
#id 3 CLOB: OK
#id 4 VARCHAR: OK
#id 4 CLOB: OK
#id 5 VARCHAR: OK
#id 5 CLOB: OK
#id 6 VARCHAR: OK
#id 6 CLOB: OK
#id 7 VARCHAR: OK
#id 7 CLOB: OK
#id 8 VARCHAR: OK
#id 8 CLOB: OK

