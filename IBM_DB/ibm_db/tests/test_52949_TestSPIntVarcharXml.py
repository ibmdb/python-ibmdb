# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

  def test_52949_TestSPIntVarcharXml(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_52949)

  def test_int(self, conn):
    sql = "CALL PROCESSINT(?)"
    stmt = ibm_db.prepare(conn, sql)
    return_value = 0
    ibm_db.bind_param(stmt, 1, return_value, ibm_db.SQL_PARAM_OUTPUT)
    ibm_db.execute(stmt)
    print "ProcessINT:", return_value

  def test_varchar(self, conn):
    sql = "CALL PROCESSVAR(?)"
    stmt = ibm_db.prepare(conn, sql)
    return_value = ""
    ibm_db.bind_param(stmt, 1, return_value, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_CHAR, None, None, 4)
    ibm_db.execute(stmt)
    print "ProcessVAR:", return_value

  def test_xml(self, conn):
    sql = "CALL PROCESSXML(?)"
    stmt = ibm_db.prepare(conn, sql)
    return_value = ""
    ibm_db.bind_param(stmt, 1, return_value, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_CHAR, None, None, 100)
    ibm_db.execute(stmt)
    print "ProcessXML:", return_value

  def run_test_52949(self):
   conn = ibm_db.connect(config.database, config.user, config.password)

   if conn:
     serverinfo = ibm_db.server_info(conn )
     server = serverinfo.DBMS_NAME[0:3]
     dr = "DROP PROCEDURE processxml"
     result = ''
     try:
       result = ibm_db.exec_immediate(conn, dr)
       dr = "DROP PROCEDURE processint"
       result = ibm_db.exec_immediate(conn, dr)
       dr = "DROP PROCEDURE processvar"
       result = ibm_db.exec_immediate(conn, dr)
       dr = "DROP TABLE test_stored"
       result = ibm_db.exec_immediate(conn, dr)
     except:
       pass

     try:
       cr1 = "CREATE TABLE test_stored (id INT, name VARCHAR(50), age int, cv XML)"
       result = ibm_db.exec_immediate(conn, cr1)
       in1 = "INSERT INTO test_stored values (1, 'Kellen', 24, '<example>This is an example</example>')"
       result = ibm_db.exec_immediate(conn, in1)
       st1 = "CREATE PROCEDURE processxml(OUT risorsa xml) LANGUAGE SQL BEGIN SELECT cv INTO risorsa FROM test_stored WHERE ID = 1; END"
       result = ibm_db.exec_immediate(conn, st1)

       test_xml(conn)
     except:
       cr1 = "CREATE TABLE test_stored (id INT, name VARCHAR(50), age int, cv VARCHAR(200))"
       result = ibm_db.exec_immediate(conn, cr1)
       in1 = "INSERT INTO test_stored values (1, 'Kellen', 24, '<example>This is an example</example>')"
       result = ibm_db.exec_immediate(conn, in1)

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

     test_int(conn)
     test_varchar(conn)

     ibm_db.close(conn)
   else:
     print "Connection failed."

#__END__
#__LUW_EXPECTED__
#ProcessXML:%s<example>This is an example</example>
#ProcessINT: 24
#ProcessVAR: Kel
#__ZOS_EXPECTED__
#ProcessXML:%s<example>This is an example</example>
#ProcessINT: 24
#ProcessVAR: Kel
#__SYSTEMI_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kel
#__IDS_EXPECTED__
#ProcessINT: 24
#ProcessVAR: Kel
