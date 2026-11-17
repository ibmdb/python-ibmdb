#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2026
#

from __future__ import print_function
import gc
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_6795_SetOptionNoLeak(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6795)

    def count_lists(self):
        gc.collect()
        return sum(1 for o in gc.get_objects() if type(o) is list)

    def run_test_6795(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            server = ibm_db.server_info(conn)
            if not server.DBMS_NAME.startswith('DB2/'):
                print("SKIPPED")
                ibm_db.close(conn)
                return

            stmt = ibm_db.prepare(conn, "SELECT 1 FROM SYSIBM.SYSDUMMY1")
            n = 2000

            # Each options dict used to leak the list of its keys
            before = self.count_lists()
            for i in range(n):
                ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT: 0}, 0)
            leaked = self.count_lists() - before
            print("int option leaked lists: %s" % ("yes" if leaked >= n // 2 else "no"))

            # Same on the early return taken when an option is invalid
            before = self.count_lists()
            for i in range(n):
                try:
                    ibm_db.set_option(stmt, {ibm_db.ATTR_CASE: 99}, 0)
                except Exception:
                    pass
            leaked = self.count_lists() - before
            print("error path leaked lists: %s" % ("yes" if leaked >= n // 2 else "no"))

            # A string option value must not gain a reference per call
            schema = str(bytearray(config.user.upper(), "utf-8"), "utf-8")
            base = sys.getrefcount(schema)
            for i in range(1000):
                ibm_db.set_option(conn, {ibm_db.SQL_ATTR_CURRENT_SCHEMA: schema}, 1)
            print("string option refcount delta: %d" % (sys.getrefcount(schema) - base))
            print("string still usable: %s" % (schema == config.user.upper()))

            # Same for the string-valued zLOAD statement attributes
            if hasattr(ibm_db, 'SQL_ATTR_DB2ZLOAD_LOADSTMT'):
                load_stmt = str(bytearray("LOAD DATA INTO TABLE T1", "utf-8"), "utf-8")
                base = sys.getrefcount(load_stmt)
                for i in range(1000):
                    try:
                        ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_DB2ZLOAD_LOADSTMT: load_stmt}, 0)
                    except Exception:
                        pass
                delta = sys.getrefcount(load_stmt) - base
            else:
                delta = 0
            print("zload string option refcount delta: %d" % delta)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int option leaked lists: no
#error path leaked lists: no
#string option refcount delta: 0
#string still usable: True
#zload string option refcount delta: 0
#__ZOS_EXPECTED__
#SKIPPED
#__SYSTEMI_EXPECTED__
#SKIPPED
#__IDS_EXPECTED__
#SKIPPED
