#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2013
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

def strip_bom(s):
    return s[1:] if (s and s[0] in (u'\ufeff', u'\uffef')) else s

class IbmDbTestCase(unittest.TestCase):

    def test_265_NoAffectedRows(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_265)

    def run_test_265(self):
        # Make a connection
        conn = ibm_db.connect(config.database, config.user, config.password)

        cursor_option = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC}

        if conn:
            server = ibm_db.server_info( conn )
            if (server.DBMS_NAME[0:3] == 'IDS'):
                op = {ibm_db.ATTR_CASE: ibm_db.CASE_UPPER}
                ibm_db.set_option(conn, op, 1)

            try:
                sql = 'drop table test'

                stmt = ibm_db.prepare(conn, sql)
                if sys.platform != 'zos':
                    ibm_db.set_option(stmt, cursor_option, 0)
                ibm_db.execute(stmt)
            except:
                pass

            if ((server.DBMS_NAME[0:3] == 'IDS') or (server.DBMS_NAME[0:2] == "AS")):
                sql = "create table test(id integer, name VARCHAR(10), clob_col CLOB, some_var VARCHAR(100) )"
            else:
                sql = "create table test(id integer, name VARCHAR(10), clob_col CLOB, some_var XML )"

            stmt = ibm_db.prepare(conn, sql)
            if sys.platform != 'zos':
                ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))

            sql = 'select id from test'

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))

            sql = "insert into test values( 1, 'some', 'here is a clob value', '<?xml version=\"1.0\" encoding=\"UTF-8\" ?><test attribute=\"value\"/>')"

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))

            sql = "insert into test values(2, 'value', 'clob data', NULL)"

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))

            sql = "insert into test values(2, 'in varchar', 'data2', NULL)"

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))

            sql = 'select * from test'

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))
            row = ibm_db.fetch_tuple(stmt)
            while ( row ):
                print("%s, %s, %s, %s\n" %(row[0], row[1], row[2], strip_bom(row[3])))
                row = ibm_db.fetch_tuple(stmt)

            sql = 'select id, name from test where id = ?'

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            ibm_db.execute(stmt, (2,))
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))
            row = ibm_db.fetch_tuple(stmt)
            while ( row ):
                print("%s, %s\n" %(row[0], row[1]))
                row = ibm_db.fetch_tuple(stmt)

            if (server.DBMS_NAME[0:3] == 'IDS'):
                sql = "select * from test"
            else:
                sql = 'select * from test fetch first 12 rows only optimize for 12 rows'

            stmt = ibm_db.prepare(conn, sql)
            ibm_db.set_option(stmt, cursor_option, 0)
            #ibm_db.num_fields(stmt)
            ibm_db.execute(stmt)
            print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))
            row = ibm_db.fetch_tuple(stmt)
            while ( row ):
                print("%s, %s, %s, %s\n" % (row[0], row[1], row[2], strip_bom(row[3])))
                row = ibm_db.fetch_tuple(stmt)

            try:
                sql = 'drop table test'

                stmt = ibm_db.prepare(conn, sql)
                ibm_db.set_option(stmt, cursor_option, 0)
                ibm_db.execute(stmt)
                print("Number of affected rows: %d" % ibm_db.get_num_result(stmt))
            except:
                pass

            ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#Number of affected rows: -1
#Number of affected rows: 0
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: -1
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: -1
#__ZOS_EXPECTED__
#Number of affected rows: -1
#Number of affected rows: 0
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: -1
#__SYSTEMI_EXPECTED__
#Number of affected rows: -2
#Number of affected rows: 0
#Number of affected rows: -2
#Number of affected rows: -1
#Number of affected rows: -2
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: -2
#__IDS_EXPECTED__
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: -1
