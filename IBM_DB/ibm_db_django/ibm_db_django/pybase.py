# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009.                                      |
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

# Importing IBM_DB wrapper ibm_db_dbi
try:
    import ibm_db_dbi as Database
except ImportError, e:
    raise ImportError( "ibm_db module not found. Install ibm_db module from http://code.google.com/p/ibm-db/." )

# For checking django's version
from django import VERSION as djangoVersion

import decimal
if ( djangoVersion[0:2] > ( 1, 1 ) ):
    from django.db import utils
    import sys

DatabaseError = Database.DatabaseError
IntegrityError = Database.IntegrityError

class DatabaseWrapper( object ):
    # Over-riding _cursor method to return DB2 cursor.
    def _cursor( self, connection, kwargs ):
        if not connection: 
            kwargsKeys = kwargs.keys()
            if ( kwargsKeys.__contains__( 'port' ) and 
                kwargsKeys.__contains__( 'host' ) ):
                kwargs['dsn'] = "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;" % ( 
                         kwargs.get( 'database' ),
                         kwargs.get( 'host' ),
                         kwargs.get( 'port' )
                )
            else:
                kwargs['dsn'] = kwargs.get( 'database' )
            
            # Setting AUTO COMMIT off on connection.
            conn_options = {Database.SQL_ATTR_AUTOCOMMIT : Database.SQL_AUTOCOMMIT_OFF}
            kwargs['conn_options'] = conn_options
            kwargs.update( kwargs.get( 'options' ) )
            del kwargs['options']
            del kwargs['port']
            
            connection = Database.pconnect( **kwargs )
            connection.autocommit = connection.set_autocommit
            return connection, DB2CursorWrapper( connection )
        else:
            return DB2CursorWrapper( connection )
        
    def close( self, connection ):
        connection.close()
        
    def get_server_version( self, connection ):
        self.connection = connection
        if not self.connection:
            self.cursor()
        return tuple( int( version ) for version in self.connection.server_info()[1].split( "." ) )
    
class DB2CursorWrapper( Database.Cursor ):
        
    """
    This is the wrapper around IBM_DB_DBI in order to support format parameter style
    IBM_DB_DBI supports qmark, where as Django support format style, 
    hence this conversion is required. 
    """
    
    def __init__( self, connection ): 
        super( DB2CursorWrapper, self ).__init__( connection.conn_handler, connection )
        
    def __iter__( self ):
        return self
        
    def next( self ):
        row = self.fetchone()
        if row == None:
            raise StopIteration
        return row
            
    # Over-riding this method to modify SQLs which contains format parameter to qmark. 
    def execute( self, operation, parameters = () ):
        try:
            operation = operation % ( tuple( "?" * operation.count( "%s" ) ) )
            if ( djangoVersion[0:2] <= ( 1, 1 ) ):
                return super( DB2CursorWrapper, self ).execute( operation, parameters )
            else:
                try:
                    return super( DB2CursorWrapper, self ).execute( operation, parameters )
                except IntegrityError, e:
                    raise utils.IntegrityError, utils.IntegrityError( *tuple( e ) ), sys.exc_info()[2]
                except DatabaseError, e:
                    raise utils.DatabaseError, utils.DatabaseError( *tuple( e ) ), sys.exc_info()[2]   
        except ( TypeError ):
            return None
        
    # Over-riding this method to modify SQLs which contains format parameter to qmark.
    def executemany( self, operation, seq_parameters ):
        try:
            operation = operation % ( tuple( "?" * operation.count( "%s" ) ) )
            if ( djangoVersion[0:2] <= ( 1, 1 ) ):
                return super( DB2CursorWrapper, self ).executemany( operation, seq_parameters )
            else:
                try:
                    return super( DB2CursorWrapper, self ).executemany( operation, seq_parameters )
                except IntegrityError, e:
                    raise utils.IntegrityError, utils.IntegrityError( *tuple( e ) ), sys.exc_info()[2]
                except DatabaseError, e:
                    raise utils.DatabaseError, utils.DatabaseError( *tuple( e ) ), sys.exc_info()[2] 
        except ( IndexError, TypeError ):
            return None
    