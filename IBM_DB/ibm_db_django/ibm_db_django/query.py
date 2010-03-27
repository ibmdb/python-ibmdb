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
Custom Query class for DB2.
Derives from: django.db.models.sql.query.Query
"""

def query_class(QueryClass):
    
    class DB2QueryClass(QueryClass):
        __rownum = 'Z.__ROWNUM'
        
        # To get ride of LIMIT/OFFSET problem in DB2, this method has been implemented.
        def as_sql(self, with_limits=True, with_col_aliases=False):
            if not (with_limits and (self.high_mark is not None or self.low_mark)):
                return super(DB2QueryClass, self).as_sql(False, with_col_aliases)
            else:                
                self.pre_sql_setup()
                self.get_columns()
                extra_order_list = []
                if self.extra_order_by:
                    for extra_order_by in self.extra_order_by:
                        if(extra_order_by in self.extra_select):
                            extra_order_list.append(self.extra_select[extra_order_by][0])
                    for index in range(len(extra_order_list)):
                        self.extra_order_by[index] = extra_order_list[index]
                        self.extra_order_by[index] = extra_order_list[index]

                from django import VERSION as djangoVersion
                if (djangoVersion[0:2] <= (1, 0)):
                    order = self.get_ordering()
                else:
                    order, group_by = self.get_ordering()
                                
                if order is not None and len(order) is not 0:
                    order_sql = "ROW_NUMBER() OVER (ORDER BY %s)" % (self.__order_columns(order))
                else:
                    meta = self.model._meta
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
                
                sql_ori, params = super(DB2QueryClass, self).as_sql(False, with_col_aliases)
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
                if self.distinct:
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
                
                if self.low_mark is not 0:
                    sql = '%s "%s" > %d' % (sql, self.__rownum, self.low_mark)
                    
                if self.low_mark is not 0 and self.high_mark is not None:
                    sql = '%s AND ' % (sql)

                if self.high_mark is not None:
                    sql = '%s "%s" <= %d' % (sql, self.__rownum, self.high_mark)

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
        
        # http://www.python.org/dev/peps/pep-0307/
        # See Extended __reduce__ API
        def __reduce__(self):
            return (__newobj__, (QueryClass, ))
        
        # For case insensitive search, converting parameter value to upper case.
        # The right hand side will get converted to upper case in the SQL itself.
        from django.db.models.sql.where import AND
        def add_filter(self, filter_expr, connector=AND, negate=False, trim=False,
                       can_reuse=None, process_extras=True):
            if len(filter_expr) != 0 and filter_expr is not None:
                filter_expr = list(filter_expr)
                if filter_expr[0].find("__iendswith") != - 1 or \
                    filter_expr[0].find("__istartswith") != - 1 or \
                    filter_expr[0].find("__icontains") != - 1 or \
                    filter_expr[0].find("__iexact") != - 1:
                    filter_expr[1] = filter_expr[1].upper()
                    
                filter_expr = tuple(filter_expr)                    
            return super(DB2QueryClass, self).add_filter(filter_expr, connector,
                        negate, trim, can_reuse, process_extras)
            
    return DB2QueryClass

# Method to make DB2QueryClass picklable
def __newobj__(QueryClass):
    # http://www.python.org/dev/peps/pep-0307/
    # The __newobj__ unpickling function
    DB2QueryClass = query_class(QueryClass)
    return DB2QueryClass.__new__(DB2QueryClass)
