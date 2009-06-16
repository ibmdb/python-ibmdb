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
# | Authors: Ambrish Bhargava                                                |
# | Version: 0.1.0                                                           |
# +--------------------------------------------------------------------------+

"""
DB2 database backend for Django.
Requires: ibm_db_dbi (http://pypi.python.org/pypi/ibm_db)
"""

# Import IBM_DB wrapper ibm_db_dbi
try:
    import ibm_db_dbi as Database
except ImportError, e:
    raise ImportError("ibm_db module not found. Install ibm_db module from http://code.google.com/p/ibm-db/.")

# Importing class from base module of django.db.backends
from django.db.backends import BaseDatabaseFeatures
from django.db.backends import BaseDatabaseWrapper
from django.db.backends import BaseDatabaseValidation

# Importing internal classes from django.db.backends.db2 package.
from django.db.backends.db2.client import DatabaseClient
from django.db.backends.db2.creation import DatabaseCreation
from django.db.backends.db2.introspection import DatabaseIntrospection
from django.db.backends.db2.operations import DatabaseOperations

# For validation, importing types class
import types

DatabaseError = Database.DatabaseError
IntegrityError = Database.IntegrityError

class DatabaseFeatures ( BaseDatabaseFeatures ):    
    can_use_chunked_reads               = False
    
    #Save point is supported by DB2.
    uses_savepoints                     = True
    
    #Custom query class has been implemented 
    #django.db.backends.db2.query.query_class.DB2QueryClass
    uses_custom_query_class             = True

class DatabaseValidation ( BaseDatabaseValidation ):    
    #Need to do validation for DB2 and ibm_db version
    def validate_field ( self, errors, opts, f ):
        pass

class DatabaseWrapper (BaseDatabaseWrapper):
    
    """
    This is the base class for DB2 backend support for Django. The under lying 
    wrapper is IBM_DB_DBI (latest version can be downloaded from http://code.google.com/p/ibm-db/ or
    http://pypi.python.org/pypi/ibm_db). 
    """
        
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
    def __init__(self, **kwargs):
        super(DatabaseWrapper, self).__init__(**kwargs)

        self.features = DatabaseFeatures()
        self.ops = DatabaseOperations()
        self.client = DatabaseClient()
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = DatabaseValidation()

    # Method to check if connection is live or not.
    def __is_connection(self):
        return self.connection is not None
    
    # Over-riding _cursor method to return DB2 cursor.
    def _cursor (self, settings):
        if not self.__is_connection():            
            kwargs 			 = { }
            
            if(isinstance(settings.DATABASE_NAME, types.StringType) or
               isinstance(settings.DATABASE_NAME, types.UnicodeType)):
                kwargs['database'] = settings.DATABASE_NAME
                
            if(isinstance(settings.DATABASE_USER, types.StringType) or 
               isinstance(settings.DATABASE_USER, types.UnicodeType)):
                kwargs['user'] = settings.DATABASE_USER
            
            if(isinstance(settings.DATABASE_PASSWORD, types.StringType) or
               isinstance(settings.DATABASE_PASSWORD, types.UnicodeType)):
                kwargs['password'] = settings.DATABASE_PASSWORD
            
            if(isinstance(settings.DATABASE_HOST, types.StringType) or
               isinstance(settings.DATABASE_HOST, types.UnicodeType)):
                kwargs['host'] = settings.DATABASE_HOST
                
            if((isinstance(settings.DATABASE_PORT, types.StringType) or
                isinstance(settings.DATABASE_PORT, types.UnicodeType)) and 
                (isinstance(settings.DATABASE_HOST, types.StringType) or
                isinstance(settings.DATABASE_HOST, types.UnicodeType))):
                kwargs['dsn'] = "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;" % (
                         settings.DATABASE_NAME,
                         settings.DATABASE_HOST,
                         settings.DATABASE_PORT
                )
            else:
                kwargs['dsn'] = "%s" % (settings.DATABASE_NAME)
            
            # Setting AUTO COMMIT off on connection.
            conn_options = {Database.SQL_ATTR_AUTOCOMMIT : Database.SQL_AUTOCOMMIT_OFF}
            kwargs['conn_options'] = conn_options
    
            self.connection = Database.connect (**kwargs)
        
        return DB2CursorWrapper(self.connection)
            
    def get_server_version(self):
        return self.connection.server_info()[1]
    
class DB2CursorWrapper(Database.Cursor):
    
    """
    This is the wrapper around IBM_DB_DBI in order to support format parameter style
    IBM_DB_DBI supports qmark, where as Django support format style, 
    hence this conversion is required. 
    """
    
    def __init__(self, connection):
        super(DB2CursorWrapper, self).__init__(connection.conn_handler, connection)
    
    # Over-riding this method to modify SQLs which contains format parameter to qmark. 
    def execute(self, operation, parameters = ()):
        try:
            operation = operation % (tuple("?" * len(parameters)))
            return super(DB2CursorWrapper, self).execute(operation, parameters)
        except (TypeError):
            return None
    
    # Over-riding this method to modify SQLs which contains format parameter to qmark.
    def executemany(self, operation, seq_parameters):
        try:
            operation = operation % (tuple("?" * len(seq_parameters[0])))
            return super(DB2CursorWrapper, self).executemany(operation, seq_parameters)
        except (IndexError, TypeError):
            return None
