
#ifdef PASE
#define IBM_DB_UTF8
#endif


#ifdef IBM_DB_UTF8
#define SQLTCHAR SQLCHAR
#define SQL_C_TCHAR SQL_C_CHAR

#define SQLColAttributeT SQLColAttribute
#define SQLColAttributesT SQLColAttributes
#define SQLColumnPrivilegesT SQLColumnPrivileges
#define SQLColumnsT SQLColumns
#define SQLConnectT SQLConnect
#define SQLDataSourcesT SQLDataSources
#define SQLDescribeColT SQLDescribeCol
#define SQLDriverConnectT SQLDriverConnect
#define SQLErrorT SQLError
#define SQLExecDirectT SQLExecDirect
#define SQLForeignKeysT SQLForeignKeys
#define SQLGetConnectOptionT SQLGetConnectOption
#define SQLGetCursorNameT SQLGetCursorName
#define SQLGetConnectAttrT SQLGetConnectAttr
#define SQLGetDescFieldT SQLGetDescField
#define SQLGetDescRecT SQLGetDescRec
#define SQLGetDiagFieldT SQLGetDiagField
#define SQLGetDiagRecT SQLGetDiagRec
#define SQLGetInfoT SQLGetInfo
#define SQLGetPositionT SQLGetPosition
#define SQLGetStmtAttrT SQLGetStmtAttr
#define SQLGetStmtOptionT SQLGetStmtOption
#define SQLGetSubStringT SQLGetSubString
#define SQLGetTypeInfoT SQLGetTypeInfo
#define SQLNativeSqlT SQLNativeSql
#define SQLPrepareT SQLPrepare
#define SQLPrimaryKeysT SQLPrimaryKeys
#define SQLProcedureColumnsT SQLProcedureColumns
#define SQLProceduresT SQLProcedures
#define SQLSetConnectAttrT SQLSetConnectAttr
#define SQLSetConnectOptionT SQLSetConnectOption
#define SQLSetCursorNameT SQLSetCursorName
#define SQLSetDescFieldT SQLSetDescField
#define SQLSetStmtAttrT SQLSetStmtAttr
#define SQLSetStmtOptionT SQLSetStmtOption
#define SQLSpecialColumnsT SQLSpecialColumns
#define SQLStatisticsT SQLStatistics
#define SQLTablePrivilegesT SQLTablePrivileges
#define SQLTablesT SQLTables
#else
#define SQLTCHAR SQLWCHAR
#define SQL_C_TCHAR SQL_C_WCHAR

#define SQLColAttributeT SQLColAttributeW
#define SQLColAttributesT SQLColAttributesW
#define SQLColumnPrivilegesT SQLColumnPrivilegesW
#define SQLColumnsT SQLColumnsW
#define SQLConnectT SQLConnectW
#define SQLDataSourcesT SQLDataSourcesW
#define SQLDescribeColT SQLDescribeColW
#define SQLDriverConnectT SQLDriverConnectW
#define SQLErrorT SQLErrorW
#define SQLExecDirectT SQLExecDirectW
#define SQLForeignKeysT SQLForeignKeysW
#define SQLGetConnectOptionT SQLGetConnectOptionW
#define SQLGetCursorNameT SQLGetCursorNameW
#define SQLGetConnectAttrT SQLGetConnectAttrW
#define SQLGetDescFieldT SQLGetDescFieldW
#define SQLGetDescRecT SQLGetDescRecW
#define SQLGetDiagFieldT SQLGetDiagFieldW
#define SQLGetDiagRecT SQLGetDiagRecW
#define SQLGetInfoT SQLGetInfoW
#define SQLGetPositionT SQLGetPositionW
#define SQLGetStmtAttrT SQLGetStmtAttrW
#define SQLGetStmtOptionT SQLGetStmtOptionW
#define SQLGetSubStringT SQLGetSubStringW
#define SQLGetTypeInfoT SQLGetTypeInfoW
#define SQLNativeSqlT SQLNativeSqlW
#define SQLPrepareT SQLPrepareW
#define SQLPrimaryKeysT SQLPrimaryKeysW
#define SQLProcedureColumnsT SQLProcedureColumnsW
#define SQLProceduresT SQLProceduresW
#define SQLSetConnectAttrT SQLSetConnectAttrW
#define SQLSetConnectOptionT SQLSetConnectOptionW
#define SQLSetCursorNameT SQLSetCursorNameW
#define SQLSetDescFieldT SQLSetDescFieldW
#define SQLSetStmtAttrT SQLSetStmtAttrW
#define SQLSetStmtOptionT SQLSetStmtOptionW
#define SQLSpecialColumnsT SQLSpecialColumnsW
#define SQLStatisticsT SQLStatisticsW
#define SQLTablePrivilegesT SQLTablePrivilegesW
#define SQLTablesT SQLTablesW
#endif
