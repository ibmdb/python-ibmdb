from __future__ import print_function
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sparray_cardinality_regressions(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_sparray_cardinality_regressions)

    def run_test_sparray_cardinality_regressions(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return

        cleanup = (
            "DROP PROCEDURE REGRESSION_ARRAY_LARGE_INPUT",
            "DROP PROCEDURE REGRESSION_ARRAY_PARTIAL_OUT",
            "DROP PROCEDURE REGRESSION_ARRAY_EMPTY_OUT",
            "DROP PROCEDURE REGRESSION_ARRAY_NULL_OUT",
            "DROP TYPE REGRESSION_LARGE_ARRAY",
            "DROP TYPE REGRESSION_SMALL_ARRAY",
        )
        for statement in cleanup:
            try:
                ibm_db.exec_immediate(conn, statement)
            except Exception:
                pass

        # Cardinality above SQLSMALLINT range must not be truncated.
        ibm_db.exec_immediate(
            conn, "CREATE TYPE REGRESSION_LARGE_ARRAY AS INTEGER ARRAY[32768]")
        ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE REGRESSION_ARRAY_LARGE_INPUT(
                IN var1 REGRESSION_LARGE_ARRAY,
                OUT var2 INTEGER
            )
            LANGUAGE SQL
            BEGIN
                SET var2 = CARDINALITY(var1);
            END
            """)
        stmt = ibm_db.prepare(conn, "CALL REGRESSION_ARRAY_LARGE_INPUT(?, ?)")
        ibm_db.bind_param(stmt, 1, list(range(32768)), ibm_db.SQL_PARAM_INPUT)
        ibm_db.bind_param(stmt, 2, 0, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_INTEGER)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_callproc(stmt)
        print("Large input cardinality:", result[2])

        # Driver reports fewer elements than were bound.
        ibm_db.exec_immediate(
            conn, "CREATE TYPE REGRESSION_SMALL_ARRAY AS INTEGER ARRAY[10]")
        ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE REGRESSION_ARRAY_PARTIAL_OUT(
                OUT var1 REGRESSION_SMALL_ARRAY
            )
            LANGUAGE SQL
            BEGIN
                SET var1[1] = 111;
                SET var1[2] = 222;
                SET var1[3] = 333;
            END
            """)
        stmt = ibm_db.prepare(conn, "CALL REGRESSION_ARRAY_PARTIAL_OUT(?)")
        ibm_db.bind_param(stmt, 1, [999] * 10, ibm_db.SQL_PARAM_OUTPUT)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_callproc(stmt)
        print("Partial output array:", result[1])

        # Unassigned OUT array comes back as a NULL array.
        ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE REGRESSION_ARRAY_NULL_OUT(
                OUT var1 REGRESSION_SMALL_ARRAY
            )
            LANGUAGE SQL
            BEGIN
                DECLARE unused INTEGER DEFAULT 0;
                SET unused = 1;
            END
            """)
        stmt = ibm_db.prepare(conn, "CALL REGRESSION_ARRAY_NULL_OUT(?)")
        ibm_db.bind_param(stmt, 1, [999] * 10, ibm_db.SQL_PARAM_OUTPUT)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_callproc(stmt)
        print("Null output array:", result[1])

        ibm_db.exec_immediate(conn, "DROP PROCEDURE REGRESSION_ARRAY_PARTIAL_OUT")
        ibm_db.exec_immediate(conn, "DROP PROCEDURE REGRESSION_ARRAY_NULL_OUT")
        ibm_db.exec_immediate(conn, "DROP TYPE REGRESSION_SMALL_ARRAY")

        # Empty OUT array reported as cardinality 0.
        ibm_db.exec_immediate(
            conn, "CREATE TYPE REGRESSION_SMALL_ARRAY AS INTEGER ARRAY[2]")
        ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE REGRESSION_ARRAY_EMPTY_OUT(
                OUT var1 REGRESSION_SMALL_ARRAY
            )
            LANGUAGE SQL
            BEGIN
                SET var1 = CAST(ARRAY[] AS REGRESSION_SMALL_ARRAY);
            END
            """)
        stmt = ibm_db.prepare(conn, "CALL REGRESSION_ARRAY_EMPTY_OUT(?)")
        ibm_db.bind_param(stmt, 1, [999, 999], ibm_db.SQL_PARAM_OUTPUT)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_callproc(stmt)
        print("Empty output array:", result[1])

        ibm_db.exec_immediate(conn, "DROP PROCEDURE REGRESSION_ARRAY_EMPTY_OUT")
        ibm_db.exec_immediate(conn, "DROP TYPE REGRESSION_SMALL_ARRAY")

        # Declared cardinality of 1 still honours a shrink to zero.
        ibm_db.exec_immediate(
            conn, "CREATE TYPE REGRESSION_SMALL_ARRAY AS INTEGER ARRAY[1]")
        ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE REGRESSION_ARRAY_EMPTY_OUT(
                OUT var1 REGRESSION_SMALL_ARRAY
            )
            LANGUAGE SQL
            BEGIN
                SET var1 = CAST(ARRAY[] AS REGRESSION_SMALL_ARRAY);
            END
            """)
        stmt = ibm_db.prepare(conn, "CALL REGRESSION_ARRAY_EMPTY_OUT(?)")
        ibm_db.bind_param(stmt, 1, [999], ibm_db.SQL_PARAM_OUTPUT)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_callproc(stmt)
        print("Single cardinality output array:", result[1])

        for statement in cleanup:
            try:
                ibm_db.exec_immediate(conn, statement)
            except Exception:
                pass
        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#Large input cardinality: 32768
#Partial output array: [111, 222, 333]
#Null output array: None
#Empty output array: []
#Single cardinality output array: []
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

