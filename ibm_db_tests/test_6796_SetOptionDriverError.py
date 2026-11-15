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

    def test_6796_SetOptionDriverError(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6796)

    def raised(self, func):
        try:
            func()
        except Exception as e:
            return e
        return None

    def run_test_6796(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            server = ibm_db.server_info(conn)
            # Driver attribute validation is only verified against Db2 LUW
            if sys.platform == 'zos' or not server.DBMS_NAME.startswith('DB2/'):
                print("SKIPPED")
                ibm_db.close(conn)
                return

            sql = "SELECT 1 FROM SYSIBM.SYSDUMMY1"
            # Statement attribute value rejected by the CLI driver
            bad_stmt_opt = {ibm_db.SQL_ATTR_REOPT: 99}
            # Connection attribute value rejected by the CLI driver
            bad_conn_opt = {ibm_db.SQL_ATTR_TXN_ISOLATION: 12345}

            stmt = ibm_db.prepare(conn, sql)
            e = self.raised(lambda: ibm_db.set_option(stmt, bad_stmt_opt, 0))
            print("stmt rejected: %s %s" % (type(e).__name__, type(e) is Exception))
            print("stmt message has SQLSTATE: %s" % ("SQLSTATE=" in str(e)))
            ibm_db.execute(stmt)
            print("stmt still usable: %s" % ibm_db.fetch_tuple(stmt)[0])

            e = self.raised(lambda: ibm_db.prepare(conn, sql, bad_stmt_opt))
            print("prepare rejected: %s %s" % (type(e).__name__, type(e) is Exception))
            e = self.raised(lambda: ibm_db.exec_immediate(conn, sql, bad_stmt_opt))
            print("exec_immediate rejected: %s %s" % (type(e).__name__, type(e) is Exception))

            # The statement allocated by a rejected call must be released.
            # set_option() on an existing statement parses the same options
            # without allocating one, so it serves as the baseline.
            def allocated(func):
                before = sys.getallocatedblocks()
                for i in range(1000):
                    self.raised(func)
                return sys.getallocatedblocks() - before
            baseline = allocated(lambda: ibm_db.set_option(stmt, bad_stmt_opt, 0))
            for name, func in (("prepare", ibm_db.prepare), ("exec_immediate", ibm_db.exec_immediate)):
                leaked = allocated(lambda: func(conn, sql, bad_stmt_opt)) - baseline
                print("rejected %s leaks: %s" % (name, "yes" if leaked >= 500 else "no"))

            # 3 is SQL_REOPT_ONCE
            stmt = ibm_db.prepare(conn, sql)
            rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_REOPT: 3}, 0)
            print("stmt reopt once: %s" % rc)

            e = self.raised(lambda: ibm_db.set_option(stmt, {ibm_db.ATTR_CASE: 99}, 0))
            print("attr_case message unchanged: %s" % (str(e) == "ATTR_CASE attribute must be one of CASE_LOWER, CASE_UPPER, or CASE_NATURAL"))
            e = self.raised(lambda: ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_ROW_ARRAY_SIZE: 0}, 0))
            print("row_array_size message unchanged: %s" % (str(e) == "SQL_ATTR_ROW_ARRAY_SIZE must be >= 1"))
            e = self.raised(lambda: ibm_db.prepare(conn, sql, {ibm_db.SQL_ATTR_ROW_ARRAY_SIZE: 0}))
            print("prepare row_array_size message unchanged: %s" % (str(e) == "SQL_ATTR_ROW_ARRAY_SIZE must be >= 1"))

            rc = ibm_db.set_option(conn, bad_conn_opt, 1)
            print("conn rejected: %s" % rc)
            msg = ibm_db.conn_errormsg(conn)
            print("conn errormsg set: %s" % ("SQLSTATE=" in msg))
            print("global conn errormsg untouched: %s" % (ibm_db.conn_errormsg() == ""))
            rc = ibm_db.set_option(conn, {ibm_db.SQL_ATTR_AUTOCOMMIT: ibm_db.SQL_AUTOCOMMIT_ON}, 1)
            print("conn valid set_option: %s" % rc)

            # A rejected string value must be released like an accepted one
            def refs_gained(value):
                value = str(bytearray(value, "utf-8"), "utf-8")
                base = sys.getrefcount(value)
                for i in range(1000):
                    rc = ibm_db.set_option(conn, {ibm_db.SQL_ATTR_INFO_USERID: value}, 1)
                return sys.getrefcount(value) - base, rc
            long_gained, long_rc = refs_gained("U" * 5000)
            short_gained, short_rc = refs_gained("TESTUSER")
            print("long string option rejected: %s" % (long_rc is False and short_rc is True))
            leaked = long_gained - short_gained
            print("rejected string option leaks: %s" % ("yes" if leaked >= 500 else "no"))
            ibm_db.close(conn)

            conn = ibm_db.connect(config.database, config.user, config.password, bad_conn_opt)
            print("connect with rejected attr: %s" % ("ok" if conn else "failed"))
            print("server_info after connect: %s" % ("ok" if ibm_db.server_info(conn) else "failed"))
            print("global conn errormsg after connect: %s" % repr(ibm_db.conn_errormsg()))
            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#stmt rejected: Exception True
#stmt message has SQLSTATE: True
#stmt still usable: 1
#prepare rejected: Exception True
#exec_immediate rejected: Exception True
#rejected prepare leaks: no
#rejected exec_immediate leaks: no
#stmt reopt once: True
#attr_case message unchanged: True
#row_array_size message unchanged: True
#prepare row_array_size message unchanged: True
#conn rejected: False
#conn errormsg set: True
#global conn errormsg untouched: True
#conn valid set_option: True
#long string option rejected: True
#rejected string option leaks: no
#connect with rejected attr: ok
#server_info after connect: ok
#global conn errormsg after connect: ''
#__ZOS_EXPECTED__
#SKIPPED
#__SYSTEMI_EXPECTED__
#SKIPPED
#__IDS_EXPECTED__
#SKIPPED
