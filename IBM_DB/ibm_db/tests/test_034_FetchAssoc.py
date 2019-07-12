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

    def test_034_FetchAssoc(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_034)

    def run_test_034(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        result = ibm_db.exec_immediate(conn, "select * from staff")
        row = ibm_db.fetch_assoc(result)
        if( row ):
            #printf("%5d  ",row['ID'])
            #printf("%-10s ",row['NAME'])
            #printf("%5d ",row['DEPT'])
            #printf("%-7s ",row['JOB'])
            #printf("%5d ", row['YEARS'])
            #printf("%15s ", row['SALARY'])
            #printf("%10s ", row['COMM'])
            #puts ""
            print("%5d %-10s %5d %-7s %5d %15s %10s" % (row['ID'], row['NAME'], row['DEPT'], row['JOB'], row['YEARS'], row['SALARY'], row['COMM']))

        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#   10 Sanders       20 Mgr         7        18357.50       None
#__ZOS_EXPECTED__
#   10 Sanders       20 Mgr         7        18357.50       None
#__SYSTEMI_EXPECTED__
#   10 Sanders       20 Mgr         7        18357.50       None
#__IDS_EXPECTED__
#   10 Sanders       20 Mgr         7        18357.50       None
