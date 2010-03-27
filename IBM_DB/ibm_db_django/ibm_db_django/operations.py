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

from django.db.backends import BaseDatabaseOperations
from ibm_db_django import query
from string import upper
from django import VERSION as djangoVersion

class DatabaseOperations(BaseDatabaseOperations):
    if(djangoVersion[0:2] >= (1, 2)):
        compiler_module = "ibm_db_django.compiler"

    # Function to extract day, month or year from the date.
    # Reference: http://publib.boulder.ibm.com/infocenter/db2luw/v9r5/topic/com.ibm.db2.luw.sql.ref.doc/doc/r0023457.html
    def date_extract_sql(self, lookup_type, field_name):
        if upper(lookup_type) == 'WEEK_DAY':
            return " DAYOFWEEK(%s) " % (field_name)
        else:
            return " %s(%s) " % (upper(lookup_type), field_name)
     
    # Rounding of date on the basic of looktype.
    # e.g If input is 2008-12-04 and month then output will be 2008-12-01 00:00:00
    # Reference: http://www.ibm.com/developerworks/data/library/samples/db2/0205udfs/index.html
    def date_trunc_sql(self, lookup_type, field_name):
        sql = "TIMESTAMP(DATE(SUBSTR(CHAR(%s), 1, %d) || '%s'), TIME('00:00:00'))"
        if upper(lookup_type) == 'DAY':
            sql = sql % (field_name, 10, '')
        elif upper(lookup_type) == 'MONTH':
            sql = sql % (field_name, 7, '-01')
        elif upper(lookup_type) == 'YEAR':
            sql = sql % (field_name, 4, '-01-01')

        return sql
        
    #This function casts the field and returns it for use in the where clause
    def field_cast_sql(self, db_type):
        if db_type == 'CLOB':
            return "VARCHAR(%s, 4096)"
        else:
            return " %s"
            
    #As casting is not required, so nothing is required to do in this function.
    def datetime_cast_sql(self):
        return "%s"
    
    # This function will allow us to call sql_flush function. If following function 
    # is not implemented then sql_flush will throw an error on foreign key
    # constraint violation.
    def deferrable_sql(self):
        return " ON DELETE CASCADE"
    
    # Function to return SQL from dropping foreign key.
    def drop_foreignkey_sql(self):
        return "DROP FOREIGN KEY"
    
    # Dropping auto generated property of the identity column.
    def drop_sequence_sql(self, table):
        return "ALTER TABLE %s ALTER COLUMN ID DROP IDENTITY" % (self.quote_name(table))
            
    def fulltext_search_sql(self, field_name):
        sql = "WHERE %s = ?" % field_name
        return sql
    
    # Function to return value of auto-generated field of last executed insert query. 
    def last_insert_id(self, cursor, table_name, pk_name):
        return cursor.last_identity_val
    
    # In case of WHERE clause, if the search is required to be case insensitive then converting 
    # left hand side field to upper.
    def lookup_cast(self, lookup_type):
        if lookup_type in ('iexact', 'icontains', 'istartswith', 'iendswith'):
            return "UPPER(%s)"
        return "%s"
    
    # As DB2 v91 specifications, 
    # Maximum length of a table name and Maximum length of a column name is 128
    # http://publib.boulder.ibm.com/infocenter/db2e/v9r1/index.jsp?topic=/com.ibm.db2e.doc/db2elimits.html
    def max_name_length(self):
        return 128
    
    def no_limit_value(self):
        return None
    
    # Method to point custom query class implementation.
    def query_class(self, DefaultQueryClass):
        return query.query_class(DefaultQueryClass)
        
    # Function to quote the name of schema, table and column.
    def quote_name(self, name):
        name = upper(name)
        if(name.startswith("\"") & name.endswith("\"")):
            return name
        
        if(name.startswith("\"")):
            return "%s\"" % name
        
        if(name.endswith("\"")):
            return "\"%s" % name

        return "\"%s\"" % name
    
    # SQL to return RANDOM number.
    # Reference: http://publib.boulder.ibm.com/infocenter/db2luw/v8/topic/com.ibm.db2.udb.doc/admin/r0000840.htm
    def random_function_sql(self):
        return "SYSFUN.RAND()"
    
    # As save-point is supported by DB2, following function will return SQL to create savepoint.
    def savepoint_create_sql(self, sid):
        return "SAVEPOINT %s ON ROLLBACK RETAIN CURSORS" % sid
    
    # Function to commit savepoint.   
    def savepoint_commit_sql(self, sid):
        return "COMMIT %s" % sid
    
    # Function to rollback savepoint.
    def savepoint_rollback_sql(self, sid):
        return "ROLLBACK TO SAVEPOINT %s" % sid
    
    # Deleting all the rows from the list of tables provided and resetting all the
    # sequences.
    def sql_flush(self, style, tables, sequences):
        sqls = []
        if tables:
            for table in tables:
                sqls.append(style.SQL_KEYWORD("DELETE") + " " + 
                           style.SQL_KEYWORD("FROM") + " " +
                           style.SQL_TABLE("%s" % self.quote_name(table)))
                
            for sequence in sequences:
                if(sequence['column'] != None):
                    sqls.append(style.SQL_KEYWORD("ALTER TABLE") + " " + 
                            style.SQL_TABLE("%s" % self.quote_name(sequence['table'])) +
                            " " + style.SQL_KEYWORD("ALTER COLUMN") + " %s "
                            % self.quote_name(sequence['column']) +
                            style.SQL_KEYWORD("RESTART WITH 1"))
            return sqls
        else:
            return []
    
    # Table many contains rows when this is get called, hence resetting sequence
    # to a large value (10000).
    def sequence_reset_sql( self, style, model_list ):
        from django.db import models
        from django.db import connection
        cursor = connection.cursor()
        sqls = []
        for model in model_list:
            table = model._meta.db_table
            for field in model._meta.local_fields:
                if isinstance(field, models.AutoField):
                    max_sql = "SELECT MAX(%s) FROM %s" % (self.quote_name(field.column), self.quote_name(table))
                    cursor.execute(max_sql)
                    max_id = [row[0] for row in cursor.fetchall()]
                    sqls.append(style.SQL_KEYWORD("ALTER TABLE") + " " + 
                        style.SQL_TABLE("%s" % self.quote_name(table)) +
                        " " + style.SQL_KEYWORD("ALTER COLUMN") + " %s "
                        % self.quote_name(field.column) +
                        style.SQL_KEYWORD("RESTART WITH %s" %(max_id[0] + 1)))
                    break

            for field in model._meta.many_to_many:
                m2m_table = field.m2m_db_table()
                if not field.rel.through:
                    max_sql = "SELECT MAX(%s) FROM %s" % (self.quote_name('ID'), self.quote_name(table))
                    cursor.execute(max_sql)
                    max_id = [row[0] for row in cursor.fetchall()]
                    sqls.append(style.SQL_KEYWORD("ALTER TABLE") + " " + 
                        style.SQL_TABLE("%s" % self.quote_name(m2m_table)) +
                        " " + style.SQL_KEYWORD("ALTER COLUMN") + " %s "
                        % self.quote_name('ID') +
                        style.SQL_KEYWORD("RESTART WITH %s" %(max_id[0] + 1)))
        if cursor:
            cursor.close()
            
        return sqls
    
    def tablespace_sql(self, tablespace, inline=False):
        # inline is used for column indexes defined in-line with column definition, like:
        #   CREATE TABLE "TABLE1" ("ID_OTHER" VARCHAR(20) NOT NULL UNIQUE) IN "TABLESPACE1";
        # couldn't find support for this in create table 
        #   (http://publib.boulder.ibm.com/infocenter/db2luw/v9/topic/com.ibm.db2.udb.admin.doc/doc/r0000927.htm)
        if inline:
            sql = ""
        else:
            sql = "IN %s" % self.quote_name(tablespace)
        return sql
    
    def year_lookup_bounds_for_date_field(self, value):
        lower_bound = "%s-01-01"
        upper_bound = "%s-12-31"
        return [lower_bound % value, upper_bound % value]
