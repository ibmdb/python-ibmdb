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

    def test_159_FetchAssocSeveralRows_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_159)

    def run_test_159(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        result = ibm_db.exec_immediate(conn, "select name,job from staff")
        i = 1
        row = ibm_db.fetch_assoc(result)
        while ( row ):
            #printf("%3d %10s %10s\n",i, row['NAME'], row['JOB'])
            print("%3d %10s %10s" % (i, row['NAME'], row['JOB']))
            i += 1
            row = ibm_db.fetch_assoc(result)

#__END__
#__LUW_EXPECTED__
#  1    Sanders      Mgr  
#  2     Pernal      Sales
#  3   Marenghi      Mgr  
#  4     OBrien      Sales
#  5      Hanes      Mgr  
#  6    Quigley      Sales
#  7    Rothman      Sales
#  8      James      Clerk
#  9    Koonitz      Sales
# 10      Plotz      Mgr  
# 11       Ngan      Clerk
# 12   Naughton      Clerk
# 13  Yamaguchi      Clerk
# 14      Fraye      Mgr  
# 15   Williams      Sales
# 16   Molinare      Mgr  
# 17   Kermisch      Clerk
# 18   Abrahams      Clerk
# 19    Sneider      Clerk
# 20   Scoutten      Clerk
# 21         Lu      Mgr  
# 22      Smith      Sales
# 23  Lundquist      Clerk
# 24    Daniels      Mgr  
# 25    Wheeler      Clerk
# 26      Jones      Mgr  
# 27        Lea      Mgr  
# 28     Wilson      Sales
# 29      Quill      Mgr  
# 30      Davis      Sales
# 31     Graham      Sales
# 32   Gonzales      Sales
# 33      Burke      Clerk
# 34    Edwards      Sales
# 35     Gafney      Clerk
#__ZOS_EXPECTED__
#  1    Sanders      Mgr  
#  2     Pernal      Sales
#  3   Marenghi      Mgr  
#  4     OBrien      Sales
#  5      Hanes      Mgr  
#  6    Quigley      Sales
#  7    Rothman      Sales
#  8      James      Clerk
#  9    Koonitz      Sales
# 10      Plotz      Mgr  
# 11       Ngan      Clerk
# 12   Naughton      Clerk
# 13  Yamaguchi      Clerk
# 14      Fraye      Mgr  
# 15   Williams      Sales
# 16   Molinare      Mgr  
# 17   Kermisch      Clerk
# 18   Abrahams      Clerk
# 19    Sneider      Clerk
# 20   Scoutten      Clerk
# 21         Lu      Mgr  
# 22      Smith      Sales
# 23  Lundquist      Clerk
# 24    Daniels      Mgr  
# 25    Wheeler      Clerk
# 26      Jones      Mgr  
# 27        Lea      Mgr  
# 28     Wilson      Sales
# 29      Quill      Mgr  
# 30      Davis      Sales
# 31     Graham      Sales
# 32   Gonzales      Sales
# 33      Burke      Clerk
# 34    Edwards      Sales
# 35     Gafney      Clerk
#__SYSTEMI_EXPECTED__
#  1    Sanders      Mgr  
#  2     Pernal      Sales
#  3   Marenghi      Mgr  
#  4     OBrien      Sales
#  5      Hanes      Mgr  
#  6    Quigley      Sales
#  7    Rothman      Sales
#  8      James      Clerk
#  9    Koonitz      Sales
# 10      Plotz      Mgr  
# 11       Ngan      Clerk
# 12   Naughton      Clerk
# 13  Yamaguchi      Clerk
# 14      Fraye      Mgr  
# 15   Williams      Sales
# 16   Molinare      Mgr  
# 17   Kermisch      Clerk
# 18   Abrahams      Clerk
# 19    Sneider      Clerk
# 20   Scoutten      Clerk
# 21         Lu      Mgr  
# 22      Smith      Sales
# 23  Lundquist      Clerk
# 24    Daniels      Mgr  
# 25    Wheeler      Clerk
# 26      Jones      Mgr  
# 27        Lea      Mgr  
# 28     Wilson      Sales
# 29      Quill      Mgr  
# 30      Davis      Sales
# 31     Graham      Sales
# 32   Gonzales      Sales
# 33      Burke      Clerk
# 34    Edwards      Sales
# 35     Gafney      Clerk
#__IDS_EXPECTED__
#  1    Sanders      Mgr  
#  2     Pernal      Sales
#  3   Marenghi      Mgr  
#  4     OBrien      Sales
#  5      Hanes      Mgr  
#  6    Quigley      Sales
#  7    Rothman      Sales
#  8      James      Clerk
#  9    Koonitz      Sales
# 10      Plotz      Mgr  
# 11       Ngan      Clerk
# 12   Naughton      Clerk
# 13  Yamaguchi      Clerk
# 14      Fraye      Mgr  
# 15   Williams      Sales
# 16   Molinare      Mgr  
# 17   Kermisch      Clerk
# 18   Abrahams      Clerk
# 19    Sneider      Clerk
# 20   Scoutten      Clerk
# 21         Lu      Mgr  
# 22      Smith      Sales
# 23  Lundquist      Clerk
# 24    Daniels      Mgr  
# 25    Wheeler      Clerk
# 26      Jones      Mgr  
# 27        Lea      Mgr  
# 28     Wilson      Sales
# 29      Quill      Mgr  
# 30      Davis      Sales
# 31     Graham      Sales
# 32   Gonzales      Sales
# 33      Burke      Clerk
# 34    Edwards      Sales
# 35     Gafney      Clerk
