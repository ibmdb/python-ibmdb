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

    def test_261_FetchObjectAccess(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_261)

    def run_test_261(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info( conn )
        if (server.DBMS_NAME[0:3] == 'IDS'):
            op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
            ibm_db.set_option(conn, op, 1)

        if (server.DBMS_NAME[0:3] == 'IDS'):
            sql = "SELECT breed, TRIM(TRAILING FROM name) AS name FROM animals WHERE id = ?"
        else:
            sql = "SELECT breed, RTRIM(name) AS name FROM animals WHERE id = ?"

        if conn:
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt, (0,))

#      NOTE: This is a workaround
#      function fetch_object() to be implemented...
#      pet = ibm_db.fetch_object(stmt)
#      while (pet):
#          print "Come here, %s, my little %s!" % (pet.NAME, pet.BREED)
#          pet = ibm_db.fetch_object(stmt)

            class Pet:
                pass

            data = ibm_db.fetch_assoc(stmt)
            while ( data ):
                pet = Pet()
                pet.NAME = data['NAME']
                pet.BREED = data['BREED']
                print("Come here, %s, my little %s!" % (pet.NAME, pet.BREED))
                data = ibm_db.fetch_assoc(stmt)

            ibm_db.close(conn)

        else:
            print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Come here, Pook, my little cat!
#__ZOS_EXPECTED__
#Come here, Pook, my little cat!
#__SYSTEMI_EXPECTED__
#Come here, Pook, my little cat!
#__IDS_EXPECTED__
#Come here, Pook, my little cat!
