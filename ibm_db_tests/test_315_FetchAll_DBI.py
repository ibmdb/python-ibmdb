#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_315_FetchAll_DBI(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_315)

    def run_test_315(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)

        # Drop the test table, in case it exists
        drop = 'DROP TABLE varigraph'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass

        # Create the test table
        create = 'CREATE TABLE varigraph( i INT, g VARGRAPHIC(10000))'
        result = ibm_db.exec_immediate(conn, create)

        vargraphic_string = "a" * 8192

        insert_sql = "INSERT INTO varigraph (i, g) VALUES (?, ?)"
        stmt = ibm_db.prepare(conn, insert_sql)

        ibm_db.bind_param(stmt, 1, 0)
        ibm_db.bind_param(stmt, 2, 'hogehoge')
        ibm_db.execute(stmt)

        ibm_db.bind_param(stmt, 1, 1)
        ibm_db.bind_param(stmt, 2, vargraphic_string)
        ibm_db.execute(stmt)

        db2_conn = ibm_db_dbi.Connection(conn)
        db2_cur = db2_conn.cursor()

        sql = "SELECT i, length(g||g) FROM varigraph"

        try:
            db2_conn.cursor()
            db2_cur.execute(sql)
            for (i, len) in db2_cur.fetchall():
                print("i: {} , len: {} ".format(i, len))
        except:
            err = ibm_db.stmt_errormsg()
            print(err)

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver][DB2/LINUXX8664] SQL0137N  The length resulting from "CONCAT" is greater than "0000016350 ".  SQLSTATE=54006  SQLCODE=-137
#__ZOS_EXPECTED__
#[IBM][CLI Driver][DB2/LINUXX8664] SQL0137N  The length resulting from "CONCAT" is greater than "0000016350 ".  SQLSTATE=54006  SQLCODE=-137
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver][AS] SQL0137N  The length resulting from "CONCAT" is greater than "0000016350 ".  SQLSTATE=54006  SQLCODE=-137
#__IDS_EXPECTED__
#[IBM][CLI Driver][IDS/LINUXX8664] SQL0137N  The length resulting from "CONCAT" is greater than "0000016350 ".  SQLSTATE=54006  SQLCODE=-137
