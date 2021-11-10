#
#    Licensed Materials - Property of IBM
#
#    (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import os
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):
    @unittest.skipIf((os.environ.get("CI", False)) or (sys.platform == 'zos'), "Test fails in CI")
    # Throws exception:
    # Exception: [IBM][CLI Driver] SQL30082N  Security processing failed
    # with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001
    # SQLCODE=-30082
    def test_trusted_context_pconnect(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_trusted_context_pconnect)

    def run_test_trusted_context_pconnect(self):
        sql_drop_role = "DROP ROLE role_01"
        sql_create_role = "CREATE ROLE role_01"

        sql_drop_trusted_context = "DROP TRUSTED CONTEXT ctx"

        sql_create_trusted_context = "CREATE TRUSTED CONTEXT ctx BASED UPON CONNECTION USING SYSTEM AUTHID "
        sql_create_trusted_context += config.auth_user
        sql_create_trusted_context += " ATTRIBUTES (ADDRESS '"
        sql_create_trusted_context += config.hostname
        sql_create_trusted_context += "') DEFAULT ROLE role_01 ENABLE WITH USE FOR "
        sql_create_trusted_context += config.tc_user

        sql_drop_table = "DROP TABLE trusted_table"
        sql_create_table = "CREATE TABLE trusted_table (i1 int, i2 int)"

        sql_select = "SELECT * FROM trusted_table"

        # Setting up database.
        conn = ibm_db.connect(config.database, config.user, config.password)
        if conn:
            sql_grant_permission = "GRANT INSERT ON TABLE trusted_table TO ROLE role_01"
            sql_create_trusted_context_01 = sql_create_trusted_context + " WITH AUTHENTICATION"
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_trusted_context)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_table)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_role)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_create_role)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_create_table)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_grant_permission)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_create_trusted_context_01)
            except:
                pass

            # Populate the trusted_table
            values = (\
                (10, 20),\
                (20, 40),\
            )
            sql_insert = 'INSERT INTO trusted_table (i1, i2) VALUES (?, ?)'
            stmt = ibm_db.prepare(conn, sql_insert)
            if stmt:
                for value in values:
                    result = ibm_db.execute(stmt, value)
            ibm_db.close(conn)
        else:
            print("Connection failed.")

        options = {ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT:    ibm_db.SQL_TRUE}
        tc_options = {ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: config.tc_user, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: config.tc_pass}
        dsn = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (config.database, config.hostname, config.port, config.auth_user, config.auth_pass)

        # Making trusted connection and performing normal operations.
        tc_conn = ibm_db.pconnect(dsn, "", "", options)
        if tc_conn:
            print("Trusted connection succeeded.")
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                userBefore = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                ibm_db.set_option(tc_conn, tc_options, 1)
                userAfter = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                if userBefore != userAfter:
                    print("User has been switched.")

                    # Inserting into table using trusted_user.
                    sql_insert = "INSERT INTO " + config.user + ".trusted_table (i1, i2) VALUES (?, ?)"
                    stmt = ibm_db.prepare(tc_conn, sql_insert)
                    result = ibm_db.execute(stmt, (300, 500))

                    # Updating table using trusted_user.
                    sql_update = "UPDATE " + config.user + ".trusted_table set i1 = 400 WHERE i2 = 500"
                    try:
                        stmt = ibm_db.exec_immediate(tc_conn, sql_update)
                    except:
                        print(ibm_db.stmt_errormsg())
            ibm_db.close(tc_conn)
        else:
            print("Trusted connection failed.")

        # Creating 10 Persistance connections and checking if trusted context is enabled (Cataloged connections)
        for i in range(10):
            tc_conn = ibm_db.pconnect(dsn, "", "")
            if tc_conn:
                val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
                if val:
                    userAfter = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                    if userBefore != userAfter:
                        print("Explicit Trusted Connection succeeded.")

        # Cleaning up database.
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            print("Connection succeeded.")

            try:
                result = ibm_db.exec_immediate(conn, sql_drop_trusted_context)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_table)
            except:
                pass
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_role)
            except:
                pass
            ibm_db.close(conn)
        else:
            print("Connection failed.")
#__END__
#__LUW_EXPECTED__
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  "%s" does not have the %s privilege to perform operation "UPDATE" on object "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Connection succeeded.
#__ZOS_EXPECTED__
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  "%s" does not have the %s privilege to perform operation "UPDATE" on object "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Connection succeeded.
#__SYSTEMI_EXPECTED__
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  "%s" does not have the privilege to perform operation "UPDATE" on object "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Connection succeeded.
#__IDS_EXPECTED__
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  "%s" does not have the %s privilege to perform operation "UPDATE" on object "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Explicit Trusted Connection succeeded.
#Connection succeeded.
