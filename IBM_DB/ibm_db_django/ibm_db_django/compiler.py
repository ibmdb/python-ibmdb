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

from django.db.models.sql import compiler
import sys
if sys.version_info >= (3, ):
    try:
        from itertools import zip_longest
    except ImportError:
        from itertools import izip_longest as zip_longest
# For checking django's version
from django import VERSION as djangoVersion
        
class SQLCompiler( compiler.SQLCompiler ):
    __rownum = 'Z.__ROWNUM'

    # To get ride of LIMIT/OFFSET problem in DB2, this method has been implemented.
    def as_sql( self, with_limits=True, with_col_aliases=False, subquery=False ):
        self.subquery = subquery
        self.__do_filter( self.query.where.children )
        self.pre_sql_setup()
        if self.query.distinct:
            if ((self.connection.settings_dict.keys()).__contains__('FETCH_DISTINCT_ON_TEXT')) and not self.connection.settings_dict['FETCH_DISTINCT_ON_TEXT']:
                out_cols = self.get_columns(False)
                for col in out_cols:
                    col = col.split(".")[1].replace('"', '').lower()
                    field = self.query.model._meta.get_field_by_name(col)[0]
                    fieldType = field.get_internal_type()
                    if fieldType == 'TextField':
                        self.query.distinct = False
                        break
        if not ( with_limits and ( self.query.high_mark is not None or self.query.low_mark ) ):
            return super( SQLCompiler, self ).as_sql( False, with_col_aliases )
        else:
            if self.query.high_mark == self.query.low_mark:
                return '', ()
            
            sql_ori, params = super( SQLCompiler, self ).as_sql( False, with_col_aliases )
            if self.query.low_mark is 0:
                return sql_ori + " FETCH FIRST %s ROWS ONLY" % ( self.query.high_mark ), params
            sql_split = sql_ori.split( " FROM " )
            
            sql_sec = ""
            if len( sql_split ) > 2:
                for i in range( 1, len( sql_split ) ):
                    sql_sec = " %s FROM %s " % ( sql_sec, sql_split[i] )
            else:
                sql_sec = " FROM %s " % ( sql_split[1] )
            
            dummyVal = "Z.__db2_"
            sql_pri = ""
            
            sql_sel = "SELECT"
            if self.query.distinct:
                sql_sel = "SELECT DISTINCT"

            sql_select_token = sql_split[0].split( "," )
            i = 0
            while ( i < len( sql_select_token ) ):
                if sql_select_token[i].count( "TIMESTAMP(DATE(SUBSTR(CHAR(" ) == 1:
                    sql_sel = "%s \"%s%d\"," % ( sql_sel, dummyVal, i + 1 )
                    sql_pri = '%s %s,%s,%s,%s AS "%s%d",' % ( 
                                    sql_pri,
                                    sql_select_token[i],
                                    sql_select_token[i + 1],
                                    sql_select_token[i + 2],
                                    sql_select_token[i + 3],
                                    dummyVal, i + 1 )
                    i = i + 4
                    continue
                
                if sql_select_token[i].count( " AS " ) == 1:
                    temp_col_alias = sql_select_token[i].split( " AS " )
                    sql_pri = '%s %s,' % ( sql_pri, sql_select_token[i] )
                    sql_sel = "%s %s," % ( sql_sel, temp_col_alias[1] )
                    i = i + 1
                    continue
            
                sql_pri = '%s %s AS "%s%d",' % ( sql_pri, sql_select_token[i], dummyVal, i + 1 )
                sql_sel = "%s \"%s%d\"," % ( sql_sel, dummyVal, i + 1 )
                i = i + 1

            sql_pri = sql_pri[:len( sql_pri ) - 1]
            sql_pri = "%s%s" % ( sql_pri, sql_sec )
            sql_sel = sql_sel[:len( sql_sel ) - 1]
            sql = '%s, ( ROW_NUMBER() OVER() ) AS "%s" FROM ( %s ) AS M' % ( sql_sel, self.__rownum, sql_pri )
            sql = '%s FROM ( %s ) Z WHERE' % ( sql_sel, sql )
            
            if self.query.low_mark is not 0:
                sql = '%s "%s" > %d' % ( sql, self.__rownum, self.query.low_mark )
                
            if self.query.low_mark is not 0 and self.query.high_mark is not None:
                sql = '%s AND ' % ( sql )

            if self.query.high_mark is not None:
                sql = '%s "%s" <= %d' % ( sql, self.__rownum, self.query.high_mark )

        return sql, params
    
    def __map23(self, value, field):
        if sys.version_info >= (3, ):
            return zip_longest(value, field)
        else:
            return map(None, value, field)
        
    #This function  convert 0/1 to boolean type for BooleanField/NullBooleanField
    def resolve_columns( self, row, fields = () ):
        values = []
        index_extra_select = len( self.query.extra_select.keys() )
        for value, field in self.__map23( row[index_extra_select:], fields ):
            if ( field and field.get_internal_type() in ( "BooleanField", "NullBooleanField" ) and value in ( 0, 1 ) ):
                value = bool( value )
            values.append( value )
        return row[:index_extra_select] + tuple( values )
    
    # For case insensitive search, converting parameter value to upper case.
    # The right hand side will get converted to upper case in the SQL itself.
    def __do_filter( self, children ):
        for index in range( len( children ) ):
            if not isinstance( children[index], ( tuple, list ) ):
                if hasattr( children[index], 'children' ):
                    self.__do_filter( children[index].children )
            elif isinstance( children[index], tuple ):
                node = list( children[index] )
                if node[1].find( "iexact" ) != -1 or \
                    node[1].find( "icontains" ) != -1 or \
                    node[1].find( "istartswith" ) != -1 or \
                    node[1].find( "iendswith" ) != -1:
                    if node[2] == True:
                        node[3] = node[3].upper()
                        children[index] = tuple( node )

class SQLInsertCompiler( compiler.SQLInsertCompiler, SQLCompiler ):
    pass

class SQLDeleteCompiler( compiler.SQLDeleteCompiler, SQLCompiler ):
    pass

class SQLUpdateCompiler( compiler.SQLUpdateCompiler, SQLCompiler ):
    pass

class SQLAggregateCompiler( compiler.SQLAggregateCompiler, SQLCompiler ):
    pass

if djangoVersion[0:2] < ( 1, 8 ):
    class SQLDateCompiler(compiler.SQLDateCompiler, SQLCompiler):
        pass

if djangoVersion[0:2] >= ( 1, 6 ) and djangoVersion[0:2] < ( 1, 8 ):
    class SQLDateTimeCompiler(compiler.SQLDateTimeCompiler, SQLCompiler):
        pass
