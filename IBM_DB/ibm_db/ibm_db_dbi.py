# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2007-2013                                  |
# +--------------------------------------------------------------------------+
# | This module complies with SQLAlchemy and is                              |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Swetha Patel, Abhigyan Agrawal, Tarun Pasrija,                  |
# | Rahul Priyadarshi, Kevin Adler                                           |
# +--------------------------------------------------------------------------+

"""
This module implements the Python DB API Specification v2.0 for DB2 database.
"""

import types, string, time, datetime, decimal, sys
import weakref
import platform
import six
from warnings import warn

if sys.version_info >= (3, ):
   buffer = memoryview

if sys.version_info < (3, ):
   import exceptions
   exception = exceptions.StandardError
else:
   exception = Exception
   
import ibm_db
__version__ = ibm_db.__version__

# Constants for specifying database connection options.
SQL_ATTR_AUTOCOMMIT = ibm_db.SQL_ATTR_AUTOCOMMIT
SQL_ATTR_CURRENT_SCHEMA = ibm_db.SQL_ATTR_CURRENT_SCHEMA
SQL_AUTOCOMMIT_OFF = ibm_db.SQL_AUTOCOMMIT_OFF
SQL_AUTOCOMMIT_ON = ibm_db.SQL_AUTOCOMMIT_ON
ATTR_CASE = ibm_db.ATTR_CASE
CASE_NATURAL = ibm_db.CASE_NATURAL
CASE_LOWER = ibm_db.CASE_LOWER
CASE_UPPER = ibm_db.CASE_UPPER
SQL_FALSE = ibm_db.SQL_FALSE
SQL_TRUE = ibm_db.SQL_TRUE
SQL_TABLE_STAT = ibm_db.SQL_TABLE_STAT
SQL_INDEX_CLUSTERED = ibm_db.SQL_INDEX_CLUSTERED
SQL_INDEX_OTHER = ibm_db.SQL_INDEX_OTHER
SQL_DBMS_VER = ibm_db.SQL_DBMS_VER
SQL_DBMS_NAME = ibm_db.SQL_DBMS_NAME

# Module globals
apilevel = '2.0'
threadsafety = 0
paramstyle = 'qmark'

def _is_ibmi():
    """Returns whether we're running on IBM i platform or not.
    Useful, since IBM i uses native CLI and not DB2 Connect, which
    has slightly different features"""
    return platform.system() == 'OS400'


class Error(exception):
    """This is the base class of all other exception thrown by this
    module.  It can be use to catch all exceptions with a single except
    statement.
    
    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        self._message = message
    def __str__(self):
        """Converts the message to a string."""
        return 'ibm_db_dbi::'+str(self.__class__.__name__)+': '+str(self._message)


class Warning(exception):
    """This exception is used to inform the user about important 
    warnings such as data truncations.

    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        self._message = message
    def __str__(self):
        """Converts the message to a string."""
        return 'ibm_db_dbi::'+str(self.__class__.__name__)+': '+str(self._message)


class InterfaceError(Error):
    """This exception is raised when the module interface is being
    used incorrectly.

    """
    pass


class DatabaseError(Error):
    """This exception is raised for errors related to database."""
    pass


class InternalError(DatabaseError):
    """This exception is raised when internal database error occurs,
    such as cursor is not valid anymore.

    """
    pass


class OperationalError(DatabaseError):
    """This exception is raised when database operation errors that are
    not under the programmer control occur, such as unexpected
    disconnect.

    """ 
    pass


class ProgrammingError(DatabaseError):
    """This exception is raised for programming errors, such as table 
    not found.

    """
    pass

class IntegrityError(DatabaseError):
    """This exception is thrown when errors occur when the relational
    integrity of database fails, such as foreign key check fails. 

    """
    pass


class DataError(DatabaseError):
    """This exception is raised when errors due to data processing,
    occur, such as divide by zero. 

    """
    pass


class NotSupportedError(DatabaseError):
    """This exception is thrown when a method in this module or an 
    database API is not supported.

    """
    pass


def Date(year, month, day):
    """This method can be used to get date object from integers, for 
    inserting it into a DATE column in the database.

    """
    return datetime.date(year, month, day)

def Time(hour, minute, second):
    """This method can be used to get time object from integers, for 
    inserting it into a TIME column in the database.

    """
    return datetime.time(hour, minute, second)

def Timestamp(year, month, day, hour, minute, second):
    """This method can be used to get timestamp object from integers, 
    for inserting it into a TIMESTAMP column in the database.

    """
    return datetime.datetime(year, month, day, hour, minute, second)

def DateFromTicks(ticks):
    """This method can be used to get date object from ticks seconds,
    for inserting it into a DATE column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.date(time_tuple[0], time_tuple[1], time_tuple[2])

def TimeFromTicks(ticks):
    """This method can be used to get time object from ticks seconds,
    for inserting it into a TIME column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.time(time_tuple[3], time_tuple[4], time_tuple[5])

def TimestampFromTicks(ticks):
    """This method can be used to get timestamp object from ticks  
    seconds, for inserting it into a TIMESTAMP column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2], 
                                time_tuple[3], time_tuple[4], time_tuple[5])

def Binary(string):
    """This method can be used to store binary information, for 
    inserting it into a binary type column in the database.

    """
    if not isinstance( string, (str, buffer) ):
        raise InterfaceError("Binary function expects type string argument.")
    return buffer(string)


class DBAPITypeObject(frozenset):
    """Class used for creating objects that can be used to compare
    in order to determine the python type to provide in parameter 
    sequence argument of the execute method.

    """
    def __new__(cls, col_types):
        return frozenset.__new__(cls, col_types)
        
    def __init__(self, col_types):
        """Constructor for DBAPITypeObject.  It takes a tuple of 
        database column type as an argument.
        """
        self.col_types = col_types

    def __cmp__(self, cmp):
        """This method checks if the string compared with is in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        if cmp in self.col_types:
            return 0
        elif cmp < self.col_types:
            return 1
        else:
            return -1
            
    def __eq__(self, cmp):
        """This method checks if the string compared with is in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        return cmp in self.col_types
           
    def __ne__(self, cmp):
        """This method checks if the string compared with is not in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        return cmp not in self.col_types
        
    def __hash__(self):
        return id(self)

# The user can use these objects to compare the database column types
# with in order to determine the python type to provide in the 
# parameter sequence argument of the execute method.
STRING = DBAPITypeObject(("CHARACTER", "CHAR", "VARCHAR", 
                          "CHARACTER VARYING", "CHAR VARYING", "STRING",))

TEXT = DBAPITypeObject(("CLOB", "DBCLOB", "CHARACTER LARGE OBJECT", "CHAR LARGE OBJECT",))

XML = DBAPITypeObject(("XML",))

BINARY = DBAPITypeObject(("BLOB", "BINARY LARGE OBJECT",))

NUMBER = DBAPITypeObject(("INTEGER", "INT", "SMALLINT",))

BIGINT = DBAPITypeObject(("BIGINT",))

FLOAT = DBAPITypeObject(("FLOAT", "REAL", "DOUBLE", "DECFLOAT"))

DECIMAL = DBAPITypeObject(("DECIMAL", "DEC", "NUMERIC", "NUM",))

DATE = DBAPITypeObject(("DATE",))

TIME = DBAPITypeObject(("TIME",))

DATETIME = DBAPITypeObject(("TIMESTAMP",))

ROWID = DBAPITypeObject(())

# This method is used to determine the type of error that was 
# generated.  It takes an exception instance as an argument, and 
# returns exception object of the appropriate type.
def _get_exception(inst):
    # These tuple are used to determine the type of exceptions that are
    # thrown by the database.  They store the SQLSTATE code and the
    # SQLSTATE class code(the 2 digit prefix of the SQLSTATE code)  
    warning_error_tuple = ('01', )
    data_error_tuple = ('02', '22', '10601', '10603', '10605', '10901', '10902', 
                                                               '38552', '54')

    operational_error_tuple = ( '08', '09', '10502', '10000', '10611', '38501', 
                          '38503', '38553', '38H01', '38H02', '38H03', '38H04',
                                   '38H05', '38H06', '38H07', '38H09', '38H0A')

    integrity_error_tuple = ('23', )

    internal_error_tuple = ('24', '25', '26', '2D', '51', '57')

    programming_error_tuple = ('08002', '07', 'OD', 'OF','OK','ON','10', '27',
                               '28', '2E', '34', '36', '38', '39', '56', '42',
                               '3B', '40', '44', '53', '55', '58', '5U', '21')

    not_supported_error_tuple = ('0A', '10509')

    # These tuple are used to determine the type of exceptions that are
    # thrown from the driver module. 
    interface_exceptions = (                  "Supplied parameter is invalid",
                                        "ATTR_CASE attribute must be one of "
                                    "CASE_LOWER, CASE_UPPER, or CASE_NATURAL",
                          "Connection or statement handle must be passed in.",
                                                       "Param is not a tuple")

    programming_exceptions = (                     "Connection is not active", 
                                                 "qualifier must be a string",
                                                   "unique must be a boolean",
                                                       "Parameters not bound",
                                                     "owner must be a string",
                                                "table_name must be a string",
                                                "table type must be a string", 
                                               "column_name must be a string", 
                                                "Column ordinal out of range", 
                                            "procedure name must be a string",
                              "Requested row number must be a positive value", 
                                     "Options Array must have string indexes")

    database_exceptions = (                                   "Binding Error", 
                                   "Column information cannot be retrieved: ", 
                                            "Column binding cannot be done: ",
                                             "Failed to Determine XML Size: ")

    statement_exceptions = (                     "Statement Execute Failed: ",
                                                    "Describe Param Failed: ",
                                                      "Sending data failed: ",
                                                            "Fetch Failure: ",
                                                  "SQLNumResultCols failed: ",
                                                       "SQLRowCount failed: ",
                                                   "SQLGetDiagField failed: ",
                                                 "Statement prepare Failed: ")

    operational_exceptions = (          "Connection Resource cannot be found", 
                                                  "Failed to Allocate Memory",
                                                    "Describe Param Failed: ",
                                                 "Statement Execute Failed: ",
                                                      "Sending data failed: ", 
                                     "Failed to Allocate Memory for XML Data",
                                     "Failed to Allocate Memory for LOB Data")

    # First check if the exception is from the database.  If it is 
    # determine the SQLSTATE code which is used further to determine 
    # the exception type.  If not check if the exception is thrown by 
    # by the driver and return the appropriate exception type.  If it 
    # is not possible to determine the type of exception generated 
    # return the generic Error exception.
    if inst is not None:
        message = repr(inst)
        if message.startswith("Exception('") and message.endswith("',)"):
            message = message[11:]
            message = message[:len(message)-3]

        index = message.find('SQLSTATE=')
        if( message != '') & (index != -1):
            error_code = message[(index+9):(index+14)]
            prefix_code = error_code[:2]
        else:
            for key in interface_exceptions:
                if message.find(key) != -1:
                    return InterfaceError(message)
            for key in programming_exceptions:
                if message.find(key) != -1:
                    return ProgrammingError(message)
            for key in operational_exceptions:
                if message.find(key) != -1:
                    return OperationalError(message)
            for key in database_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)  
            for key in statement_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)
            return Error(message)
    else:
        return Error('An error has occured')

    # First check if the SQLSTATE is in the tuples, if not check
    # if the SQLSTATE class code is in the tuples to determine the
    # exception type. 
    if ( error_code in warning_error_tuple or 
         prefix_code in warning_error_tuple ):
        return Warning(message)
    if ( error_code in data_error_tuple or 
         prefix_code in data_error_tuple ):
        return DataError(message)
    if ( error_code in operational_error_tuple or 
         prefix_code in operational_error_tuple ):
        return OperationalError(message)
    if ( error_code in integrity_error_tuple or 
         prefix_code in integrity_error_tuple ):
        return IntegrityError(message)
    if ( error_code in internal_error_tuple or
         prefix_code in internal_error_tuple ):
        return InternalError(message)
    if ( error_code in programming_error_tuple or
         prefix_code in programming_error_tuple ):
        return ProgrammingError(message)
    if ( error_code in not_supported_error_tuple or
         prefix_code in not_supported_error_tuple ):
        return NotSupportedError(message)
    return DatabaseError(message)

def _server_connect(dsn, user='', password='', host=''):
    """This method create connection with server
    """
    
    if dsn is None:
        raise InterfaceError("dsn value should not be None")
    
    if (not isinstance(dsn, six.string_types)) | \
       (not isinstance(user, six.string_types)) | \
       (not isinstance(password, six.string_types)) | \
       (not isinstance(host, six.string_types)):
        raise InterfaceError("Arguments should be of type string or unicode")
    
    # If the dsn does not contain port and protocal adding database
    # and hostname is no good.  Add these when required, that is,
    # if there is a '=' in the dsn.  Else the dsn string is taken to be
    # a DSN entry.
    if dsn.find('=') != -1:
        if dsn[len(dsn) - 1] != ';':
            dsn = dsn + ";"
        if host != '' and dsn.find('HOSTNAME=') == -1:
            dsn = dsn + "HOSTNAME=" + host + ";"
    else:
        dsn = "DSN=" + dsn + ";"

    if dsn.find('attach=') == -1:
        dsn = dsn + "attach=true;"
    if user != '' and dsn.find('UID=') == -1:
        dsn = dsn + "UID=" + user + ";"
    if password != '' and dsn.find('PWD=') == -1:
        dsn = dsn + "PWD=" + password + ";"
    try:    
        conn = ibm_db.connect(dsn, '', '')
    except Exception as inst:
        raise _get_exception(inst)
    
    return conn
    
def createdb(database, dsn, user='', password='', host='', codeset='', mode=''):
    """This method creates a database by using the specified database name, code set, and mode
    """
    
    if database is None:
        raise InterfaceError("createdb expects a not None database name value")
    if (not isinstance(database, six.string_types)) | \
       (not isinstance(codeset, six.string_types)) | \
       (not isinstance(mode, six.string_types)):
        raise InterfaceError("Arguments sould be string or unicode")
        
    conn = _server_connect(dsn, user=user, password=password, host=host)
    try:
        return_value = ibm_db.createdb(conn, database, codeset, mode)
    except Exception as inst:
        raise _get_exception(inst)
    finally:
        try:
            ibm_db.close(conn)
        except Exception as inst:
            raise _get_exception(inst)
        
    return return_value
    
def dropdb(database, dsn, user='', password='', host=''):
    """This method drops the specified database
    """
    
    if database is None:
        raise InterfaceError("dropdb expects a not None database name value")
    if (not isinstance(database, six.string_types)):
        raise InterfaceError("Arguments sould be string or unicode")
        
    conn = _server_connect(dsn, user=user, password=password, host=host)
    try:
        return_value = ibm_db.dropdb(conn, database)
    except Exception as inst:
        raise _get_exception(inst)
    finally:
        try:
            ibm_db.close(conn)
        except Exception as inst:
            raise _get_exception(inst)
        
    return return_value
    
def recreatedb(database, dsn, user='', password='', host='', codeset='', mode=''):
    """This method drops and then recreate the database by using the specified database name, code set, and mode
    """
    
    if database is None:
        raise InterfaceError("recreatedb expects a not None database name value")
    if (not isinstance(database, six.string_types)) | \
       (not isinstance(codeset, six.string_types)) | \
       (not isinstance(mode, six.string_types)):
        raise InterfaceError("Arguments sould be string or unicode")
        
    conn = _server_connect(dsn, user=user, password=password, host=host)
    try:
        return_value = ibm_db.recreatedb(conn, database, codeset, mode)
    except Exception as inst:
        raise _get_exception(inst)
    finally:
        try:
            ibm_db.close(conn)
        except Exception as inst:
            raise _get_exception(inst)
        
    return return_value
    
def createdbNX(database, dsn, user='', password='', host='', codeset='', mode=''):
    """This method creates a database if it not exist by using the specified database name, code set, and mode
    """
    
    if database is None:
        raise InterfaceError("createdbNX expects a not None database name value")
    if (not isinstance(database, six.string_types)) | \
       (not isinstance(codeset, six.string_types)) | \
       (not isinstance(mode, six.string_types)):
        raise InterfaceError("Arguments sould be string or unicode")
        
    conn = _server_connect(dsn, user=user, password=password, host=host)
    try:
        return_value = ibm_db.createdbNX(conn, database, codeset, mode)
    except Exception as inst:
        raise _get_exception(inst)
    finally:
        try:
            ibm_db.close(conn)
        except Exception as inst:
            raise _get_exception(inst)
        
    return return_value


def _connect_helper(conn_func, dsn, user, password, host, database, conn_options):
    if not _is_ibmi():
        if dsn is None:
            raise InterfaceError("connect expects a not None dsn value")
        
        if (not isinstance(dsn, six.string_types)) | \
           (not isinstance(user, six.string_types)) | \
           (not isinstance(password, six.string_types)) | \
           (not isinstance(host, six.string_types)) | \
           (not isinstance(database, six.string_types)):
            raise InterfaceError("connect expects the first five arguments to be of type string or unicode")
    else:
        if dsn is not None:
            if (not isinstance(dsn, six.string_types)):
                raise InterfaceError("connect expects dsn argument to be of type string or unicode")
            
            # Convert K1=V1;K2=V2;K3=V3; syntax in to tuple table like ((K1,V1), (K2,V2), (K3,V3))
            tokens = [ k.strip().split('=') for k in dsn.split(';') if not (k.isspace() or k == '') ]
            
            # Convert tuple table in to a dict like {K1:V1, K2:V2, K3:V3}
            options = dict( (k.strip().upper(), v.strip()) for k, v in tokens )
            
            allowed_keys = ('UID', 'PWD', 'DATABASE')
            required_keys = ('DATABASE', )
            
            # Make sure there's no options specified that we don't support
            for key in options:
                if key not in allowed_keys:
                    raise InterfaceError("IBM i does not support DSN keywords '%s'" % key)
            
            # Make sure they specified all options needed
            for key in required_keys:
                if not key in options:
                    raise InterfaceError("DSN keyword '%s' missing from connection string" % key)
            
            database = options['DATABASE']
            user = options.get('UID')
            password = options.get('PWD')
        else:
            if database is not None and not isinstance(database, six.string_types):
                raise InterfaceError("connect expects the database argument to be of type string or unicode")
            
            if user is not None and not isinstance(user, six.string_types):
                raise InterfaceError("connect expects the user argument to be of type string or unicode")
            
            if password is not None and not isinstance(password, six.string_types):
                raise InterfaceError("connect expects the password argument to be of type string or unicode")
            
            # IBM i doesn't support connecting to arbitrary hosts in an uncatalogued manner.
            # Just ignore, but give a warning to the user
            if host != '':
                warn("IBM i does not support host parameter, ignored", stacklevel=2)
            
        # IBM i CLI allows passing NULL as the username/password to connect as the current user,
        # but no longer supports passing in empty string for those values. Instead, we treat empty
        # string as None here. Same for database: treat empty string or None as *LOCAL.
        if user == '':
            user = None
            
        if password == '':
            password = None;
        
        if database is None or database == '':
            database = '*LOCAL'
        
    if (conn_options is not None) and (not isinstance(conn_options, dict)):
        raise InterfaceError("connect expects the sixth argument"
                             " (conn_options) to be of type dict")

    options = { SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_OFF }
    if conn_options is not None:
        options.update(conn_options)

    if not _is_ibmi():
        # If the dsn does not contain port and protocal adding database
        # and hostname is no good.  Add these when required, that is,
        # if there is a '=' in the dsn.  Else the dsn string is taken to be
        # a DSN entry.
        if dsn.find('=') != -1:
            if dsn[len(dsn) - 1] != ';':
                dsn = dsn + ";"
            if database != '' and dsn.find('DATABASE=') == -1:
                dsn = dsn + "DATABASE=" + database + ";"
            if host != '' and dsn.find('HOSTNAME=') == -1:
                dsn = dsn + "HOSTNAME=" + host + ";"
        else:
            dsn = "DSN=" + dsn + ";"

        if user != '' and dsn.find('UID=') == -1:
            dsn = dsn + "UID=" + user + ";"
        if password != '' and dsn.find('PWD=') == -1:
            dsn = dsn + "PWD=" + password + ";"
    
    try:
        if not _is_ibmi():
            conn = conn_func(dsn, '', '', options)
        else:
            conn = conn_func(database, user, password, options)
        
        ibm_db.set_option(conn, {SQL_ATTR_CURRENT_SCHEMA : user}, 1)
    except Exception as inst:
        raise _get_exception(inst)

    return Connection(conn)

def connect(dsn=None, user='', password='', host='', database='', conn_options=None):
    """This method creates a non persistent connection to the database. It returns
        a ibm_db_dbi.Connection object.
    """
    return _connect_helper(ibm_db.connect, dsn, user, password, host, database, conn_options)

def pconnect(dsn=None, user='', password='', host='', database='', conn_options=None):
    """This method creates persistent connection to the database. It returns
        a ibm_db_dbi.Connection object.
    """
    return _connect_helper(ibm_db.pconnect, dsn, user, password, host, database, conn_options)

class Connection(object):
    """This class object represents a connection between the database 
    and the application.

    """
    def __init__(self, conn_handler):
        """Constructor for Connection object. It takes ibm_db 
        connection handler as an argument. 

        """
        self.conn_handler = conn_handler

        # Used to identify close cursors for generating exceptions 
        # after the connection is closed.
        self._cursor_list = []
        self.__dbms_name = ibm_db.get_db_info(conn_handler, SQL_DBMS_NAME)
        self.__dbms_ver = ibm_db.get_db_info(conn_handler, SQL_DBMS_VER)

    # This method is used to get the DBMS_NAME 
    def __get_dbms_name( self ):
        return self.__dbms_name

    # This attribute specifies the DBMS_NAME
    # It is a read only attribute. 
    dbms_name = property(__get_dbms_name, None, None, "")

    # This method is used to get the DBMS_ver 
    def __get_dbms_ver( self ):
        return self.__dbms_ver

    # This attribute specifies the DBMS_ver
    # It is a read only attribute. 
    dbms_ver = property(__get_dbms_ver, None, None, "")

    def close(self):
        """This method closes the Database connection associated with
        the Connection object.  It takes no arguments.

        """
        self.rollback()
        try:
            if self.conn_handler is None:
                raise ProgrammingError("Connection cannot be closed; "
                                     "connection is no longer active.")
            else:
                return_value = ibm_db.close(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        self.conn_handler = None
        for index in range(len(self._cursor_list)):
            if (self._cursor_list[index]() != None):
                tmp_cursor =  self._cursor_list[index]()
                tmp_cursor.conn_handler = None
                tmp_cursor.stmt_handler = None
                tmp_cursor._all_stmt_handlers = None
        self._cursor_list = []
        return return_value

    def commit(self):
        """This method commits the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = ibm_db.commit(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        return return_value

    def rollback(self):
        """This method rollbacks the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = ibm_db.rollback(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        return return_value

    def cursor(self):
        """This method returns a Cursor object associated with the 
        Connection.  It takes no arguments.

        """
        if self.conn_handler is None:
            raise ProgrammingError("Cursor cannot be returned; "
                               "connection is no longer active.")
        cursor = Cursor(self.conn_handler, self)
        self._cursor_list.append(weakref.ref(cursor))
        return cursor

    # Sets connection attribute values
    def set_option(self, attr_dict):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        return ibm_db.set_option(self.conn_handler, attr_dict, 1)

    # Retrieves connection attributes values
    def get_option(self, attr_key):
        """Input: connection attribute key
           Return: current setting of the resource attribute requested
        """
        return ibm_db.get_option(self.conn_handler, attr_key, 1)

    # Sets connection AUTOCOMMIT attribute
    def set_autocommit(self, is_on):
        """Input: connection attribute: true if AUTOCOMMIT ON, false otherwise (i.e. OFF)
           Return: True on success or False on failure
        """
        try:
          if is_on:
            is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_ON}, 1)
          else:
            is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_OFF}, 1)
        except Exception as inst:
          raise _get_exception(inst)
        return is_set

    # Sets connection attribute values
    def set_current_schema(self, schema_name):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        self.current_schema = schema_name
        try:
          if not _is_ibmi():
              is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_CURRENT_SCHEMA : schema_name}, 1)
          else:
              stmt = ibm_db.prepare(self.conn_handler, "set current schema = ?")
              if(stmt):
                  is_set = ibm_db.execute(stmt, (schema_name, ))
              else:
                  is_set = False     
        except Exception as inst:
          raise _get_exception(inst)
        return is_set

    # Retrieves connection attributes values
    def get_current_schema(self):
        """Return: current setting of the schema attribute
        """
        try:
          if not _is_ibmi():
              conn_schema = ibm_db.get_option(self.conn_handler, SQL_ATTR_CURRENT_SCHEMA, 1)
              if conn_schema is not None and conn_schema != '':
                self.current_schema = conn_schema
          else:
              stmt = ibm_db.exec_immediate(self.conn_handler, "select current_schema from sysibm.sysdummy1")
              result = ibm_db.fetch_both(stmt)
              self.current_schema = result[0]
        except Exception as inst:
          raise _get_exception(inst)
        return self.current_schema

    # Retrieves the IBM Data Server version for a given Connection object
    def server_info(self):
        """Return: tuple (DBMS_NAME, DBMS_VER)
        """
        try:
          server_info = []
          server_info.append(self.dbms_name)
          server_info.append(self.dbms_ver)
        except Exception as inst:
          raise _get_exception(inst)
        return tuple(server_info)
    
    def set_case(self, server_type, str_value):
        return str_value.upper()

    # Retrieves the tables for a specified schema (and/or given table name)
    def tables(self, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of table metadata dicts for the specified schema
        """
            
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:      
          stmt = ibm_db.tables(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result

    # Retrieves metadata pertaining to index for specified schema (and/or table name)
    def indexes(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of index metadata dicts for the specified table
        Example:
           Index metadata retrieved from schema 'PYTHONIC.TEST_TABLE' table
           {
           'TABLE_SCHEM':       'PYTHONIC',              'TABLE_CAT':          None, 
           'TABLE_NAME':        'ENGINE_USERS',          'PAGES':              None, 
           'COLUMN_NAME':       'USER_ID'                'FILTER_CONDITION':   None, 
           'INDEX_NAME':        'SQL071201150750170',    'CARDINALITY':        None,
           'ORDINAL_POSITION':   1,                      'INDEX_QUALIFIER':   'SYSIBM', 
           'TYPE':               3, 
           'NON_UNIQUE':         0, 
           'ASC_OR_DESC':       'A'
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.statistics(self.conn_handler, None, schema_name, table_name, unique)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              if row['TYPE'] == SQL_INDEX_OTHER:
                  result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result        

    # Retrieves metadata pertaining to primary keys for specified schema (and/or table name)
    def primary_keys(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of PK metadata dicts for the specified table
        Example:
           PK metadata retrieved from 'PYTHONIC.ORDERS' table
           {  
           'TABLE_SCHEM':  'PYTHONIC',                 'TABLE_CAT': None, 
           'TABLE_NAME':   'ORDERS', 
           'COLUMN_NAME':  'ORDER_ID'
           'PK_NAME':      'SQL071128122038680', 
           'KEY_SEQ':       1
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.primary_keys(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result        

    # Retrieves metadata pertaining to foreign keys for specified schema (and/or table name)
    def foreign_keys(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of FK metadata dicts for the specified table
        Example:
           FK metadata retrieved from 'PYTHONIC.ENGINE_EMAIL_ADDRESSES' table
           {  
           'PKTABLE_SCHEM': 'PYTHONIC',                 'PKTABLE_CAT':    None, 
           'PKTABLE_NAME':  'ENGINE_USERS',             'FKTABLE_CAT':    None,
           'PKCOLUMN_NAME': 'USER_ID',                  'UPDATE_RULE':    3,
           'PK_NAME':       'SQL071205090958680',       'DELETE_RULE':    3
           'KEY_SEQ':        1,                         'DEFERRABILITY':  7, 
           'FK_NAME':       'SQL071205091000160', 
           'FKCOLUMN_NAME': 'REMOTE_USER_ID', 
           'FKTABLE_NAME':  'ENGINE_EMAIL_ADDRESSES', 
           'FKTABLE_SCHEM': 'PYTHONIC' 
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.foreign_keys(self.conn_handler, None, None, None, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result        
    
    # Retrieves the columns for a specified schema (and/or table name and column name)
    def columns(self, schema_name=None, table_name=None, column_names=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of column metadata dicts for the specified schema
        Example:
           Column metadata retrieved from schema 'PYTHONIC.FOO' table, column 'A'
           {
           'TABLE_NAME':        'FOO',        'NULLABLE':           1, 
           'ORDINAL_POSITION':   2L,          'REMARKS':            None, 
           'COLUMN_NAME':       'A',          'BUFFER_LENGTH':      30L, 
           'TYPE_NAME':         'VARCHAR',    'SQL_DATETIME_SUB':   None, 
           'COLUMN_DEF':         None,        'DATA_TYPE':          12, 
           'IS_NULLABLE':       'YES',        'SQL_DATA_TYPE':      12, 
           'COLUMN_SIZE':        30L,         'TABLE_CAT':          None, 
           'CHAR_OCTET_LENGTH':  30L,         'TABLE_SCHEM':       'PYTHONIC',
           'NUM_PREC_RADIX':     None,
           'DECIMAL_DIGITS':     None
           }
        """
        result = []
        if schema_name is not None:
          schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
          table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.columns(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
            result.append( row )
            i += 1    
            row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)

          col_names_lower = []
          if column_names is not None:
            for name in column_names:
              col_names_lower.append(name.lower())
            include_columns = []
            if column_names and column_names != '':
              for column in result:
                if column['COLUMN_NAME'].lower() in col_names_lower:
                  column['COLUMN_NAME'] = column['COLUMN_NAME'].lower()
                  include_columns.append(column)
              result = include_columns
        except Exception as inst:
          raise _get_exception(inst)

        return result


# Defines a cursor for the driver connection
class Cursor(object):
    """This class represents a cursor of the connection.  It can be
    used to process an SQL statement.
    """
    
    # This method is used to get the description attribute.
    def __get_description(self):
        """ If this method has already been called, after executing a select statement,
            return the stored information in the self.__description.
        """
        if self.__description is not None:
            return self.__description 

        if self.stmt_handler is None:
            return None
        self.__description = []
        
        try:
            num_columns = ibm_db.num_fields(self.stmt_handler)
            """ If the execute statement did not produce a result set return None.
            """
            if num_columns == False:
                self.__description = None
                return None
            for column_index in range(num_columns):
                column_desc = []
                column_desc.append(ibm_db.field_name(self.stmt_handler,
                                                          column_index))
                field_type = ibm_db.field_type(self.stmt_handler, column_index).upper()
                
                if STRING == field_type:
                    column_desc.append(STRING)
                elif TEXT == field_type:
                    column_desc.append(TEXT)
                elif XML == field_type:
                    column_desc.append(XML)
                elif BINARY == field_type:
                    column_desc.append(BINARY)
                elif NUMBER == field_type:
                    column_desc.append(NUMBER)
                elif BIGINT == field_type:
                    column_desc.append(BIGINT) 
                elif FLOAT == field_type:
                    column_desc.append(FLOAT)
                elif DECIMAL == field_type:
                    column_desc.append(DECIMAL)
                elif DATE == field_type:
                    column_desc.append(DATE)
                elif TIME == field_type:
                    column_desc.append(TIME)
                elif DATETIME == field_type:
                    column_desc.append(DATETIME)
                elif ROWID == field_type:
                    column_desc.append(ROWID)
                else:
                    self.messages.append(InterfaceError("Unsupported type for column %d: '%s'" % (column_index, field_type)))
                    raise self.messages[-1]

                column_desc.append(ibm_db.field_display_size(
                                             self.stmt_handler, column_index))

                column_desc.append(ibm_db.field_display_size(
                                             self.stmt_handler, column_index))
                
                column_desc.append(ibm_db.field_precision(
                                             self.stmt_handler, column_index))

                column_desc.append(ibm_db.field_scale(self.stmt_handler,
                                                                column_index))
                                                                
                column_desc.append(ibm_db.field_nullable(
                                             self.stmt_handler, column_index))
                                             
                self.__description.append(column_desc)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]

        return self.__description

    # This attribute provides the metadata information of the columns  
    # in the result set produced by the last execute function.  It is
    # a read only attribute.
    description = property(fget = __get_description)

    # This method is used to get the rowcount attribute. 
    def __get_rowcount( self ):
        return self.__rowcount

    def __iter__( self ):
        return self
    
    def __next__( self ):
        row = self.fetchone()
        if row == None:
            raise StopIteration
        return row
        
    def next( self ):
        self.__next__()
        
    # This attribute specifies the number of rows the last executeXXX()
    # produced or affected.  It is a read only attribute. 
    rowcount = property(__get_rowcount, None, None, "")
    
    # This method is used to get the Connection object
    def __get_connection( self ):
        return self.__connection
    
    # This attribute specifies the connection object.
    # It is a read only attribute. 
    connection = property(__get_connection, None, None, "")

    def __init__(self, conn_handler, conn_object=None):
        """Constructor for Cursor object. It takes ibm_db connection
        handler as an argument.
        """
        
        # This attribute is used to determine the fetch size for fetchmany
        # operation. It is a read/write attribute
        self.arraysize = 1
        self.__rowcount = -1
        self._result_set_produced = False
        self.__description = None
        self.conn_handler = conn_handler
        self.stmt_handler = None
        self._is_scrollable_cursor = False
        self.__connection = conn_object
        self.messages = []
    
    # This method closes the statemente associated with the cursor object.
    # It takes no argument.
    def close(self):
        """This method closes the cursor object.  After this method is 
        called the cursor object is no longer usable.  It takes no
        arguments.

        """
        messages = []
        if self.conn_handler is None:
            self.messages.append(ProgrammingError("Cursor cannot be closed; connection is no longer active."))
            raise self.messages[-1]
        try:
            return_value = ibm_db.free_stmt(self.stmt_handler)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]
        self.stmt_handler = None
        self.conn_handler = None
        self._all_stmt_handlers = None
        if self.__connection is not None:
            try:
                self.__connection._cursor_list.remove(weakref.ref(self))
            except:
                pass
        return return_value

    # helper for calling procedure
    def _callproc_helper(self, procname, parameters=None):
        if parameters is not None:
            buff = []
            # Convert date/time and binary objects to string for 
            # inserting into the database. 
            for param in parameters:
                if isinstance(param, buffer):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)
            
            try:
                result = ibm_db.callproc(self.conn_handler, procname,parameters)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
        else:
            try:
                result = ibm_db.callproc(self.conn_handler, procname)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
        return result
       

    def callproc(self, procname, parameters=None):
        """This method can be used to execute a stored procedure.  
        It takes the name of the stored procedure and the parameters to
        the stored procedure as arguments. 

        """
        self.messages = []
        if not isinstance(procname, six.string_types):
            self.messages.append(InterfaceError("callproc expects the first argument to be of type String or Unicode."))
            raise self.messages[-1]
        if parameters is not None:
            if not isinstance(parameters, (list, tuple)):
                self.messages.append(InterfaceError("callproc expects the second argument to be of type list or tuple."))
                raise self.messages[-1]
        result = self._callproc_helper(procname, parameters)
        return_value = None
        self.__description = None
        self._all_stmt_handlers = []
        if isinstance(result, tuple):
            self.stmt_handler = result[0]
            return_value = result[1:]
        else:
            self.stmt_handler = result
        self._result_set_produced = True
        return return_value

    # Helper for preparing an SQL statement. 
    def _prepare_helper(self, operation, parameters=None):
        try:
            ibm_db.free_stmt(self.stmt_handler)
        except:
            pass

        try:
            # Uncomment the below print line for debug purposes
            #print("operation=", operation)
            self.stmt_handler = ibm_db.prepare(self.conn_handler, operation)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]

    # Helper for preparing an SQL statement.
    def _set_cursor_helper(self):
        if (ibm_db.get_option(self.stmt_handler, ibm_db.SQL_ATTR_CURSOR_TYPE, 0) != ibm_db.SQL_CURSOR_FORWARD_ONLY):
            self._is_scrollable_cursor = True
        else:
            self._is_scrollable_cursor = False
        self._result_set_produced = False
        try:
            num_columns = ibm_db.num_fields(self.stmt_handler)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]
        if not num_columns:
            return True
        self._result_set_produced = True

        return True

    # Helper for executing an SQL statement.
    def _execute_helper(self, parameters=None):
        if parameters is not None:
            buff = []
            # Convert date/time and binary objects to string for 
            # inserting into the database. 
            for param in parameters:
                if isinstance(param, buffer):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)
            try:   
                if not _is_ibmi():
                    return_value = ibm_db.execute(self.stmt_handler, parameters)	
                else:
                    # On IBM i we need to temporarily switch to using the System Reply List (*SYSRPYL) 
                    # in case someone has added a reply list entry for the following message ID:
                    # CPA32B2 -  Change of file &1 may cause data to be lost. (C I)
                    # Once the SQL statement has been processed we immediately switch back to *RQD.                                                                         					
                    ibm_db.exec_immediate(self.conn_handler, "CALL QSYS2.QCMDEXC('CHGJOB INQMSGRPY(*SYSRPYL)')")            
                    return_value = ibm_db.execute(self.stmt_handler, parameters)
                    ibm_db.exec_immediate(self.conn_handler, "CALL QSYS2.QCMDEXC('CHGJOB INQMSGRPY(*RQD)')")
                if not return_value:
                    if ibm_db.conn_errormsg() is not None:
                        self.messages.append(Error(str(ibm_db.conn_errormsg())))
                        raise self.messages[-1]
                    if ibm_db.stmt_errormsg() is not None:
                        self.messages.append(Error(str(ibm_db.stmt_errormsg())))
                        raise self.messages[-1]
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
        else:
            try:
                return_value = ibm_db.execute(self.stmt_handler)
                if not return_value:
                    if ibm_db.conn_errormsg() is not None:
                        self.messages.append(Error(str(ibm_db.conn_errormsg())))
                        raise self.messages[-1]
                    if ibm_db.stmt_errormsg() is not None:
                        self.messages.append(Error(str(ibm_db.stmt_errormsg())))
                        raise self.messages[-1]
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
        return return_value

    # This method is used to set the rowcount after executing an SQL 
    # statement. 
    def _set_rowcount(self):
        self.__rowcount = -1
        if not self._result_set_produced:
            try:
                counter = ibm_db.num_rows(self.stmt_handler)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
            self.__rowcount = counter
        elif self._is_scrollable_cursor:
            try:
                counter = ibm_db.get_num_result(self.stmt_handler)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[-1]
            if counter >= 0:
                self.__rowcount = counter
        return True

    # Retrieves the last generated identity value from the DB2 catalog
    def _get_last_identity_val(self):
        """
        The result of the IDENTITY_VAL_LOCAL function is not affected by the following:
         - A single row INSERT statement with a VALUES clause for a table without an
        identity column
         - A multiple row INSERT statement with a VALUES clause
         - An INSERT statement with a fullselect

        """
        operation = 'SELECT IDENTITY_VAL_LOCAL() FROM SYSIBM.SYSDUMMY1'
        try:
            stmt_handler = ibm_db.prepare(self.conn_handler, operation)
            if ibm_db.execute(stmt_handler):
                row = ibm_db.fetch_tuple(stmt_handler)
                if row[0] is not None:
                  identity_val = int(row[0])
                else:
                  identity_val = None
            else:
                if ibm_db.conn_errormsg() is not None:
                    self.messages.append(Error(str(ibm_db.conn_errormsg())))
                    raise self.messages[-1]
                if ibm_db.stmt_errormsg() is not None:
                    self.messages.append(Error(str(ibm_db.stmt_errormsg())))
                    raise self.messages[-1]
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]
        return identity_val
    last_identity_val = property(_get_last_identity_val, None, None, "")

    def execute(self, operation, parameters=None):
        """
        This method can be used to prepare and execute an SQL 
        statement.  It takes the SQL statement(operation) and a 
        sequence of values to substitute for the parameter markers in  
        the SQL statement as arguments.
        """
        self.messages = []
        if not isinstance(operation, six.string_types):
            self.messages.append(InterfaceError("execute expects the first argument [%s] to be of type String or Unicode." % operation ))
            raise self.messages[-1]
        if parameters is not None:
            if not isinstance(parameters, (list, tuple, dict)):
                self.messages.append(InterfaceError("execute parameters argument should be sequence."))
                raise self.messages[-1]
        self.__description = None
        self._all_stmt_handlers = []
        self._prepare_helper(operation)
        self._set_cursor_helper()
        self._execute_helper(parameters)
        return self._set_rowcount()

    def executemany(self, operation, seq_parameters):
        """
        This method can be used to prepare, and then execute an SQL 
        statement many times.  It takes the SQL statement(operation) 
        and sequence of sequence of values to substitute for the 
        parameter markers in the SQL statement as its argument.
        """
        self.messages = []
        if not isinstance(operation, six.string_types):
            self.messages.append(InterfaceError("executemany expects the first argument to be of type String or Unicode."))
            raise self.messages[-1]
        if seq_parameters is None:
            self.messages.append(InterfaceError("executemany expects a not None seq_parameters value"))
            raise self.messages[-1]

        if not isinstance(seq_parameters, (list, tuple)):
            self.messages.append(InterfaceError("executemany expects the second argument to be of type list or tuple of sequence."))
            raise self.messages[-1]
        
        # Convert date/time and binary objects to string for
        # inserting into the database.
        buff = []
        seq_buff = []
        for index in range(len(seq_parameters)):
            buff = []
            for param in seq_parameters[index]:
                if isinstance(param, buffer):
                    param = str(param)
                buff.append(param)
            seq_buff.append(tuple(buff))
        seq_parameters = tuple(seq_buff)
        self.__description = None
        self._all_stmt_handlers = []
        self.__rowcount = -1
        self._prepare_helper(operation)
        try:
            autocommit = ibm_db.autocommit(self.conn_handler)
            if autocommit !=  0:
                ibm_db.autocommit(self.conn_handler, 0)
            self.__rowcount = ibm_db.execute_many(self.stmt_handler, seq_parameters)
            if autocommit != 0:
                ibm_db.commit(self.conn_handler)
                ibm_db.autocommit(self.conn_handler, autocommit)
            if self.__rowcount == -1:
                if ibm_db.conn_errormsg() is not None:
                    self.messages.append(Error(str(ibm_db.conn_errormsg())))
                    raise self.messages[-1]
                if ibm_db.stmt_errormsg() is not None:
                    self.messages.append(Error(str(ibm_db.stmt_errormsg())))
                    raise self.messages[-1]   
        except Exception as inst:
            self._set_rowcount()
            self.messages.append(Error(inst))
            raise self.messages[-1]
        return True

    def _fetch_helper(self, fetch_size=-1):
        """
        This method is a helper function for fetching fetch_size number of 
        rows, after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.
        If this is not provided it fetches all the remaining rows.
        """
        if self.stmt_handler is None:
            self.messages.append(ProgrammingError("Please execute an SQL statement in order to get a row from result set."))
            raise self.messages[-1]
        if self._result_set_produced == False:
            self.messages.append(ProgrammingError("The last call to execute did not produce any result set."))
            raise  self.messages[-1]
        row_list = []
        rows_fetched = 0
        while (fetch_size == -1) or (rows_fetched < fetch_size):
            try:
                row = ibm_db.fetch_tuple(self.stmt_handler)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                if len(row_list) == 0:
                    raise self.messages[-1]
                else:
                    return row_list
            
            if row != False:
                row_list.append(self._fix_return_data_type(row))
            else:
                return row_list
            rows_fetched = rows_fetched + 1
        return row_list

    def fetchone(self):
        """This method fetches one row from the database, after 
        executing an SQL statement which produces a result set.
        
        """
        row_list = self._fetch_helper(1)
        if len(row_list) == 0:
            return None
        else:
            return row_list[0]

    def fetchmany(self, size=0):
        """This method fetches size number of rows from the database,
        after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.  If this 
        is not provided it fetches self.arraysize number of rows. 
        """
        if not isinstance(size, six.integer_types):
            self.messages.append(InterfaceError( "fetchmany expects argument type int or long."))
            raise self.messages[-1]
        if size == 0:
            size = self.arraysize
        if size < -1:
            self.messages.append(ProgrammingError("fetchmany argument size expected to be positive."))
            raise self.messages[-1]

        return self._fetch_helper(size)

    def fetchall(self):
        """This method fetches all remaining rows from the database,
        after executing an SQL statement which produces a result set.
        """
        return self._fetch_helper()

    def nextset(self):
        """This method can be used to get the next result set after 
        executing a stored procedure, which produces multiple result sets.
        """
        self.messages = []
        if self.stmt_handler is None:
            self.messages.append(ProgrammingError("Please execute an SQL statement in order to get result sets."))
            raise self.messages[-1]
        if self._result_set_produced == False:
            self.messages.append(ProgrammingError("The last call to execute did not produce any result set."))
            raise self.messages[-1]
        try:
            # Store all the stmt handler that were created.  The 
            # handler was the one created by the execute method.  It 
            # should be used to get next result set. 
            self.__description = None
            self._all_stmt_handlers.append(self.stmt_handler)
            self.stmt_handler = ibm_db.next_result(self._all_stmt_handlers[0])
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[-1]

        if self.stmt_handler == False:
            self.stmt_handler = None
        if self.stmt_handler == None:
            return None 
        return True

    def setinputsizes(self, sizes):
        """This method currently does nothing."""
        pass

    def setoutputsize(self, size, column=-1):
        """This method currently does nothing."""
        pass

    # This method is used to convert a string representing decimal 
    # and binary data in a row tuple fetched from the database 
    # to decimal and binary objects, for returning it to the user.
    def _fix_return_data_type(self, row):
        row_list = []
        index = -1
        
        for col in row:
            index += 1
            
            if col is None:
                row_list.append(col)
            else:
                field_type = ibm_db.field_type(self.stmt_handler, index)

                try:
                    new_col = col
                    if field_type == 'blob':
                        new_col = buffer(col)
                    elif field_type == 'decimal' or field_type == 'decfloat':
                        new_col = decimal.Decimal(str(col).replace(",", "."))

                    row_list.append(new_col)

                except Exception as inst:
                    self.messages.append(DataError("Data type format error: "+ str(inst)))
                    raise self.messages[-1]

        return tuple(row_list)
