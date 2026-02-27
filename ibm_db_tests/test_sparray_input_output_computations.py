from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sparray_input_output_computations(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_sparray_input_output_computations)

    def run_test_sparray_input_output_computations(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        array_procs = [
            ("int_array", "array_int41", [1, 2, 3, 4, 5]),
            ("sint_array", "array_sint41", [7, 512, -29000, 32000]),
            ("bint_array", "array_bint41", [1234567890123, None, -9876543210]),
            ("float_array", "array_float41", [1.1, 2.2, 3.3]),
            ("double_array", "array_double41", [10.5, 20.25, 30.75]),
            ("real_array", "array_real41", [0.5, 1.5, 2.5]),
            ("decfloat16_array", "array_decfloat1641", [1.23, None, 4.56, None]),
            ("decfloat34_array", "array_decfloat3441", [12345678.1234, None]),
            ("decimal_array", "array_decimal41", [12.34, None, 56.78]),
            ("time_array", "array_time41", [time(12, 20, 30), time(13, 30, 45)]),
            ("date_array", "array_date41", [date(2025, 1, 1), date(2025, 12, 31)]),
            ("ts_array", "array_ts41", [ datetime(1989, 2, 12, 23, 55, 59, 342380),datetime(1990, 2, 12, 23, 55, 59, 342380)]),
            ("vc_array", "array_vc41", ["hello", "world"]),
            ("vcfbd_array", "array_vcfbd41", [b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']),
            ("blob_array", "array_blob41", [b"binarydata", b"morebytes", None, b'abc']),
            ]
        for type_name, proc_name, input_array in array_procs:
            sql = f"CALL {proc_name}(?, ?)"
            stmt = ibm_db.prepare(conn, sql)
            
            ibm_db.bind_param(stmt, 1, input_array, ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt, 2, input_array, ibm_db.SQL_PARAM_OUTPUT)
            
            ibm_db.execute(stmt)
            result = ibm_db.fetch_callproc(stmt)
            
            print(f"Procedure: {proc_name}")
            print(f"{proc_name} input array:", input_array)
            print(f"{type_name} output array:", result[2])



#__END__
#__LUW_EXPECTED__
#Procedure: array_int41
#array_int41 input array: [1, 2, 3, 4, 5]
#int_array output array: [0, 1, 2, 3, 4]
#Procedure: array_sint41
#array_sint41 input array: [7, 512, -29000, 32000]
#sint_array output array: [6, 511, -29001, 31999]
#Procedure: array_bint41
#array_bint41 input array: [1234567890123, None, -9876543210]
#bint_array output array: [1234567890122, None, -9876543211]
#Procedure: array_float41
#array_float41 input array: [1.1, 2.2, 3.3]
#float_array output array: [-0.5699999999999998, 0.5300000000000002, 1.63]
#Procedure: array_double41
#array_double41 input array: [10.5, 20.25, 30.75]
#double_array output array: [8.83, 18.58, 29.08]
#Procedure: array_real41
#array_real41 input array: [0.5, 1.5, 2.5]
#real_array output array: [-1.1699999570846558, -0.17000000178813934, 0.8299999833106995]
#Procedure: array_decfloat1641
#array_decfloat1641 input array: [1.23, None, 4.56, None]
#decfloat16_array output array: [0.23, None, 3.56, None]
#Procedure: array_decfloat3441
#array_decfloat3441 input array: [12345678.1234, None]
#decfloat34_array output array: [12345677.1234, None]
#Procedure: array_decimal41
#array_decimal41 input array: [12.34, None, 56.78]
#decimal_array output array: [11.34, None, 55.78]
#Procedure: array_time41
#array_time41 input array: [datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#time_array output array: [datetime.time(13, 19, 31), datetime.time(14, 29, 46)]
#Procedure: array_date41
#array_date41 input array: [datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#date_array output array: [datetime.date(2024, 1, 31), datetime.date(2025, 1, 30)]
#Procedure: array_ts41
#array_ts41 input array: [datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#ts_array output array: [datetime.datetime(1988, 3, 12, 0, 55, 0, 342380), datetime.datetime(1989, 3, 12, 0, 55, 0, 342380)]
#Procedure: array_vc41
#array_vc41 input array: ['hello', 'world']
#vc_array output array: ['hello - o', 'world - d']
#Procedure: array_vcfbd41
#array_vcfbd41 input array: [b'basketball', b'baseball', b'football', b'pingpong', b'lacrosse']
#vcfbd_array output array: [b'basketball - l', b'baseball - l', b'football - l', b'pingpong - g', b'lacrosse - e']
#Procedure: array_blob41
#array_blob41 input array: [b'binarydata', b'morebytes', None, b'abc']
#blob_array output array: [b'binarydata', b'morebytes', None, b'abc']
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

