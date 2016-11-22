# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009-2014.                                      |
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
from collections import namedtuple
import sys
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

try:
    from django.db.backends import BaseDatabaseIntrospection, FieldInfo
except ImportError:
    from django.db.backends.base.introspection import BaseDatabaseIntrospection, FieldInfo

from django import VERSION as djangoVersion

class DatabaseIntrospection( BaseDatabaseIntrospection ):
    
    """
    This is the class where database metadata information can be generated.
    """

    if not _IS_JYTHON:
        data_types_reverse = {
            Database.STRING :           "CharField",
            Database.TEXT :             "TextField",
            Database.XML :              "XMLField",
            Database.NUMBER :           "IntegerField",
            Database.FLOAT :            "FloatField",
            Database.DECIMAL :          "DecimalField",
            Database.DATE :             "DateField",
            Database.TIME :             "TimeField",
            Database.DATETIME :         "DateTimeField",
        }    
        if(djangoVersion[0:2] > (1, 1)):
            data_types_reverse[Database.BINARY] = "BinaryField"
            data_types_reverse[Database.BIGINT] = "BigIntegerField"
        else:
            data_types_reverse[Database.BIGINT] = "IntegerField"
    else:
        data_types_reverse = {
            zxJDBC.CHAR:                "CharField",
            zxJDBC.BIGINT:              "BigIntegerField",
            zxJDBC.BINARY:              "BinaryField",
            zxJDBC.BIT:                 "SmallIntegerField",
            zxJDBC.BLOB:                "BinaryField",
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
     
    def get_field_type(self, data_type, description):
        if not _IS_JYTHON:
            if data_type == Database.NUMBER:
                if description.precision == 5:
                    return 'SmallIntegerField'
        return super(DatabaseIntrospection, self).get_field_type(data_type, description)
    
    # Converting table name to lower case.
    def table_name_converter ( self, name ):        
        return name.lower()
    
    # Getting the list of all tables, which are present under current schema.
    def get_table_list ( self, cursor ):
        TableInfo = namedtuple('TableInfo', ['name', 'type'])
        table_list = []
        if not _IS_JYTHON:
            for table in cursor.connection.tables( cursor.connection.get_current_schema() ):
                if( djangoVersion[0:2] < ( 1, 8 ) ):
                    table_list.append( table['TABLE_NAME'].lower() )
                else:
                    table_list.append(TableInfo( table['TABLE_NAME'].lower(),'t'))
        else:
            cursor.execute( "select current_schema from sysibm.sysdummy1" )
            schema = cursor.fetchone()[0]
            # tables(String catalog, String schemaPattern, String tableNamePattern, String[] types) gives a description of tables available in a catalog 
            cursor.tables( None, schema, None, ( "TABLE", ) )
            for table in cursor.fetchall():
                # table[2] is table name
                if( djangoVersion[0:2] < ( 1, 8 ) ):
                    table_list.append( table[2].lower() )
            table_list.append(TableInfo(table[2].lower(),"t"))
                
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
    
    def get_key_columns(self, cursor, table_name):
        relations = []
        if not _IS_JYTHON:
            schema = cursor.connection.get_current_schema()
            for fk in cursor.connection.foreign_keys( True, schema, table_name ):
                relations.append( (fk['FKCOLUMN_NAME'].lower(), fk['PKTABLE_NAME'].lower(), fk['PKCOLUMN_NAME'].lower()) )
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
                relations.append( (fk[7], fk[2], fk[3]) )
        return relations
        
    # Getting list of indexes associated with the table provided.
    def get_indexes( self, cursor, table_name ):
        indexes = {}
        # To skip indexes across multiple fields
        multifield_indexSet = set()
        if not _IS_JYTHON:
            schema = cursor.connection.get_current_schema()
            all_indexes = cursor.connection.indexes( True, schema, table_name )
            for index in all_indexes:
                if (index['ORDINAL_POSITION'] is not None) and (index['ORDINAL_POSITION']== 2):
                    multifield_indexSet.add(index['INDEX_NAME'])
                    
            for index in all_indexes:
                temp = {}
                if index['INDEX_NAME'] in multifield_indexSet:
                    continue
                
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
            all_indexes = cursor.fetchall()
            for index in all_indexes:
                #index[7] indicate ORDINAL_POSITION within index, and index[5] is index name
                if index[7] == 2:
                    multifield_indexSet.add(index[5])
                    
            for index in all_indexes:
                temp = {}
                if index[5] in multifield_indexSet:
                    continue
                
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
        description = []
        table_type = 'T'
        if not _IS_JYTHON:
            dbms_name='dbms_name'
            schema = cursor.connection.get_current_schema()
            if getattr(cursor.connection, dbms_name) != 'DB2':
                sql = "SELECT TYPE FROM SYSCAT.TABLES WHERE TABSCHEMA='%(schema)s' AND TABNAME='%(table)s'" % {'schema': schema.upper(), 'table': table_name.upper()}
            else:
                sql = "SELECT TYPE FROM SYSIBM.SYSTABLES WHERE CREATOR='%(schema)s' AND NAME='%(table)s'" % {'schema': schema.upper(), 'table': table_name.upper()}
            cursor.execute(sql)
            table_type = cursor.fetchone()[0]

        if table_type != 'X':
            cursor.execute( "SELECT * FROM %s FETCH FIRST 1 ROWS ONLY" % qn( table_name ) )
            if djangoVersion < (1, 6):
                for desc in cursor.description:
                    description.append( [ desc[0].lower(), ] + desc[1:] )
            else:
                for desc in cursor.description:
                    description.append(FieldInfo(*[desc[0].lower(), ] + desc[1:]))
        
        return description

    def get_constraints(self, cursor, table_name):
        constraints = {} 
        if not _IS_JYTHON:
            schema = cursor.connection.get_current_schema()
            dbms_name='dbms_name'
            if getattr(cursor.connection, dbms_name) != 'DB2':
                sql = "SELECT CONSTNAME, COLNAME FROM SYSCAT.COLCHECKS WHERE TABSCHEMA='%(schema)s' AND TABNAME='%(table)s'" % {'schema': schema.upper(), 'table': table_name.upper()}
            else:
                sql = "SELECT CHECKNAME, COLNAME FROM SYSIBM.SYSCHECKDEP WHERE TBOWNER='%(schema)s' AND TBNAME='%(table)s'" % {'schema': schema.upper(), 'table': table_name.upper()}
            cursor.execute(sql)
            for constname, colname in cursor.fetchall():
                if constname not in constraints:
                    constraints[constname] = {
                        'columns': [],
                        'primary_key': False,
                        'unique': False,
                        'foreign_key': None,
                        'check': True,
                        'index': False
                    }
                constraints[constname]['columns'].append(colname.lower())
                
            if getattr(cursor.connection, dbms_name) != 'DB2':
                sql = "SELECT KEYCOL.CONSTNAME, KEYCOL.COLNAME FROM SYSCAT.KEYCOLUSE KEYCOL INNER JOIN SYSCAT.TABCONST TABCONST ON KEYCOL.CONSTNAME=TABCONST.CONSTNAME WHERE TABCONST.TABSCHEMA='%(schema)s' and TABCONST.TABNAME='%(table)s' and TABCONST.TYPE='U'" % {'schema': schema.upper(), 'table': table_name.upper()}
            else:
                sql = "SELECT KEYCOL.CONSTNAME, KEYCOL.COLNAME FROM SYSIBM.SYSKEYCOLUSE KEYCOL INNER JOIN SYSIBM.SYSTABCONST TABCONST ON KEYCOL.CONSTNAME=TABCONST.CONSTNAME WHERE TABCONST.TBCREATOR='%(schema)s' AND TABCONST.TBNAME='%(table)s' AND TABCONST.TYPE='U'" % {'schema': schema.upper(), 'table': table_name.upper()}
            cursor.execute(sql)
            for constname, colname in cursor.fetchall():
                if constname not in constraints:
                    constraints[constname] = {
                        'columns': [],
                        'primary_key': False,
                        'unique': True,
                        'foreign_key': None,
                        'check': False,
                        'index': True
                    }
                constraints[constname]['columns'].append(colname.lower())
            
            for pkey in cursor.connection.primary_keys(None, schema, table_name):
                if pkey['PK_NAME'] not in constraints:
                    constraints[pkey['PK_NAME']] = {
                        'columns': [],
                        'primary_key': True,
                        'unique': False,
                        'foreign_key': None,
                        'check': False,
                        'index': True
                    }
                constraints[pkey['PK_NAME']]['columns'].append(pkey['COLUMN_NAME'].lower())    
            
            for fk in cursor.connection.foreign_keys( True, schema, table_name ):
                if fk['FK_NAME'] not in constraints:
                    constraints[fk['FK_NAME']] = {
                        'columns': [],
                        'primary_key': False,
                        'unique': False,
                        'foreign_key': (fk['PKTABLE_NAME'].lower(), fk['PKCOLUMN_NAME'].lower()),
                        'check': False,
                        'index': False
                    }
                constraints[fk['FK_NAME']]['columns'].append(fk['FKCOLUMN_NAME'].lower())
                if fk['PKCOLUMN_NAME'].lower() not in constraints[fk['FK_NAME']]['foreign_key']:
                    fkeylist = list(constraints[fk['FK_NAME']]['foreign_key'])
                    fkeylist.append(fk['PKCOLUMN_NAME'].lower())
                    constraints[fk['FK_NAME']]['foreign_key'] = tuple(fkeylist)
                
            for index in cursor.connection.indexes( True, schema, table_name ):
                if index['INDEX_NAME'] not in constraints:
                    constraints[index['INDEX_NAME']] = {
                        'columns': [],
                        'primary_key': False,
                        'unique': False,
                        'foreign_key': None,
                        'check': False,
                        'index': True
                    }
                elif constraints[index['INDEX_NAME']]['unique'] :
                    continue
                elif constraints[index['INDEX_NAME']]['primary_key']:
                    continue
                constraints[index['INDEX_NAME']]['columns'].append(index['COLUMN_NAME'].lower())
            return constraints
