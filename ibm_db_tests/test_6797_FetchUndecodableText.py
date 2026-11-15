#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2026
#

from __future__ import print_function
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_6797_FetchUndecodableText(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6797)

    def fetch(self, conn, api):
        sql = "SELECT c FROM test_6797 WHERE id = 1"
        try:
            if api.startswith("dbi "):
                cursor = ibm_db_dbi.Connection(conn).cursor()
                cursor.execute(sql)
                if api == "dbi fetchmany":
                    cursor.fetchmany(1)
                else:
                    getattr(cursor, api.split()[1])()
            else:
                stmt = ibm_db.exec_immediate(conn, sql)
                if api == "result":
                    ibm_db.fetch_row(stmt)
                    ibm_db.result(stmt, 0)
                elif api == "fetchmany":
                    ibm_db.fetchmany(stmt, 1)
                else:
                    getattr(ibm_db, api)(stmt)
        except Exception as e:
            return type(e).__name__
        return "no error"

    def run_test_6797(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            server = ibm_db.server_info(conn)
            if not server.DBMS_NAME.startswith('DB2/'):
                print("SKIPPED")
                ibm_db.close(conn)
                return

            try:
                ibm_db.exec_immediate(conn, "DROP TABLE test_6797")
            except:
                pass
            ibm_db.exec_immediate(conn, "CREATE TABLE test_6797 (id INTEGER, c VARCHAR(20))")
            # "SERVER " followed by the UTF-8 style encoding of a lone high
            # surrogate (U+D83E), which cannot be decoded. Older drivers could
            # store such values when an emoji was cut in half on insert.
            # Needs a Unicode (UTF-8) database, like the other emoji tests.
            ibm_db.exec_immediate(conn, "INSERT INTO test_6797 VALUES (1, CAST(X'53455256455220EDA0BE' AS VARCHAR(20) FOR BIT DATA))")
            ibm_db.exec_immediate(conn, "INSERT INTO test_6797 VALUES (2, 'valid')")

            for api in ("fetch_tuple", "fetch_assoc", "fetch_both", "result", "fetchone",
                        "fetchmany", "fetchall", "dbi fetchone", "dbi fetchmany", "dbi fetchall"):
                print("%s: %s" % (api, self.fetch(conn, api)))

            stmt = ibm_db.exec_immediate(conn, "SELECT c FROM test_6797 WHERE id = 2")
            print("valid row after: %s" % ibm_db.fetch_tuple(stmt)[0])

            ibm_db.exec_immediate(conn, "DROP TABLE test_6797")
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#fetch_tuple: UnicodeDecodeError
#fetch_assoc: UnicodeDecodeError
#fetch_both: UnicodeDecodeError
#result: UnicodeDecodeError
#fetchone: UnicodeDecodeError
#fetchmany: UnicodeDecodeError
#fetchall: UnicodeDecodeError
#dbi fetchone: UnicodeDecodeError
#dbi fetchmany: UnicodeDecodeError
#dbi fetchall: UnicodeDecodeError
#valid row after: valid
#__ZOS_EXPECTED__
#SKIPPED
#__SYSTEMI_EXPECTED__
#SKIPPED
#__IDS_EXPECTED__
#SKIPPED
