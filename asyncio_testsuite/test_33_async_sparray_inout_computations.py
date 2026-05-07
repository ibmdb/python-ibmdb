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

    def test_33_async_sparray_inout_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_33)

    def run_test_33(self):
        ARRAY_PROCS = [
            ("int_array",        "array_int31",         [1, 2, 3, 4, 5]),
            ("sint_array",       "array_sint31",        [7, 512, -29000, 32000]),
            ("bint_array",       "array_bint31",        [1234567890123, None, -9876543210]),
            ("float_array",      "array_float31",       [1.1, 2.2, 3.3]),
            ("double_array",     "array_double31",      [10.5, 20.25, 30.75]),
            ("real_array",       "array_real31",        [0.5, 1.5, 2.5]),
            ("decfloat16_array", "array_decflt1631",    [1.23, None, 4.56, None]),
            ("decfloat34_array", "array_decfloat3431",  [12345678.1234, None]),
            ("dec_array",        "array_dec31",         [12.34, None, 56.78]),
            ("time_array",       "array_time31",        [time(12, 20, 30), time(13, 30, 45)]),
            ("date_array",       "array_date31",        [date(2025, 1, 1), date(2025, 12, 31)]),
            ("ts_array",         "array_ts31",          [datetime(1989, 2, 12, 23, 55, 59, 342380),
                                                         datetime(1990, 2, 12, 23, 55, 59, 342380)]),
            ("ts_array",         "array_ts31",          [b'1981-07-08 10:42:34.000010',
                                                         b'1982-07-08 10:42:34.000010']),
            ("char_array",       "array_char31",        ["abc", "defg"]),
            ("vc_array",         "array_vc31",          ["hello", "world"]),
            ("vc_array",         "array_vc31",          [b'hello', b'world']),
            ("vcfbd_array",      "array_vcfbd31",       [b'basketball', b'baseball', b'football',
                                                         b'pingpong', b'lacrosse']),
            ("clob_array",       "array_clob31",        [b'long text here', b'another clob']),
            ("blob_array",       "array_blob31",        [b"binarydata", b"morebytes", b'abc']),
            ("char_array",       "array_char31",        [b'abc', None, b'defg']),
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
                    sql = "CALL %s.%s(?)" % (config.user.upper(), proc_name.upper())
                    await cursor.prepare(sql)

                    await cursor.bind_param(1, input_array, ibm_db.SQL_PARAM_INPUT_OUTPUT)

                    await cursor.execute()
                    result = await cursor.fetch_callproc()

                    # result = (stmt, inout_array)
                    out_arr = result[1]
                    print("%-25s %-20s" % (proc_name, type_name))
                    print("input =%r" % (input_array,))
                    print("output=%r" % (out_arr,))

                    if isinstance(out_arr, list) and len(out_arr) > 0:
                        passed += 1
                    else:
                        print("    *** UNEXPECTED output: %r" % (out_arr,))
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
            total = len(ARRAY_PROCS)
            print("\nResults: %d passed, %d skipped, %d failed out of %d" % (passed, skipped, failed, total))
            if failed == 0:
                print("PASSED" if passed > 0 else "ALL SKIPPED")
            else:
                print("FAILED")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#array_int31               int_array           
#input =[1, 2, 3, 4, 5]
#output=[2, 3, 4, 5, 6]
#array_sint31              sint_array          
#input =[7, 512, -29000, 32000]
#output=[8, 513, -28999, 32001]
#array_bint31              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890124, None, -9876543209]
#array_float31             float_array         
#input =[1.1, 2.2, 3.3]
#output=[2.43, 3.5300000000000002, 4.63]
#array_double31            double_array        
#input =[10.5, 20.25, 30.75]
#output=[11.83, 21.58, 32.08]
#array_real31              real_array          
#input =[0.5, 1.5, 2.5]
#output=[1.8300000429153442, 2.8299999237060547, 3.8299999237060547]
#array_decflt1631          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[2.56, None, 5.89, None]
#array_decfloat3431        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345679.4534, None]
#array_dec31               dec_array           
#input =[12.34, None, 56.78]
#output=[13.67, None, 58.11]
#array_time31              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(11, 21, 29), datetime.time(12, 31, 44)]
#array_date31              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2025, 12, 2), datetime.date(2026, 12, 1)]
#array_ts31                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1990, 1, 13, 22, 56, 58, 342380), datetime.datetime(1991, 1, 13, 22, 56, 58, 342380)]
#array_ts31                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1982, 6, 9, 9, 43, 33, 10), datetime.datetime(1983, 6, 9, 9, 43, 33, 10)]
#array_char31              char_array          
#input =['abc', 'defg']
#output=['abc - a', 'defg - d']
#array_vc31                vc_array            
#input =['hello', 'world']
#output=['hello - h', 'world - w']
#array_vc31                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - h', b'world - w']
#array_vcfbd31             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - b', b'baseball - b', b'football - f', b'pingpong - p', b'lacrosse - l']
#array_clob31              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'another clob', b'long text here']
#array_blob31              blob_array          
#input =[b'binarydata', b'morebytes', b'abc']
#output=[b'abc', b'morebytes', b'binarydata']
#array_char31              char_array          
#input =[b'abc', None, b'defg']
#output=[b'abc - a                                ', None, b'defg - d                               ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__ZOS_EXPECTED__
#array_int31               int_array           
#input =[1, 2, 3, 4, 5]
#output=[2, 3, 4, 5, 6]
#array_sint31              sint_array          
#input =[7, 512, -29000, 32000]
#output=[8, 513, -28999, 32001]
#array_bint31              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890124, None, -9876543209]
#array_float31             float_array         
#input =[1.1, 2.2, 3.3]
#output=[2.43, 3.5300000000000002, 4.63]
#array_double31            double_array        
#input =[10.5, 20.25, 30.75]
#output=[11.83, 21.58, 32.08]
#array_real31              real_array          
#input =[0.5, 1.5, 2.5]
#output=[1.8300000429153442, 2.8299999237060547, 3.8299999237060547]
#array_decflt1631          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[2.56, None, 5.89, None]
#array_decfloat3431        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345679.4534, None]
#array_dec31               dec_array           
#input =[12.34, None, 56.78]
#output=[13.67, None, 58.11]
#array_time31              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(11, 21, 29), datetime.time(12, 31, 44)]
#array_date31              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2025, 12, 2), datetime.date(2026, 12, 1)]
#array_ts31                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1990, 1, 13, 22, 56, 58, 342380), datetime.datetime(1991, 1, 13, 22, 56, 58, 342380)]
#array_ts31                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1982, 6, 9, 9, 43, 33, 10), datetime.datetime(1983, 6, 9, 9, 43, 33, 10)]
#array_char31              char_array          
#input =['abc', 'defg']
#output=['abc - a', 'defg - d']
#array_vc31                vc_array            
#input =['hello', 'world']
#output=['hello - h', 'world - w']
#array_vc31                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - h', b'world - w']
#array_vcfbd31             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - b', b'baseball - b', b'football - f', b'pingpong - p', b'lacrosse - l']
#array_clob31              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'another clob', b'long text here']
#array_blob31              blob_array          
#input =[b'binarydata', b'morebytes', b'abc']
#output=[b'abc', b'morebytes', b'binarydata']
#array_char31              char_array          
#input =[b'abc', None, b'defg']
#output=[b'abc - a                                ', None, b'defg - d                               ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__SYSTEMI_EXPECTED__
#array_int31               int_array           
#input =[1, 2, 3, 4, 5]
#output=[2, 3, 4, 5, 6]
#array_sint31              sint_array          
#input =[7, 512, -29000, 32000]
#output=[8, 513, -28999, 32001]
#array_bint31              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890124, None, -9876543209]
#array_float31             float_array         
#input =[1.1, 2.2, 3.3]
#output=[2.43, 3.5300000000000002, 4.63]
#array_double31            double_array        
#input =[10.5, 20.25, 30.75]
#output=[11.83, 21.58, 32.08]
#array_real31              real_array          
#input =[0.5, 1.5, 2.5]
#output=[1.8300000429153442, 2.8299999237060547, 3.8299999237060547]
#array_decflt1631          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[2.56, None, 5.89, None]
#array_decfloat3431        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345679.4534, None]
#array_dec31               dec_array           
#input =[12.34, None, 56.78]
#output=[13.67, None, 58.11]
#array_time31              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(11, 21, 29), datetime.time(12, 31, 44)]
#array_date31              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2025, 12, 2), datetime.date(2026, 12, 1)]
#array_ts31                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1990, 1, 13, 22, 56, 58, 342380), datetime.datetime(1991, 1, 13, 22, 56, 58, 342380)]
#array_ts31                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1982, 6, 9, 9, 43, 33, 10), datetime.datetime(1983, 6, 9, 9, 43, 33, 10)]
#array_char31              char_array          
#input =['abc', 'defg']
#output=['abc - a', 'defg - d']
#array_vc31                vc_array            
#input =['hello', 'world']
#output=['hello - h', 'world - w']
#array_vc31                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - h', b'world - w']
#array_vcfbd31             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - b', b'baseball - b', b'football - f', b'pingpong - p', b'lacrosse - l']
#array_clob31              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'another clob', b'long text here']
#array_blob31              blob_array          
#input =[b'binarydata', b'morebytes', b'abc']
#output=[b'abc', b'morebytes', b'binarydata']
#array_char31              char_array          
#input =[b'abc', None, b'defg']
#output=[b'abc - a                                ', None, b'defg - d                               ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__IDS_EXPECTED__
#array_int31               int_array           
#input =[1, 2, 3, 4, 5]
#output=[2, 3, 4, 5, 6]
#array_sint31              sint_array          
#input =[7, 512, -29000, 32000]
#output=[8, 513, -28999, 32001]
#array_bint31              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890124, None, -9876543209]
#array_float31             float_array         
#input =[1.1, 2.2, 3.3]
#output=[2.43, 3.5300000000000002, 4.63]
#array_double31            double_array        
#input =[10.5, 20.25, 30.75]
#output=[11.83, 21.58, 32.08]
#array_real31              real_array          
#input =[0.5, 1.5, 2.5]
#output=[1.8300000429153442, 2.8299999237060547, 3.8299999237060547]
#array_decflt1631          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[2.56, None, 5.89, None]
#array_decfloat3431        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345679.4534, None]
#array_dec31               dec_array           
#input =[12.34, None, 56.78]
#output=[13.67, None, 58.11]
#array_time31              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(11, 21, 29), datetime.time(12, 31, 44)]
#array_date31              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2025, 12, 2), datetime.date(2026, 12, 1)]
#array_ts31                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1990, 1, 13, 22, 56, 58, 342380), datetime.datetime(1991, 1, 13, 22, 56, 58, 342380)]
#array_ts31                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1982, 6, 9, 9, 43, 33, 10), datetime.datetime(1983, 6, 9, 9, 43, 33, 10)]
#array_char31              char_array          
#input =['abc', 'defg']
#output=['abc - a', 'defg - d']
#array_vc31                vc_array            
#input =['hello', 'world']
#output=['hello - h', 'world - w']
#array_vc31                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - h', b'world - w']
#array_vcfbd31             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - b', b'baseball - b', b'football - f', b'pingpong - p', b'lacrosse - l']
#array_clob31              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'another clob', b'long text here']
#array_blob31              blob_array          
#input =[b'binarydata', b'morebytes', b'abc']
#output=[b'abc', b'morebytes', b'binarydata']
#array_char31              char_array          
#input =[b'abc', None, b'defg']
#output=[b'abc - a                                ', None, b'defg - d                               ']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
