from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_scalarsp_execute(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_scalarsp_execute)

    def run_test_scalarsp_execute(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        scalar_procs = [
        ("INTEGER", "int_scalar", 42),
        ("SMALLINT", "sint_scalar", 7),
        ("BIGINT", "bint_scalar", 1234),
        ("FLOAT", "float_scalar", 3.14),
        ("DOUBLE", "double_scalar", 20.25),
        ("REAL", "real_scalar", 1.5),
        ("DECFLOAT(16)", "decfloat16_scalar", 4.56),
        ("DECFLOAT(34)", "decfloat34_scalar", 123456.1234),
        ("DECIMAL(10,2)", "decimal_scalar", 56.78),
        ("DATE", "date_scalar", date(2025, 1, 1)),
        ("TIME", "time_scalar", time(12, 20, 30)),
        ("TIMESTAMP", "ts_scalar", datetime(1989, 2, 12, 23, 55, 59)),
        ]

        for base_type, proc_name, input_val in scalar_procs:
            sql = f"CALL {proc_name}(?, ?)"
            stmt = ibm_db.prepare(conn, sql)
            output_val = input_val

            ibm_db.bind_param(stmt, 1, input_val, ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt, 2, output_val, ibm_db.SQL_PARAM_OUTPUT)

            ibm_db.execute(stmt)
            result = ibm_db.fetch_callproc(stmt)
            print(f"Procedure: {proc_name} {base_type} input: {result[1]} {base_type} output: {result[2]}")



#__END__
#__LUW_EXPECTED__
#Procedure: int_scalar INTEGER input: 42 INTEGER output: 43
#Procedure: sint_scalar SMALLINT input: 7 SMALLINT output: 8
#Procedure: bint_scalar BIGINT input: 1234 BIGINT output: 1235
#Procedure: float_scalar FLOAT input: 3.14 FLOAT output: 4.140000000000001
#Procedure: double_scalar DOUBLE input: 20.25 DOUBLE output: 21.25
#Procedure: real_scalar REAL input: 1.5 REAL output: 2.5
#Procedure: decfloat16_scalar DECFLOAT(16) input: 4.56 DECFLOAT(16) output: 5.56
#Procedure: decfloat34_scalar DECFLOAT(34) input: 123456.1234 DECFLOAT(34) output: 123457.1234
#Procedure: decimal_scalar DECIMAL(10,2) input: 56.78 DECIMAL(10,2) output: 57.78
#Procedure: date_scalar DATE input: 2025-01-01 DATE output: 2025-01-02
#Procedure: time_scalar TIME input: 12:20:30 TIME output: 12:21:30
#Procedure: ts_scalar TIMESTAMP input: 1989-02-12 23:55:59 TIMESTAMP output: 1989-02-12 23:56:00
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

