#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2016
#

from __future__ import print_function
import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class Wrapper(str):
  def __del__(self):
    print("Wrapper(" + self + ") being deleted")

class IbmDbTestCase(unittest.TestCase):

  def test_312_CacheBoundParameters(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_312)
  
  def run_test_312(self):
    conn = ibm_db.connect(config.database, config.user, config.password)

    ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
    
    query = "INSERT INTO department (deptno, deptname, mgrno, admrdept, location) VALUES (?, ?, ?, ?, ?)"
    
    if conn:
      stmt = ibm_db.prepare(conn, query)
      params = ['STG', 'Systems & Technology', '123456', 'RSF', 'Fiji']

      print("Binding parameters")
      for i,p in enumerate(params, 1):
        ibm_db.bind_param(stmt, i, Wrapper(p))
      
      if ibm_db.execute(stmt):
        print("Executing statement")
        ibm_db.execute(stmt)

        # force the cache to be unbound
        for i,p in enumerate(params, 1):
          ibm_db.bind_param(stmt, i, p)
        
        ibm_db.rollback(conn)
      else:
        print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Binding parameters
#Executing statement
#Wrapper(STG) being deleted
#Wrapper(Systems & Technology) being deleted
#Wrapper(123456) being deleted
#Wrapper(RSF) being deleted
#Wrapper(Fiji) being deleted
#__ZOS_EXPECTED__
#Binding parameters
#Executing statement
#Wrapper(STG) being deleted
#Wrapper(Systems & Technology) being deleted
#Wrapper(123456) being deleted
#Wrapper(RSF) being deleted
#Wrapper(Fiji) being deleted
#__SYSTEMI_EXPECTED__
#Binding parameters
#Executing statement
#Wrapper(STG) being deleted
#Wrapper(Systems & Technology) being deleted
#Wrapper(123456) being deleted
#Wrapper(RSF) being deleted
#Wrapper(Fiji) being deleted
#__IDS_EXPECTED__
#Binding parameters
#Executing statement
#Wrapper(STG) being deleted
#Wrapper(Systems & Technology) being deleted
#Wrapper(123456) being deleted
#Wrapper(RSF) being deleted
#Wrapper(Fiji) being deleted
