from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db
import config
from ibm_db_dbi import AsyncConnection
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_35_async_scalarsp_execute(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_35)

    def run_test_35(self):
        SCALAR_PROCS = [
            # Numeric types
            ("INTEGER",       "int_scalar",            42),
            ("SMALLINT",      "sint_scalar",           7),
            ("BIGINT",        "bint_scalar",           1234),
            ("FLOAT",         "float_scalar",          3.14),
            ("DOUBLE",        "double_scalar",         20.25),
            ("REAL",          "real_scalar",           1.5),
            ("DECFLOAT(16)",  "decfloat16_scalar",     4.56),
            ("DECFLOAT(34)",  "decfloat34_scalar",     123456.1234),
            ("DECIMAL(10,2)", "decimal_scalar",        56.78),
            # Temporal types
            ("DATE",          "date_scalar",           date(2025, 1, 1)),
            ("TIME",          "time_scalar",           time(12, 20, 30)),
            ("TIMESTAMP",     "ts_scalar",             datetime(1989, 2, 12, 23, 55, 59)),
            ("TIMESTAMP",     "ts_scalar",             b'1989-02-12 23:55:59'),
            # Character/string types
            ("CHAR(20)",      "char_scalar",           "hello"),
            ("CHAR(20)",      "char_scalar",           b'hello'),
            ("VARCHAR(20)",   "vc_scalar",             "testdata"),
            ("VARCHAR(20)",   "vc_scalar",             b'testdata'),
            ("CLOB",          "clob_scalar",           b'long clob text data'),
            # Binary types
            ("BLOB",          "blob_scalar",           b'binarydata'),
            ("VARBINARY",     "vcfbd_scalar",          b'varbindata'),
        ]

        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            passed = 0
            failed = 0
            skipped = 0

            for base_type, proc_name, input_val in SCALAR_PROCS:
                cursor = await conn.cursor()
                try:
                    sql = "CALL %s.%s(?, ?)" % (config.user.upper(), proc_name.upper())
                    await cursor.prepare(sql)

                    await cursor.bind_param(1, input_val, ibm_db.SQL_PARAM_INPUT)
                    await cursor.bind_param(2, input_val, ibm_db.SQL_PARAM_OUTPUT)

                    await cursor.execute()
                    result = await cursor.fetch_callproc()

                    # result = (stmt, input_echo, output_value)
                    in_echo = result[1]
                    out_val = result[2]
                    print("%-22s %-15s input=%r output=%r" % (proc_name, base_type, in_echo, out_val))

                    if out_val is not None:
                        passed += 1
                    else:
                        print("    *** UNEXPECTED: output is None")
                        failed += 1
                except Exception as e:
                    err_str = str(e)
                    if 'SQL0440N' in err_str or 'CLI0102E' in err_str:
                        print("%-22s %-15s SKIP: procedure not available" % (proc_name, base_type))
                        skipped += 1
                    else:
                        print("  %-22s %-15s ERROR: %s" % (proc_name, base_type, e))
                        failed += 1
                finally:
                    await cursor.close()

            await conn.close()
            total = len(SCALAR_PROCS)
            print("\nResults: %d passed, %d skipped, %d failed out of %d" % (passed, skipped, failed, total))
            if failed == 0:
                print("PASSED" if passed > 0 else "ALL SKIPPED")
            else:
                print("FAILED")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#int_scalar             INTEGER         input=42 output=43
#sint_scalar            SMALLINT        input=7 output=8
#bint_scalar            BIGINT          input=1234 output=1235
#float_scalar           FLOAT           input=3.14 output=4.140000000000001
#double_scalar          DOUBLE          input=20.25 output=21.25
#real_scalar            REAL            input=1.5 output=2.5
#decfloat16_scalar      DECFLOAT(16)    input=4.56 output=5.56
#decfloat34_scalar      DECFLOAT(34)    input=123456.1234 output=123457.1234
#decimal_scalar         DECIMAL(10,2)   input=56.78 output=57.78
#date_scalar            DATE            input=datetime.date(2025, 1, 1) output=datetime.date(2025, 1, 2)
#time_scalar            TIME            input=datetime.time(12, 20, 30) output=datetime.time(12, 21, 30)
#ts_scalar              TIMESTAMP       input=datetime.datetime(1989, 2, 12, 23, 55, 59) output=datetime.datetime(1989, 2, 12, 23, 56)
#ts_scalar              TIMESTAMP       input=b'1989-02-12 23:55:59' output=datetime.datetime(1989, 2, 12, 23, 56)
#char_scalar            CHAR(20)        input='hello' output='hello_OUT'
#char_scalar            CHAR(20)        input=b'hello' output=b'hello_OUT           '
#vc_scalar              VARCHAR(20)     input='testdata' output='testdata_OUT'
#vc_scalar              VARCHAR(20)     input=b'testdata' output=b'testdata_OUT'
#clob_scalar            CLOB            input=b'long clob text data' output=b'long clob text data'
#blob_scalar            BLOB            input=b'binarydata' output=b'binarydata'
#vcfbd_scalar           VARBINARY       input=b'varbindata' output=b'varbindata'
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__ZOS_EXPECTED__
#int_scalar             INTEGER         input=42 output=43
#sint_scalar            SMALLINT        input=7 output=8
#bint_scalar            BIGINT          input=1234 output=1235
#float_scalar           FLOAT           input=3.14 output=4.140000000000001
#double_scalar          DOUBLE          input=20.25 output=21.25
#real_scalar            REAL            input=1.5 output=2.5
#decfloat16_scalar      DECFLOAT(16)    input=4.56 output=5.56
#decfloat34_scalar      DECFLOAT(34)    input=123456.1234 output=123457.1234
#decimal_scalar         DECIMAL(10,2)   input=56.78 output=57.78
#date_scalar            DATE            input=datetime.date(2025, 1, 1) output=datetime.date(2025, 1, 2)
#time_scalar            TIME            input=datetime.time(12, 20, 30) output=datetime.time(12, 21, 30)
#ts_scalar              TIMESTAMP       input=datetime.datetime(1989, 2, 12, 23, 55, 59) output=datetime.datetime(1989, 2, 12, 23, 56)
#ts_scalar              TIMESTAMP       input=b'1989-02-12 23:55:59' output=datetime.datetime(1989, 2, 12, 23, 56)
#char_scalar            CHAR(20)        input='hello' output='hello_OUT'
#char_scalar            CHAR(20)        input=b'hello' output=b'hello_OUT           '
#vc_scalar              VARCHAR(20)     input='testdata' output='testdata_OUT'
#vc_scalar              VARCHAR(20)     input=b'testdata' output=b'testdata_OUT'
#clob_scalar            CLOB            input=b'long clob text data' output=b'long clob text data'
#blob_scalar            BLOB            input=b'binarydata' output=b'binarydata'
#vcfbd_scalar           VARBINARY       input=b'varbindata' output=b'varbindata'
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__SYSTEMI_EXPECTED__
#int_scalar             INTEGER         input=42 output=43
#sint_scalar            SMALLINT        input=7 output=8
#bint_scalar            BIGINT          input=1234 output=1235
#float_scalar           FLOAT           input=3.14 output=4.140000000000001
#double_scalar          DOUBLE          input=20.25 output=21.25
#real_scalar            REAL            input=1.5 output=2.5
#decfloat16_scalar      DECFLOAT(16)    input=4.56 output=5.56
#decfloat34_scalar      DECFLOAT(34)    input=123456.1234 output=123457.1234
#decimal_scalar         DECIMAL(10,2)   input=56.78 output=57.78
#date_scalar            DATE            input=datetime.date(2025, 1, 1) output=datetime.date(2025, 1, 2)
#time_scalar            TIME            input=datetime.time(12, 20, 30) output=datetime.time(12, 21, 30)
#ts_scalar              TIMESTAMP       input=datetime.datetime(1989, 2, 12, 23, 55, 59) output=datetime.datetime(1989, 2, 12, 23, 56)
#ts_scalar              TIMESTAMP       input=b'1989-02-12 23:55:59' output=datetime.datetime(1989, 2, 12, 23, 56)
#char_scalar            CHAR(20)        input='hello' output='hello_OUT'
#char_scalar            CHAR(20)        input=b'hello' output=b'hello_OUT           '
#vc_scalar              VARCHAR(20)     input='testdata' output='testdata_OUT'
#vc_scalar              VARCHAR(20)     input=b'testdata' output=b'testdata_OUT'
#clob_scalar            CLOB            input=b'long clob text data' output=b'long clob text data'
#blob_scalar            BLOB            input=b'binarydata' output=b'binarydata'
#vcfbd_scalar           VARBINARY       input=b'varbindata' output=b'varbindata'
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__IDS_EXPECTED__
#int_scalar             INTEGER         input=42 output=43
#sint_scalar            SMALLINT        input=7 output=8
#bint_scalar            BIGINT          input=1234 output=1235
#float_scalar           FLOAT           input=3.14 output=4.140000000000001
#double_scalar          DOUBLE          input=20.25 output=21.25
#real_scalar            REAL            input=1.5 output=2.5
#decfloat16_scalar      DECFLOAT(16)    input=4.56 output=5.56
#decfloat34_scalar      DECFLOAT(34)    input=123456.1234 output=123457.1234
#decimal_scalar         DECIMAL(10,2)   input=56.78 output=57.78
#date_scalar            DATE            input=datetime.date(2025, 1, 1) output=datetime.date(2025, 1, 2)
#time_scalar            TIME            input=datetime.time(12, 20, 30) output=datetime.time(12, 21, 30)
#ts_scalar              TIMESTAMP       input=datetime.datetime(1989, 2, 12, 23, 55, 59) output=datetime.datetime(1989, 2, 12, 23, 56)
#ts_scalar              TIMESTAMP       input=b'1989-02-12 23:55:59' output=datetime.datetime(1989, 2, 12, 23, 56)
#char_scalar            CHAR(20)        input='hello' output='hello_OUT'
#char_scalar            CHAR(20)        input=b'hello' output=b'hello_OUT           '
#vc_scalar              VARCHAR(20)     input='testdata' output='testdata_OUT'
#vc_scalar              VARCHAR(20)     input=b'testdata' output=b'testdata_OUT'
#clob_scalar            CLOB            input=b'long clob text data' output=b'long clob text data'
#blob_scalar            BLOB            input=b'binarydata' output=b'binarydata'
#vcfbd_scalar           VARBINARY       input=b'varbindata' output=b'varbindata'
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
