from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sparray_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_sparray_computations)

    def run_test_sparray_computations(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        scalar_procs = [
        ("int_array", "array_int22", 7),
        ("sint_array", "array_sint22", 10),
        ("bint_array", "array_bint22", 12345),
        ("float_array", "array_float22", 3.14),
        ("double_array", "array_double22", 20.25),
        ("real_array", "array_real22", 1.5),
        ("decfloat16_array", "array_decfloat1622", 4.56),
        ("decfloat34_array", "array_decfloat3422", 123456.1234),
        ("decimal_array", "array_decimal22", 56.78),
        ("time_array", "array_time22", time(12, 20, 30)),
        ("date_array", "array_date22", date(2025, 1, 1)),
        ("ts_array", "array_ts22", datetime(1989, 2, 12, 23, 55, 59, 342380)),
        ("char_array", "array_char22", b'HelloWorld'),
        ("vc_array", "array_vc22", b'basketball'),
        ("vcfbd_array", "array_vcfbd22", b'foobar'),
        ]
        for type_name, proc_name, input_val in scalar_procs:
            sql = f"CALL {proc_name}(?, ?)"
            stmt = ibm_db.prepare(conn, sql)
            output_array = [input_val]*4

            ibm_db.bind_param(stmt, 1, input_val, ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt, 2, output_array, ibm_db.SQL_PARAM_OUTPUT)

            ibm_db.execute(stmt)
            result = ibm_db.fetch_callproc(stmt)
            ibm_db.debug(False)

            print(f"Procedure: {proc_name}")
            print(f"{type_name} input:", input_val)
            print(f"{type_name} output array:", result[2])

#__END__
#__LUW_EXPECTED__
#Procedure: array_int22
#int_array input: 7
#int_array output array: [49, 343, 28, 2]
#Procedure: array_sint22
#sint_array input: 10
#sint_array output array: [100, 1000, 40, 5]
#Procedure: array_bint22
#bint_array input: 12345
#bint_array output array: [152399025, 1881365963625, 49380, 12340]
#Procedure: array_float22
#float_array input: 3.14
#float_array output array: [9.8596, 30.959144000000002, 12.56, -1.8599999999999999]
#Procedure: array_double22
#double_array input: 20.25
#double_array output array: [410.0625, 8303.765625, 81.0, 15.25]
#Procedure: array_real22
#real_array input: 1.5
#real_array output array: [2.25, 3.375, 6.0, -3.5]
#Procedure: array_decfloat1622
#decfloat16_array input: 4.56
#decfloat16_array output array: [20.7936, 94.818816, 18.24, -0.44]
#Procedure: array_decfloat3422
#decfloat34_array input: 123456.1234
#decfloat34_array output array: [15241414404.956028, 1881645937568789.0, 493824.4936, 123451.1234]
#Procedure: array_decimal22
#decimal_array input: 56.78
#decimal_array output array: [3223.96, 183056.92, 227.12, 51.78]
#Procedure: array_time22
#time_array input: 12:20:30
#time_array output array: [datetime.time(13, 21, 31), datetime.time(11, 19, 29), datetime.time(12, 20, 31), datetime.time(12, 20, 29)]
#Procedure: array_date22
#date_array input: 2025-01-01
#date_array output array: [datetime.date(2026, 2, 2), datetime.date(2023, 11, 30), datetime.date(2025, 1, 2), datetime.date(2024, 12, 31)]
#Procedure: array_ts22
#ts_array input: 1989-02-12 23:55:59.342380
#ts_array output array: [datetime.datetime(1990, 3, 14, 0, 57, 0, 342380), datetime.datetime(1988, 1, 11, 22, 54, 58, 342380), datetime.datetime(1989, 2, 13, 23, 56, 0, 342380), datetime.datetime(1989, 2, 11, 23, 55, 58, 342380)]
#Procedure: array_char22
#char_array input: b'HelloWorld'
#char_array output array: [b'HelloWorld                             ', b'HelloWorld                             ', b'Hell                                   ', b'                                       ']
#Procedure: array_vc22
#vc_array input: b'basketball'
#vc_array output array: [b'basketballbasketbal', b'basketballbasketbal', b'bask', b'tball']
#Procedure: array_vcfbd22
#vcfbd_array input: b'foobar'
#vcfbd_array output array: [b'foobarfoobar', b'foobarfoobarfoobar', b'foobar', b'oobarr']
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

