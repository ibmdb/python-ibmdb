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
    def test_trusted_context_connect(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_trusted_context_connect)

    def run_test_trusted_context_connect(self):
        # if the Db2-server cannot resolve the remote-client hostname(where testcase runs), then use config.py tc_appserver_address to give IP-address
        # and use that IP-address in the trusted-context definition, to allow operation remotely from the Db2-server.

        if ( sys.platform == 'win32'):  # on ms-windows get hostname from env to avoid importing other modules
            this_hostname = os.environ['COMPUTERNAME']
        else:
            this_hostname = os.uname()[1]  # get local non-windows hostname

        if config.tc_appserver_address:
            if config.tc_appserver_address != '':
                this_hostname = config.tc_appserver_address # in case Db2-server cannot resolve remote-client hostname
 
        
        sql_drop_role = "DROP ROLE role_01"
        sql_create_role = "CREATE ROLE role_01"

        sql_drop_trusted_context = "DROP TRUSTED CONTEXT ctx"

        sql_create_trusted_context = "CREATE TRUSTED CONTEXT ctx BASED UPON CONNECTION USING SYSTEM AUTHID "
        sql_create_trusted_context += config.auth_user
        sql_create_trusted_context += " ATTRIBUTES (ADDRESS '"
        sql_create_trusted_context += this_hostname
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

        options = {ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT: ibm_db.SQL_TRUE}
        tc_options = {
            ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: config.tc_user,
            ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: config.tc_pass
        }
        tc_all_options = {
            ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT: ibm_db.SQL_TRUE,
            ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: config.tc_user,
            ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: config.tc_pass
        }
        dsn = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (config.database, config.hostname, config.port, config.auth_user, config.auth_pass)

        # Makeing normal connection and playing with it.
        tc_conn = ibm_db.connect(dsn, "", "")
        if tc_conn:
            print("Normal connection established.")
            result = ibm_db.set_option(tc_conn, tc_options, 1)
            print(ibm_db.conn_errormsg(tc_conn))
            ibm_db.close(tc_conn)

        tc_conn = ibm_db.connect(dsn, "", "")
        if tc_conn:
            print("Normal connection established.")
            result = ibm_db.set_option(tc_conn, tc_all_options, 1)
            print(ibm_db.conn_errormsg(tc_conn))
            ibm_db.close(tc_conn)

        tc_conn = ibm_db.connect(dsn, "", "", tc_all_options)
        if tc_conn:
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                print("Trusted connection succeeded.")
                get_tc_user = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                if config.tc_user != get_tc_user:
                    print("But trusted user is not switched.")
        ibm_db.close(tc_conn)

        # Making trusted connection and performing normal operations.
        tc_conn = ibm_db.connect(dsn, "", "", options)
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

        # Making trusted connection and switching to fake user.
        tc_conn = ibm_db.connect(dsn, "", "", options)

        if tc_conn:
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                print("Trusted connection succeeded.")
                ibm_db.set_option(tc_conn, {ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: "fakeuser", ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: "fakepassword"}, 1)

                sql_update = "UPDATE " + config.user + ".trusted_table set i1 = 400 WHERE i2 = 500"
                try:
                    stmt = ibm_db.exec_immediate(tc_conn, sql_update)
                except:
                    print(ibm_db.stmt_errormsg())
            ibm_db.close(tc_conn)
        else:
            print("Connection failed.")

        # Making trusted connection and passing password first then user while switching.
        tc_conn = ibm_db.connect(dsn, "", "", options)
        tc_options_reversed = {ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: config.tc_pass, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: config.tc_user}

        if tc_conn:
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                print("Trusted connection succeeded.")
                userBefore = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                ibm_db.set_option(tc_conn, tc_options_reversed, 1)
                userAfter = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                if userBefore != userAfter:
                    print("User has been switched.")
            ibm_db.close(tc_conn)
        else:
            print("Connection failed.")

        # Making trusted connection and passing password first then user while switching.
        tc_conn = ibm_db.connect(dsn, "", "", options)
        tc_user_options = {ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID: config.tc_user}
        tc_pass_options = {ibm_db.SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: config.tc_pass}

        if tc_conn:
            print("Trusted connection succeeded.")
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                userBefore = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                try:
                    ibm_db.set_option(tc_conn, tc_pass_options, 1)
                except:
                    print(ibm_db.conn_errormsg(tc_conn))
            ibm_db.close(tc_conn)
        else:
            print("Connection failed.")


        # Making trusted connection and passing only user while switching when both user and password are required.
        tc_conn = ibm_db.connect(dsn, "", "", options)

        if tc_conn:
            print("Trusted connection succeeded.")
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                ibm_db.set_option(tc_conn, tc_user_options, 1)

                sql_update = "UPDATE " + config.user + ".trusted_table set i1 = 400 WHERE i2 = 500"
                try:
                    stmt = ibm_db.exec_immediate(tc_conn, sql_update)
                except:
                    print(ibm_db.stmt_errormsg())
            ibm_db.close(tc_conn)
        else:
            print("Connection failed.")


        # Make a connection
        conn = ibm_db.connect(config.database, config.user, config.password)

        if conn:
            # Dropping the trusted context, in case it exists
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_trusted_context)
            except:
                pass

            # Dropping Role.
            try:
                result = ibm_db.exec_immediate(conn, sql_drop_role)
            except:
                pass

            # Creating Role.
            try:
                result = ibm_db.exec_immediate(conn, sql_create_role)
            except:
                pass

            # Granting permissions to role.
            try:
                sql_grant_permission = "GRANT UPDATE ON TABLE trusted_table TO ROLE role_01"
                result = ibm_db.exec_immediate(conn, sql_grant_permission)
            except:
                pass

            # Creating trusted context
            try:
                sql_create_trusted_context_01 = sql_create_trusted_context + " WITHOUT AUTHENTICATION"
                result = ibm_db.exec_immediate(conn, sql_create_trusted_context_01)
            except:
                pass

            # Closing connection
            ibm_db.close(conn)
        else:
            print("Connection failed.")

        # Making trusted connection
        tc_conn = ibm_db.connect(dsn, "", "", options)
        if tc_conn:
            print("Trusted connection succeeded.")
            val = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_USE_TRUSTED_CONTEXT, 1)
            if val:
                userBefore = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                ibm_db.set_option(tc_conn, tc_user_options, 1)
                userAfter = ibm_db.get_option(tc_conn, ibm_db.SQL_ATTR_TRUSTED_CONTEXT_USERID, 1)
                if userBefore != userAfter:
                    print("User has been switched.")

                    # Inserting into table using trusted_user.
                    sql_insert = "INSERT INTO " + config.user + ".trusted_table (i1, i2) VALUES (300, 500)"
                    try:
                        stmt = ibm_db.exec_immediate(tc_conn, sql_insert)
                    except:
                        print(ibm_db.stmt_errormsg())

                    # Updating table using trusted_user.
                    sql_update = "UPDATE " + config.user + ".trusted_table set i1 = 400 WHERE i2 = 20"
                    stmt = ibm_db.exec_immediate(tc_conn, sql_update)
            ibm_db.close(tc_conn)
        else:
            print("Connection failed.")

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
#Normal connection established.
#[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Normal connection established.[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Trusted connection succeeded.
#But trusted user is not switched.
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "UPDATE". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Trusted connection succeeded.
#[%s][%s][%s] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#Trusted connection succeeded.
#User has been switched.
#Trusted connection succeeded.
#Trusted connection succeeded.
#[%s][%s][%s] SQL20361N  The switch user request using authorization ID "%s" within trusted context "CTX" failed with reason code "2".  SQLSTATE=42517 SQLCODE=-20361
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "INSERT". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Connection succeeded.
#__ZOS_EXPECTED__
#Normal connection established.
#[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Normal connection established.[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Trusted connection succeeded.
#But trusted user is not switched.
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "UPDATE". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Trusted connection succeeded.
#[%s][%s][%s] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#Trusted connection succeeded.
#User has been switched.
#Trusted connection succeeded.
#Trusted connection succeeded.
#[%s][%s][%s] SQL20361N  The switch user request using authorization ID "%s" within trusted context "CTX" failed with reason code "2".  SQLSTATE=42517 SQLCODE=-20361
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "INSERT". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Connection succeeded.
#__SYSTEMI_EXPECTED__
#Normal connection established.
#[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Normal connection established.[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Trusted connection succeeded.
#But trusted user is not switched.
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "UPDATE". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Trusted connection succeeded.
#[%s][%s][%s] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#Trusted connection succeeded.
#User has been switched.
#Trusted connection succeeded.
#Trusted connection succeeded.
#[%s][%s][%s] SQL20361N  The switch user request using authorization ID "%s" within trusted context "CTX" failed with reason code "2".  SQLSTATE=42517 SQLCODE=-20361
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "INSERT". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Connection succeeded.
#__IDS_EXPECTED__
#Normal connection established.
#[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Normal connection established.[%s][%s] CLI0197E  A trusted context is not enabled on this connection. Invalid attribute value. SQLSTATE=HY010 SQLCODE=-99999
#Trusted connection succeeded.
#But trusted user is not switched.
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "UPDATE". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Trusted connection succeeded.
#[%s][%s][%s] SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID").  SQLSTATE=08001 SQLCODE=-30082
#Trusted connection succeeded.
#User has been switched.
#Trusted connection succeeded.
#Trusted connection succeeded.
#[%s][%s][%s] SQL20361N  The switch user request using authorization ID "%s" within trusted context "CTX" failed with reason code "2".  SQLSTATE=42517 SQLCODE=-20361
#Trusted connection succeeded.
#User has been switched.
#[%s][%s][%s] SQL0551N  The statement failed because the authorization ID does not have the required authorization or privilege to perform the operation.  Authorization ID: "%s".  Operation: "INSERT". Object: "%s.TRUSTED_TABLE".  SQLSTATE=42501 SQLCODE=-551
#Connection succeeded.
