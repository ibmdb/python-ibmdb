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

  def test_061_Tables_02(self):
    obj = IbmDbTestFunctions()
    obj.assert_expectf(self.run_test_061)

  def run_test_061(self):
    conn = ibm_db.connect(config.database, config.user, config.password)

    create = 'CREATE SCHEMA AUTHORIZATION t'
    try:
      result = ibm_db.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t1( c1 integer, c2 varchar(40))'
    try:
      result = ibm_db.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t2( c1 integer, c2 varchar(40))'
    try:
      result = ibm_db.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t3( c1 integer, c2 varchar(40))'
    try:
      result = ibm_db.exec_immediate(conn, create) 
    except:
      pass
      
    create = 'CREATE TABLE t.t4( c1 integer, c2 varchar(40))'
    try:
      result = ibm_db.exec_immediate(conn, create) 
    except:
      pass
    
    if conn:
      server = ibm_db.server_info( conn )
      if (server.DBMS_NAME[0:3] == 'IDS'):
        op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
        ibm_db.set_option(conn, op, 0)

      result = ibm_db.tables(conn, None, 'T');    
      i = 0
      row = ibm_db.fetch_both(result)
      while ( row ):
        str = row['TABLE_SCHEM'] + row['TABLE_NAME'] + row['TABLE_TYPE']
        if (i < 4):
          print str
        i = i + 1
	row = ibm_db.fetch_both(result)

      ibm_db.exec_immediate(conn, 'DROP TABLE t.t1')
      ibm_db.exec_immediate(conn, 'DROP TABLE t.t2')
      ibm_db.exec_immediate(conn, 'DROP TABLE t.t3')
      ibm_db.exec_immediate(conn, 'DROP TABLE t.t4')

      print "done!"
    else:
      print "no connection: %s" % ibm_db.conn_errormsg()

#__END__
#__LUW_EXPECTED__
#TT1TABLE
#TT2TABLE
#TT3TABLE
#TT4TABLE
#done!
#__ZOS_EXPECTED__
#TT1TABLE
#TT2TABLE
#TT3TABLE
#TT4TABLE
#done!
#__SYSTEMI_EXPECTED__
#TT1TABLE
#TT2TABLE
#TT3TABLE
#TT4TABLE
#done!
#__IDS_EXPECTED__
#T%st1TABLE%s
#T%st2TABLE%s
#T%st3TABLE%s
#T%st4TABLE%s
#done!
