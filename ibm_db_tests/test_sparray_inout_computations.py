from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sparray_inout_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_sparray_inout_computations)

    def run_test_sparray_inout_computations(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        array_procs = [
    ("int_array", "array_int31", [1, 2, 3, 4, 5]),          # each element +1
    ("sint_array", "array_sint31", [7, 512, -29000, 32000]),# each element +1
    ("bint_array", "array_bint31", [1234567890123, None, -9876543210]), # each element +1
    ("float_array", "array_float31", [1.1, 2.2, 3.3]),      # each element +1.33
    ("double_array", "array_double31", [10.5, 20.25, 30.75]), # each element +1.33
    ("real_array", "array_real31", [0.5, 1.5, 2.5]),        # each element +1.33
    ("decfloat16_array", "array_decfloat1631", [1.23, None, 4.56, None]), # each element +1.33
    ("decfloat34_array", "array_decfloat3431", [12345678.1234, None]), # each element +1.33
    ("decimal_array", "array_decimal31", [12.34, None, 56.78]), # each element +1.33
    ("time_array", "array_time31", [time(12, 20, 30), time(13, 30, 45)]), # time manipulations
    ("date_array", "array_date31", [date(2025, 1, 1), date(2025, 12, 31)]), # +1 YEAR -1 MONTH +1 DAY
    ("ts_array", "array_ts31", [datetime(1989, 2, 12, 23, 55, 59, 342380), datetime(1990, 2, 12, 23, 55, 59, 342380)]), # timestamp manipulations
    ("vc_array", "array_vc31", ["hello", "world"]),         # same string transformation
    ("vc_array", "array_vc31", [b'hello', b'world']),         # same string transformation
    ("vcfbd_array", "array_vcfbd31", [b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']), #unicode
    ("clob_array", "array_clob31", [b'long text here', b'another clob']),
    ("blob_array", "array_blob31", [b"binarydata", b"morebytes", b'abc']),
    ("char_array", "array_char31", [b'abc', None,b'defg']),
]
 
        for type_name, proc_name, input_array in array_procs:
            sql = f"CALL {proc_name}(?)"
            stmt = ibm_db.prepare(conn, sql)
            b1 = ibm_db.bind_param(stmt, 1, input_array, ibm_db.SQL_PARAM_INPUT_OUTPUT)
            ibm_db.execute(stmt)
            inout_value = ibm_db.fetch_callproc(stmt)
            print(f"Procedure: {proc_name}")
            print(f"{type_name} input:", input_array)
            print(f"{type_name} output array:", inout_value[1])


#__END__
#__LUW_EXPECTED__
#Procedure: array_int31
#int_array input: [1, 2, 3, 4, 5]
#int_array output array: [2, 3, 4, 5, 6]
#Procedure: array_sint31
#sint_array input: [7, 512, -29000, 32000]
#sint_array output array: [8, 513, -28999, 32001]
#Procedure: array_bint31
#bint_array input: [1234567890123, None, -9876543210]
#bint_array output array: [1234567890124, None, -9876543209]
#Procedure: array_float31
#float_array input: [1.1, 2.2, 3.3]
#float_array output array: [2.43, 3.5300000000000002, 4.63]
#Procedure: array_double31
#double_array input: [10.5, 20.25, 30.75]
#double_array output array: [11.83, 21.58, 32.08]
#Procedure: array_real31
#real_array input: [0.5, 1.5, 2.5]
#real_array output array: [1.8300000429153442, 2.8299999237060547, 3.8299999237060547]
#Procedure: array_decfloat1631
#decfloat16_array input: [1.23, None, 4.56, None]
#decfloat16_array output array: [2.23, None, 5.56, None]
#Procedure: array_decfloat3431
#decfloat34_array input: [12345678.1234, None]
#decfloat34_array output array: [12345679.1234, None]
#Procedure: array_decimal31
#decimal_array input: [12.34, None, 56.78]
#decimal_array output array: [13.34, None, 57.78]
#Procedure: array_time31
#time_array input: [datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#time_array output array: [datetime.time(11, 21, 29), datetime.time(12, 31, 44)]
#Procedure: array_date31
#date_array input: [datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#date_array output array: [datetime.date(2025, 12, 2), datetime.date(2026, 12, 1)]
#Procedure: array_ts31
#ts_array input: [datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#ts_array output array: [datetime.datetime(1990, 1, 13, 22, 56, 58, 342380), datetime.datetime(1991, 1, 13, 22, 56, 58, 342380)]
#Procedure: array_vc31
#vc_array input: ['hello', 'world']
#vc_array output array: ['hello - h', 'world - w']
#Procedure: array_vc31
#vc_array input: [b'hello', b'world']
#vc_array output array: [b'hello - h', b'world - w']
#Procedure: array_vcfbd31
#vcfbd_array input: [b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#vcfbd_array output array: [b'basketball - b', b'baseball - b', b'football - f', b'pingpong - p', b'lacrosse - l']
#Procedure: array_clob31
#clob_array input: [b'long text here', b'another clob']
#clob_array output array: [b'another clob', b'long text here']
#Procedure: array_blob31
#blob_array input: [b'binarydata', b'morebytes', b'abc']
#blob_array output array: [b'abcarydata', b'morebytes', b'binarydata']
#Procedure: array_char31
#char_array input: [b'abc', None, b'defg']
#char_array output array: [b'abc - a                                ', None, b'defg - d                               ']
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

