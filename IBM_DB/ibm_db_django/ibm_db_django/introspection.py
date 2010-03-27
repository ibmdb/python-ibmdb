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

# Import IBM_DB wrapper ibm_db_dbi
from string import upper
try:
    import ibm_db_dbi as Database
    #from Database import DatabaseError
except ImportError, e:
    raise ImportError("ibm_db module not found. Install ibm_db module from http://code.google.com/p/ibm-db/.")

from django.db.backends import BaseDatabaseIntrospection
from django import VERSION as djangoVersion

class DatabaseIntrospection(BaseDatabaseIntrospection):
    
    """
    This is the class where database metadata information can be generated.
    """
    if(djangoVersion[0:2] <= (1, 1)):
        data_types_reverse = {
            Database.STRING :           "CharField",
            Database.TEXT :             "TextField",
            Database.XML :              "XMLField",
            Database.NUMBER :           "IntegerField",
            Database.BIGINT :           "IntegerField",
            Database.FLOAT :            "FloatField",
            Database.DECIMAL :          "DecimalField",
            Database.DATE :             "DateField",
            Database.TIME :             "TimeField",
            Database.DATETIME :         "DateTimeField",
            Database.BINARY :           "ImageField",
        }
    else:
        data_types_reverse = {
            Database.STRING :           "CharField",
            Database.TEXT :             "TextField",
            Database.XML :              "XMLField",
            Database.NUMBER :           "IntegerField",
            Database.BIGINT :           "BigIntegerField",
            Database.FLOAT :            "FloatField",
            Database.DECIMAL :          "DecimalField",
            Database.DATE :             "DateField",
            Database.TIME :             "TimeField",
            Database.DATETIME :         "DateTimeField",
            Database.BINARY :           "ImageField",
        }
    
    # Converting table name to upper case.
    def table_name_converter (self, name):        
        return upper(name)
    
    # Getting the list of all tables, which are present under current schema.
    def get_table_list (self, cursor):
        table_list = []
        for table in cursor.connection.tables(cursor.connection.get_current_schema()):
            table_list.append(table['TABLE_NAME'])

        return table_list
    
    # Generating a dictionary for foreign key details, which are present under current schema.
    def get_relations(self, cursor, table_name):
        schema = cursor.connection.get_current_schema()
        relations = {}
        for fk in cursor.connection.foreign_keys(True, schema, table_name):
            relations[self.__get_col_index(cursor, schema, table_name, fk['FKCOLUMN_NAME'])] = (
                self.__get_col_index(cursor, schema, fk['PKTABLE_NAME'], fk['PKCOLUMN_NAME']),
                fk['PKTABLE_NAME'])

        return relations
    
    # Private method. Getting Index position of column by its name
    def __get_col_index(self, cursor, schema, table_name, col_name):
        for col in cursor.connection.columns(schema, table_name, [col_name]):
            return col['ORDINAL_POSITION'] - 1
    
    # Getting list of indexes associated with the table provided.
    def get_indexes(self, cursor, table_name):
        indexes = {}
        schema = cursor.connection.get_current_schema()
        for index in cursor.connection.indexes(True, schema, table_name):
            temp = {}
            if (index['NON_UNIQUE']):
                temp['unique'] = False
            else:
                temp['unique'] = True
            temp['primary_key'] = False
            indexes[index['COLUMN_NAME'].lower()] = temp
        
        for index in cursor.connection.primary_keys(True, schema, table_name):
            indexes[index['COLUMN_NAME'].lower()]['primary_key'] = True
            
        return indexes
    
    # Getting the description of the table.
    def get_table_description(self, cursor, table_name):
        cursor.execute("SELECT * FROM %s FETCH FIRST 1 ROWS ONLY" % table_name)        
        return cursor.description
