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

    def test_52949_TestSPIntVarcharXml(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_52949)

    def test_int(self, conn):
        return_value = 0
        stmt, return_value = ibm_db.callproc(conn, 'PROCESSINT', (return_value,))
        print("ProcessINT:", return_value)

    def test_varchar(self, conn):
        return_value = ""
        stmt, return_value = ibm_db.callproc(conn, 'PROCESSVAR', (return_value,))
        print("ProcessVAR:", return_value)

    def test_xml(self, conn):
        return_value = "This is just a test for XML Column. The data gets truncated since we do not "
        stmt, return_value = ibm_db.callproc(conn, 'PROCESSXML', (return_value,))
        print("ProcessXML:", return_value.__str__())

    def drop_tables(self, conn):
        if conn:
            dr = "DROP PROCEDURE processxml"
            try:
                ibm_db.exec_immediate(conn, dr)
            except:
                pass
            try:
                dr = "DROP PROCEDURE processint"
                ibm_db.exec_immediate(conn, dr)
            except:
                pass
            try:
                dr = "DROP PROCEDURE processvar"
                ibm_db.exec_immediate(conn, dr)
            except:
                pass
            try:
                dr = "DROP TABLE test_stored"
                ibm_db.exec_immediate(conn, dr)
            except:
                pass

    def run_test_52949(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            serverinfo = ibm_db.server_info(conn )
            server = serverinfo.DBMS_NAME[0:3]
            result = ''
            self.drop_tables(conn)

            try:
                cr1 = "CREATE TABLE test_stored (id INT, name VARCHAR(50), age int, cv XML)"
                result = ibm_db.exec_immediate(conn, cr1)
                in1 = "INSERT INTO test_stored values (1, 'Kellen', 24, '<example>This is an example</example>')"
                result = ibm_db.exec_immediate(conn, in1)
                st1 = "CREATE PROCEDURE processxml(OUT risorsa xml) LANGUAGE SQL BEGIN SELECT cv INTO risorsa FROM test_stored WHERE ID = 1; END"
                result = ibm_db.exec_immediate(conn, st1)

                #self.test_xml(conn)
            except:
                pass

            try:
                self.drop_tables(conn)
                cr1 = "CREATE TABLE test_stored (id INT, name VARCHAR(50), age int, cv VARCHAR(200))"
                result = ibm_db.exec_immediate(conn, cr1)
                in1 = "INSERT INTO test_stored values (1, 'Kellen', 24, '<example>This is an example</example>')"
                result = ibm_db.exec_immediate(conn, in1)
            except:
                pass

            if (server == 'IDS'):
                st2 = "CREATE PROCEDURE processint(OUT risorsa int); SELECT age INTO risorsa FROM test_stored WHERE ID = 1; END PROCEDURE;"
            else:
                st2 = "CREATE PROCEDURE processint(OUT risorsa int) LANGUAGE SQL BEGIN SELECT age INTO risorsa FROM test_stored WHERE ID = 1; END"
            result = ibm_db.exec_immediate(conn, st2)

            if (server == 'IDS'):
                st3 = "CREATE PROCEDURE processvar(OUT risorsa varchar(50)); SELECT name INTO risorsa FROM test_stored WHERE ID = 1; END PROCEDURE;"
            else:
                st3 = "CREATE PROCEDURE processvar(OUT risorsa varchar(50)) LANGUAGE SQL BEGIN SELECT name INTO risorsa FROM test_stored WHERE ID = 1; END"
            result = ibm_db.exec_immediate(conn, st3)

            self.test_int(conn)
            self.test_varchar(conn)

            ibm_db.close(conn)
        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kellen
#__ZOS_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kellen
#__SYSTEMI_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kellen
#__IDS_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kellen
