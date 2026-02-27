from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_scalarsp_create(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_scalarsp_create)

    def run_test_scalarsp_create(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        scalar_types = [
            ("int_scalar", "INTEGER"),
            ("sint_scalar", "SMALLINT"),
            ("bint_scalar", "BIGINT"),
            ("float_scalar", "FLOAT"), 
            ("double_scalar", "DOUBLE"),
            ("real_scalar", "REAL"),
            ("decfloat16_scalar", "DECFLOAT(16)"),
            ("decfloat34_scalar", "DECFLOAT(34)"),
            ("decimal_scalar", "DECIMAL(10,2)"),
            ("date_scalar", "DATE"),
            ("time_scalar", "TIME"),
            ("ts_scalar", "TIMESTAMP"),
            ]
        for proc_name, base_type in scalar_types:
            try:
                ibm_db.exec_immediate(conn, f"DROP PROCEDURE {proc_name}")
            except:
                pass
            if base_type in ["INTEGER", "SMALLINT", "BIGINT"]:
                operation = "SET var2 = var1 + 1;"
            elif base_type in ["FLOAT", "DOUBLE", "REAL"]:
                operation = "SET var2 = var1 + 1.0;"
            elif base_type in ["DECFLOAT(16)", "DECFLOAT(34)", "DECIMAL(10,2)"]:
                operation = "SET var2 = var1 + Decimal(1.25);"
            elif base_type == "DATE":
                operation = "SET var2 = var1 + 1 DAY;"
            elif base_type == "TIME":
                operation = "SET var2 = var1 + 1 MINUTE;"
            elif base_type == "TIMESTAMP":
                operation = "SET var2 = var1 + 1 SECOND;"
            else:
                operation = "SET var2 = var1;"
            ibm_db.exec_immediate(conn, f"""
            CREATE PROCEDURE {proc_name}(IN var1 {base_type}, OUT var2 {base_type})
            LANGUAGE SQL
            BEGIN
            {operation}
            END
            """)
        print("Preparation complete: scalar stored procedures with safe operations created.")

#__END__
#__LUW_EXPECTED__
#Preparation complete: scalar stored procedures with safe operations created.
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

