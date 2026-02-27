#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2026
#

from __future__ import print_function
import sys
import os
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_ArrayTypeAndSPCreation(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_arraytypeandspcreation)

    def run_test_arraytypeandspcreation(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info(conn)

        array_types = [
            ("int_array", "INTEGER"),
            ("sint_array", "SMALLINT"),
            ("bint_array", "BIGINT"),
            ("float_array", "FLOAT"),
            ("double_array", "DOUBLE"),
            ("real_array", "REAL"),
            ("decfloat16_array", "DECFLOAT(16)"),
            ("decfloat34_array", "DECFLOAT(34)"),
            ("decimal_array", "DECIMAL(10,2)"),
            ("char_array", "CHAR(40)"),
            ("vc_array", "VARCHAR(20)"),
            ("vcfbd_array", "VARCHAR(20) FOR BIT DATA"),
            ("date_array", "DATE"),
            ("time_array", "TIME"),
            ("ts_array", "TIMESTAMP"),
            ("clob_array", "CLOB(500)"),
            ("blob_array", "BLOB(500)")
        ]

        # Create array types
        for type_name, base_type in array_types:
            try:
                ibm_db.exec_immediate(conn, f"DROP TYPE {type_name}")
            except:
                pass
            ibm_db.exec_immediate(conn, f"CREATE TYPE {type_name} AS {base_type} ARRAY[100]")
            
            proc_name = f"array_{type_name.replace('_array','')}12"
            try:
                ibm_db.exec_immediate(conn, f"DROP PROCEDURE {proc_name}")
            except:
                pass

            ibm_db.exec_immediate(conn, f"""CREATE PROCEDURE {proc_name}( IN var1 {type_name}, OUT var2 INTEGER)
            LANGUAGE SQL
            BEGIN
                SET var2 = CARDINALITY(var1);
            END""")

        
        try:
            ibm_db.exec_immediate(conn, "drop procedure array_bint22")
            ibm_db.exec_immediate(conn, "drop procedure array_bint31")
            ibm_db.exec_immediate(conn, "drop procedure array_bint41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_int22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_int31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_int41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_sint22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_sint31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_sint41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_real22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_real31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_real41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_float22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_float31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_float41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_double22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_double31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_double41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_dec22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_dec31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_dec41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_decflt1622")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_decflt1631")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_decflt1641")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_char22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_char31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_char41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vc22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vc31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vc41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vcfbd22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vcfbd31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_vcfbd41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_date22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_date31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_date41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_time22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_time31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_time41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_ts22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_ts31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_ts41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_clob22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_clob31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_clob41")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_blob22")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_blob31")
            ibm_db.exec_immediate(conn, "DROP PROCEDURE array_blob41")
        except:
            pass

        ibm_db.exec_immediate(conn,"""create procedure array_int22( in var1 integer, out var2 int_array )
            LANGUAGE SQL \
            BEGIN \
                    SET var2[1] = var1 * var1; \
                    SET var2[2] = var1 * var1 * var1; \
                    SET var2[3] = var1 * 4; \
                    SET var2[4] = var1 - 5; \
            END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_int31( INOUT var1 int_array)
        LANGUAGE SQL
        BEGIN
            DECLARE var2 int_array;
            FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx) ORDER BY idx ASC
            DO
                SET var2[idx] = val + 1;
            END FOR;
            SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_int41(IN var1 int_array,  OUT var2 int_array)
        LANGUAGE SQL
        BEGIN FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx) ORDER BY idx ASC
        DO
            SET var2[idx] = val - 1;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_sint22(IN var1 SMALLINT, OUT var2 sint_array)
        LANGUAGE SQL
        BEGIN
            SET var2[1] = var1 * var1;
            SET var2[2] = var1 * var1 * var1;
            SET var2[3] = var1 * 4;
            SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_sint31(INOUT var1 sint_array)
        LANGUAGE SQL
        BEGIN
            DECLARE var2 sint_array;
            FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
            DO
                SET var2[idx] = val + 1;
            END FOR;
            SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_sint41( IN var1 sint_array, OUT var2 sint_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
            SET var2[idx] = val - 1;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_bint22( IN var1 BIGINT, OUT var2 bint_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_bint31(INOUT var1 bint_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 bint_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_bint41(IN var1 bint_array,OUT var2 bint_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_real22( IN var1 REAL, OUT var2 real_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_real31(INOUT var1 real_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 real_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1.33;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_real41( IN var1 real_array, OUT var2 real_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
           SET var2[idx] = val - 1.67;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_float22(IN var1 FLOAT, OUT var2 float_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_float31(INOUT var1 float_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 float_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1.33;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """create procedure array_float41(in var1 float_array,out var2 float_array )
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx) ORDER BY idx ASC
        DO
            SET var2[idx] = val - 1.67;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_double22(IN var1 DOUBLE, OUT var2 double_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_double31(INOUT var1 double_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 double_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
            SET var2[idx] = val + 1.33;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_double41(IN var1 double_array, OUT var2 double_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
           SET var2[idx] = val - 1.67;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_dec22(IN var1 DECIMAL(12,2), OUT var2 dec_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_dec31(INOUT var1 dec_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 dec_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1.33;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_dec41( IN var1 dec_array, OUT var2 dec_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1.67;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_decflt1622(IN var1 DECFLOAT(16), OUT var2 decfloat16_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 * var1;
        SET var2[2] = var1 * var1 * var1;
        SET var2[3] = var1 * 4;
        SET var2[4] = var1 - 5;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_decflt1631(INOUT var1 decfloat16_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 decfloat16_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1.33;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_decflt1641(IN var1 decfloat16_array, OUT var2 decfloat16_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1.67;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_char22( IN var1 CHAR(40), OUT var2 char_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 || var1;
        SET var2[2] = var1 || var1 || var1;
        SET var2[3] = LEFT(var1,4);
        SET var2[4] = RIGHT(var1,5);
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_char31(INOUT var1 char_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 char_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || LEFT(RTRIM(val),1);
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_char41(IN var1 char_array, OUT var2 char_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || RIGHT(RTRIM(val),1);
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vc22(IN var1 VARCHAR(20),OUT var2 vc_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 || var1;
        SET var2[2] = var1 || var1 || var1;
        SET var2[3] = LEFT(var1,4);
        SET var2[4] = RIGHT(var1,5);
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vc31(INOUT var1 vc_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 vc_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || LEFT(RTRIM(val),1);
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vc41(IN var1 vc_array, OUT var2 vc_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || RIGHT(RTRIM(val),1);
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vcfbd22(IN var1 VARCHAR(20) FOR BIT DATA, OUT var2 vcfbd_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 || var1;
        SET var2[2] = var1 || var1 || var1;
        SET var2[3] = LEFT(var1,4);
        SET var2[4] = RIGHT(var1,5);
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vcfbd31(INOUT var1 vcfbd_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 vcfbd_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || LEFT(RTRIM(val),1);
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_vcfbd41(IN var1 vcfbd_array, OUT var2 vcfbd_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = RTRIM(val) || ' - ' || RIGHT(RTRIM(val),1);
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_date22(IN var1 DATE, OUT var2 date_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 + 1 YEAR + 1 MONTH + 1 DAY;
        SET var2[2] = var1 - 1 YEAR - 1 MONTH - 1 DAY;
        SET var2[3] = var1 + 1 DAY;
        SET var2[4] = var1 - 1 DAY;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_date31(INOUT var1 date_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 date_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1 YEAR - 1 MONTH + 1 DAY;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_date41(IN var1 date_array, OUT var2 date_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1 YEAR + 1 MONTH - 1 DAY;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_time22(IN var1 TIME, OUT var2 time_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 + 1 HOUR + 1 MINUTE + 1 SECOND;
        SET var2[2] = var1 - 1 HOUR - 1 MINUTE - 1 SECOND;
        SET var2[3] = var1 + 1 SECOND;
        SET var2[4] = var1 - 1 SECOND;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_time31(INOUT var1 time_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 time_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1 HOUR + 1 MINUTE - 1 SECOND;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_time41(IN var1 time_array, OUT var2 time_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1 HOUR - 1 MINUTE + 1 SECOND;
        END FOR;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_ts22(IN var1 TIMESTAMP, OUT var2 ts_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = var1 + 1 YEAR + 1 MONTH + 1 DAY + 1 HOUR + 1 MINUTE + 1 SECOND;
        SET var2[2] = var1 - 1 YEAR - 1 MONTH - 1 DAY - 1 HOUR - 1 MINUTE - 1 SECOND;
        SET var2[3] = var1 + 1 DAY + 1 SECOND;
        SET var2[4] = var1 - 1 DAY - 1 SECOND;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_ts31(INOUT var1 ts_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 ts_array;
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val + 1 YEAR - 1 MONTH + 1 DAY - 1 HOUR + 1 MINUTE - 1 SECOND;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_ts41(IN var1 ts_array, OUT var2 ts_array)
        LANGUAGE SQL
        BEGIN
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[idx] = val - 1 YEAR + 1 MONTH - 1 DAY + 1 HOUR - 1 MINUTE + 1 SECOND;
        END FOR;
        END""")


        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_clob22(IN var1 INTEGER, OUT var2 clob_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = CLOB(CHAR(var1+1));
        SET var2[2] = CLOB(CHAR(var1+2));
        SET var2[3] = CLOB(CHAR(var1+3));
        SET var2[4] = CLOB(CHAR(var1+4));
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_clob31(INOUT var1 clob_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 clob_array;
        DECLARE var3 INTEGER;
        SET var3 = CARDINALITY(var1);
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[var3-idx+1] = val;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_clob41(IN var1 clob_array, OUT var2 clob_array)
        LANGUAGE SQL
        BEGIN
        SET var2 = var1;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_blob22(IN var1 INTEGER, OUT var2 blob_array)
        LANGUAGE SQL
        BEGIN
        SET var2[1] = BLOB(CHAR(var1+1));
        SET var2[2] = BLOB(CHAR(var1+2));
        SET var2[3] = BLOB(CHAR(var1+3));
        SET var2[4] = BLOB(CHAR(var1+4));
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_blob31(INOUT var1 blob_array)
        LANGUAGE SQL
        BEGIN
        DECLARE var2 blob_array;
        DECLARE var3 INTEGER;
        SET var3 = CARDINALITY(var1);
        FOR v AS SELECT val, idx FROM UNNEST(var1) WITH ORDINALITY AS T(val, idx)
        DO
        SET var2[var3-idx+1] = val;
        END FOR;
        SET var1 = var2;
        END""")

        ibm_db.exec_immediate(conn, """CREATE PROCEDURE array_blob41(IN var1 blob_array, OUT var2 blob_array)
        LANGUAGE SQL
        BEGIN
        SET var2 = var1;
        END""")

        print("Preparation complete: array types and stored procedures created.")

#__END__
#__LUW_EXPECTED__
#Preparation complete: array types and stored procedures created.
#__ZOS_EXPECTED__
#Preparation complete: array types and stored procedures created.
#__SYSTEMI_EXPECTED__
#Preparation complete: array types and stored procedures created.
#__IDS_EXPECTED__
#Preparation complete: array types and stored procedures created.

