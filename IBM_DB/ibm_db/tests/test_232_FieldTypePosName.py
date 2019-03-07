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

    def test_232_FieldTypePosName(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_232)

    def run_test_232(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        result = ibm_db.exec_immediate(conn, "select * from sales")

        for i in range(0, ibm_db.num_fields(result) + 1):
            field_name = ibm_db.field_name(result,i)
            field_type = ibm_db.field_type(result, ibm_db.field_name(result,i))
            print(str(ibm_db.field_name(result, i)) + ":" + str(ibm_db.field_type(result, ibm_db.field_name(result, i))))

        print("-----")

        t = ibm_db.field_type(result,99)
        print(t)

        t1 = ibm_db.field_type(result, "HELMUT")
        print(t1)

#__END__
#__LUW_EXPECTED__
#SALES_DATE:date
#SALES_PERSON:string
#REGION:string
#SALES:int
#False:False
#-----
#False
#False
#__ZOS_EXPECTED__
#SALES_DATE:date
#SALES_PERSON:string
#REGION:string
#SALES:int
#False:False
#-----
#False
#False
#__SYSTEMI_EXPECTED__
#SALES_DATE:date
#SALES_PERSON:string
#REGION:string
#SALES:int
#False:False
#-----
#False
#False
#__IDS_EXPECTED__
#sales_date:date
#sales_person:string
#region:string
#sales:int
#False:False
#-----
#False
#False
