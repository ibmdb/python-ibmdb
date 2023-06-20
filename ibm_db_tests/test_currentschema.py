#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2020
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import ibm_db_dbi
import config

class IbmDbTestCase(unittest.TestCase):

    def test_currentschema(self):
        self.run_default_current_schema()
        self.run_setup_schema()

    def _assert_current_schema(self, conn, schema_name):
        query = "SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1"
        try:
            stmt = ibm_db.exec_immediate(conn, query)
            res = ibm_db.fetch_tuple(stmt)
            self.assertEqual(res[0].strip(), schema_name.upper())
        except:
            self.assertIsNone(sys.exc_info()[0], "Query failed")

    def run_default_current_schema(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            self._assert_current_schema(conn, config.user)

        else:
            print ("Connection failed.")


    def run_setup_schema(self):
        conn = ibm_db_dbi.connect(
            'CURRENTSCHEMA=SYSIBM;PORT=%d;PROTOCOL=TCPIP;' % config.port,
            config.user, config.password, config.hostname, config.database
        )

        if conn:
            self.assertEqual(conn.get_current_schema(), 'SYSIBM')
            self._assert_current_schema(conn.conn_handler, 'SYSIBM')

        else:
            print ("Connection failed.")





