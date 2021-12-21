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

    def test_checkBooleanType(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_checkBooleanType)

    def run_test_checkBooleanType(self):
        conn = ibm_db.connect("DATABASE=" + config.database + ";HOSTNAME=" + config.hostname + ";PORT=" + str(config.port) + ";UID=" + config.user + ";PWD=" + config.password + ";PROTOCOL=TCPIP;PATCH2=88", config.user, config.password)
        if (not conn):
            print("Could not make a connection.")
            return 0
        server = ibm_db.server_info( conn )

        if( not server.DBMS_NAME.startswith('DB2/')):
            print("Boolean is not supported")
            return 0

        try:
            ibm_db.exec_immediate(conn,"DROP TABLE bool_test")
        except:
            pass

        try:
            ibm_db.exec_immediate(conn, "CREATE TABLE bool_test(col1 INTEGER, col2 BOOLEAN, col3 BOOLEAN)")
        except Exception as e:
            print("Error : {}\n".format(str(e)))
            exit(-1)

        try:
            select_sql = 'SELECT * FROM bool_test'
            stmt = ibm_db.exec_immediate(conn, select_sql)

            for i in range(0,ibm_db.num_fields(stmt)):
                print(str(ibm_db.field_type(stmt,i)))

            ibm_db.close(conn)
        except Exception as e:
            print("Error:{}".format(str(e))) 
            

#__END__
#__LUW_EXPECTED__
#int
#boolean
#boolean
#__ZOS_EXPECTED__
#Boolean is not supported
#__SYSTEMI_EXPECTED__
#Boolean is not supported
#__IDS_EXPECTED__
#Boolean is not supported
