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
import getpass

class IbmDbTestCase(unittest.TestCase):

    def test_146_CallSPINAndOUTParams(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_146)

    def run_test_146(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            name = "Peaches"
            second_name = "Rickety Ride"
            weight = 0

            print("Values of bound parameters _before_ CALL:")
            print("  1: %s 2: %s 3: %d\n" % (name, second_name, weight))

            if('zos' in sys.platform):
                proc_name = getpass.getuser() + ".MATCH_ANIMAL"
            else:
                proc_name = "match_animal"
            stmt, name, second_name, weight = ibm_db.callproc(conn, proc_name, (name, second_name, weight))

            if stmt is not None:
                print("Values of bound parameters _after_ CALL:")
                print("  1: %s 2: %s 3: %d\n" % (name, second_name, weight))

                if (server.DBMS_NAME[0:3] != 'IDS'):
                    print("Results:")
                    row = ibm_db.fetch_tuple(stmt)
                    while ( row ):
                        print("  %s, %s, %s" % (row[0].strip(), row[1].strip(), row[2]))
                        row = ibm_db.fetch_tuple(stmt)

#__END__
#__LUW_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: Peaches 2: Rickety Ride 3: 0
#
#Values of bound parameters _after_ CALL:
#  1: Peaches 2: TRUE 3: 12
#
#Results:
#  Peaches, dog, 12.30
#  Pook, cat, 3.20
#  Rickety Ride, goat, 9.70
#  Smarty, horse, 350.00
#  Sweater, llama, 150.00
#__ZOS_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: Peaches 2: Rickety Ride 3: 0
#
#Values of bound parameters _after_ CALL:
#  1: Peaches 2: TRUE 3: 12
#
#Results:
#  Peaches, dog, 12.30
#  Pook, cat, 3.20
#  Rickety Ride, goat, 9.70
#  Smarty, horse, 350.00
#  Sweater, llama, 150.00
#__SYSTEMI_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: Peaches 2: Rickety Ride 3: 0
#
#Values of bound parameters _after_ CALL:
#  1: Peaches 2: TRUE 3: 12
#
#Results:
#  Peaches, dog, 12.30
#  Pook, cat, 3.20
#  Rickety Ride, goat, 9.70
#  Smarty, horse, 350.00
#  Sweater, llama, 150.00
#__IDS_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: Peaches 2: Rickety Ride 3: 0
#
#Values of bound parameters _after_ CALL:
#  1: Peaches 2: TRUE 3: 12
#
