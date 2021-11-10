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

    def test_053_AttrThruConn(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_053)

    def run_test_053(self):
        print("Client attributes passed through conection string:")

        options1 = {ibm_db.SQL_ATTR_INFO_USERID: 'db2inst1'}
        conn1 = ibm_db.connect(config.database, config.user, config.password, options1)
        val = ibm_db.get_option(conn1, ibm_db.SQL_ATTR_INFO_USERID, 1)
        print(val)
        ibm_db.close(conn1)

        options2 = {ibm_db.SQL_ATTR_INFO_ACCTSTR: 'account'}
        conn2 = ibm_db.connect(config.database, config.user, config.password, options2)
        val = ibm_db.get_option(conn2, ibm_db.SQL_ATTR_INFO_ACCTSTR, 1)
        print(val)
        ibm_db.close(conn2)

        options3 = {ibm_db.SQL_ATTR_INFO_APPLNAME: 'myapp'}
        conn3 = ibm_db.connect(config.database, config.user, config.password, options3)
        val = ibm_db.get_option(conn3, ibm_db.SQL_ATTR_INFO_APPLNAME, 1)
        print(val)
        ibm_db.close(conn3)

        options4 = {ibm_db.SQL_ATTR_INFO_WRKSTNNAME: 'workstation'}
        conn4 = ibm_db.connect(config.database, config.user, config.password, options4)
        val = ibm_db.get_option(conn4, ibm_db.SQL_ATTR_INFO_WRKSTNNAME, 1)
        print(val)
        ibm_db.close(conn4)

        options5 = {ibm_db.SQL_ATTR_INFO_USERID: 'kfb',
                    ibm_db.SQL_ATTR_INFO_WRKSTNNAME: 'kfbwork',
                    ibm_db.SQL_ATTR_INFO_ACCTSTR: 'kfbacc',
                    ibm_db.SQL_ATTR_INFO_APPLNAME: 'kfbapp'}
        conn5 = ibm_db.connect(config.database, config.user, config.password, options5)
        val = ibm_db.get_option(conn5, ibm_db.SQL_ATTR_INFO_USERID, 1)
        print(val)
        val = ibm_db.get_option(conn5, ibm_db.SQL_ATTR_INFO_ACCTSTR, 1)
        print(val)
        val = ibm_db.get_option(conn5, ibm_db.SQL_ATTR_INFO_APPLNAME, 1)
        print(val)
        val = ibm_db.get_option(conn5, ibm_db.SQL_ATTR_INFO_WRKSTNNAME, 1)
        print(val)
        ibm_db.close(conn5)

        print("Client attributes passed post-conection:")

        options5 = {ibm_db.SQL_ATTR_INFO_USERID: 'db2inst1'}
        conn5 = ibm_db.connect(config.database, config.user, config.password)
        rc = ibm_db.set_option(conn5, options5, 1)
        val = ibm_db.get_option(conn5, ibm_db.SQL_ATTR_INFO_USERID, 1)
        print(val)
        ibm_db.close(conn5)

        options6 = {ibm_db.SQL_ATTR_INFO_ACCTSTR: 'account'}
        conn6 = ibm_db.connect(config.database, config.user, config.password)
        rc = ibm_db.set_option(conn6, options6, 1)
        val = ibm_db.get_option(conn6, ibm_db.SQL_ATTR_INFO_ACCTSTR, 1)
        print(val)
        ibm_db.close(conn6)

        options7 = {ibm_db.SQL_ATTR_INFO_APPLNAME: 'myapp'}
        conn7 = ibm_db.connect(config.database, config.user, config.password)
        rc = ibm_db.set_option(conn7, options7, 1)
        val = ibm_db.get_option(conn7, ibm_db.SQL_ATTR_INFO_APPLNAME, 1)
        print(val)
        ibm_db.close(conn7)

        options8 = {ibm_db.SQL_ATTR_INFO_WRKSTNNAME: 'workstation'}
        conn8 = ibm_db.connect(config.database, config.user, config.password)
        rc = ibm_db.set_option(conn8, options8, 1)
        val = ibm_db.get_option(conn8, ibm_db.SQL_ATTR_INFO_WRKSTNNAME, 1)
        print(val)
        ibm_db.close(conn8)

#__END__
#__LUW_EXPECTED__
#Client attributes passed through conection string:
#db2inst1
#account
#myapp
#workstation
#kfb
#kfbacc
#kfbapp
#kfbwork
#Client attributes passed post-conection:
#db2inst1
#account
#myapp
#workstation
#__ZOS_EXPECTED__
#Client attributes passed through conection string:
#db2inst1
#account
#myapp
#workstation
#kfb
#kfbacc
#kfbapp
#kfbwork
#Client attributes passed post-conection:
#db2inst1
#account
#myapp
#workstation
#__SYSTEMI_EXPECTED__
#Client attributes passed through conection string:
#db2inst1
#account
#myapp
#workstation
#kfb
#kfbacc
#kfbapp
#kfbwork
#Client attributes passed post-conection:
#db2inst1
#account
#myapp
#workstation
#__IDS_EXPECTED__
#Client attributes passed through conection string:
#db2inst1
#account
#myapp
#workstation
#kfb
#kfbacc
#kfbapp
#kfbwork
#Client attributes passed post-conection:
#db2inst1
#account
#myapp
#workstation
#__ZOS_ODBC_EXPECTED__
#Client attributes passed through conection string:
#Client attributes passed post-conection:
#db2inst1
#account
#myapp
#workstation
