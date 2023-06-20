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

    def test_240_FieldWidthPosName_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_240)

    def run_test_240(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")
        result2 = ibm_db.exec_immediate(conn, "select * from staff")
        result3 = ibm_db.exec_immediate(conn, "select * from emp_photo")

        for i in range(0, ibm_db.num_fields(result)):
            print(str(i) + ":" + str(ibm_db.field_width(result,i)))

        print("\n-----")

        for i in range(0, ibm_db.num_fields(result2)):
            print(str(i) + ":" + str(ibm_db.field_width(result2,ibm_db.field_name(result2,i))))

        print("\n-----")

        for i in range(0, 3):
            print(str(i) + ":" + str(ibm_db.field_width(result3,i)) + "," + str(ibm_db.field_display_size(result3,i)))

        print("\n-----")
        print("region:%s" % ibm_db.field_type(result,'region'))

        print("5:%s" % ibm_db.field_type(result2,5))

#__END__
#__LUW_EXPECTED__
#0:10
#1:15
#2:15
#3:11
#
#-----
#0:6
#1:9
#2:6
#3:5
#4:6
#5:9
#6:9
#
#-----
#0:6,6
#1:10,10
#2:1048576,2097152
#
#-----
#region:False
#5:decimal
#__ZOS_EXPECTED__
#0:10
#1:15
#2:15
#3:11
#
#-----
#0:6
#1:9
#2:6
#3:5
#4:6
#5:9
#6:9
#
#-----
#0:6,6
#1:10,10
#2:1048576,2097152
#
#-----
#region:False
#5:decimal
#__SYSTEMI_EXPECTED__
#0:10
#1:15
#2:15
#3:11
#
#-----
#0:6
#1:9
#2:6
#3:5
#4:6
#5:9
#6:9
#
#-----
#0:6,6
#1:10,10
#2:1048576,2097152
#
#-----
#region:False
#5:decimal
#__IDS_EXPECTED__
#0:10
#1:15
#2:15
#3:11
#
#-----
#0:6
#1:9
#2:6
#3:5
#4:6
#5:9
#6:9
#
#-----
#0:6,6
#1:10,10
#2:2147483647,-2
#
#-----
#region:string
#5:decimal
#__ZOS_ODBC_EXPECTED__
#0:10
#1:15
#2:15
#3:10
#-----
#0:5
#1:9
#2:5
#3:5
#4:5
#5:7
#6:7
#-----
#0:6,6
#1:10,10
#2:1048576,2097152
#-----
#region:False
#5:decimal
