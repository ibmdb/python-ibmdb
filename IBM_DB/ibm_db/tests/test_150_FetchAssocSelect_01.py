#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_150_FetchAssocSelect_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_150)

    def run_test_150(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        result = ibm_db.exec_immediate(conn, "select * from staff")

        row = ibm_db.fetch_assoc(result)
        while ( row ):
            #print "%5d  " % row['ID']
            #print "%-10s " % row['NAME']
            #print "%5d " % row['DEPT']
            #print "%-7s " % row['JOB']
            #print "%5d " % row['YEARS']
            #print "%15s " % row['SALARY']
            #print "%10s " % row['COMM']
            if (row['YEARS'] == None):
                row['YEARS'] = 0
            if (row['COMM'] == None):
                row['COMM'] = ''
            print("%5d  %-10s %5d %-7s %5s %15s %10s " % (row['ID'], row['NAME'], row['DEPT'], row['JOB'], row['YEARS'], row['SALARY'], row['COMM']))
            row = ibm_db.fetch_assoc(result)

#__END__
#__LUW_EXPECTED__
#   10  Sanders       20 Mgr         7        18357.50            
#   20  Pernal        20 Sales       8        18171.25     612.45 
#   30  Marenghi      38 Mgr         5        17506.75            
#   40  OBrien        38 Sales       6        18006.00     846.55 
#   50  Hanes         15 Mgr        10        20659.80            
#   60  Quigley       38 Sales       0        16808.30     650.25 
#   70  Rothman       15 Sales       7        16502.83    1152.00 
#   80  James         20 Clerk       0        13504.60     128.20 
#   90  Koonitz       42 Sales       6        18001.75    1386.70 
#  100  Plotz         42 Mgr         7        18352.80            
#  110  Ngan          15 Clerk       5        12508.20     206.60 
#  120  Naughton      38 Clerk       0        12954.75     180.00 
#  130  Yamaguchi     42 Clerk       6        10505.90      75.60 
#  140  Fraye         51 Mgr         6        21150.00            
#  150  Williams      51 Sales       6        19456.50     637.65 
#  160  Molinare      10 Mgr         7        22959.20            
#  170  Kermisch      15 Clerk       4        12258.50     110.10 
#  180  Abrahams      38 Clerk       3        12009.75     236.50 
#  190  Sneider       20 Clerk       8        14252.75     126.50 
#  200  Scoutten      42 Clerk       0        11508.60      84.20 
#  210  Lu            10 Mgr        10        20010.00            
#  220  Smith         51 Sales       7        17654.50     992.80 
#  230  Lundquist     51 Clerk       3        13369.80     189.65 
#  240  Daniels       10 Mgr         5        19260.25            
#  250  Wheeler       51 Clerk       6        14460.00     513.30 
#  260  Jones         10 Mgr        12        21234.00            
#  270  Lea           66 Mgr         9        18555.50            
#  280  Wilson        66 Sales       9        18674.50     811.50 
#  290  Quill         84 Mgr        10        19818.00            
#  300  Davis         84 Sales       5        15454.50     806.10 
#  310  Graham        66 Sales      13        21000.00     200.30 
#  320  Gonzales      66 Sales       4        16858.20     844.00 
#  330  Burke         66 Clerk       1        10988.00      55.50 
#  340  Edwards       84 Sales       7        17844.00    1285.00 
#  350  Gafney        84 Clerk       5        13030.50     188.00 
#__ZOS_EXPECTED__
#   10  Sanders       20 Mgr         7        18357.50            
#   20  Pernal        20 Sales       8        18171.25     612.45 
#   30  Marenghi      38 Mgr         5        17506.75            
#   40  OBrien        38 Sales       6        18006.00     846.55 
#   50  Hanes         15 Mgr        10        20659.80            
#   60  Quigley       38 Sales       0        16808.30     650.25 
#   70  Rothman       15 Sales       7        16502.83    1152.00 
#   80  James         20 Clerk       0        13504.60     128.20 
#   90  Koonitz       42 Sales       6        18001.75    1386.70 
#  100  Plotz         42 Mgr         7        18352.80            
#  110  Ngan          15 Clerk       5        12508.20     206.60 
#  120  Naughton      38 Clerk       0        12954.75     180.00 
#  130  Yamaguchi     42 Clerk       6        10505.90      75.60 
#  140  Fraye         51 Mgr         6        21150.00            
#  150  Williams      51 Sales       6        19456.50     637.65 
#  160  Molinare      10 Mgr         7        22959.20            
#  170  Kermisch      15 Clerk       4        12258.50     110.10 
#  180  Abrahams      38 Clerk       3        12009.75     236.50 
#  190  Sneider       20 Clerk       8        14252.75     126.50 
#  200  Scoutten      42 Clerk       0        11508.60      84.20 
#  210  Lu            10 Mgr        10        20010.00            
#  220  Smith         51 Sales       7        17654.50     992.80 
#  230  Lundquist     51 Clerk       3        13369.80     189.65 
#  240  Daniels       10 Mgr         5        19260.25            
#  250  Wheeler       51 Clerk       6        14460.00     513.30 
#  260  Jones         10 Mgr        12        21234.00            
#  270  Lea           66 Mgr         9        18555.50            
#  280  Wilson        66 Sales       9        18674.50     811.50 
#  290  Quill         84 Mgr        10        19818.00            
#  300  Davis         84 Sales       5        15454.50     806.10 
#  310  Graham        66 Sales      13        21000.00     200.30 
#  320  Gonzales      66 Sales       4        16858.20     844.00 
#  330  Burke         66 Clerk       1        10988.00      55.50 
#  340  Edwards       84 Sales       7        17844.00    1285.00 
#  350  Gafney        84 Clerk       5        13030.50     188.00 
#__SYSTEMI_EXPECTED__
#   10  Sanders       20 Mgr         7        18357.50            
#   20  Pernal        20 Sales       8        18171.25     612.45 
#   30  Marenghi      38 Mgr         5        17506.75            
#   40  OBrien        38 Sales       6        18006.00     846.55 
#   50  Hanes         15 Mgr        10        20659.80            
#   60  Quigley       38 Sales       0        16808.30     650.25 
#   70  Rothman       15 Sales       7        16502.83    1152.00 
#   80  James         20 Clerk       0        13504.60     128.20 
#   90  Koonitz       42 Sales       6        18001.75    1386.70 
#  100  Plotz         42 Mgr         7        18352.80            
#  110  Ngan          15 Clerk       5        12508.20     206.60 
#  120  Naughton      38 Clerk       0        12954.75     180.00 
#  130  Yamaguchi     42 Clerk       6        10505.90      75.60 
#  140  Fraye         51 Mgr         6        21150.00            
#  150  Williams      51 Sales       6        19456.50     637.65 
#  160  Molinare      10 Mgr         7        22959.20            
#  170  Kermisch      15 Clerk       4        12258.50     110.10 
#  180  Abrahams      38 Clerk       3        12009.75     236.50 
#  190  Sneider       20 Clerk       8        14252.75     126.50 
#  200  Scoutten      42 Clerk       0        11508.60      84.20 
#  210  Lu            10 Mgr        10        20010.00            
#  220  Smith         51 Sales       7        17654.50     992.80 
#  230  Lundquist     51 Clerk       3        13369.80     189.65 
#  240  Daniels       10 Mgr         5        19260.25            
#  250  Wheeler       51 Clerk       6        14460.00     513.30 
#  260  Jones         10 Mgr        12        21234.00            
#  270  Lea           66 Mgr         9        18555.50            
#  280  Wilson        66 Sales       9        18674.50     811.50 
#  290  Quill         84 Mgr        10        19818.00            
#  300  Davis         84 Sales       5        15454.50     806.10 
#  310  Graham        66 Sales      13        21000.00     200.30 
#  320  Gonzales      66 Sales       4        16858.20     844.00 
#  330  Burke         66 Clerk       1        10988.00      55.50 
#  340  Edwards       84 Sales       7        17844.00    1285.00 
#  350  Gafney        84 Clerk       5        13030.50     188.00 
#__IDS_EXPECTED__
#   10  Sanders       20 Mgr         7        18357.50            
#   20  Pernal        20 Sales       8        18171.25     612.45 
#   30  Marenghi      38 Mgr         5        17506.75            
#   40  OBrien        38 Sales       6        18006.00     846.55 
#   50  Hanes         15 Mgr        10        20659.80            
#   60  Quigley       38 Sales       0        16808.30     650.25 
#   70  Rothman       15 Sales       7        16502.83    1152.00 
#   80  James         20 Clerk       0        13504.60     128.20 
#   90  Koonitz       42 Sales       6        18001.75    1386.70 
#  100  Plotz         42 Mgr         7        18352.80            
#  110  Ngan          15 Clerk       5        12508.20     206.60 
#  120  Naughton      38 Clerk       0        12954.75     180.00 
#  130  Yamaguchi     42 Clerk       6        10505.90      75.60 
#  140  Fraye         51 Mgr         6        21150.00            
#  150  Williams      51 Sales       6        19456.50     637.65 
#  160  Molinare      10 Mgr         7        22959.20            
#  170  Kermisch      15 Clerk       4        12258.50     110.10 
#  180  Abrahams      38 Clerk       3        12009.75     236.50 
#  190  Sneider       20 Clerk       8        14252.75     126.50 
#  200  Scoutten      42 Clerk       0        11508.60      84.20 
#  210  Lu            10 Mgr        10        20010.00            
#  220  Smith         51 Sales       7        17654.50     992.80 
#  230  Lundquist     51 Clerk       3        13369.80     189.65 
#  240  Daniels       10 Mgr         5        19260.25            
#  250  Wheeler       51 Clerk       6        14460.00     513.30 
#  260  Jones         10 Mgr        12        21234.00            
#  270  Lea           66 Mgr         9        18555.50            
#  280  Wilson        66 Sales       9        18674.50     811.50 
#  290  Quill         84 Mgr        10        19818.00            
#  300  Davis         84 Sales       5        15454.50     806.10 
#  310  Graham        66 Sales      13        21000.00     200.30 
#  320  Gonzales      66 Sales       4        16858.20     844.00 
#  330  Burke         66 Clerk       1        10988.00      55.50 
#  340  Edwards       84 Sales       7        17844.00    1285.00 
#  350  Gafney        84 Clerk       5        13030.50     188.00 
