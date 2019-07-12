#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#
# NOTE: IDS does not support XML as a native datatype (test is invalid for IDS)

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_195_InsertRetrieveXMLData_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_195)

    def run_test_195(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if ((server.DBMS_NAME[0:3] != 'IDS') and (server.DBMS_NAME[0:2] != "AS")):
            drop = 'DROP TABLE test_195'
            try:
                result = ibm_db.exec_immediate(conn, drop)
            except:
                pass
            create = 'CREATE TABLE test_195 (id INTEGER, data XML)'
            result = ibm_db.exec_immediate(conn, create)

            insert = "INSERT INTO test_195 values (0, '<TEST><def><xml/></def></TEST>')"

            ibm_db.exec_immediate(conn, insert)

            sql =  "SELECT data FROM test_195"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            result = ibm_db.fetch_assoc(stmt)
            while( result ):
                print("Output:", result)
                result = ibm_db.fetch_assoc(stmt)
            ibm_db.close(conn)
        else:
            print("Native XML datatype is not supported.")

#__END__
#__LUW_EXPECTED__
#Output:%s<TEST><def><xml/></def></TEST>
#__ZOS_EXPECTED__
#Output:%s<TEST><def><xml/></def></TEST>
#__SYSTEMI_EXPECTED__
#Native XML datatype is not supported.
#__IDS_EXPECTED__
#Native XML datatype is not supported.
