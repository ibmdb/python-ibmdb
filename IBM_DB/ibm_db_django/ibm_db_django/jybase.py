# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009-2013.                                      |
# +--------------------------------------------------------------------------+
# | This module complies with Django 1.0 and is                              |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Ambrish Bhargava, Tarun Pasrija, Rahul Priyadarshi              |
# +--------------------------------------------------------------------------+

# Importing necessary classes
try:
    from com.ziclix.python.sql import zxJDBC, PyConnection, DataHandler, PyCursor
    import datetime, decimal
    from java.sql import Connection
except ImportError, e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured( "Error loading zxJDBC module: %s" % e )
# For checking django's version
from django import VERSION as djangoVersion

DatabaseError = zxJDBC.DatabaseError
IntegrityError = zxJDBC.IntegrityError
if ( djangoVersion[0:2] >= ( 1, 6 )):
    Error = zxJDBC.Error
    InterfaceError = zxJDBC.InterfaceError
    DataError = zxJDBC.DataError
    OperationalError = zxJDBC.OperationalError
    InternalError = zxJDBC.InternalError
    ProgrammingError = zxJDBC.ProgrammingError
    NotSupportedError = zxJDBC.NotSupportedError

class DatabaseWrapper( object ):
    # Get new database connection for non persistance connection 
    def get_new_connection(self, kwargs):
        self.connectionFactory = kwargs.get( 'options' ) and kwargs.get( 'options' ).get( 'CONNECTION_FACTORY' ) or None
        if self.connectionFactory:
            con = self.connectionFactory.getConnection()
            connection = PyConnection( con )
        else:
            host = kwargs.get( 'host' ) or 'localhost'
            port = kwargs.get( 'port' ) and ( ':%s' % kwargs.get( 'port' )) or ''
            DriverType = 4
            kwargsKeys = kwargs.keys()
            if kwargsKeys.__contains__( 'DriverType' ):
                DriverType = kwargs['DriverType']
            if DriverType == 4:
                conn_string = "jdbc:db2://%s%s/%s" % ( host, port, kwargs.get( 'database' ) )
            elif DriverType == 2:
                conn_string = "jdbc:db2:%s" % ( kwargs.get( 'database' ) )
            else:
                raise ImproperlyConfigured( "Wrong Driver type" )
            
            # for Setting default AUTO COMMIT off on connection.
            autocommit = False
            
            if kwargs.get( 'options' ) and kwargs.get( 'options' ).keys().__contains__( 'autocommit' ):
                autocommit = kwargs.get( 'options' ).get( 'autocommit' )
                del kwargs.get( 'options' )['autocommit']
                
            connection = zxJDBC.connect( conn_string,
                                           kwargs.get( 'user' ),
                                           kwargs.get( 'password' ),
                                           'com.ibm.db2.jcc.DB2Driver', kwargs.get( 'options' ) )
            # To prevent dirty reads
            self.__prevent_dirty_reads( connection )
            connection.__connection__.setAutoCommit( autocommit )
        return connection
        
    def is_active( self, connection ):
        cursor = connection.cursor()
        try:
            cursor.execute("select 1 from sysibm.sysdummy1")
            return True
        except:
            return False
            
    # Over-riding _cursor method to return DB2 cursor.
    def _cursor( self, connection):
        return DB2CursorWrapper( connection.cursor() ) 
        
    def close( self, connection ):
        if self.connectionFactory:
            self.connectionFactory.closeConnection( connection.__connection__ )
        else:                
            # db2  fails if active transaction ....            
            connection.rollback()
            connection.close()

    #prohibits a transaction from reading a row with uncommitted changes in it.
    def __prevent_dirty_reads( self, connection ):
        JDBC_conn = connection.__connection__
        JDBC_conn.setTransactionIsolation( Connection.TRANSACTION_READ_COMMITTED )
        
    def get_server_version( self, connection ):
        version = connection.dbversion.split( "SQL" )[1]
        return ( int( version[:2] ), int( version[2:4] ), int( version[4:] ) )
        
class DB2CursorWrapper( object ):
    def __init__( self, cursor ):
        self.cursor = cursor
        
    # Over-riding this method to modify SQLs which contains format parameter to qmark. 
    def execute( self, operation, parameters = () ):
        try:
            operation = operation % ( tuple( "?" * operation.count( "%s" ) ) )
            if operation.endswith( ';' ) or operation.endswith( '/' ):
                operation = operation[:-1]
            returnValue = self.cursor.execute( operation, parameters )
            if ( self.cursor.updatecount is not None ) and  self.cursor.updatecount != -1:
                self.rowcount = self.cursor.updatecount
            else:
                self.rowcount = self.cursor.rowcount
            return returnValue
        except ( TypeError ):
            return None
    
    # Over-riding this method to modify SQLs which contains format parameter to qmark.
    def executemany( self, operation, seq_parameters ):
        try:
            operation = operation % ( tuple( "?" * operation.count( "%s" ) ) )
            if operation.endswith( ';' ) or operation.endswith( '/' ):
                operation = operation[:-1]
            returnValue = self.cursor.executemany( operation, seq_parameters )
            if ( self.cursor.updatecount is not None ) and  self.cursor.updatecount != -1:
                self.rowcount = self.cursor.updatecount
            else:
                self.rowcount = self.cursor.rowcount
            return returnValue 
        except ( IndexError, TypeError ):
            return None
        
    def fetchone( self, ):
        row = self.cursor.fetchone()
        return self._fix_return_data_type( row )
        
    def fetchmany( self, size = 0 ):
        if size == 0:
            size = self.arraysize
        row_list = []
        for row in self.cursor.fetchmany( size ):
            row_list.append( self._fix_return_data_type( row ) )
        return row_list
        
    def fetchall( self ):
        row_list = []
        for row in self.cursor.fetchall():
            row_list.append( self._fix_return_data_type( row ) )
        return row_list
        
    def __getattr__( self, attr ):
            if attr in self.__dict__:
                return self.__dict__[attr]
            else:
                return getattr( self.cursor, attr )
        
    # This method is used to convert a string representing date/time 
    # and binary data in a row tuple fetched from the database 
    # to date/time and binary objects, for returning it to the user.
    def _fix_return_data_type( self, row ):
        row = list( row )
        description = self.cursor.description
        for index in range( len( row ) ):
            if row[index] is not None:
                if description[index][1] == zxJDBC.BLOB:
                    row[index] = buffer( row[index] )
                elif description[index][1] == zxJDBC.DECIMAL:
                    row[index] = decimal.Decimal( str( row[index] ).replace( ",", "." ) )    
        return tuple( row )
