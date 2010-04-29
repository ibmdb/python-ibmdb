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
Requires: ibm_db_dbi (http://pypi.python.org/pypi/ibm_db)
"""

# Import IBM_DB wrapper ibm_db_dbi
try:
    import ibm_db_dbi as Database
except ImportError, e:
    raise ImportError("ibm_db module not found. Install ibm_db module from http://code.google.com/p/ibm-db/.")
import sys

# Importing class from base module of django.db.backends
from django.db.backends import BaseDatabaseFeatures
from django.db.backends import BaseDatabaseWrapper
from django.db.backends import BaseDatabaseValidation

# Importing internal classes from ibm_db_django package.
from ibm_db_django.client import DatabaseClient
from ibm_db_django.creation import DatabaseCreation
from ibm_db_django.introspection import DatabaseIntrospection
from ibm_db_django.operations import DatabaseOperations
from django.db.backends.signals import connection_created

# For validation, importing types class
import types
from django import VERSION as djangoVersion
if (djangoVersion[0:2] > (1, 1)):
    from django.db import utils

DatabaseError = Database.DatabaseError
IntegrityError = Database.IntegrityError

class DatabaseFeatures(BaseDatabaseFeatures):    
    can_use_chunked_reads               = False
    
    #Save point is supported by DB2.
    uses_savepoints                     = True
    
    #Custom query class has been implemented 
    #django.db.backends.db2.query.query_class.DB2QueryClass
    uses_custom_query_class             = True

class DatabaseValidation(BaseDatabaseValidation):    
    #Need to do validation for DB2 and ibm_db version
    def validate_field(self, errors, opts, f):
        pass

class DatabaseWrapper(BaseDatabaseWrapper):
    
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
    def __init__(self, *args):
        super(DatabaseWrapper, self).__init__(*args)

        self.features = DatabaseFeatures()
        self.ops = DatabaseOperations()
        if(djangoVersion[0:2] <= (1, 0)):
            self.client = DatabaseClient()
        else:
            self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        if(djangoVersion[0:2] <= (1, 1)):
            self.validation = DatabaseValidation()
        else:
            self.validation = DatabaseValidation(self)

    # Method to check if connection is live or not.
    def __is_connection(self):
        return self.connection is not None
    
    # Over-riding _cursor method to return DB2 cursor.
    def _cursor(self, settings=None):
        if not self.__is_connection():
            kwargs = { }
            if (djangoVersion[0:2] <= (1, 0)):
                database_name = settings.DATABASE_NAME
                database_user = settings.DATABASE_USER
                database_pass = settings.DATABASE_PASSWORD
                database_host = settings.DATABASE_HOST
                database_port = settings.DATABASE_PORT
                database_options = settings.DATABASE_OPTIONS
            elif (djangoVersion[0:2] <= (1, 1)):
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
                
            if database_name =='':
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured("Please specify the database Name to connect to")
            
            if isinstance(database_name, basestring):
                kwargs['database'] = database_name
                
            if isinstance(database_user, basestring):
                kwargs['user'] = database_user
            
            if isinstance(database_pass, basestring):
                kwargs['password'] = database_pass
            
            if isinstance(database_host, basestring):
                kwargs['host'] = database_host
                
            if (isinstance(database_port, basestring) and 
                isinstance(database_host, basestring)):
                kwargs['dsn'] = "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;" % (
                         database_name,
                         database_host,
                         database_port
                )
            else:
                kwargs['dsn'] = "%s" % (database_name)
            
            # Setting AUTO COMMIT off on connection.
            conn_options = {Database.SQL_ATTR_AUTOCOMMIT : Database.SQL_AUTOCOMMIT_OFF}
            kwargs['conn_options'] = conn_options
            kwargs.update(database_options)
            self.connection = Database.pconnect(**kwargs)
            connection_created.send(sender=self.__class__)
        
        return DB2CursorWrapper(self.connection)
    
    
            
    def get_server_version(self):
        if not (self.__is_connection()):
            self.cursor()
        return tuple(int(version) for version in self.connection.server_info()[1].split("."))
    
class DB2CursorWrapper(Database.Cursor):
    
    """
    This is the wrapper around IBM_DB_DBI in order to support format parameter style
    IBM_DB_DBI supports qmark, where as Django support format style, 
    hence this conversion is required. 
    """
    
    def __init__(self, connection): 
        super(DB2CursorWrapper, self).__init__(connection.conn_handler, connection)
    
    def __iter__(self):
        return self
    
    def next(self):
        row = self.fetchone()
        if row == None:
            raise StopIteration
        return row
        
    # Over-riding this method to modify SQLs which contains format parameter to qmark. 
    def execute(self, operation, parameters=()):
        try:
            operation = operation % (tuple("?" * len(parameters)))
            if (djangoVersion[0:2] <= (1, 1)):
                return super(DB2CursorWrapper, self).execute(operation, parameters)
            else:
                try:
                    return super(DB2CursorWrapper, self).execute(operation, parameters)
                except IntegrityError, e:
                    raise utils.IntegrityError, utils.IntegrityError(*tuple(e)), sys.exc_info()[2]
                except DatabaseError, e:
                    raise utils.DatabaseError, utils.DatabaseError(*tuple(e)), sys.exc_info()[2]   
        except (TypeError):
            return None
    
    # Over-riding this method to modify SQLs which contains format parameter to qmark.
    def executemany(self, operation, seq_parameters):
        try:
            operation = operation % (tuple("?" * len(seq_parameters[0])))
            if (djangoVersion[0:2] <= (1, 1)):
                return super(DB2CursorWrapper, self).executemany(operation, seq_parameters)
            else:
                try:
                    return super(DB2CursorWrapper, self).executemany(operation, seq_parameters)
                except IntegrityError, e:
                    raise utils.IntegrityError, utils.IntegrityError(*tuple(e)), sys.exc_info()[2]
                except DatabaseError, e:
                    raise utils.DatabaseError, utils.DatabaseError(*tuple(e)), sys.exc_info()[2] 
        except (IndexError, TypeError):
            return None
