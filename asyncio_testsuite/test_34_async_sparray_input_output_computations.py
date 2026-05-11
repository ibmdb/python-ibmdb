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

    def test_34_async_sparray_input_output_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_34)

    def run_test_34(self):
        ARRAY_PROCS = [
            ("int_array",        "array_int41",         [1, 2, 3, 4, 5]),
            ("sint_array",       "array_sint41",        [7, 512, -29000, 32000]),
            ("bint_array",       "array_bint41",        [1234567890123, None, -9876543210]),
            ("float_array",      "array_float41",       [1.1, 2.2, 3.3]),
            ("double_array",     "array_double41",      [10.5, 20.25, 30.75]),
            ("real_array",       "array_real41",        [0.5, 1.5, 2.5]),
            ("decfloat16_array", "array_decflt1641",    [1.23, None, 4.56, None]),
            ("decfloat34_array", "array_decfloat3441",  [12345678.1234, None]),
            ("dec_array",        "array_dec41",         [12.34, None, 56.78]),
            ("time_array",       "array_time41",        [time(12, 20, 30), time(13, 30, 45)]),
            ("date_array",       "array_date41",        [date(2025, 1, 1), date(2025, 12, 31)]),
            ("ts_array",         "array_ts41",          [datetime(1989, 2, 12, 23, 55, 59, 342380),
                                                         datetime(1990, 2, 12, 23, 55, 59, 342380)]),
            ("ts_array",         "array_ts41",          [b'1981-07-08 10:42:34.000010',
                                                         b'1982-07-08 10:42:34.000010']),
            ("char_array",       "array_char41",        ["abc", "defg"]),
            ("char_array",       "array_char41",        [b'abc', b'defg']),
            ("vc_array",         "array_vc41",          ["hello", "world"]),
            ("vc_array",         "array_vc41",          [b'hello', b'world']),
            ("vcfbd_array",      "array_vcfbd41",       [b'basketball', b'baseball', b'football',
                                                         b'pingpong', b'lacrosse']),
            ("blob_array",       "array_blob41",        [b"binarydata", b"morebytes", None, b'abc']),
            ("clob_array",       "array_clob41",        [b'long text here', b'another clob']),
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
                    sql = "CALL %s.%s(?, ?)" % (config.user.upper(), proc_name.upper())
                    await cursor.prepare(sql)

                    await cursor.bind_param(1, input_array, ibm_db.SQL_PARAM_INPUT)
                    await cursor.bind_param(2, input_array, ibm_db.SQL_PARAM_OUTPUT)

                    await cursor.execute()
                    result = await cursor.fetch_callproc()

                    # result = (stmt, input_array_echo, output_array)
                    out_arr = result[2]
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
#array_int41               int_array           
#input =[1, 2, 3, 4, 5]
#output=[0, 1, 2, 3, 4]
#array_sint41              sint_array          
#input =[7, 512, -29000, 32000]
#output=[6, 511, -29001, 31999]
#array_bint41              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890122, None, -9876543211]
#array_float41             float_array         
#input =[1.1, 2.2, 3.3]
#output=[-0.5699999999999998, 0.5300000000000002, 1.63]
#array_double41            double_array        
#input =[10.5, 20.25, 30.75]
#output=[8.83, 18.58, 29.08]
#array_real41              real_array          
#input =[0.5, 1.5, 2.5]
#output=[-1.1699999570846558, -0.17000000178813934, 0.8299999833106995]
#array_decflt1641          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[-0.44, None, 2.89, None]
#array_decfloat3441        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345676.4534, None]
#array_dec41               dec_array           
#input =[12.34, None, 56.78]
#output=[10.67, None, 55.11]
#array_time41              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(13, 19, 31), datetime.time(14, 29, 46)]
#array_date41              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2024, 1, 31), datetime.date(2025, 1, 30)]
#array_ts41                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1988, 3, 12, 0, 55, 0, 342380), datetime.datetime(1989, 3, 12, 0, 55, 0, 342380)]
#array_ts41                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1980, 8, 7, 11, 41, 35, 10), datetime.datetime(1981, 8, 7, 11, 41, 35, 10)]
#array_char41              char_array          
#input =['abc', 'defg']
#output=['abc - c', 'defg - g']
#array_char41              char_array          
#input =[b'abc', b'defg']
#output=[b'abc - c                                ', b'defg - g                               ']
#array_vc41                vc_array            
#input =['hello', 'world']
#output=['hello - o', 'world - d']
#array_vc41                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - o', b'world - d']
#array_vcfbd41             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - l', b'baseball - l', b'football - l', b'pingpong - g', b'lacrosse - e']
#array_blob41              blob_array          
#input =[b'binarydata', b'morebytes', None, b'abc']
#output=[b'binarydata', b'morebytes', None, b'abc']
#array_clob41              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'long text here', b'another clob']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__ZOS_EXPECTED__
#array_int41               int_array           
#input =[1, 2, 3, 4, 5]
#output=[0, 1, 2, 3, 4]
#array_sint41              sint_array          
#input =[7, 512, -29000, 32000]
#output=[6, 511, -29001, 31999]
#array_bint41              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890122, None, -9876543211]
#array_float41             float_array         
#input =[1.1, 2.2, 3.3]
#output=[-0.5699999999999998, 0.5300000000000002, 1.63]
#array_double41            double_array        
#input =[10.5, 20.25, 30.75]
#output=[8.83, 18.58, 29.08]
#array_real41              real_array          
#input =[0.5, 1.5, 2.5]
#output=[-1.1699999570846558, -0.17000000178813934, 0.8299999833106995]
#array_decflt1641          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[-0.44, None, 2.89, None]
#array_decfloat3441        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345676.4534, None]
#array_dec41               dec_array           
#input =[12.34, None, 56.78]
#output=[10.67, None, 55.11]
#array_time41              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(13, 19, 31), datetime.time(14, 29, 46)]
#array_date41              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2024, 1, 31), datetime.date(2025, 1, 30)]
#array_ts41                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1988, 3, 12, 0, 55, 0, 342380), datetime.datetime(1989, 3, 12, 0, 55, 0, 342380)]
#array_ts41                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1980, 8, 7, 11, 41, 35, 10), datetime.datetime(1981, 8, 7, 11, 41, 35, 10)]
#array_char41              char_array          
#input =['abc', 'defg']
#output=['abc - c', 'defg - g']
#array_char41              char_array          
#input =[b'abc', b'defg']
#output=[b'abc - c                                ', b'defg - g                               ']
#array_vc41                vc_array            
#input =['hello', 'world']
#output=['hello - o', 'world - d']
#array_vc41                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - o', b'world - d']
#array_vcfbd41             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - l', b'baseball - l', b'football - l', b'pingpong - g', b'lacrosse - e']
#array_blob41              blob_array          
#input =[b'binarydata', b'morebytes', None, b'abc']
#output=[b'binarydata', b'morebytes', None, b'abc']
#array_clob41              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'long text here', b'another clob']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__SYSTEMI_EXPECTED__
#array_int41               int_array           
#input =[1, 2, 3, 4, 5]
#output=[0, 1, 2, 3, 4]
#array_sint41              sint_array          
#input =[7, 512, -29000, 32000]
#output=[6, 511, -29001, 31999]
#array_bint41              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890122, None, -9876543211]
#array_float41             float_array         
#input =[1.1, 2.2, 3.3]
#output=[-0.5699999999999998, 0.5300000000000002, 1.63]
#array_double41            double_array        
#input =[10.5, 20.25, 30.75]
#output=[8.83, 18.58, 29.08]
#array_real41              real_array          
#input =[0.5, 1.5, 2.5]
#output=[-1.1699999570846558, -0.17000000178813934, 0.8299999833106995]
#array_decflt1641          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[-0.44, None, 2.89, None]
#array_decfloat3441        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345676.4534, None]
#array_dec41               dec_array           
#input =[12.34, None, 56.78]
#output=[10.67, None, 55.11]
#array_time41              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(13, 19, 31), datetime.time(14, 29, 46)]
#array_date41              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2024, 1, 31), datetime.date(2025, 1, 30)]
#array_ts41                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1988, 3, 12, 0, 55, 0, 342380), datetime.datetime(1989, 3, 12, 0, 55, 0, 342380)]
#array_ts41                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1980, 8, 7, 11, 41, 35, 10), datetime.datetime(1981, 8, 7, 11, 41, 35, 10)]
#array_char41              char_array          
#input =['abc', 'defg']
#output=['abc - c', 'defg - g']
#array_char41              char_array          
#input =[b'abc', b'defg']
#output=[b'abc - c                                ', b'defg - g                               ']
#array_vc41                vc_array            
#input =['hello', 'world']
#output=['hello - o', 'world - d']
#array_vc41                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - o', b'world - d']
#array_vcfbd41             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - l', b'baseball - l', b'football - l', b'pingpong - g', b'lacrosse - e']
#array_blob41              blob_array          
#input =[b'binarydata', b'morebytes', None, b'abc']
#output=[b'binarydata', b'morebytes', None, b'abc']
#array_clob41              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'long text here', b'another clob']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
#__IDS_EXPECTED__
#array_int41               int_array           
#input =[1, 2, 3, 4, 5]
#output=[0, 1, 2, 3, 4]
#array_sint41              sint_array          
#input =[7, 512, -29000, 32000]
#output=[6, 511, -29001, 31999]
#array_bint41              bint_array          
#input =[1234567890123, None, -9876543210]
#output=[1234567890122, None, -9876543211]
#array_float41             float_array         
#input =[1.1, 2.2, 3.3]
#output=[-0.5699999999999998, 0.5300000000000002, 1.63]
#array_double41            double_array        
#input =[10.5, 20.25, 30.75]
#output=[8.83, 18.58, 29.08]
#array_real41              real_array          
#input =[0.5, 1.5, 2.5]
#output=[-1.1699999570846558, -0.17000000178813934, 0.8299999833106995]
#array_decflt1641          decfloat16_array    
#input =[1.23, None, 4.56, None]
#output=[-0.44, None, 2.89, None]
#array_decfloat3441        decfloat34_array    
#input =[12345678.1234, None]
#output=[12345676.4534, None]
#array_dec41               dec_array           
#input =[12.34, None, 56.78]
#output=[10.67, None, 55.11]
#array_time41              time_array          
#input =[datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#output=[datetime.time(13, 19, 31), datetime.time(14, 29, 46)]
#array_date41              date_array          
#input =[datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#output=[datetime.date(2024, 1, 31), datetime.date(2025, 1, 30)]
#array_ts41                ts_array            
#input =[datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#output=[datetime.datetime(1988, 3, 12, 0, 55, 0, 342380), datetime.datetime(1989, 3, 12, 0, 55, 0, 342380)]
#array_ts41                ts_array            
#input =[b'1981-07-08 10:42:34.000010', b'1982-07-08 10:42:34.000010']
#output=[datetime.datetime(1980, 8, 7, 11, 41, 35, 10), datetime.datetime(1981, 8, 7, 11, 41, 35, 10)]
#array_char41              char_array          
#input =['abc', 'defg']
#output=['abc - c', 'defg - g']
#array_char41              char_array          
#input =[b'abc', b'defg']
#output=[b'abc - c                                ', b'defg - g                               ']
#array_vc41                vc_array            
#input =['hello', 'world']
#output=['hello - o', 'world - d']
#array_vc41                vc_array            
#input =[b'hello', b'world']
#output=[b'hello - o', b'world - d']
#array_vcfbd41             vcfbd_array         
#input =[b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#output=[b'basketball - l', b'baseball - l', b'football - l', b'pingpong - g', b'lacrosse - e']
#array_blob41              blob_array          
#input =[b'binarydata', b'morebytes', None, b'abc']
#output=[b'binarydata', b'morebytes', None, b'abc']
#array_clob41              clob_array          
#input =[b'long text here', b'another clob']
#output=[b'long text here', b'another clob']
#
#Results: 20 passed, 0 skipped, 0 failed out of 20
#PASSED
