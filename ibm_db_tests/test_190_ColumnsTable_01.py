#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#
# NOTE: IDS requires that you pass the schema name (cannot pass None)

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_190_ColumnsTable_01(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_190)

    def run_test_190(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if conn:
            if (server.DBMS_NAME[0:3] == 'IDS'):
                result = ibm_db.columns(conn,None,config.user,"employee")
            else:
                result = ibm_db.columns(conn,None,(config.user).upper(),"EMPLOYEE")

            row = ibm_db.fetch_tuple(result)
            while ( row ):
                str = row[1] + "/" + row[3]
                print(str)
                row = ibm_db.fetch_tuple(result)
            print("done!")
        else:
            print("no connection:", ibm_db.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__ZOS_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__SYSTEMI_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__IDS_EXPECTED__
#%s/empno
#%s/firstnme
#%s/midinit
#%s/lastname
#%s/workdept
#%s/phoneno
#%s/hiredate
#%s/job
#%s/edlevel
#%s/sex
#%s/birthdate
#%s/salary
#%s/bonus
#%s/comm
#done!
