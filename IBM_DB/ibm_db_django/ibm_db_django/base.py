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

"""
DB2 database backend for Django.
Requires: ibm_db_dbi (http://pypi.python.org/pypi/ibm_db) for python
"""
import sys
_IS_JYTHON = sys.platform.startswith( 'java' )

from django.core.exceptions import ImproperlyConfigured

# Importing class from base module of django.db.backends
from django.db.backends import BaseDatabaseFeatures
from django.db.backends import BaseDatabaseWrapper
from django.db.backends import BaseDatabaseValidation
from django.db.backends.signals import connection_created

# Importing internal classes from ibm_db_django package.
from ibm_db_django.client import DatabaseClient
from ibm_db_django.creation import DatabaseCreation
from ibm_db_django.introspection import DatabaseIntrospection
from ibm_db_django.operations import DatabaseOperations
if not _IS_JYTHON:
    import ibm_db_django.pybase as baseWrapper
else:
    import ibm_db_django.jybase as baseWrapper 
    
# For checking django's version
from django import VERSION as djangoVersion

DatabaseError = baseWrapper.DatabaseError
IntegrityError = baseWrapper.IntegrityError

class DatabaseFeatures( BaseDatabaseFeatures ):    
    can_use_chunked_reads = False
    
    #Save point is supported by DB2.
    uses_savepoints = True
    
    #Custom query class has been implemented 
    #django.db.backends.db2.query.query_class.DB2QueryClass
    uses_custom_query_class = True
    
    #transaction is supported by DB2
    supports_transactions = True
    
    supports_tablespaces = True
    
    interprets_empty_strings_as_nulls = False
    allows_primary_key_0 = True
    can_defer_constraint_checks = False
    supports_forward_references = False
    requires_rollback_on_dirty_transaction = True
    supports_regex_backreferencing = False
    supports_timezones = False
    has_bulk_insert = True
    has_select_for_update = True
    supports_long_model_names = False
    can_distinct_on_fields = False
    
class DatabaseValidation( BaseDatabaseValidation ):    
    #Need to do validation for DB2 and ibm_db version
    def validate_field( self, errors, opts, f ):
        pass

class DatabaseWrapper( BaseDatabaseWrapper ):
    
    """
    This is the base class for DB2 backend support for Django. The under lying 
    wrapper is IBM_DB_DBI (latest version can be downloaded from http://code.google.com/p/ibm-db/ or
    http://pypi.python.org/pypi/ibm_db). 
    """
    vendor = 'DB2'
    operators = {
        "exact":        "= %s",
        "iexact":       "LIKE %s ESCAPE '\\'",
        "contains":     "LIKE %s ESCAPE '\\'",
        "icontains":    "LIKE %s ESCAPE '\\'",
        "gt":           "> %s",
        "gte":          ">= %s",
        "lt":           "< %s",
        "lte":          "<= %s",
        "startswith":   "LIKE %s ESCAPE '\\'",
        "endswith":     "LIKE %s ESCAPE '\\'",
        "istartswith":  "LIKE %s ESCAPE '\\'",
        "iendswith":    "LIKE %s ESCAPE '\\'",
    }

    # Constructor of DB2 backend support. Initializing all other classes.
    def __init__( self, *args ):
        super( DatabaseWrapper, self ).__init__( *args )
        self.ops = DatabaseOperations( self )
        if( djangoVersion[0:2] <= ( 1, 0 ) ):
            self.client = DatabaseClient()
        else:
            self.client = DatabaseClient( self )
        if( djangoVersion[0:2] <= ( 1, 2 ) ):
            self.features = DatabaseFeatures()
        else:
            self.features = DatabaseFeatures( self )
        self.creation = DatabaseCreation( self )
        self.introspection = DatabaseIntrospection( self )
        if( djangoVersion[0:2] <= ( 1, 1 ) ):
            self.validation = DatabaseValidation()
        else:
            self.validation = DatabaseValidation( self )
        self.databaseWrapper = baseWrapper.DatabaseWrapper()
    
    # Method to check if connection is live or not.
    def __is_connection( self ):
        return self.connection is not None
        
    # Over-riding _cursor method to return DB2 cursor.
    def _cursor( self, settings = None ):
        if not self.__is_connection():
            kwargs = { }
            if ( djangoVersion[0:2] <= ( 1, 0 ) ):
                database_name = settings.DATABASE_NAME
                database_user = settings.DATABASE_USER
                database_pass = settings.DATABASE_PASSWORD
                database_host = settings.DATABASE_HOST
                database_port = settings.DATABASE_PORT
                database_options = settings.DATABASE_OPTIONS
            elif ( djangoVersion[0:2] <= ( 1, 1 ) ):
                settings_dict = self.settings_dict
                database_name = settings_dict['DATABASE_NAME']
                database_user = settings_dict['DATABASE_USER']
                database_pass = settings_dict['DATABASE_PASSWORD']
                database_host = settings_dict['DATABASE_HOST']
                database_port = settings_dict['DATABASE_PORT']
                database_options = settings_dict['DATABASE_OPTIONS']
            else:
                settings_dict = self.settings_dict
                database_name = settings_dict['NAME']
                database_user = settings_dict['USER']
                database_pass = settings_dict['PASSWORD']
                database_host = settings_dict['HOST']
                database_port = settings_dict['PORT']
                database_options = settings_dict['OPTIONS']
            
            if database_name != '' and isinstance( database_name, basestring ):
                kwargs['database'] = database_name
            else:
                raise ImproperlyConfigured( "Please specify the valid database Name to connect to" )
                
            if isinstance( database_user, basestring ):
                kwargs['user'] = database_user
            
            if isinstance( database_pass, basestring ):
                kwargs['password'] = database_pass
            
            if isinstance( database_host, basestring ):
                kwargs['host'] = database_host
            
            if isinstance( database_port, basestring ):
                kwargs['port'] = database_port
                
            if isinstance( database_host, basestring ):
                kwargs['host'] = database_host
            
            if isinstance( database_options, dict ):
                kwargs['options'] = database_options
            
            if ( djangoVersion[0:2] <= ( 1, 0 ) ):
               if( hasattr( settings, 'PCONNECT' ) ):
                   kwargs['PCONNECT'] = settings.PCONNECT
            else:
                if ( settings_dict.keys() ).__contains__( 'PCONNECT' ):
                    kwargs['PCONNECT'] = settings_dict['PCONNECT']
            self.connection, cursor = self.databaseWrapper._cursor( None, kwargs )
            
            if( djangoVersion[0:3] <= ( 1, 2, 2 ) ):
                connection_created.send( sender = self.__class__ )
            else:
                connection_created.send( sender = self.__class__, connection = self )
        else:
            cursor = self.databaseWrapper._cursor( self.connection, None )
        return cursor
    
    def close( self ):
        if self.connection is not None:
            self.databaseWrapper.close( self.connection )
            self.connection = None
        
    def get_server_version( self ):
        if not self.connection:
            self.cursor()
        return self.databaseWrapper.get_server_version( self.connection )
   
    
    
            
