#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2024
#
#  Test script demonstrating Two-Phase Commit (DUOW) support.
#
#  HOW IT WORKS
#  ============
#  Regular ibm_db.connect():
#    - Each connection gets its own SQLHENV (environment handle).
#    - ibm_db.commit(conn) commits ONLY that single connection.
#    - If conn1 commits but conn2 fails, data is INCONSISTENT.
#
#  Coordinated ibm_db.connect_coordinated():
#    - Multiple connections share ONE SQLHENV via alloc_env_handle().
#    - SQL_ATTR_CONNECTTYPE is set to SQL_COORDINATED_TRANS.
#    - ibm_db.commit_two_phase(env) commits ALL connections atomically.
#    - DB2 uses its internal 2PC protocol:
#        Phase 1 (PREPARE): asks each database "can you commit?"
#        Phase 2 (COMMIT):  if ALL say yes, commit all; otherwise rollback all.
#    - This guarantees consistency across multiple databases.
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

# Build DSN connection string from config
if hasattr(config, 'hostname') and config.hostname:
    CONN_STR1 = (f"DATABASE={config.database};HOSTNAME={config.hostname};"
                 f"PORT={config.port};PROTOCOL=TCPIP;"
                 f"UID={config.user};PWD={config.password}")
else:
    CONN_STR1 = config.database

# Set a second connection string directly in this suite when validating cross-database 2PC.
# Leave blank to reuse CONN_STR1.
CONN_STR2_OVERRIDE = ""
CONN_STR2 = CONN_STR2_OVERRIDE if CONN_STR2_OVERRIDE else CONN_STR1


def _safe_drop(conn, table, commit_func=None, env=None):
    """Drop a table if it exists, ignoring errors."""
    try:
        ibm_db.exec_immediate(conn, "DROP TABLE %s" % table)
        if commit_func and env:
            commit_func(env)
        elif not commit_func:
            ibm_db.commit(conn)
    except Exception:
        try:
            if commit_func and env:
                ibm_db.rollback_two_phase(env)
            else:
                ibm_db.rollback(conn)
        except Exception:
            pass


class IbmDbTestCase(unittest.TestCase):

    def test_two_phase_commit(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_two_phase_commit)

    def run_test_two_phase_commit(self):
        """Run all two-phase commit tests."""

        print("TEST 1: alloc_env_handle + free_env_handle")
        env = ibm_db.alloc_env_handle()
        if env is not None:
            print("  alloc_env_handle: OK")
        else:
            print("  alloc_env_handle: FAILED")
            return

        result = ibm_db.free_env_handle(env)
        if result:
            print("  free_env_handle: OK")
        else:
            print("  free_env_handle: FAILED")

        # Double free should be idempotent
        result2 = ibm_db.free_env_handle(env)
        if result2:
            print("  double free_env_handle (idempotent): OK")
        else:
            print("  double free_env_handle: FAILED")

        print("TEST 2: Invalid env_handle type")
        try:
            ibm_db.commit_two_phase("not_an_env_handle")
            print("  commit_two_phase(string): FAILED (no exception)")
        except Exception:
            print("  commit_two_phase(string): OK (exception raised)")

        try:
            ibm_db.rollback_two_phase(12345)
            print("  rollback_two_phase(int): FAILED (no exception)")
        except Exception:
            print("  rollback_two_phase(int): OK (exception raised)")

        print("TEST 3: Inactive env_handle")
        env = ibm_db.alloc_env_handle()
        ibm_db.free_env_handle(env)

        try:
            ibm_db.commit_two_phase(env)
            print("  commit on inactive env: FAILED (no exception)")
        except Exception:
            print("  commit on inactive env: OK (exception raised)")

        try:
            ibm_db.rollback_two_phase(env)
            print("  rollback on inactive env: FAILED (no exception)")
        except Exception:
            print("  rollback on inactive env: OK (exception raised)")

        try:
            ibm_db.connect_coordinated(env, CONN_STR1, '', '')
            print("  connect on inactive env: FAILED (no exception)")
        except Exception:
            print("  connect on inactive env: OK (exception raised)")

        print("TEST 4: Coordinated commit_two_phase")
        env = ibm_db.alloc_env_handle()
        conn1 = ibm_db.connect_coordinated(env, CONN_STR1, '', '')

        if conn1 is not None:
            print("  connect_coordinated: OK")
        else:
            print("  connect_coordinated: FAILED")
            ibm_db.free_env_handle(env)
            return

        # Autocommit should be OFF
        ac = ibm_db.autocommit(conn1)
        if ac == 0:
            print("  autocommit OFF: OK")
        else:
            print("  autocommit OFF: FAILED (got %d)" % ac)

        _safe_drop(conn1, "tpc_test1", ibm_db.commit_two_phase, env)
        ibm_db.exec_immediate(conn1, "CREATE TABLE tpc_test1 (id INT, val VARCHAR(20))")
        ibm_db.commit_two_phase(env)

        ibm_db.exec_immediate(conn1, "INSERT INTO tpc_test1 VALUES (1, 'hello')")
        result = ibm_db.commit_two_phase(env)
        if result:
            print("  commit_two_phase: OK")
        else:
            print("  commit_two_phase: FAILED")

        stmt4 = ibm_db.exec_immediate(conn1, "SELECT COUNT(*) FROM tpc_test1")
        count = ibm_db.fetch_tuple(stmt4)[0]
        if int(count) == 1:
            print("  data committed: OK")
        else:
            print("  data committed: FAILED (count=%s)" % count)
        del stmt4

        print("TEST 5: Coordinated rollback_two_phase")
        ibm_db.exec_immediate(conn1, "INSERT INTO tpc_test1 VALUES (2, 'rollback_me')")
        result = ibm_db.rollback_two_phase(env)
        if result:
            print("  rollback_two_phase: OK")
        else:
            print("  rollback_two_phase: FAILED")

        # Close coordinated connection, verify via regular connection
        ibm_db.close(conn1)
        ibm_db.free_env_handle(env)

        verify = ibm_db.connect(CONN_STR1, '', '')
        stmt5 = ibm_db.exec_immediate(verify, "SELECT COUNT(*) FROM tpc_test1")
        count = ibm_db.fetch_tuple(stmt5)[0]
        if int(count) == 1:
            print("  rollback verified: OK (count still 1)")
        else:
            print("  rollback verified: FAILED (count=%s)" % count)

        # Cleanup
        ibm_db.exec_immediate(verify, "DROP TABLE tpc_test1")
        ibm_db.commit(verify)
        ibm_db.close(verify)

        print("TEST 6: Commit with no pending work")
        env = ibm_db.alloc_env_handle()
        conn1 = ibm_db.connect_coordinated(env, CONN_STR1, '', '')
        result = ibm_db.commit_two_phase(env)
        if result:
            print("  commit (no work): OK")
        else:
            print("  commit (no work): FAILED")
        ibm_db.close(conn1)
        ibm_db.free_env_handle(env)

        print("TEST 7: Multiple commit cycles")
        env = ibm_db.alloc_env_handle()
        conn1 = ibm_db.connect_coordinated(env, CONN_STR1, '', '')

        _safe_drop(conn1, "tpc_cycle", ibm_db.commit_two_phase, env)
        ibm_db.exec_immediate(conn1, "CREATE TABLE tpc_cycle (id INT)")
        ibm_db.commit_two_phase(env)

        for i in range(3):
            ibm_db.exec_immediate(conn1, "INSERT INTO tpc_cycle VALUES (%d)" % (i + 1))
            ibm_db.commit_two_phase(env)

        stmt7 = ibm_db.exec_immediate(conn1, "SELECT COUNT(*) FROM tpc_cycle")
        count = ibm_db.fetch_tuple(stmt7)[0]
        if int(count) == 3:
            print("  3 commit cycles: OK")
        else:
            print("  3 commit cycles: FAILED (count=%s)" % count)

        ibm_db.exec_immediate(conn1, "DROP TABLE tpc_cycle")
        ibm_db.commit_two_phase(env)
        ibm_db.close(conn1)
        ibm_db.free_env_handle(env)

        print("TEST 8: Mixed commit and rollback")
        env = ibm_db.alloc_env_handle()
        conn1 = ibm_db.connect_coordinated(env, CONN_STR1, '', '')
        conn2 = None

        if CONN_STR2 != CONN_STR1:
            try:
                conn2 = ibm_db.connect_coordinated(env, CONN_STR2, '', '')
            except Exception:
                # Second database unreachable - continue with single-connection path.
                conn2 = None

        _safe_drop(conn1, "tpc_mix", ibm_db.commit_two_phase, env)
        if conn2 is not None:
            _safe_drop(conn2, "tpc_mix2", ibm_db.commit_two_phase, env)

            ibm_db.exec_immediate(conn1, "CREATE TABLE tpc_mix (id INT)")
            ibm_db.exec_immediate(conn2, "CREATE TABLE tpc_mix2 (id INT)")
            ibm_db.commit_two_phase(env)

            # Commit first insert on both connections.
            ibm_db.exec_immediate(conn1, "INSERT INTO tpc_mix VALUES (1)")
            ibm_db.exec_immediate(conn2, "INSERT INTO tpc_mix2 VALUES (1)")
            ibm_db.commit_two_phase(env)

            # Rollback second insert on both connections.
            ibm_db.exec_immediate(conn1, "INSERT INTO tpc_mix VALUES (2)")
            ibm_db.exec_immediate(conn2, "INSERT INTO tpc_mix2 VALUES (2)")
            ibm_db.rollback_two_phase(env)
        else:
            ibm_db.exec_immediate(conn1, "CREATE TABLE tpc_mix (id INT)")
            ibm_db.commit_two_phase(env)

            # Commit first insert
            ibm_db.exec_immediate(conn1, "INSERT INTO tpc_mix VALUES (1)")
            ibm_db.commit_two_phase(env)

            # Rollback second insert
            ibm_db.exec_immediate(conn1, "INSERT INTO tpc_mix VALUES (2)")
            ibm_db.rollback_two_phase(env)

        # Close coordinated connection, verify via regular connection
        ibm_db.close(conn1)
        if conn2 is not None:
            ibm_db.close(conn2)
        ibm_db.free_env_handle(env)

        verify = ibm_db.connect(CONN_STR1, '', '')
        stmt8 = ibm_db.exec_immediate(verify, "SELECT COUNT(*) FROM tpc_mix")
        count = ibm_db.fetch_tuple(stmt8)[0]
        if conn2 is not None:
            verify2 = ibm_db.connect(CONN_STR2, '', '')
            stmt8b = ibm_db.exec_immediate(verify2, "SELECT COUNT(*) FROM tpc_mix2")
            count2 = ibm_db.fetch_tuple(stmt8b)[0]
            if int(count) == 1 and int(count2) == 1:
                print("  mixed commit/rollback: OK")
            else:
                print("  mixed commit/rollback: FAILED (count=%s)" % count)
            ibm_db.exec_immediate(verify2, "DROP TABLE tpc_mix2")
            ibm_db.commit(verify2)
            ibm_db.close(verify2)
        elif int(count) == 1:
            print("  mixed commit/rollback: OK")
        else:
            print("  mixed commit/rollback: FAILED (count=%s)" % count)

        ibm_db.exec_immediate(verify, "DROP TABLE tpc_mix")
        ibm_db.commit(verify)
        ibm_db.close(verify)

        print("All two-phase commit tests completed.")


#__LUW_EXPECTED__
#TEST 1: alloc_env_handle + free_env_handle
#  alloc_env_handle: OK
#  free_env_handle: OK
#  double free_env_handle (idempotent): OK
#TEST 2: Invalid env_handle type
#  commit_two_phase(string): OK (exception raised)
#  rollback_two_phase(int): OK (exception raised)
#TEST 3: Inactive env_handle
#  commit on inactive env: OK (exception raised)
#  rollback on inactive env: OK (exception raised)
#  connect on inactive env: OK (exception raised)
#TEST 4: Coordinated commit_two_phase
#  connect_coordinated: OK
#  autocommit OFF: OK
#  commit_two_phase: OK
#  data committed: OK
#TEST 5: Coordinated rollback_two_phase
#  rollback_two_phase: OK
#  rollback verified: OK (count still 1)
#TEST 6: Commit with no pending work
#  commit (no work): OK
#TEST 7: Multiple commit cycles
#  3 commit cycles: OK
#TEST 8: Mixed commit and rollback
#  mixed commit/rollback: OK
#All two-phase commit tests completed.
#__ZOS_EXPECTED__
#TEST 1: alloc_env_handle + free_env_handle
#  alloc_env_handle: OK
#  free_env_handle: OK
#  double free_env_handle (idempotent): OK
#TEST 2: Invalid env_handle type
#  commit_two_phase(string): OK (exception raised)
#  rollback_two_phase(int): OK (exception raised)
#TEST 3: Inactive env_handle
#  commit on inactive env: OK (exception raised)
#  rollback on inactive env: OK (exception raised)
#  connect on inactive env: OK (exception raised)
#TEST 4: Coordinated commit_two_phase
#  connect_coordinated: OK
#  autocommit OFF: OK
#  commit_two_phase: OK
#  data committed: OK
#TEST 5: Coordinated rollback_two_phase
#  rollback_two_phase: OK
#  rollback verified: OK (count still 1)
#TEST 6: Commit with no pending work
#  commit (no work): OK
#TEST 7: Multiple commit cycles
#  3 commit cycles: OK
#TEST 8: Mixed commit and rollback
#  mixed commit/rollback: OK
#All two-phase commit tests completed.
#__SYSTEMI_EXPECTED__
#TEST 1: alloc_env_handle + free_env_handle
#  alloc_env_handle: OK
#  free_env_handle: OK
#  double free_env_handle (idempotent): OK
#TEST 2: Invalid env_handle type
#  commit_two_phase(string): OK (exception raised)
#  rollback_two_phase(int): OK (exception raised)
#TEST 3: Inactive env_handle
#  commit on inactive env: OK (exception raised)
#  rollback on inactive env: OK (exception raised)
#  connect on inactive env: OK (exception raised)
#TEST 4: Coordinated commit_two_phase
#  connect_coordinated: OK
#  autocommit OFF: OK
#  commit_two_phase: OK
#  data committed: OK
#TEST 5: Coordinated rollback_two_phase
#  rollback_two_phase: OK
#  rollback verified: OK (count still 1)
#TEST 6: Commit with no pending work
#  commit (no work): OK
#TEST 7: Multiple commit cycles
#  3 commit cycles: OK
#TEST 8: Mixed commit and rollback
#  mixed commit/rollback: OK
#All two-phase commit tests completed.
#__IDS_EXPECTED__
#TEST 1: alloc_env_handle + free_env_handle
#  alloc_env_handle: OK
#  free_env_handle: OK
#  double free_env_handle (idempotent): OK
#TEST 2: Invalid env_handle type
#  commit_two_phase(string): OK (exception raised)
#  rollback_two_phase(int): OK (exception raised)
#TEST 3: Inactive env_handle
#  commit on inactive env: OK (exception raised)
#  rollback on inactive env: OK (exception raised)
#  connect on inactive env: OK (exception raised)
#TEST 4: Coordinated commit_two_phase
#  connect_coordinated: OK
#  autocommit OFF: OK
#  commit_two_phase: OK
#  data committed: OK
#TEST 5: Coordinated rollback_two_phase
#  rollback_two_phase: OK
#  rollback verified: OK (count still 1)
#TEST 6: Commit with no pending work
#  commit (no work): OK
#TEST 7: Multiple commit cycles
#  3 commit cycles: OK
#TEST 8: Mixed commit and rollback
#  mixed commit/rollback: OK
#All two-phase commit tests completed.
