#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

# This test will use a lot of the heap size allocated
# for DB2.  If is is failing on your system, please
# increase the application heap size.

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_156_FetchAssocNestedSelects_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_156)

    def run_test_156(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        result = ibm_db.exec_immediate(conn, "select * from staff")

        row = ibm_db.fetch_assoc(result)
        count = 1
        while ( row ):
            if (row['YEARS'] == None):
                row['YEARS'] = ''
            if (row['COMM'] == None):
                row['COMM'] = ''
            print(row['ID'],row['NAME'],row['JOB'],row['YEARS'], row['SALARY'], row['COMM'])
            row = ibm_db.fetch_assoc(result)

        result2 = ibm_db.exec_immediate(conn,"select * from department where substr(deptno,1,1) in ('A','B','C','D','E')")
        row2 = ibm_db.fetch_assoc(result2)
        while ( row2 ):
            if (row2['MGRNO'] == None):
                row2['MGRNO'] = ''
            print(row2['DEPTNO'], row2['DEPTNAME'], row2['MGRNO'], row2['ADMRDEPT'], row2['LOCATION'])
            row2 = ibm_db.fetch_assoc(result2)

#__END__
#__LUW_EXPECTED__
#10 Sanders Mgr   7 18357.50 
#20 Pernal Sales 8 18171.25 612.45
#30 Marenghi Mgr   5 17506.75 
#40 OBrien Sales 6 18006.00 846.55
#50 Hanes Mgr   10 20659.80 
#60 Quigley Sales  16808.30 650.25
#70 Rothman Sales 7 16502.83 1152.00
#80 James Clerk  13504.60 128.20
#90 Koonitz Sales 6 18001.75 1386.70
#100 Plotz Mgr   7 18352.80 
#110 Ngan Clerk 5 12508.20 206.60
#120 Naughton Clerk  12954.75 180.00
#130 Yamaguchi Clerk 6 10505.90 75.60
#140 Fraye Mgr   6 21150.00 
#150 Williams Sales 6 19456.50 637.65
#160 Molinare Mgr   7 22959.20 
#170 Kermisch Clerk 4 12258.50 110.10
#180 Abrahams Clerk 3 12009.75 236.50
#190 Sneider Clerk 8 14252.75 126.50
#200 Scoutten Clerk  11508.60 84.20
#210 Lu Mgr   10 20010.00 
#220 Smith Sales 7 17654.50 992.80
#230 Lundquist Clerk 3 13369.80 189.65
#240 Daniels Mgr   5 19260.25 
#250 Wheeler Clerk 6 14460.00 513.30
#260 Jones Mgr   12 21234.00 
#270 Lea Mgr   9 18555.50 
#280 Wilson Sales 9 18674.50 811.50
#290 Quill Mgr   10 19818.00 
#300 Davis Sales 5 15454.50 806.10
#310 Graham Sales 13 21000.00 200.30
#320 Gonzales Sales 4 16858.20 844.00
#330 Burke Clerk 1 10988.00 55.50
#340 Edwards Sales 7 17844.00 1285.00
#350 Gafney Clerk 5 13030.50 188.00
#A00 SPIFFY COMPUTER SERVICE DIV. 000010 A00 None
#B01 PLANNING 000020 A00 None
#C01 INFORMATION CENTER 000030 A00 None
#D01 DEVELOPMENT CENTER  A00 None
#D11 MANUFACTURING SYSTEMS 000060 D01 None
#D21 ADMINISTRATION SYSTEMS 000070 D01 None
#E01 SUPPORT SERVICES 000050 A00 None
#E11 OPERATIONS 000090 E01 None
#E21 SOFTWARE SUPPORT 000100 E01 None
#__ZOS_EXPECTED__
#10 Sanders Mgr   7 18357.50 
#20 Pernal Sales 8 18171.25 612.45
#30 Marenghi Mgr   5 17506.75 
#40 OBrien Sales 6 18006.00 846.55
#50 Hanes Mgr   10 20659.80 
#60 Quigley Sales  16808.30 650.25
#70 Rothman Sales 7 16502.83 1152.00
#80 James Clerk  13504.60 128.20
#90 Koonitz Sales 6 18001.75 1386.70
#100 Plotz Mgr   7 18352.80 
#110 Ngan Clerk 5 12508.20 206.60
#120 Naughton Clerk  12954.75 180.00
#130 Yamaguchi Clerk 6 10505.90 75.60
#140 Fraye Mgr   6 21150.00 
#150 Williams Sales 6 19456.50 637.65
#160 Molinare Mgr   7 22959.20 
#170 Kermisch Clerk 4 12258.50 110.10
#180 Abrahams Clerk 3 12009.75 236.50
#190 Sneider Clerk 8 14252.75 126.50
#200 Scoutten Clerk  11508.60 84.20
#210 Lu Mgr   10 20010.00 
#220 Smith Sales 7 17654.50 992.80
#230 Lundquist Clerk 3 13369.80 189.65
#240 Daniels Mgr   5 19260.25 
#250 Wheeler Clerk 6 14460.00 513.30
#260 Jones Mgr   12 21234.00 
#270 Lea Mgr   9 18555.50 
#280 Wilson Sales 9 18674.50 811.50
#290 Quill Mgr   10 19818.00 
#300 Davis Sales 5 15454.50 806.10
#310 Graham Sales 13 21000.00 200.30
#320 Gonzales Sales 4 16858.20 844.00
#330 Burke Clerk 1 10988.00 55.50
#340 Edwards Sales 7 17844.00 1285.00
#350 Gafney Clerk 5 13030.50 188.00
#A00 SPIFFY COMPUTER SERVICE DIV. 000010 A00 None
#B01 PLANNING 000020 A00 None
#C01 INFORMATION CENTER 000030 A00 None
#D01 DEVELOPMENT CENTER  A00 None
#D11 MANUFACTURING SYSTEMS 000060 D01 None
#D21 ADMINISTRATION SYSTEMS 000070 D01 None
#E01 SUPPORT SERVICES 000050 A00 None
#E11 OPERATIONS 000090 E01 None
#E21 SOFTWARE SUPPORT 000100 E01 None
#__SYSTEMI_EXPECTED__
#10 Sanders Mgr   7 18357.50 
#20 Pernal Sales 8 18171.25 612.45
#30 Marenghi Mgr   5 17506.75 
#40 OBrien Sales 6 18006.00 846.55
#50 Hanes Mgr   10 20659.80 
#60 Quigley Sales  16808.30 650.25
#70 Rothman Sales 7 16502.83 1152.00
#80 James Clerk  13504.60 128.20
#90 Koonitz Sales 6 18001.75 1386.70
#100 Plotz Mgr   7 18352.80 
#110 Ngan Clerk 5 12508.20 206.60
#120 Naughton Clerk  12954.75 180.00
#130 Yamaguchi Clerk 6 10505.90 75.60
#140 Fraye Mgr   6 21150.00 
#150 Williams Sales 6 19456.50 637.65
#160 Molinare Mgr   7 22959.20 
#170 Kermisch Clerk 4 12258.50 110.10
#180 Abrahams Clerk 3 12009.75 236.50
#190 Sneider Clerk 8 14252.75 126.50
#200 Scoutten Clerk  11508.60 84.20
#210 Lu Mgr   10 20010.00 
#220 Smith Sales 7 17654.50 992.80
#230 Lundquist Clerk 3 13369.80 189.65
#240 Daniels Mgr   5 19260.25 
#250 Wheeler Clerk 6 14460.00 513.30
#260 Jones Mgr   12 21234.00 
#270 Lea Mgr   9 18555.50 
#280 Wilson Sales 9 18674.50 811.50
#290 Quill Mgr   10 19818.00 
#300 Davis Sales 5 15454.50 806.10
#310 Graham Sales 13 21000.00 200.30
#320 Gonzales Sales 4 16858.20 844.00
#330 Burke Clerk 1 10988.00 55.50
#340 Edwards Sales 7 17844.00 1285.00
#350 Gafney Clerk 5 13030.50 188.00
#A00 SPIFFY COMPUTER SERVICE DIV. 000010 A00 None
#B01 PLANNING 000020 A00 None
#C01 INFORMATION CENTER 000030 A00 None
#D01 DEVELOPMENT CENTER  A00 None
#D11 MANUFACTURING SYSTEMS 000060 D01 None
#D21 ADMINISTRATION SYSTEMS 000070 D01 None
#E01 SUPPORT SERVICES 000050 A00 None
#E11 OPERATIONS 000090 E01 None
#E21 SOFTWARE SUPPORT 000100 E01 None
#__IDS_EXPECTED__
#10 Sanders Mgr   7 18357.50 
#20 Pernal Sales 8 18171.25 612.45
#30 Marenghi Mgr   5 17506.75 
#40 OBrien Sales 6 18006.00 846.55
#50 Hanes Mgr   10 20659.80 
#60 Quigley Sales  16808.30 650.25
#70 Rothman Sales 7 16502.83 1152.00
#80 James Clerk  13504.60 128.20
#90 Koonitz Sales 6 18001.75 1386.70
#100 Plotz Mgr   7 18352.80 
#110 Ngan Clerk 5 12508.20 206.60
#120 Naughton Clerk  12954.75 180.00
#130 Yamaguchi Clerk 6 10505.90 75.60
#140 Fraye Mgr   6 21150.00 
#150 Williams Sales 6 19456.50 637.65
#160 Molinare Mgr   7 22959.20 
#170 Kermisch Clerk 4 12258.50 110.10
#180 Abrahams Clerk 3 12009.75 236.50
#190 Sneider Clerk 8 14252.75 126.50
#200 Scoutten Clerk  11508.60 84.20
#210 Lu Mgr   10 20010.00 
#220 Smith Sales 7 17654.50 992.80
#230 Lundquist Clerk 3 13369.80 189.65
#240 Daniels Mgr   5 19260.25 
#250 Wheeler Clerk 6 14460.00 513.30
#260 Jones Mgr   12 21234.00 
#270 Lea Mgr   9 18555.50 
#280 Wilson Sales 9 18674.50 811.50
#290 Quill Mgr   10 19818.00 
#300 Davis Sales 5 15454.50 806.10
#310 Graham Sales 13 21000.00 200.30
#320 Gonzales Sales 4 16858.20 844.00
#330 Burke Clerk 1 10988.00 55.50
#340 Edwards Sales 7 17844.00 1285.00
#350 Gafney Clerk 5 13030.50 188.00
#A00 SPIFFY COMPUTER SERVICE DIV. 000010 A00 None
#B01 PLANNING 000020 A00 None
#C01 INFORMATION CENTER 000030 A00 None
#D01 DEVELOPMENT CENTER  A00 None
#D11 MANUFACTURING SYSTEMS 000060 D01 None
#D21 ADMINISTRATION SYSTEMS 000070 D01 None
#E01 SUPPORT SERVICES 000050 A00 None
#E11 OPERATIONS 000090 E01 None
#E21 SOFTWARE SUPPORT 000100 E01 None
