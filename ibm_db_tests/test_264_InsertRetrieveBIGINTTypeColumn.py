#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

try:
    long        # Python 3
except NameError:
    long = int  # Python 3


class IbmDbTestCase(unittest.TestCase):

    def test_264_InsertRetrieveBIGINTTypeColumn(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_264)

    def run_test_264(self):
        # Make a connection
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            server = ibm_db.server_info( conn )
            if (server.DBMS_NAME[0:3] == 'IDS'):
                op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
                ibm_db.set_option(conn, op, 1)

            # Drop the tab_bigint table, in case it exists
            drop = 'DROP TABLE tab_bigint'
            result = ''
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass
            # Create the tab_bigint table
            if (server.DBMS_NAME[0:3] == 'IDS'):
                create = "CREATE TABLE tab_bigint (col1 INT8, col2 INT8, col3 INT8, col4 INT8)"
            else:
                create = "CREATE TABLE tab_bigint (col1 BIGINT, col2 BIGINT, col3 BIGINT, col4 BIGINT)"
            result = ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO tab_bigint values (-9223372036854775807, 9223372036854775807, 0, NULL)"
            res = ibm_db.exec_immediate(conn, insert)
            print("Number of inserted rows:", ibm_db.num_rows(res))

            stmt = ibm_db.prepare(conn, "SELECT * FROM tab_bigint")
            ibm_db.execute(stmt)
            data = ibm_db.fetch_both(stmt)
            while ( data ):
                print(data[0])
                print(data[1])
                print(data[2])
                print(data[3])
                print(type(data[0]) is long)
                print(type(data[1]) is long)
                print(type(data[2]) is long)
                data = ibm_db.fetch_both(stmt)

            ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#Number of inserted rows: 1
#-9223372036854775807
#9223372036854775807
#0
#None
#True
#True
#True
#__ZOS_EXPECTED__
#Number of inserted rows: 1
#-9223372036854775807
#9223372036854775807
#0
#None
#True
#True
#True
#__SYSTEMI_EXPECTED__
#Number of inserted rows: 1
#-9223372036854775807
#9223372036854775807
#0
#None
#True
#True
#True
#__IDS_EXPECTED__
#Number of inserted rows: 1
#-9223372036854775807
#9223372036854775807
#0
#None
#True
#True
#True
