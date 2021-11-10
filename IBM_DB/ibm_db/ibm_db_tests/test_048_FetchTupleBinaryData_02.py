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

    def test_048_FetchTupleBinaryData_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_048)

    def run_test_048(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        if (not conn):
            print("Could not make a connection.")
            return 0
        server = ibm_db.server_info( conn )

        with open("ibm_db_tests/spook_out.png", "wb") as fp:
            if (server.DBMS_NAME[0:3] == 'IDS'):
                result = ibm_db.exec_immediate(conn, "SELECT picture FROM animal_pics WHERE name = 'Spook'")
            else:
                result = ibm_db.exec_immediate(conn, "SELECT picture, LENGTH(picture) FROM animal_pics WHERE name = 'Spook'")
            if (not result):
                print("Could not execute SELECT statement.")
                return 0
            row = ibm_db.fetch_tuple(result)
            if row:
                fp.write(row[0])
            else:
                print(ibm_db.stmt_errormsg())
        with open('ibm_db_tests/spook_out.png', 'rb') as fp:
            pic_out = fp.read()
        with open('ibm_db_tests/spook.png', 'rb') as fp1:
            pic_in = fp1.read()
        cmp = pic_in == pic_out
        print("Are the files the same:", cmp)

#__END__
#__LUW_EXPECTED__
#Are the files the same: True
#__ZOS_EXPECTED__
#Are the files the same: True
#__SYSTEMI_EXPECTED__
#Are the files the same: True
#__IDS_EXPECTED__
#Are the files the same: True
