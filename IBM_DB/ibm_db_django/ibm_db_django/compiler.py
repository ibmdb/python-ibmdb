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

from django.db.models.sql import compiler

class SQLCompiler(compiler.SQLCompiler):
    __rownum = 'Z.__ROWNUM'

    # To get ride of LIMIT/OFFSET problem in DB2, this method has been implemented.
    def as_sql(self, with_limits=True, with_col_aliases=False):
        self.__do_filter(self.query.where.children)
        if not (with_limits and (self.query.high_mark is not None or self.query.low_mark)):
            return super(SQLCompiler, self).as_sql(False, with_col_aliases)
        else:                
            self.pre_sql_setup()
            self.get_columns()
            extra_order_list = []
            if self.query.extra_order_by:
                for extra_order_by in self.query.extra_order_by:
                    if(extra_order_by in self.query.extra_select):
                        extra_order_list.append(self.query.extra_select[extra_order_by][0])
                for index in range(len(extra_order_list)):
                    self.query.extra_order_by[index] = extra_order_list[index]
                    self.query.extra_order_by[index] = extra_order_list[index]

            order, group_by = self.get_ordering()                 
            if order is not None and len(order) is not 0:
                if not order == ['SYSFUN.RAND()']:
                    order_sql = "ROW_NUMBER() OVER (ORDER BY %s)" % (self.__order_columns(order))
                else:
                    order_sql = "ROW_NUMBER() OVER()"
            else:
                meta = self.query.model._meta
                db_table = meta.db_table
                db_pk_col = ""
                for field in meta.fields:
                    if field.primary_key:
                        if meta.pk.db_column:
                            db_pk_col = meta.pk.db_column
                        else:
                            db_pk_col = meta.pk.column
                        break
                order_sql = """
                                ROW_NUMBER() OVER (ORDER BY %s.%s ASC)
                            """ % (self.quote_name_unless_alias(db_table), 
                                   self.quote_name_unless_alias(db_pk_col)) 
            
            sql_ori, params = super(SQLCompiler, self).as_sql(False, with_col_aliases)
            sql_split = sql_ori.split(" FROM ")
            
            sql_sec = ""
            if len(sql_split) > 2:
                for i in range(1, len(sql_split)):
                    sql_sec = " %s FROM %s " % (sql_sec, sql_split[i])
            else:
                sql_sec = " FROM %s " % (sql_split[1])
            
            dummyVal = "Z.__db2_"
            sql_sel = ""
            
            sql = "SELECT"
            if self.query.distinct:
                sql = "SELECT DISTINCT"

            sql_select_token = sql_split[0].split(",")
            i = 0
            while (i < len(sql_select_token)):
                if sql_select_token[i].count("TIMESTAMP(DATE(SUBSTR(CHAR(") == 1:
                    sql = "%s \"%s%d\"," % (sql, dummyVal, i + 1)
                    sql_sel = '%s %s,%s,%s,%s AS "%s%d",' % (
                                    sql_sel, 
                                    sql_select_token[i], 
                                    sql_select_token[i + 1], 
                                    sql_select_token[i + 2], 
                                    sql_select_token[i + 3], 
                                    dummyVal, i + 1)
                    i = i + 4
                    continue
                
                if sql_select_token[i].count(" AS ") == 1:
                    temp = sql_select_token[i].split(" AS ")
                    sql_sel = '%s %s,' % (sql_sel, sql_select_token[i])
                    sql = "%s %s," % (sql, temp[1])
                    i = i + 1
                    continue
            
                sql_sel = '%s %s AS "%s%d",' % (sql_sel, sql_select_token[i], dummyVal, i + 1)
                sql = "%s \"%s%d\"," % (sql, dummyVal, i + 1)
                i = i + 1

            sql_sel = "%s, (%s) AS \"%s\"" % (sql_sel[1:len(sql_sel) - 1], order_sql, self.__rownum)
            sql_sel = "%s%s" % (sql_sel, sql_sec)
                
            sql = "%s FROM (%s) Z WHERE" % (sql[:len(sql) - 1], sql_sel)
            
            if self.query.low_mark is not 0:
                sql = '%s "%s" > %d' % (sql, self.__rownum, self.query.low_mark)
                
            if self.query.low_mark is not 0 and self.query.high_mark is not None:
                sql = '%s AND ' % (sql)

            if self.query.high_mark is not None:
                sql = '%s "%s" <= %d' % (sql, self.__rownum, self.query.high_mark)

        return sql, params
    
    # Converting array to String. In this method, orders argument is a list 
    # provided  by super class. Reading each element and converting them 
    # into a string, which will finally get appended to SQL.
    def __order_columns(self, orders):
        ret_order_columns = "%s"
        for i in range(len(orders)):
            if i is 0:
                ret_order_columns = ret_order_columns % (orders[i])
            else:
                ret_order_columns = ret_order_columns + ", %s" % (orders[i])
                
        return ret_order_columns
    
    # For case insensitive search, converting parameter value to upper case.
    # The right hand side will get converted to upper case in the SQL itself.
    def __do_filter(self, children):
        for index in range(len(children)):
            if not isinstance(children[index], (tuple, list)):
                if hasattr(children[index], 'children'):
                    self.__do_filter(children[index].children)
            elif isinstance(children[index], tuple):
                node = list(children[index])
                if node[1].find("iexact") != -1 or \
                    node[1].find("icontains") != -1 or \
                    node[1].find("istartswith") != -1 or \
                    node[1].find("iendswith") != -1:
                    if node[2] == True:
                        node[3] = node[3].upper()
                        children[index] = tuple(node)
    

class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    pass

class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):
    pass

class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):
    pass

class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    pass

class SQLDateCompiler(compiler.SQLDateCompiler, SQLCompiler):
    pass 
