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

    def test_014_KeysetDrivenCursorNegativeRow(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_014)

    def run_test_014(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        serverinfo = ibm_db.server_info( conn )

        query = 'SELECT * FROM animals ORDER BY name'

        if (serverinfo.DBMS_NAME[0:3] != 'IDS'):
            stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
        else:
            stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_both( stmt )
        while ( data ):
            print ("%s : %s : %s : %s\n" % (data[0], data[1], data[2], data[3]))
            data = ibm_db.fetch_both( stmt )
        try:
            stmt = ibm_db.prepare(conn, query, {ibm_db.SQL_ATTR_CURSOR_TYPE:  ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            ibm_db.execute(stmt)
            rc = ibm_db.fetch_row(stmt, -1)
            print ("Fetch row -1: %s" % str(rc))
        except:
            print ("Requested row number must be a positive value")

        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#3 : gold fish : Bubbles          : 0.10
#4 : budgerigar : Gizmo            : 0.20
#1 : dog : Peaches          : 12.30
#0 : cat : Pook             : 3.20
#5 : goat : Rickety Ride     : 9.70
#2 : horse : Smarty           : 350.00
#6 : llama : Sweater          : 150.00
#Requested row number must be a positive value
#__ZOS_EXPECTED__
#3 : gold fish : Bubbles          : 0.10
#4 : budgerigar : Gizmo            : 0.20
#1 : dog : Peaches          : 12.30
#0 : cat : Pook             : 3.20
#5 : goat : Rickety Ride     : 9.70
#2 : horse : Smarty           : 350.00
#6 : llama : Sweater          : 150.00
#Requested row number must be a positive value
#__SYSTEMI_EXPECTED__
#3 : gold fish : Bubbles          : 0.10
#4 : budgerigar : Gizmo            : 0.20
#1 : dog : Peaches          : 12.30
#0 : cat : Pook             : 3.20
#5 : goat : Rickety Ride     : 9.70
#2 : horse : Smarty           : 350.00
#6 : llama : Sweater          : 150.00
#Requested row number must be a positive value
#__IDS_EXPECTED__
#3 : gold fish : Bubbles          : 0.10
#4 : budgerigar : Gizmo            : 0.20
#1 : dog : Peaches          : 12.30
#0 : cat : Pook             : 3.20
#5 : goat : Rickety Ride     : 9.70
#2 : horse : Smarty           : 350.00
#6 : llama : Sweater          : 150.00
#Requested row number must be a positive value
