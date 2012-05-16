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

import sys
from string import upper
_IS_JYTHON = sys.platform.startswith( 'java' )

if not _IS_JYTHON:
    try:    
        # Import IBM_DB wrapper ibm_db_dbi
        import ibm_db_dbi as Database
        #from Database import DatabaseError
    except ImportError, e:
        raise ImportError( "ibm_db module not found. Install ibm_db module from http://code.google.com/p/ibm-db/. Error: %s" % e )
else:
    from com.ziclix.python.sql import zxJDBC

from django.db.backends import BaseDatabaseIntrospection
from django import VERSION as djangoVersion

class DatabaseIntrospection( BaseDatabaseIntrospection ):
    
    """
    This is the class where database metadata information can be generated.
    """

    if not _IS_JYTHON:
        if( djangoVersion[0:2] <= ( 1, 1 ) ):
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
    else:
        data_types_reverse = {
            zxJDBC.CHAR:                "CharField",
            zxJDBC.BIGINT:              "BigIntegerField",
            zxJDBC.BINARY:              "ImageField",
            zxJDBC.BIT:                 "SmallIntegerField",
            zxJDBC.BLOB:                "ImageField",
            zxJDBC.CLOB:                "TextField",
            zxJDBC.DATE:                "DateField",
            zxJDBC.DECIMAL:             "DecimalField",
            zxJDBC.DOUBLE:              "FloatField",
            zxJDBC.FLOAT:               "FloatField",
            zxJDBC.INTEGER:             "IntegerField",
            zxJDBC.LONGVARCHAR:         "TextField",
            zxJDBC.LONGVARBINARY:       "ImageField",
            zxJDBC.NUMERIC:             "DecimalField",
            zxJDBC.REAL:                "FloatField",
            zxJDBC.SMALLINT:            "SmallIntegerField",
            zxJDBC.VARCHAR:             "CharField",
            zxJDBC.TIMESTAMP:           "DateTimeField",
            zxJDBC.TIME:                "TimeField",
        }
     
    # Converting table name to lower case.
    def table_name_converter ( self, name ):        
        return name.lower()
    
    # Getting the list of all tables, which are present under current schema.
    def get_table_list ( self, cursor ):
        table_list = []
        if not _IS_JYTHON:
            for table in cursor.connection.tables( cursor.connection.get_current_schema() ):
                table_list.append( table['TABLE_NAME'].lower() )
        else:
            cursor.execute( "select current_schema from sysibm.sysdummy1" )
            schema = cursor.fetchone()[0]
            # tables(String catalog, String schemaPattern, String tableNamePattern, String[] types) gives a description of tables available in a catalog 
            cursor.tables( None, schema, None, ( "TABLE", ) )
            for table in cursor.fetchall():
                # table[2] is table name
                table_list.append( table[2].lower() )
                
        return table_list
    
    # Generating a dictionary for foreign key details, which are present under current schema.
    def get_relations( self, cursor, table_name ):
        relations = {}
        if not _IS_JYTHON:
            schema = cursor.connection.get_current_schema()
            for fk in cursor.connection.foreign_keys( True, schema, table_name ):
                relations[self.__get_col_index( cursor, schema, table_name, fk['FKCOLUMN_NAME'] )] = ( self.__get_col_index( cursor, schema, fk['PKTABLE_NAME'], fk['PKCOLUMN_NAME'] ), fk['PKTABLE_NAME'].lower() )
        else:
            cursor.execute( "select current_schema from sysibm.sysdummy1" )
            schema = cursor.fetchone()[0]
            # foreign_keys(String primaryCatalog, String primarySchema, String primaryTable, String foreignCatalog, String foreignSchema, String foreignTable) 
            # gives a description of the foreign key columns in the foreign key table that reference the primary key columns 
            # of the primary key table (describe how one table imports another's key.) This should normally return a single foreign key/primary key pair 
            # (most tables only import a foreign key from a table once.) They are ordered by FKTABLE_CAT, FKTABLE_SCHEM, FKTABLE_NAME, and KEY_SEQ
            cursor.foreignkeys( None, schema, table_name, None, '%', '%' )
            for fk in cursor.fetchall():
                # fk[2] is primary key table name, fk[3] is primary key column name, fk[7] is foreign key column name being exported
                relations[self.__get_col_index( cursor, schema, table_name, fk[7] )] = ( self.__get_col_index( cursor, schema, fk[2], fk[3] ), fk[3], fk[2] )
        return relations
    
    # Private method. Getting Index position of column by its name
    def __get_col_index ( self, cursor, schema, table_name, col_name ):
        if not _IS_JYTHON:
            for col in cursor.connection.columns( schema, table_name, [col_name] ):
                return col['ORDINAL_POSITION'] - 1
        else:
            cursor.execute( "select current_schema from sysibm.sysdummy1" )
            schema = cursor.fetchone()[0]
            # columns(String catalog, String schemaPattern, String tableNamePattern, String columnNamePattern) gives a description of table columns available in the specified catalog
            cursor.columns( None, schema, table_name, col_name )
            for col in cursor.fetchall():
                #col[16] is index of column in table
                return col[16] - 1
    
    # Getting list of indexes associated with the table provided.
    def get_indexes( self, cursor, table_name ):
        indexes = {}
        if not _IS_JYTHON:
            schema = cursor.connection.get_current_schema()
            for index in cursor.connection.indexes( True, schema, table_name ):
                temp = {}
                if ( index['NON_UNIQUE'] ):
                    temp['unique'] = False
                else:
                    temp['unique'] = True
                temp['primary_key'] = False
                indexes[index['COLUMN_NAME'].lower()] = temp
            
            for index in cursor.connection.primary_keys( True, schema, table_name ):
                indexes[index['COLUMN_NAME'].lower()]['primary_key'] = True
        else:
            cursor.execute( "select current_schema from sysibm.sysdummy1" )
            schema = cursor.fetchone()[0]
            # statistics(String catalog, String schema, String table, boolean unique, boolean approximate) returns a description of a table's indices and statistics. 
            cursor.statistics( None, schema, table_name, 0, 0 )
            for index in cursor.fetchall():
                temp = {}
                # index[3] indicate non-uniqueness of column
                if ( index[3] != None ):
                    if ( index[3] ) == 1:
                        temp['unique'] = False
                    else:
                        temp['unique'] = True
                    temp['primary_key'] = False
                    # index[8] is column name
                    indexes[index[8].lower()] = temp
            
            # primarykeys(String catalog, String schema, String table) gives a description of a table's primary key columns
            cursor.primarykeys( None, schema, table_name )
            for index in cursor.fetchall():
                #index[3] is column name
                indexes[index[3].lower()]['primary_key'] = True
        return indexes
    
    # Getting the description of the table.
    def get_table_description( self, cursor, table_name ):
        qn = self.connection.ops.quote_name
        cursor.execute( "SELECT * FROM %s FETCH FIRST 1 ROWS ONLY" % qn( table_name ) )   
        description = []
        for desc in cursor.description:
            description.append( [ desc[0].lower(), ] + desc[1:] )
        return description
