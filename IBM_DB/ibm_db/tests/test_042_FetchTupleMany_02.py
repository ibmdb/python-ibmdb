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

    def test_042_FetchTupleMany_02(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_042)

    def run_test_042(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        #if ({}['EMPNO'] != None):
        #  result = ibm_db.exec_immediate(conn, "select photo_format, picture, length(picture) from emp_photo where photo_format='jpg' and empno='" + {}['EMPNO'] + "'")
        #  row = ibm_db.fetch_array(result)
        #  if row:
        #    # We'll be outputting a
        #    header('Content-type: image/' + row[0])
        #    header('Content-Length: ' + row[2])
        #    print row[1]
        #  else:
        #    print ibm_db.error()
        #  continue
        #else:
        result = ibm_db.exec_immediate(conn, "select EMPNO, PHOTO_FORMAT from emp_photo where photo_format='jpg'")
        row = ibm_db.fetch_tuple(result)
        while ( row ):
            print("<a href='test_042.php?EMPNO=%s' target=_blank>%s (%s)</a><br>" % (row[0], row[0], row[1]))
            row = ibm_db.fetch_tuple(result)

#__END__
#__LUW_EXPECTED__
#<a href='test_042.php?EMPNO=000130' target=_blank>000130 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000140' target=_blank>000140 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000150' target=_blank>000150 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000190' target=_blank>000190 (jpg)</a><br>
#__ZOS_EXPECTED__
#<a href='test_042.php?EMPNO=000130' target=_blank>000130 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000140' target=_blank>000140 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000150' target=_blank>000150 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000190' target=_blank>000190 (jpg)</a><br>
#__SYSTEMI_EXPECTED__
#<a href='test_042.php?EMPNO=000130' target=_blank>000130 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000140' target=_blank>000140 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000150' target=_blank>000150 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000190' target=_blank>000190 (jpg)</a><br>
#__IDS_EXPECTED__
#<a href='test_042.php?EMPNO=000130' target=_blank>000130 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000140' target=_blank>000140 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000150' target=_blank>000150 (jpg)</a><br>
#<a href='test_042.php?EMPNO=000190' target=_blank>000190 (jpg)</a><br>
