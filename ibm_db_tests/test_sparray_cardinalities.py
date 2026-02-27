from __future__ import print_function
import unittest
import ibm_db
import config
from datetime import date, time, datetime
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_sparray_cardinalities(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_sparray_cardinalities)

    def run_test_sparray_cardinalities(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if not conn:
            print("no connection")
            return
        array_procs = [
        ("int_array", "array_int12", [1, 2, 3, 4, 5, None]),
        ("sint_array", "array_sint12", [7, 512, -29000, 32000]),
        ("bint_array", "array_bint12", [1234567890123, None,-9876543210]),
        ("float_array", "array_float12", [1.1, 2.2, 3.3]),
        ("double_array", "array_double12", [10.5, 20.25, 30.75]),
        ("real_array", "array_real12", [0.5, 1.5, 2.5]),
        ("decfloat16_array", "array_decfloat1612", [1.23,None, 4.56, None]),
        ("decfloat34_array", "array_decfloat3412", [1234567890.1234, None]),
        ("decimal_array", "array_decimal12", [12.34, None, 56.78]),
        ("time_array", "array_time12", [time(12, 20, 30), time(13, 30, 45)]),
        ("date_array", "array_date12", [date(2025, 1, 1), date(2025, 12, 31)]),
        ("ts_array", "array_ts12", [b'1981-07-08 10:42:34.000010',None, b'1982-07-08 10:42:34.000010']),
        ("ts_array", "array_ts12", [ datetime(1989, 2, 12, 23, 55, 59, 342380), datetime(1990, 2, 12, 23, 55, 59, 342380)]),
        ("char_array", "array_char12", ["abc", "defg", "jkl"]),
        ("char_array", "array_char12", [b'abc', b'defg']),
        ("vc_array", "array_vc12", ["hello", "world"]),
        ("vc_array", "array_vc12", [b'hello', b'world']),
        ("vcfbd_array", "array_vcfbd12",[b'abc', b'dog', b'deadbeef', None, b'foobar']),
        ("clob_array", "array_clob12", [b'long text here', b'another clob']),
        ("blob_array", "array_blob12", [b"binarydata", b"morebytes", None, b'abc'])
        ]
        for type_name, proc_name, input_array in array_procs:
            sql = f"CALL {proc_name}(?,?)"
            stmt = ibm_db.prepare(conn, sql)
            output = 0

            ibm_db.bind_param(stmt, 1, input_array, ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt, 2, output, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_INTEGER)

            ibm_db.execute(stmt)
            inout_value = ibm_db.fetch_callproc(stmt)

            print(f"Procedure : {proc_name}")
            print(f"{type_name} input:", inout_value[1])
            print(f"{type_name} cardinality:", inout_value[2])

#__END__
#__LUW_EXPECTED__
#Procedure : array_int12
#int_array input: [1, 2, 3, 4, 5, None]
#int_array cardinality: 6
#Procedure : array_sint12
#sint_array input: [7, 512, -29000, 32000]
#sint_array cardinality: 4
#Procedure : array_bint12
#bint_array input: [1234567890123, None, -9876543210]
#bint_array cardinality: 3
#Procedure : array_float12
#float_array input: [1.1, 2.2, 3.3]
#float_array cardinality: 3
#Procedure : array_double12
#double_array input: [10.5, 20.25, 30.75]
#double_array cardinality: 3
#Procedure : array_real12
#real_array input: [0.5, 1.5, 2.5]
#real_array cardinality: 3
#Procedure : array_decfloat1612
#decfloat16_array input: [1.23, None, 4.56, None]
#decfloat16_array cardinality: 4
#Procedure : array_decfloat3412
#decfloat34_array input: [1234567890.1234, None]
#decfloat34_array cardinality: 2
#Procedure : array_decimal12
#decimal_array input: [12.34, None, 56.78]
#decimal_array cardinality: 3
#Procedure : array_time12
#time_array input: [datetime.time(12, 20, 30), datetime.time(13, 30, 45)]
#time_array cardinality: 2
#Procedure : array_date12
#date_array input: [datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)]
#date_array cardinality: 2
#Procedure : array_ts12
#ts_array input: [b'1981-07-08 10:42:34.000010', None, b'1982-07-08 10:42:34.000010']
#ts_array cardinality: 3
#Procedure : array_ts12
#ts_array input: [datetime.datetime(1989, 2, 12, 23, 55, 59, 342380), datetime.datetime(1990, 2, 12, 23, 55, 59, 342380)]
#ts_array cardinality: 2
#Procedure : array_char12
#char_array input: ['abc', 'defg', 'jkl']
#char_array cardinality: 3
#Procedure : array_char12
#char_array input: [b'abc', b'defg']
#char_array cardinality: 2
#Procedure : array_vc12
#vc_array input: ['hello', 'world']
#vc_array cardinality: 2
#Procedure : array_vc12
#vc_array input: [b'hello', b'world']
#vc_array cardinality: 2
#Procedure : array_vcfbd12
#vcfbd_array input: [b'abc', b'dog', b'deadbeef', None, b'foobar']
#vcfbd_array cardinality: 5
#Procedure : array_clob12
#clob_array input: [b'long text here', b'another clob']
#clob_array cardinality: 2
#Procedure : array_blob12
#blob_array input: [b'binarydata', b'morebytes', None, b'abc']
#blob_array cardinality: 4
#__ZOS_EXPECTED__
#... same as LUW ...
#__SYSTEMI_EXPECTED__
#... same as LUW ...
#__IDS_EXPECTED__
#... same as LUW ...

