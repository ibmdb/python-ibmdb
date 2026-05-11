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

    def test_31_async_sparray_cardinalities(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_31)

    def run_test_31(self):
        ARRAY_PROCS = [
            ("int_array",        "array_int12",         [1, 2, 3, 4, 5, None]),
            ("sint_array",       "array_sint12",        [7, 512, -29000, 32000]),
            ("bint_array",       "array_bint12",        [1234567890123, None, -9876543210]),
            ("float_array",      "array_float12",       [1.1, 2.2, 3.3]),
            ("double_array",     "array_double12",      [10.5, 20.25, 30.75]),
            ("real_array",       "array_real12",        [0.5, 1.5, 2.5]),
            ("decfloat16_array", "array_decfloat1612",  [1.23, None, 4.56, None]),
            ("decfloat34_array", "array_decfloat3412",  [1234567890.1234, None]),
            ("dec_array",        "array_dec12",         [12.34, None, 56.78]),
            ("time_array",       "array_time12",        [time(12, 20, 30), time(13, 30, 45)]),
            ("date_array",       "array_date12",        [date(2025, 1, 1), date(2025, 12, 31)]),
            ("ts_array",         "array_ts12",          [b'1981-07-08 10:42:34.000010', None,
                                                         b'1982-07-08 10:42:34.000010']),
            ("ts_array",         "array_ts12",          [datetime(1989, 2, 12, 23, 55, 59, 342380),
                                                         datetime(1990, 2, 12, 23, 55, 59, 342380)]),
            ("char_array",       "array_char12",        ["abc", "defg", "jkl"]),
            ("char_array",       "array_char12",        [b'abc', b'defg']),
            ("vc_array",         "array_vc12",          ["hello", "world"]),
            ("vc_array",         "array_vc12",          [b'hello', b'world']),
            ("vcfbd_array",      "array_vcfbd12",       [b'abc', b'dog', b'deadbeef', None, b'foobar']),
            ("clob_array",       "array_clob12",        [b'long text here', b'another clob']),
            ("blob_array",       "array_blob12",        [b"binarydata", b"morebytes", None, b'abc']),
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

            for type_name, proc_name, input_array in ARRAY_PROCS:
                cursor = await conn.cursor()
                try:
                    sql = "CALL %s.%s(?,?)" % (config.user.upper(), proc_name.upper())
                    await cursor.prepare(sql)

                    await cursor.bind_param(1, input_array, ibm_db.SQL_PARAM_INPUT)
                    await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_INTEGER)

                    await cursor.execute()
                    result = await cursor.fetch_callproc()

                    # result = (stmt, array_out, cardinality_out)
                    cardinality = result[2]
                    non_null = len([x for x in input_array if x is not None])
                    print("%-25s %-20s input=%r" % (proc_name, type_name, input_array))
                    print(" -> array_out=%r  cardinality=%s" % (result[1], cardinality))

                    if cardinality == non_null or cardinality == len(input_array):
                        passed += 1
                    else:
                        print("*** UNEXPECTED cardinality: got %s, expected ~%s" % (cardinality, non_null))
                        failed += 1
                except Exception as e:
                    err_str = str(e)
                    if 'SQL0440N' in err_str or 'CLI0102E' in err_str:
                        print("  %-25s %-20s SKIP: procedure not available" % (proc_name, type_name))
                        skipped += 1
                    else:
                        print("  %-25s %-20s ERROR: %s" % (proc_name, type_name, e))
                        failed += 1
                finally:
                    await cursor.close()

            await conn.close()
            total = len(ARRAY_PROCS)
            print("\nResults: %d passed, %d skipped, %d failed out of %d" % (passed, skipped, failed, total))
            if failed == 0:
                print("PASSED" if passed > 0 else "ALL SKIPPED")
            else:
                print("FAILED")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#array_int12               int_array            input=[1, 2, 3, 4, 5, None]
# -> array_out=[1, 2, 3, 4, 5, None]  cardinality=6
#array_sint12              sint_array           input=[7, 512, -29000, 32000]
# -> array_out=[7, 512, -29000, 32000]  cardinality=4
#array_bint12              bint_array           input=[1234567890123, None, -9876543210]
# -> array_out=[1234567890123, None, -9876543210]  cardinality=3
#array_float12             float_array          input=[1.1, 2.2, 3.3]
# -> array_out=[1.1, 2.2, 3.3]  cardinality=3
#array_double12            double_array         input=[10.5, 20.25, 30.75]
# -> array_out=[10.5, 20.25, 30.75]  cardinality=3
#array_real12              real_array           input=[0.5, 1.5, 2.5]
# -> array_out=[0.5, 1.5, 2.5]  cardinality=3
#array_decfloat1612        decfloat16_array     input=[1.23, None, 4.56, None]
# -> array_out=[1.23, None, 4.56, None]  cardinality=4
#array_decfloat3412        decfloat34_array     input=[1234567890.1234, None]
# -> array_out=[1234567890.1234, None]  cardinality=2
#array_dec12               dec_array            input=[12.34, None, 56.78]
# -> array_out=[12.34, None, 56.78]  cardinality=3
#array_time12              time_array           input=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
# -> array_out=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]  cardinality=2
#array_date12              date_array           input=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
# -> array_out=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]  cardinality=2
#array_ts12                ts_array             input=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']
# -> array_out=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']  cardinality=3
#array_ts12                ts_array             input=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
# -> array_out=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]  cardinality=2
#array_char12              char_array           input=['abc', 'defg', 'jkl']
# -> array_out=['abc', 'defg', 'jkl']  cardinality=3
#array_char12              char_array           input=[b'abc', b'defg']
# -> array_out=[b'abc', b'defg']  cardinality=2
#array_vc12                vc_array             input=['hello', 'world']
# -> array_out=['hello', 'world']  cardinality=2
#array_vc12                vc_array             input=[b'hello', b'world']
# -> array_out=[b'hello', b'world']  cardinality=2
#array_vcfbd12             vcfbd_array          input=[b'abc', b'dog', b'deadbeef', None, b'foobar']
# -> array_out=[b'abc', b'dog', b'deadbeef', None, b'foobar']  cardinality=5
#array_clob12              clob_array           input=[b'long text here', b'another clob']
# -> array_out=[b'long text here', b'another clob']  cardinality=2
#array_blob12              blob_array           input=[b'binarydata', b'morebytes', None, b'abc']
# -> array_out=[b'binarydata', b'morebytes', None, b'abc']  cardinality=4
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__ZOS_EXPECTED__
#array_int12               int_array            input=[1, 2, 3, 4, 5, None]
# -> array_out=[1, 2, 3, 4, 5, None]  cardinality=6
#array_sint12              sint_array           input=[7, 512, -29000, 32000]
# -> array_out=[7, 512, -29000, 32000]  cardinality=4
#array_bint12              bint_array           input=[1234567890123, None, -9876543210]
# -> array_out=[1234567890123, None, -9876543210]  cardinality=3
#array_float12             float_array          input=[1.1, 2.2, 3.3]
# -> array_out=[1.1, 2.2, 3.3]  cardinality=3
#array_double12            double_array         input=[10.5, 20.25, 30.75]
# -> array_out=[10.5, 20.25, 30.75]  cardinality=3
#array_real12              real_array           input=[0.5, 1.5, 2.5]
# -> array_out=[0.5, 1.5, 2.5]  cardinality=3
#array_decfloat1612        decfloat16_array     input=[1.23, None, 4.56, None]
# -> array_out=[1.23, None, 4.56, None]  cardinality=4
#array_decfloat3412        decfloat34_array     input=[1234567890.1234, None]
# -> array_out=[1234567890.1234, None]  cardinality=2
#array_dec12               dec_array            input=[12.34, None, 56.78]
# -> array_out=[12.34, None, 56.78]  cardinality=3
#array_time12              time_array           input=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
# -> array_out=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]  cardinality=2
#array_date12              date_array           input=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
# -> array_out=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]  cardinality=2
#array_ts12                ts_array             input=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']
# -> array_out=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']  cardinality=3
#array_ts12                ts_array             input=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
# -> array_out=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]  cardinality=2
#array_char12              char_array           input=['abc', 'defg', 'jkl']
# -> array_out=['abc', 'defg', 'jkl']  cardinality=3
#array_char12              char_array           input=[b'abc', b'defg']
# -> array_out=[b'abc', b'defg']  cardinality=2
#array_vc12                vc_array             input=['hello', 'world']
# -> array_out=['hello', 'world']  cardinality=2
#array_vc12                vc_array             input=[b'hello', b'world']
# -> array_out=[b'hello', b'world']  cardinality=2
#array_vcfbd12             vcfbd_array          input=[b'abc', b'dog', b'deadbeef', None, b'foobar']
# -> array_out=[b'abc', b'dog', b'deadbeef', None, b'foobar']  cardinality=5
#array_clob12              clob_array           input=[b'long text here', b'another clob']
# -> array_out=[b'long text here', b'another clob']  cardinality=2
#array_blob12              blob_array           input=[b'binarydata', b'morebytes', None, b'abc']
# -> array_out=[b'binarydata', b'morebytes', None, b'abc']  cardinality=4
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__SYSTEMI_EXPECTED__
#array_int12               int_array            input=[1, 2, 3, 4, 5, None]
# -> array_out=[1, 2, 3, 4, 5, None]  cardinality=6
#array_sint12              sint_array           input=[7, 512, -29000, 32000]
# -> array_out=[7, 512, -29000, 32000]  cardinality=4
#array_bint12              bint_array           input=[1234567890123, None, -9876543210]
# -> array_out=[1234567890123, None, -9876543210]  cardinality=3
#array_float12             float_array          input=[1.1, 2.2, 3.3]
# -> array_out=[1.1, 2.2, 3.3]  cardinality=3
#array_double12            double_array         input=[10.5, 20.25, 30.75]
# -> array_out=[10.5, 20.25, 30.75]  cardinality=3
#array_real12              real_array           input=[0.5, 1.5, 2.5]
# -> array_out=[0.5, 1.5, 2.5]  cardinality=3
#array_decfloat1612        decfloat16_array     input=[1.23, None, 4.56, None]
# -> array_out=[1.23, None, 4.56, None]  cardinality=4
#array_decfloat3412        decfloat34_array     input=[1234567890.1234, None]
# -> array_out=[1234567890.1234, None]  cardinality=2
#array_dec12               dec_array            input=[12.34, None, 56.78]
# -> array_out=[12.34, None, 56.78]  cardinality=3
#array_time12              time_array           input=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
# -> array_out=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]  cardinality=2
#array_date12              date_array           input=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
# -> array_out=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]  cardinality=2
#array_ts12                ts_array             input=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']
# -> array_out=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']  cardinality=3
#array_ts12                ts_array             input=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
# -> array_out=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]  cardinality=2
#array_char12              char_array           input=['abc', 'defg', 'jkl']
# -> array_out=['abc', 'defg', 'jkl']  cardinality=3
#array_char12              char_array           input=[b'abc', b'defg']
# -> array_out=[b'abc', b'defg']  cardinality=2
#array_vc12                vc_array             input=['hello', 'world']
# -> array_out=['hello', 'world']  cardinality=2
#array_vc12                vc_array             input=[b'hello', b'world']
# -> array_out=[b'hello', b'world']  cardinality=2
#array_vcfbd12             vcfbd_array          input=[b'abc', b'dog', b'deadbeef', None, b'foobar']
# -> array_out=[b'abc', b'dog', b'deadbeef', None, b'foobar']  cardinality=5
#array_clob12              clob_array           input=[b'long text here', b'another clob']
# -> array_out=[b'long text here', b'another clob']  cardinality=2
#array_blob12              blob_array           input=[b'binarydata', b'morebytes', None, b'abc']
# -> array_out=[b'binarydata', b'morebytes', None, b'abc']  cardinality=4
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__IDS_EXPECTED__
#array_int12               int_array            input=[1, 2, 3, 4, 5, None]
# -> array_out=[1, 2, 3, 4, 5, None]  cardinality=6
#array_sint12              sint_array           input=[7, 512, -29000, 32000]
# -> array_out=[7, 512, -29000, 32000]  cardinality=4
#array_bint12              bint_array           input=[1234567890123, None, -9876543210]
# -> array_out=[1234567890123, None, -9876543210]  cardinality=3
#array_float12             float_array          input=[1.1, 2.2, 3.3]
# -> array_out=[1.1, 2.2, 3.3]  cardinality=3
#array_double12            double_array         input=[10.5, 20.25, 30.75]
# -> array_out=[10.5, 20.25, 30.75]  cardinality=3
#array_real12              real_array           input=[0.5, 1.5, 2.5]
# -> array_out=[0.5, 1.5, 2.5]  cardinality=3
#array_decfloat1612        decfloat16_array     input=[1.23, None, 4.56, None]
# -> array_out=[1.23, None, 4.56, None]  cardinality=4
#array_decfloat3412        decfloat34_array     input=[1234567890.1234, None]
# -> array_out=[1234567890.1234, None]  cardinality=2
#array_dec12               dec_array            input=[12.34, None, 56.78]
# -> array_out=[12.34, None, 56.78]  cardinality=3
#array_time12              time_array           input=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
# -> array_out=[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]  cardinality=2
#array_date12              date_array           input=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
# -> array_out=[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]  cardinality=2
#array_ts12                ts_array             input=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']
# -> array_out=[b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']  cardinality=3
#array_ts12                ts_array             input=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
# -> array_out=[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]  cardinality=2
#array_char12              char_array           input=['abc', 'defg', 'jkl']
# -> array_out=['abc', 'defg', 'jkl']  cardinality=3
#array_char12              char_array           input=[b'abc', b'defg']
# -> array_out=[b'abc', b'defg']  cardinality=2
#array_vc12                vc_array             input=['hello', 'world']
# -> array_out=['hello', 'world']  cardinality=2
#array_vc12                vc_array             input=[b'hello', b'world']
# -> array_out=[b'hello', b'world']  cardinality=2
#array_vcfbd12             vcfbd_array          input=[b'abc', b'dog', b'deadbeef', None, b'foobar']
# -> array_out=[b'abc', b'dog', b'deadbeef', None, b'foobar']  cardinality=5
#array_clob12              clob_array           input=[b'long text here', b'another clob']
# -> array_out=[b'long text here', b'another clob']  cardinality=2
#array_blob12              blob_array           input=[b'binarydata', b'morebytes', None, b'abc']
# -> array_out=[b'binarydata', b'morebytes', None, b'abc']  cardinality=4
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
