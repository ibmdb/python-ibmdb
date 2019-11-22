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

    def test_241_FieldWidthPosName_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_241)

    def run_test_241(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")
        result2 = ibm_db.exec_immediate(conn, "select * from staff")
        result3 = ibm_db.exec_immediate(conn, "select * from emp_photo")

        for i in range(0, ibm_db.num_fields(result)):
            print(str(ibm_db.field_width(result,i)))

        print("\n-----")

        for i in range(0, ibm_db.num_fields(result2)):
            print(str(ibm_db.field_width(result2,ibm_db.field_name(result2,i))))

#__END__
#__LUW_EXPECTED__
#10
#15
#15
#11
#
#-----
#6
#9
#6
#5
#6
#9
#9
#__ZOS_EXPECTED__
#10
#15
#15
#11
#
#-----
#6
#9
#6
#5
#6
#9
#9
#__SYSTEMI_EXPECTED__
#10
#15
#15
#11
#
#-----
#6
#9
#6
#5
#6
#9
#9
#__IDS_EXPECTED__
#10
#15
#15
#11
#
#-----
#6
#9
#6
#5
#6
#9
#9
#__ZOS_ODBC_EXPECTED__
#10
#15
#15
#10
#
#-----
#5
#9
#5
#5
#5
#7
#7
