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

  def test_133_ExecuteLongInputParams(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_133)

  def run_test_133(self):
    conn = ibm_db.connect(config.database, config.user, config.password)

    if (not conn):
      print "Connection failed."
      return 0

    ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

    print "Starting test ..."
    res = ''
    sql =  "INSERT INTO animals (id, breed, name, weight) VALUES (?, ?, ?, ?)"
    try:
      stmt = ibm_db.prepare(conn, sql)
      res = ibm_db.execute(stmt,(128, 'hacker of human and technological nature', 'Wez the ruler of all things PECL', 88.3))
      
      stmt = ibm_db.prepare(conn, "SELECT breed, name FROM animals WHERE id = ?")
      res = ibm_db.execute(stmt, (128,))
      row = ibm_db.fetch_assoc(stmt)
      
      for i in row:
	         print i

      ibm_db.rollback(conn)
      print "Done"
    except:
      print "SQLSTATE: %s" % ibm_db.stmt_error(stmt)
      print "Message: %s" % ibm_db.stmt_errormsg(stmt)

    try:
        stmt = ibm_db.prepare(conn, "SELECT breed, name FROM animals WHERE id = ?")
        res = ibm_db.execute(stmt, (128,))
        row = ibm_db.fetch_assoc(stmt)
        if (row):
            for i in row:
                print i
        print res
        print "SQLSTATE: %s" % ibm_db.stmt_error(stmt)
        print "Message: %s" % ibm_db.stmt_errormsg(stmt)
    except:
        print "An Exception is not expected"
        print "SQLSTATE: %s" % ibm_db.stmt_error(stmt)
        print "Message: %s" % ibm_db.stmt_errormsg(stmt)

    ibm_db.rollback(conn)
    print "Done"

#__END__
#__LUW_EXPECTED__
#Starting test ...
#None
#SQLSTATE: 22001
#Message: [IBM][CLI Driver] CLI0109E  String data right truncation. SQLSTATE=22001 SQLCODE=-99999
#True
#SQLSTATE: 02000
#Message: [IBM][CLI Driver][DB2%s] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000
#Done
#__ZOS_EXPECTED__
#Starting test ...
#
#SQLSTATE: 22001
#Message: [IBM][CLI Driver] CLI0109E  String data right truncation. SQLSTATE=22001 SQLCODE=-99999
#True
#SQLSTATE: 02000
#Message: [IBM][CLI Driver][DB2] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000 SQLCODE=100
#Done
#__SYSTEMI_EXPECTED__
#Starting test ...
#
#SQLSTATE: 22001
#Message: [IBM][CLI Driver] CLI0109E  String data right truncation. SQLSTATE=22001 SQLCODE=-99999
#True
#SQLSTATE: 02000
#Message: [IBM][CLI Driver][AS] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000 SQLCODE=100
#Done
#__IDS_EXPECTED__
#Starting test ...
#None
#SQLSTATE: 22001
#Message: [IBM][CLI Driver][IDS%s] Value exceeds string column length.
#True
#SQLSTATE: 02000
#Message: [IBM][CLI Driver][IDS%s] SQL0100W  No row was found for FETCH, UPDATE or DELETE; or the result of a query is an empty table.  SQLSTATE=02000
#Done