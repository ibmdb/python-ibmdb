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

    def test_32_async_sparray_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_32)

    def run_test_32(self):
        # (type_name, proc_name, input_val[, output_template])
        SCALAR_PROCS = [
            ("int_array",        "array_int22",         7),
            ("sint_array",       "array_sint22",        10),
            ("bint_array",       "array_bint22",        12345),
            ("float_array",      "array_float22",       3.14),
            ("double_array",     "array_double22",      20.25),
            ("real_array",       "array_real22",        1.5),
            ("decfloat16_array", "array_decflt1622",    4.56),
            ("decfloat34_array", "array_decfloat3422",  123456.1234),
            ("dec_array",        "array_dec22",         56.78),
            ("time_array",       "array_time22",        time(12, 20, 30)),
            ("date_array",       "array_date22",        date(2025, 1, 1)),
            ("ts_array",         "array_ts22",          datetime(1989, 2, 12, 23, 55, 59, 342380)),
            ("ts_array",         "array_ts22",          b'1989-02-12 23:55:59.342380'),
            ("char_array",       "array_char22",        "HelloWorld"),
            ("char_array",       "array_char22",        b'HelloWorld'),
            ("vc_array",         "array_vc22",          "basketball"),
            ("vc_array",         "array_vc22",          b'basketball'),
            ("vcfbd_array",      "array_vcfbd22",       b'foobar'),
            ("clob_array",       "array_clob22",        100, [b'x' * 20] * 4),
            ("blob_array",       "array_blob22",        200, [b'x' * 20] * 4),
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

            for entry in SCALAR_PROCS:
                type_name, proc_name, input_val = entry[0], entry[1], entry[2]
                out_template = entry[3] if len(entry) > 3 else None
                cursor = await conn.cursor()
                try:
                    sql = "CALL %s.%s(?, ?)" % (config.user.upper(), proc_name.upper())
                    await cursor.prepare(sql)

                    output_array = out_template if out_template is not None else [input_val] * 4

                    await cursor.bind_param(1, input_val, ibm_db.SQL_PARAM_INPUT)
                    await cursor.bind_param(2, output_array, ibm_db.SQL_PARAM_OUTPUT)
                    await cursor.execute()
                    result = await cursor.fetch_callproc()
                    # result = (stmt, scalar_in, output_array)
                    out_arr = result[2]
                    print("%-25s %-20s input=%r" % (proc_name, type_name, input_val))
                    print("-> output array=%r" % (out_arr,))

                    if isinstance(out_arr, list) and len(out_arr) > 0:
                        passed += 1
                    else:
                        print("*** UNEXPECTED output: %r" % (out_arr,))
                        failed += 1
                except Exception as e:
                    err_str = str(e)
                    if 'SQL0440N' in err_str or 'CLI0102E' in err_str:
                        print("%-25s %-20s SKIP: procedure not available" % (proc_name, type_name))
                        skipped += 1
                    else:
                        print("%-25s %-20s ERROR: %s" % (proc_name, type_name, e))
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
#array_int22               int_array            input=7
#-> output array=[49, 343, 28, 2]
#array_sint22              sint_array           input=10
#-> output array=[100, 1000, 40, 5]
#array_bint22              bint_array           input=12345
#-> output array=[152399025, 1881365963625, 49380, 12340]
#array_float22             float_array          input=3.14
#-> output array=[9.8596, 30.959144000000002, 12.56, -1.8599999999999999]
#array_double22            double_array         input=20.25
#-> output array=[410.0625, 8303.765625, 81.0, 15.25]
#array_real22              real_array           input=1.5
#-> output array=[2.25, 3.375, 6.0, -3.5]
#array_decflt1622          decfloat16_array     input=4.56
#-> output array=[20.7936, 94.818816, 18.24, -0.44]
#array_decfloat3422        decfloat34_array     input=123456.1234
#-> output array=[15241414404.956028, 1881645937568789.0, 493824.4936, 123451.1234]
#array_dec22               dec_array            input=56.78
#-> output array=[3223.96, 183056.92, 227.12, 51.78]
#array_time22              time_array           input=datetime.time(12, 20, 30)
#-> output array=[datetime.time(13, 21, 31), datetime.time(11, 19, 29), datetime.time(12, 20, 31), datetime.time(12, 20, 29)]
#array_date22              date_array           input=datetime.date(2025, 1, 1)
#-> output array=[datetime.date(2026, 2, 2), datetime.date(2023, 11, 30), datetime.date(2025, 1, 2), datetime.date(2024, 12, 31)]
#array_ts22                ts_array             input=datetime.datetime(1989, 2, 12, 23, 55, 59, 342380)
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_ts22                ts_array             input=b'1989-02-12 23:55:59.342380'
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_char22              char_array           input='HelloWorld'
#-> output array=['HelloWorld', 'HelloWorld', 'Hell', '']
#array_char22              char_array           input=b'HelloWorld'
#-> output array=[b'HelloWorld                             ', b'HelloWorld                             ', b'Hell                                   ', b'                                       ']
#array_vc22                vc_array             input='basketball'
#-> output array=['basketballbasketball', 'basketballbasketball', 'bask', 'tball']
#array_vc22                vc_array             input=b'basketball'
#-> output array=[b'basketballbasketbal', b'basketballbasketbal', b'bask', b'tball']
#array_vcfbd22             vcfbd_array          input=b'foobar'
#-> output array=[b'foobarfoobar', b'foobarfoobarfoobar', b'foobar', b'oobarr']
#array_clob22              clob_array           input=100
#-> output array=[b'101        ', b'102        ', b'103        ', b'104        ']
#array_blob22              blob_array           input=200
#-> output array=[b'201        ', b'202        ', b'203        ', b'204        ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__ZOS_EXPECTED__
#array_int22               int_array            input=7
#-> output array=[49, 343, 28, 2]
#array_sint22              sint_array           input=10
#-> output array=[100, 1000, 40, 5]
#array_bint22              bint_array           input=12345
#-> output array=[152399025, 1881365963625, 49380, 12340]
#array_float22             float_array          input=3.14
#-> output array=[9.8596, 30.959144000000002, 12.56, -1.8599999999999999]
#array_double22            double_array         input=20.25
#-> output array=[410.0625, 8303.765625, 81.0, 15.25]
#array_real22              real_array           input=1.5
#-> output array=[2.25, 3.375, 6.0, -3.5]
#array_decflt1622          decfloat16_array     input=4.56
#-> output array=[20.7936, 94.818816, 18.24, -0.44]
#array_decfloat3422        decfloat34_array     input=123456.1234
#-> output array=[15241414404.956028, 1881645937568789.0, 493824.4936, 123451.1234]
#array_dec22               dec_array            input=56.78
#-> output array=[3223.96, 183056.92, 227.12, 51.78]
#array_time22              time_array           input=datetime.time(12, 20, 30)
#-> output array=[datetime.time(13, 21, 31), datetime.time(11, 19, 29), datetime.time(12, 20, 31), datetime.time(12, 20, 29)]
#array_date22              date_array           input=datetime.date(2025, 1, 1)
#-> output array=[datetime.date(2026, 2, 2), datetime.date(2023, 11, 30), datetime.date(2025, 1, 2), datetime.date(2024, 12, 31)]
#array_ts22                ts_array             input=datetime.datetime(1989, 2, 12, 23, 55, 59, 342380)
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_ts22                ts_array             input=b'1989-02-12 23:55:59.342380'
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_char22              char_array           input='HelloWorld'
#-> output array=['HelloWorld', 'HelloWorld', 'Hell', '']
#array_char22              char_array           input=b'HelloWorld'
#-> output array=[b'HelloWorld                             ', b'HelloWorld                             ', b'Hell                                   ', b'                                       ']
#array_vc22                vc_array             input='basketball'
#-> output array=['basketballbasketball', 'basketballbasketball', 'bask', 'tball']
#array_vc22                vc_array             input=b'basketball'
#-> output array=[b'basketballbasketbal', b'basketballbasketbal', b'bask', b'tball']
#array_vcfbd22             vcfbd_array          input=b'foobar'
#-> output array=[b'foobarfoobar', b'foobarfoobarfoobar', b'foobar', b'oobarr']
#array_clob22              clob_array           input=100
#-> output array=[b'101        ', b'102        ', b'103        ', b'104        ']
#array_blob22              blob_array           input=200
#-> output array=[b'201        ', b'202        ', b'203        ', b'204        ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__SYSTEMI_EXPECTED__
#array_int22               int_array            input=7
#-> output array=[49, 343, 28, 2]
#array_sint22              sint_array           input=10
#-> output array=[100, 1000, 40, 5]
#array_bint22              bint_array           input=12345
#-> output array=[152399025, 1881365963625, 49380, 12340]
#array_float22             float_array          input=3.14
#-> output array=[9.8596, 30.959144000000002, 12.56, -1.8599999999999999]
#array_double22            double_array         input=20.25
#-> output array=[410.0625, 8303.765625, 81.0, 15.25]
#array_real22              real_array           input=1.5
#-> output array=[2.25, 3.375, 6.0, -3.5]
#array_decflt1622          decfloat16_array     input=4.56
#-> output array=[20.7936, 94.818816, 18.24, -0.44]
#array_decfloat3422        decfloat34_array     input=123456.1234
#-> output array=[15241414404.956028, 1881645937568789.0, 493824.4936, 123451.1234]
#array_dec22               dec_array            input=56.78
#-> output array=[3223.96, 183056.92, 227.12, 51.78]
#array_time22              time_array           input=datetime.time(12, 20, 30)
#-> output array=[datetime.time(13, 21, 31), datetime.time(11, 19, 29), datetime.time(12, 20, 31), datetime.time(12, 20, 29)]
#array_date22              date_array           input=datetime.date(2025, 1, 1)
#-> output array=[datetime.date(2026, 2, 2), datetime.date(2023, 11, 30), datetime.date(2025, 1, 2), datetime.date(2024, 12, 31)]
#array_ts22                ts_array             input=datetime.datetime(1989, 2, 12, 23, 55, 59, 342380)
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_ts22                ts_array             input=b'1989-02-12 23:55:59.342380'
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_char22              char_array           input='HelloWorld'
#-> output array=['HelloWorld', 'HelloWorld', 'Hell', '']
#array_char22              char_array           input=b'HelloWorld'
#-> output array=[b'HelloWorld                             ', b'HelloWorld                             ', b'Hell                                   ', b'                                       ']
#array_vc22                vc_array             input='basketball'
#-> output array=['basketballbasketball', 'basketballbasketball', 'bask', 'tball']
#array_vc22                vc_array             input=b'basketball'
#-> output array=[b'basketballbasketbal', b'basketballbasketbal', b'bask', b'tball']
#array_vcfbd22             vcfbd_array          input=b'foobar'
#-> output array=[b'foobarfoobar', b'foobarfoobarfoobar', b'foobar', b'oobarr']
#array_clob22              clob_array           input=100
#-> output array=[b'101        ', b'102        ', b'103        ', b'104        ']
#array_blob22              blob_array           input=200
#-> output array=[b'201        ', b'202        ', b'203        ', b'204        ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__IDS_EXPECTED__
#array_int22               int_array            input=7
#-> output array=[49, 343, 28, 2]
#array_sint22              sint_array           input=10
#-> output array=[100, 1000, 40, 5]
#array_bint22              bint_array           input=12345
#-> output array=[152399025, 1881365963625, 49380, 12340]
#array_float22             float_array          input=3.14
#-> output array=[9.8596, 30.959144000000002, 12.56, -1.8599999999999999]
#array_double22            double_array         input=20.25
#-> output array=[410.0625, 8303.765625, 81.0, 15.25]
#array_real22              real_array           input=1.5
#-> output array=[2.25, 3.375, 6.0, -3.5]
#array_decflt1622          decfloat16_array     input=4.56
#-> output array=[20.7936, 94.818816, 18.24, -0.44]
#array_decfloat3422        decfloat34_array     input=123456.1234
#-> output array=[15241414404.956028, 1881645937568789.0, 493824.4936, 123451.1234]
#array_dec22               dec_array            input=56.78
#-> output array=[3223.96, 183056.92, 227.12, 51.78]
#array_time22              time_array           input=datetime.time(12, 20, 30)
#-> output array=[datetime.time(13, 21, 31), datetime.time(11, 19, 29), datetime.time(12, 20, 31), datetime.time(12, 20, 29)]
#array_date22              date_array           input=datetime.date(2025, 1, 1)
#-> output array=[datetime.date(2026, 2, 2), datetime.date(2023, 11, 30), datetime.date(2025, 1, 2), datetime.date(2024, 12, 31)]
#array_ts22                ts_array             input=datetime.datetime(1989, 2, 12, 23, 55, 59, 342380)
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_ts22                ts_array             input=b'1989-02-12 23:55:59.342380'
#-> output array=[datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#array_char22              char_array           input='HelloWorld'
#-> output array=['HelloWorld', 'HelloWorld', 'Hell', '']
#array_char22              char_array           input=b'HelloWorld'
#-> output array=[b'HelloWorld                             ', b'HelloWorld                             ', b'Hell                                   ', b'                                       ']
#array_vc22                vc_array             input='basketball'
#-> output array=['basketballbasketball', 'basketballbasketball', 'bask', 'tball']
#array_vc22                vc_array             input=b'basketball'
#-> output array=[b'basketballbasketbal', b'basketballbasketbal', b'bask', b'tball']
#array_vcfbd22             vcfbd_array          input=b'foobar'
#-> output array=[b'foobarfoobar', b'foobarfoobarfoobar', b'foobar', b'oobarr']
#array_clob22              clob_array           input=100
#-> output array=[b'101        ', b'102        ', b'103        ', b'104        ']
#array_blob22              blob_array           input=200
#-> output array=[b'201        ', b'202        ', b'203        ', b'204        ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
