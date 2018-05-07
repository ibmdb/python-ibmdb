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

    def test_157_FetchAssocScrollableCursor_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_157)

    def run_test_157(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            sql = "SELECT id, name, breed, weight FROM animals ORDER BY breed"
            if (server.DBMS_NAME[0:3] != 'IDS'):
                result = ibm_db.exec_immediate(conn, sql, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            else:
                result = ibm_db.exec_immediate(conn, sql, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC})

            i = 2
            row = ibm_db.fetch_assoc(result, i)
            while ( row ):
                if (server.DBMS_NAME[0:3] == 'IDS'):
                    print("%-5d %-16s %-32s %10s\n" % (row['id'], row['name'], row['breed'], row['weight']))
                else:
                    print("%-5d %-16s %-32s %10s\n" % (row['ID'], row['NAME'], row['BREED'], row['WEIGHT']))
                i = i + 2
                row = ibm_db.fetch_assoc(result, i)
#
#__END__
#__LUW_EXPECTED__
#0     Pook             cat                                    3.20
#5     Rickety Ride     goat                                   9.70
#2     Smarty           horse                                350.00
#__ZOS_EXPECTED__
#0     Pook             cat                                    3.20
#5     Rickety Ride     goat                                   9.70
#2     Smarty           horse                                350.00
#__SYSTEMI_EXPECTED__
#0     Pook             cat                                    3.20
#5     Rickety Ride     goat                                   9.70
#2     Smarty           horse                                350.00
#__IDS_EXPECTED__
#0     Pook             cat                                    3.20
#5     Rickety Ride     goat                                   9.70
#2     Smarty           horse                                350.00
