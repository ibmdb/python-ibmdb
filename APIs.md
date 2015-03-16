API description of ibm\_db driver is given below. If you want to access the same for ibm\_db\_dbi wrapper, please visit [Python Database API Specification v2.0](http://www.python.org/dev/peps/pep-0249/)

# API Description for the ibm\_db driver #
> 

### ibm\_db.active ###

Description
> Py\_True/Py\_False ibm\_db.active(resource connection)
> Checks if the specified connection resource is active
> Returns Py\_True if the given connection resource is active
Parameters
connection
> > The connection resource to be validated.
Return Values

> Returns Py\_True if the given connection resource is active, otherwise it will
> return Py\_False


### ibm\_db.autocommit ###

Description
> mixed ibm\_db.autocommit ( resource connection [, bool value] )
> Returns or sets the AUTOCOMMIT behavior of the specified connection resource.
Parameters
connection
> > A valid database connection resource variable as returned from connect()

> or pconnect().
value
> > One of the following constants:
> > SQL\_AUTOCOMMIT\_OFF
> > > Turns AUTOCOMMIT off.

> > SQL\_AUTOCOMMIT\_ON
> > > Turns AUTOCOMMIT on.
Return Values

> When ibm\_db.autocommit() receives only the connection parameter, it returns
> the current state of AUTOCOMMIT for the requested connection as an integer
> value. A value of 0 indicates that AUTOCOMMIT is off, while a value of 1
> indicates that AUTOCOMMIT is on.
> When ibm\_db.autocommit() receives both the connection parameter and
> autocommit parameter, it attempts to set the AUTOCOMMIT state of the
> requested connection to the corresponding state.
> Returns TRUE on success or FALSE on failure.


### ibm\_db.bind\_param ###

Description
> Py\_True/Py\_None ibm\_db.bind\_param (resource stmt, int parameter-number,
> > string variable [, int parameter-type
> > [, int data-type [, int precision
> > [, int scale [, int size[.md](.md)]]]]] )

> Binds a Python variable to an SQL statement parameter in a IBM\_DBStatement
> resource returned by ibm\_db.prepare().
> This function gives you more control over the parameter type, data type,
> precision, and scale for the parameter than simply passing the variable as
> part of the optional input array to ibm\_db.execute().
Parameters
stmt
> > A prepared statement returned from ibm\_db.prepare().
parameter-number
> > Specifies the 1-indexed position of the parameter in the prepared

> statement.
variable
> > A Python variable to bind to the parameter specified by parameter-number.
parameter-type
> > A constant specifying whether the Python variable should be bound to the

> SQL parameter as an input parameter (SQL\_PARAM\_INPUT). To avoid memory overhead, you can also specify
> PARAM\_FILE to bind the Python variable to the name of a file that contains
> large object (BLOB, CLOB, or DBCLOB) data.
data-type
> > A constant specifying the SQL data type that the Python variable should be

> bound as: one of SQL\_BINARY, DB2\_CHAR, DB2\_DOUBLE, or DB2\_LONG .
precision
> > Specifies the precision that the variable should be bound to the database.
scale
> > > Specifies the scale that the variable should be bound to the database.

Return Values

> Returns Py\_True on success or NULL on failure.


### ibm\_db.client\_info ###

Description
> object ibm\_db.client\_info ( resource connection )
> This function returns a read-only object with information about the IBM Data
> Server database client. The following table lists the client properties:
IBM Data Server client properties
> APPL\_CODEPAGE:: The application code page.
> CONN\_CODEPAGE:: The code page for the current connection.
> DATA\_SOURCE\_NAME:: The data source name (DSN) used to create the current
> connection to the database.
> DRIVER\_NAME:: The name of the library that implements the Call Level
> Interface (CLI) specification.
> DRIVER\_ODBC\_VER:: The version of ODBC that the IBM Data Server client
> supports. This returns a string "MM.mm" where MM is the major version and mm
> is the minor version. The IBM Data Server client always returns "03.51".
> DRIVER\_VER:: The version of the client, in the form of a string "MM.mm.uuuu"
> where MM is the major version, mm is the minor version, and uuuu is the
> update. For example, "08.02.0001" represents major version 8, minor version
> 2, update 1. (string)
> ODBC\_SQL\_CONFORMANCE:: There are three levels of ODBC SQL grammar supported
> by the client: MINIMAL (Supports the minimum ODBC SQL grammar), CORE
> (Supports the core ODBC SQL grammar), EXTENDED (Supports extended ODBC SQL
> grammar).
> ODBC\_VER:: The version of ODBC that the ODBC driver manager supports. This
> returns a string "MM.mm.rrrr" where MM is the major version, mm is the minor
> version, and rrrr is the release. The client always returns "03.01.0000".
Parameters
connection
> > Specifies an active IBM Data Server client connection.
Return Values

> Returns an object on a successful call. Returns FALSE on failure.


### ibm\_db.close ###

Description
> bool ibm\_db.close ( resource connection )
> This function closes a DB2 client connection created with ibm\_db.connect()
> and returns the corresponding resources to the database server.
> If you attempt to close a persistent DB2 client connection created with
> ibm\_db.pconnect(), the close request returns TRUE and the persistent IBM Data
> Server client connection remains available for the next caller.
Parameters
connection
> > Specifies an active DB2 client connection.
Return Values

> Returns TRUE on success or FALSE on failure.


### ibm\_db.column\_privileges ###

Description
> resource ibm\_db.column\_privileges ( resource connection [, string qualifier
> [, string schema [, string table-name [, string column-name]]]] )
> Returns a result set listing the columns and associated privileges for a
> table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. To match all schemas, pass NULL

> or an empty string.
table-name
> > The name of the table or view. To match all tables in the database,

> pass NULL or an empty string.
column-name
> > The name of the column. To match all columns in the table, pass NULL

> or an empty string.
Return Values
> Returns a statement resource with a result set containing rows describing
> the column privileges for columns matching the specified parameters. The rows
> are composed of the following columns:
> TABLE\_CAT:: Name of the catalog. The value is NULL if this table does not
> have catalogs.
> TABLE\_SCHEM:: Name of the schema.
> TABLE\_NAME:: Name of the table or view.
> COLUMN\_NAME:: Name of the column.
> GRANTOR:: Authorization ID of the user who granted the privilege.
> GRANTEE:: Authorization ID of the user to whom the privilege was granted.
> PRIVILEGE:: The privilege for the column.
> IS\_GRANTABLE:: Whether the GRANTEE is permitted to grant this privilege to
> other users.


### ibm\_db.columns ###

Description
> resource ibm\_db.columns ( resource connection [, string qualifier
> [, string schema [, string table-name [, string column-name]]]] )
> Returns a result set listing the columns and associated metadata for a table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. To match all schemas, pass '%'.
table-name
> > The name of the table or view. To match all tables in the database,

> pass NULL or an empty string.
column-name
> > The name of the column. To match all columns in the table, pass NULL or

> an empty string.
Return Values
> Returns a statement resource with a result set containing rows describing the
> columns matching the specified parameters.
> The rows are composed of the following columns:
> TABLE\_CAT:: Name of the catalog. The value is NULL if this table does not
> have catalogs.
> TABLE\_SCHEM:: Name of the schema.
> TABLE\_NAME:: Name of the table or view.
> COLUMN\_NAME:: Name of the column.
> DATA\_TYPE:: The SQL data type for the column represented as an integer value.
> TYPE\_NAME:: A string representing the data type for the column.
> COLUMN\_SIZE:: An integer value representing the size of the column.
> BUFFER\_LENGTH:: Maximum number of bytes necessary to store data from this
> column.
> DECIMAL\_DIGITS:: The scale of the column, or NULL where scale is not
> applicable.
> NUM\_PREC\_RADIX:: An integer value of either 10 (representing an exact numeric
> data type), 2 (representing an approximate numeric data type), or NULL
> (representing a data type for which radix is not applicable).
> NULLABLE:: An integer value representing whether the column is nullable or
> not.
> REMARKS:: Description of the column.
> COLUMN\_DEF:: Default value for the column.
> SQL\_DATA\_TYPE:: An integer value representing the size of the column.
> SQL\_DATETIME\_SUB:: Returns an integer value representing a datetime subtype
> code, or NULL for SQL data types to which this does not apply.
> CHAR\_OCTET\_LENGTH::   Maximum length in octets for a character data type
> column, which matches COLUMN\_SIZE for single-byte character set data, or
> NULL for non-character data types.
> ORDINAL\_POSITION:: The 1-indexed position of the column in the table.
> IS\_NULLABLE:: A string value where 'YES' means that the column is nullable
> and 'NO' means that the column is not nullable.


### ibm\_db.commit ###

Description
> bool ibm\_db.commit ( resource connection )
> Commits an in-progress transaction on the specified connection resource and
> begins a new transaction.
> Python applications normally default to AUTOCOMMIT mode, so ibm\_db.commit()
> is not necessary unless AUTOCOMMIT has been turned off for the connection
> resource.
> Note: If the specified connection resource is a persistent connection, all
> transactions in progress for all applications using that persistent
> connection will be committed. For this reason, persistent connections are
> not recommended for use in applications that require transactions.
Parameters
connection
> > A valid database connection resource variable as returned from

> ibm\_db.connect() or ibm\_db.pconnect().
Return Values
> Returns TRUE on success or FALSE on failure.


### ibm\_db.conn\_error ###

Description
> string ibm\_db.conn\_errormsg ( [connection](resource.md) )
> ibm\_db.conn\_errormsg() returns an error message and SQLCODE value
> representing the reason the last database connection attempt failed.
> As ibm\_db.connect() returns FALSE in the event of a failed connection
> attempt, do not pass any parameters to ibm\_db.conn\_errormsg() to retrieve
> the associated error message and SQLCODE value.
> If, however, the connection was successful but becomes invalid over time,
> you can pass the connection parameter to retrieve the associated error
> message and SQLCODE value for a specific connection.
Parameters
connection
> > A connection resource associated with a connection that initially

> succeeded, but which over time became invalid.
Return Values
> Returns a string containing the error message and SQLCODE value resulting
> from a failed connection attempt. If there is no error associated with the
> last connection attempt, ibm\_db.conn\_errormsg() returns an empty string.


### ibm\_db.conn\_errormsg ###

Description
> string ibm\_db.conn\_errormsg ( [connection](resource.md) )
> ibm\_db.conn\_errormsg() returns an error message and SQLCODE value
> representing the reason the last database connection attempt failed.
> As ibm\_db.connect() returns FALSE in the event of a failed connection
> attempt, do not pass any parameters to ibm\_db.conn\_errormsg() to retrieve
> the associated error message and SQLCODE value.
> If, however, the connection was successful but becomes invalid over time,
> you can pass the connection parameter to retrieve the associated error
> message and SQLCODE value for a specific connection.
Parameters
connection
> > A connection resource associated with a connection that initially

> succeeded, but which over time became invalid.
Return Values
> Returns a string containing the error message and SQLCODE value resulting
> from a failed connection attempt. If there is no error associated with the
> last connection attempt, ibm\_db.conn\_errormsg() returns an empty string.


### ibm\_db.connect ###

Description
> --   Returns a connection to a database
> IBM\_DBConnection ibm\_db.connect(string database, string user , string password [,
dictionary options])
> Creates a new connection to an IBM DB2 Universal Database, IBM Cloudscape,
> or Apache Derby database.
Parameters
database
> For a cataloged connection to a database, this parameter represents the database alias in the DB2 client catalog.
> For an uncataloged connection to a database, database represents a complete
> connection string in the following format:
> DRIVER={IBM DB2 ODBC DRIVER};DATABASE=database;HOSTNAME=hostname;PORT=port;
> PROTOCOL=TCPIP;UID=username;PWD=password;
> > where the parameters represent the following values:
> > > hostname
> > > > The hostname or IP address of the database server.

> > > port
> > > > The TCP/IP port on which the database is listening for requests.

> > > username
> > > > The username with which you are connecting to the database.

> > > password
> > > > The password with which you are connecting to the database.
user

> The username with which you are connecting to the database.
> For uncataloged connections, you must pass an empty string.
password
> The password with which you are connecting to the database.
> For uncataloged connections, you must pass an empty string.
options
> > An dictionary of connection options that affect the behavior of the
> > connection,
> > where valid array keys include:
> > > SQL\_ATTR\_AUTOCOMMIT
> > > > Passing the SQL\_AUTOCOMMIT\_ON value turns autocommit on for this
> > > > connection handle.
> > > > Passing the SQL\_AUTOCOMMIT\_OFF value turns autocommit off for this
> > > > connection handle.

> > > ATTR\_CASE
> > > > Passing the CASE\_NATURAL value specifies that column names are
> > > > returned in natural case.
> > > > Passing the CASE\_LOWER value specifies that column names are
> > > > returned in lower case.
> > > > Passing the CASE\_UPPER value specifies that column names are
> > > > returned in upper case.

> > > SQL\_ATTR\_CURSOR\_TYPE
> > > > Passing the SQL\_SCROLL\_FORWARD\_ONLY value specifies a forward-only
> > > > cursor for a statement resource.
> > > > This is the default cursor type and is supported on all database
> > > > servers.
> > > > Passing the SQL\_CURSOR\_KEYSET\_DRIVEN value specifies a scrollable
> > > > cursor for a statement resource.
> > > > This mode enables random access to rows in a result set, but
> > > > currently is supported only by IBM DB2 Universal Database.
set\_replace\_quoted\_literal

> > This variable indicates if the CLI Connection attribute SQL\_ATTR\_REPLACE\_QUOTED\_LITERAL is to be set or not


> To turn it ON pass  ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_ON

> To turn it OFF pass ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_OFF

> Default Setting: - ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_ON
Return Values
> Returns a IBM\_DBConnection connection object if the connection attempt is
> successful.
> If the connection attempt fails, ibm\_db.connect() returns None.

```xml

Note: Local cataloged database implicit connection
i) If database parameter specified is a local database alias name with blank userid and password
then connect/pconnect API will use current logged in user's userid for implicit connection
eg: conn = ibm_db.connect('sample', '', '')
ii) If database parameter is a connection string with value "DSN=database_name" then
connect/pconnect API will use current logged in user's userid for implicit connection
eg: conn = ibm_db.connect('DSN=sample', '', '')
```

### ibm\_db.createdb ###

Description
> True/None ibm\_db.createdb ( IBM\_DBConnection connection, string dbName [, codeSet, mode] )
> Creates a database by using the specified database name, code set and mode
Parameters
connection
> > A valid database server instance connection resource variable as returned from ibm\_db.connect() by specifying the ATTACH keyword.
dbName
> > Name of the database that is to be created.
codeSet
> > Database code set information.
> > Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
mode
> > Database logging mode.
> > Note: This value is applicable only to IDS data servers.
Return Value

> Returns True on successful creation of database else return None.


### ibm\_db.createdbNX ###

Description
> True/None ibm\_db.createdbNX ( IBM\_DBConnection connection, string dbName [, codeSet, mode] )
> Creates the database if not exist by using the specified database name, code set and mode.
Parameters
connection
> > A valid database server instance connection resource variable as returned from ibm\_db.connect() by specifying the ATTACH keyword.
dbName
> > Name of the database that is to be created.
codeSet
> > Database code set information.
> > Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
mode
> > Database logging mode.
> > Note: This value is applicable only to IDS data servers.
Return Value

> Returns True if database already exists or created successfully else return None


### ibm\_db.cursor\_type ###

Description
> int ibm\_db.cursor\_type ( resource stmt )
> Returns the cursor type used by a statement resource. Use this to determine
> if you are working with a forward-only cursor or scrollable cursor.
Parameters
stmt
> > A valid statement resource.
Return Values

> Returns either SQL\_SCROLL\_FORWARD\_ONLY if the statement resource uses a
> forward-only cursor or SQL\_CURSOR\_KEYSET\_DRIVEN if the statement resource
> uses a scrollable cursor.


### ibm\_db.dropdb ###

Description
> True/None ibm\_db.dropdb ( IBM\_DBConnection connection, string dbName )
> Drops the specified database
Parameters
connection
> > A valid database server instance connection resource variable as returned from ibm\_db.connect() by specifying the ATTACH keyword.
dbName
> > Name of the database that is to be dropped.
Return Value
> > Returns True if specified database dropped successfully else None.


### ibm\_db.exec\_immediate ###

Description

> stmt\_handle ibm\_db.exec\_immediate( IBM\_DBConnection connection, string statement
> > [, array options] )

> Prepares and executes an SQL statement.
> If you plan to interpolate Python variables into the SQL statement,
> understand that this is one of the more common security exposures. Consider
> calling ibm\_db.prepare() to prepare an SQL statement with parameter markers for input values. Then you can call ibm\_db.execute() to pass in the input
> values and avoid SQL injection attacks.
> If you plan to repeatedly issue the same SQL statement with different
> parameters, consider calling ibm\_db.:prepare() and ibm\_db.execute() to
> enable the database server to reuse its access plan and increase the
> efficiency of your database access.
Parameters
connection
> > A valid database connection resource variable as returned from

> ibm\_db.connect() or ibm\_db.pconnect().
statement
> > An SQL statement. The statement cannot contain any parameter markers.
options
> > An dictionary containing statement options. You can use this parameter to request a scrollable cursor on database servers that support this

> functionality.
> > SQL\_ATTR\_CURSOR\_TYPE
> > > Passing the SQL\_SCROLL\_FORWARD\_ONLY value requests a forward-only
> > > cursor for this SQL statement. This is the default type of
> > > cursor, and it is supported by all database servers. It is also
> > > much faster than a scrollable cursor.
> > > Passing the SQL\_CURSOR\_KEYSET\_DRIVEN value requests a scrollable
> > > cursor for this SQL statement. This type of cursor enables you to
> > > fetch rows non-sequentially from the database server. However, it
> > > is only supported by DB2 servers, and is much slower than
> > > forward-only cursors.
Return Values

> Returns a stmt\_handle resource if the SQL statement was issued
> successfully, or FALSE if the database failed to execute the SQL statement.


### ibm\_db.execute ###

Description
> `Py_True/Py_False ibm_db.execute ( IBM_DBStatement stmt [, tuple parameters] )` ibm\_db.execute() executes an SQL statement that was prepared by ibm\_db.prepare(). If the SQL statement returns a result set, for example, a SELECT statement that returns one or more result sets, you can retrieve a row as an tuple/dictionary from the stmt resource using ibm\_db.fetch\_assoc(), ibm\_db.fetch\_both(), or ibm\_db.fetch\_tuple(). Alternatively, you can use ibm\_db.fetch\_row() to move the result set pointer to the next row and fetch a column at a time from that row with ibm\_db.result(). Refer to ibm\_db.prepare() for a brief discussion of the advantages of using ibm\_db.prepare() and ibm\_db.execute() rather than ibm\_db.exec\_immediate(). To execute stored procedure refer ibm\_db.callproc()
Parameters
stmt
> > A prepared statement returned from ibm\_db.prepare().
parameters
> > An tuple of input parameters matching any parameter markers contained

> in the prepared statement.
Return Values
> Returns Py\_True on success or Py\_False on failure.

### ibm\_db.execute\_many ###

Description
> `int/NULL ibm_db.execute_many( IBM_DBStatement stmt, tuple seq_of_parameters )` ibm\_db.execute\_many() executes an SQL statement prepared by ibm\_db.prepare() against all parameter sequences or mappings found in the sequence seq\_of\_parameters.
> Use this function for bulk insert/update/delete operations. It uses ArrayInputChaining feature of DB2 CLI to ensure minimum roundtrips to the server.
> It returns the number of inserted/updated/deleted rows if the batch executed successfully or returns NULL if batch fully or partialy failed. When NULL is returned, use ibm\_db.num\_rows() to find out the inserted/updated/deleted row count.
> Samples for the API usage can be referred from test\_execute\_many.py.

Parameters
stmt
> A prepared statement returned from ibm\_db.prepare().
seq\_of\_parameters
> A tuple of input parameters matching parameter markers contained in the prepared statement.
Return Values
> Returns number of rows affected if whole batch executed sucessfully, or NULL if batch fully or partialy failed

### ibm\_db.fetch\_tuple ###

Description
> array ibm\_db.fetch\_tuple ( resource stmt [, int row\_number] )
> Returns a tuple, indexed by column position, representing a row in a result
> set. The columns are 0-indexed.
Parameters
stmt
> > A valid stmt resource containing a result set.
row\_number
> > Requests a specific 1-indexed row from the result set. Passing this

> parameter results in a warning if the result set uses a forward-only cursor.
Return Values
> Returns a 0-indexed tuple with column values indexed by the column position
> representing the next or requested row in the result set. Returns FALSE if
> there are no rows left in the result set, or if the row requested by
> row\_number does not exist in the result set.


### ibm\_db.fetch\_assoc ###

Description
> dictionary ibm\_db.fetch\_assoc ( resource stmt [, int row\_number] )
> Returns a dictionary, indexed by column name, representing a row in a result set.
Parameters
stmt
> > A valid stmt resource containing a result set.
row\_number
> > Requests a specific 1-indexed row from the result set. Passing this

> parameter results in a
> > Python warning if the result set uses a forward-only cursor.
Return Values

> Returns an associative array with column values indexed by the column name
> representing the next
> or requested row in the result set. Returns FALSE if there are no rows left
> in the result set,
> or if the row requested by row\_number does not exist in the result set.


### ibm\_db.fetch\_both ###

Description
> dictionary ibm\_db.fetch\_both ( resource stmt [, int row\_number] )
> Returns a dictionary, indexed by both column name and position, representing a row in a result set. Note that the row returned by ibm\_db.fetch\_both()
> requires more memory than the single-indexed dictionaries/arrays returned by ibm\_db.fetch\_assoc() or ibm\_db.fetch\_tuple().
Parameters
stmt
> > A valid stmt resource containing a result set.
row\_number
> > Requests a specific 1-indexed row from the result set. Passing this

> parameter results in a warning if the result set uses a forward-only cursor.
Return Values
> Returns a dictionary with column values indexed by both the column name and
> 0-indexed column number.
> The dictionary represents the next or requested row in the result set.
> Returns FALSE if there are no rows left in the result set, or if the row
> requested by row\_number does not exist in the result set.


### ibm\_db.fetch\_row ###

Description
> bool ibm\_db.fetch\_row ( resource stmt [, int row\_number] )
> Sets the result set pointer to the next row or requested row
> Use ibm\_db.fetch\_row() to iterate through a result set, or to point to a
> specific row in a result set if you requested a scrollable cursor.
> To retrieve individual fields from the result set, call the ibm\_db.result()
> function. Rather than calling ibm\_db.fetch\_row() and ibm\_db.result(), most
> applications will call one of ibm\_db.fetch\_assoc(), ibm\_db.fetch\_both(), or
> ibm\_db.fetch\_tuple() to advance the result set pointer and return a complete
> row as an array.
Parameters
stmt
> > A valid stmt resource.
row\_number
> > With scrollable cursors, you can request a specific row number in the

> result set. Row numbering is 1-indexed.
Return Values
> Returns TRUE if the requested row exists in the result set. Returns FALSE if
> the requested row does not exist in the result set.


### ibm\_db.field\_display\_size ###

Description
> int ibm\_db.field\_display\_size ( resource stmt, mixed column )
> Returns the maximum number of bytes required to display a column in a result
> set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns an integer value with the maximum number of bytes required to display
> the specified column.
> If the column does not exist in the result set, ibm\_db.field\_display\_size()
> returns FALSE.


### ibm\_db.field\_name ###

Description
> string ibm\_db.field\_name ( resource stmt, mixed column )
> Returns the name of the specified column in the result set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns a string containing the name of the specified column. If the
> specified column does not exist in the result set, ibm\_db.field\_name()
> returns FALSE.


### ibm\_db.field\_num ###

Description
> int ibm\_db.field\_num ( resource stmt, mixed column )
> Returns the position of the named column in a result set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns an integer containing the 0-indexed position of the named column in
> the result set. If the specified column does not exist in the result set,
> ibm\_db.field\_num() returns FALSE.


### ibm\_db.field\_precision ###

Description
> int ibm\_db.field\_precision ( resource stmt, mixed column )
> Returns the precision of the indicated column in a result set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns an integer containing the precision of the specified column. If the
> specified column does not exist in the result set, ibm\_db.field\_precision()
> returns FALSE.


### ibm\_db.field\_scale ###

Description
> int ibm\_db.field\_scale ( resource stmt, mixed column )
> Returns the scale of the indicated column in a result set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns an integer containing the scale of the specified column. If the
> specified column does not exist in the result set, ibm\_db.field\_scale()
> returns FALSE.


### ibm\_db.field\_type ###

Description
> string ibm\_db.field\_type ( resource stmt, mixed column )
> Returns the data type of the indicated column in a result set.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns a string containing the defined data type of the specified column.
> If the specified column does not exist in the result set, ibm\_db.field\_type()
> returns FALSE.


### ibm\_db.field\_width ###

Description
> int ibm\_db.field\_width ( resource stmt, mixed column )
> Returns the width of the current value of the indicated column in a result
> set. This is the maximum width of the column for a fixed-length data type, or
> the actual width of the column for a variable-length data type.
Parameters
stmt
> > Specifies a statement resource containing a result set.
column
> > Specifies the column in the result set. This can either be an integer

> representing the 0-indexed position of the column, or a string containing the
> name of the column.
Return Values
> Returns an integer containing the width of the specified character or binary
> data type column in a result set. If the specified column does not exist in
> the result set, ibm\_db.field\_width() returns FALSE.


### ibm\_db.foreign\_keys ###

Description
> resource ibm\_db.foreign\_keys ( resource connection, string qualifier,
> string schema, string table-name )
> Returns a result set listing the foreign keys for a table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. If schema is NULL,

> ibm\_db.foreign\_keys() matches the schema for the current connection.
table-name
> > The name of the table.
Return Values

> Returns a statement resource with a result set containing rows describing the
> foreign keys for the specified table. The result set is composed of the
> following columns:
> Column name::   Description
> PKTABLE\_CAT:: Name of the catalog for the table containing the primary key.
> The value is NULL if this table does not have catalogs.
> PKTABLE\_SCHEM:: Name of the schema for the table containing the primary key.
> PKTABLE\_NAME:: Name of the table containing the primary key.
> PKCOLUMN\_NAME:: Name of the column containing the primary key.
> FKTABLE\_CAT:: Name of the catalog for the table containing the foreign key.
> The value is NULL if this table does not have catalogs.
> FKTABLE\_SCHEM:: Name of the schema for the table containing the foreign key.
> FKTABLE\_NAME:: Name of the table containing the foreign key.
> FKCOLUMN\_NAME:: Name of the column containing the foreign key.
> KEY\_SEQ:: 1-indexed position of the column in the key.
> UPDATE\_RULE:: Integer value representing the action applied to the foreign
> key when the SQL operation is UPDATE.
> DELETE\_RULE:: Integer value representing the action applied to the foreign
> key when the SQL operation is DELETE.
> FK\_NAME:: The name of the foreign key.
> PK\_NAME:: The name of the primary key.
> DEFERRABILITY:: An integer value representing whether the foreign key
> deferrability is SQL\_INITIALLY\_DEFERRED, SQL\_INITIALLY\_IMMEDIATE, or
> SQL\_NOT\_DEFERRABLE.


### ibm\_db.free\_result ###

Description
> bool ibm\_db.free\_result ( resource stmt )
> Frees the system and database resources that are associated with a result
> set. These resources are freed implicitly when a script finishes, but you
> can call ibm\_db.free\_result() to explicitly free the result set resources
> before the end of the script.
Parameters
stmt
> > A valid statement resource.
Return Values

> Returns TRUE on success or FALSE on failure.


### ibm\_db.free\_stmt ###

Description
> bool ibm\_db.free\_stmt ( resource stmt )
> Frees the system and database resources that are associated with a statement
> resource. These resources are freed implicitly when a script finishes, but
> you can call ibm\_db.free\_stmt() to explicitly free the statement resources
> before the end of the script.
Parameters
stmt
> > A valid statement resource.
Return Values

> Returns TRUE on success or FALSE on failure.
> DEPRECATED


### ibm\_db.get\_option ###

Description
> mixed ibm\_db.get\_option ( resource resc, int options, int type )
> Returns a value, that is the current setting of a connection or statement
> attribute.
Parameters
resc
> > A valid connection or statement resource containing a result set.
options
> > The options to be retrieved
type
> > A field that specifies the resource type (1 = Connection,
> > non - 1 = Statement)
Return Values

> Returns the current setting of the resource attribute provided.


### ibm\_db.next\_result ###

Description
> resource ibm\_db.next\_result ( resource stmt )
> Requests the next result set from a stored procedure.
> A stored procedure can return zero or more result sets. While you handle the
> first result set in exactly the same way you would handle the results
> returned by a simple SELECT statement, to fetch the second and subsequent
> result sets from a stored procedure you must call the ibm\_db.next\_result()
> function and return the result to a uniquely named Python variable.
Parameters
stmt
> > A prepared statement returned from ibm\_db.exec\_immediate() or ibm\_db.execute().
Return Values

> Returns a new statement resource containing the next result set if the stored
> procedure returned another result set. Returns FALSE if the stored procedure
> did not return another result set.


### ibm\_db.num\_fields ###

Description
> int ibm\_db.num\_fields ( resource stmt )
> Returns the number of fields contained in a result set. This is most useful
> for handling the result sets returned by dynamically generated queries, or
> for result sets returned by stored procedures, where your application cannot
> otherwise know how to retrieve and use the results.
Parameters
stmt
> > A valid statement resource containing a result set.
Return Values

> Returns an integer value representing the number of fields in the result set
> associated with the specified statement resource. Returns FALSE if the
> statement resource is not a valid input value.


### ibm\_db.num\_rows ###

Description
> int ibm\_db.num\_rows ( resource stmt )
> Returns the number of rows deleted, inserted, or updated by an SQL statement.
> To determine the number of rows that will be returned by a SELECT statement,
> issue `SELECT COUNT(*) ` with the same predicates as your intended SELECT
> statement and retrieve the value. If your application logic checks the number
> of rows returned by a SELECT statement and branches if the number of rows is
> 0, consider modifying your application to attempt to return the first row
> with one of ibm\_db.fetch\_assoc(), ibm\_db.fetch\_both(), ibm\_db.fetch\_tuple(),
> or ibm\_db.fetch\_row(), and branch if the fetch function returns FALSE.
> Note: If you issue a SELECT statement using a scrollable cursor,
> ibm\_db.num\_rows() returns the number of rows returned by the SELECT
> statement. However, the overhead associated with scrollable cursors
> significantly degrades the performance of your application, so if this is the
> only reason you are considering using scrollable cursors, you should use a
> forward-only cursor and either call `SELECT COUNT(*)` or rely on the boolean
> return value of the fetch functions to achieve the equivalent functionality
> with much better performance.
Parameters
stmt
> > A valid stmt resource containing a result set.
Return Values

> Returns the number of rows affected by the last SQL statement issued by the
> specified statement handle.


### ibm\_db.pconnect ###

Description
> --   Returns a persistent connection to a database
> resource ibm\_db.pconnect ( string database, string username, string password
> [, dictionary options] )
> Returns a persistent connection to an IBM DB2 Universal Database,
> IBM Cloudscape, Apache Derby or Informix.
> Calling ibm\_db.close() on a persistent connection always returns TRUE, but
> the underlying DB2 client connection remains open and waiting to serve the
> next matching ibm\_db.pconnect() request.
Parameters
database
> > The database alias in the DB2 client catalog.
username
> > The username with which you are connecting to the database.
password
> > The password with which you are connecting to the database.
options
> > An associative array of connection options that affect the behavior of

> the connection,
> > where valid array keys include:
> > autocommit
> > > Passing the DB2\_AUTOCOMMIT\_ON value turns autocommit on for this

> connection handle.
> > Passing the DB2\_AUTOCOMMIT\_OFF value turns autocommit off for

> this connection handle.
> > DB2\_ATTR\_CASE
> > > Passing the DB2\_CASE\_NATURAL value specifies that column names

> are returned in natural case.
> > Passing the DB2\_CASE\_LOWER value specifies that column names are

> returned in lower case.
> > Passing the DB2\_CASE\_UPPER value specifies that column names are

> returned in upper case.
> > CURSOR
> > > Passing the SQL\_SCROLL\_FORWARD\_ONLY value specifies a

> forward-only cursor for a statement resource.  This is the default cursor
> type and is supported on all database servers.
> > Passing the SQL\_CURSOR\_KEYSET\_DRIVEN value specifies a scrollable

> cursor for a statement resource. This mode enables random access to rows in a
> result set, but currently is supported only by IBM DB2 Universal Database.
set\_replace\_quoted\_literal
> > This variable indicates if the CLI Connection attribute SQL\_ATTR\_REPLACE\_QUOTED\_LITERAL is to be set or not


> To turn it ON pass  ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_ON

> To turn it OFF pass ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_OFF

> Default Setting: - ibm\_db.QUOTED\_LITERAL\_REPLACEMENT\_ON

Return Values
> Returns a connection handle resource if the connection attempt is successful.
> ibm\_db.pconnect() tries to reuse an existing connection resource that exactly
> matches the database, username, and password parameters. If the connection
> attempt fails, ibm\_db.pconnect() returns FALSE.

```xml

Note: Local cataloged database implicit connection
i) If database parameter specified is a local database alias name with blank userid and password
then connect/pconnect API will use current logged in user's userid for implicit connection
eg: conn = ibm_db.pconnect('sample', '', '')
ii) If database parameter is a connection string with value "DSN=database_name" then
connect/pconnect API will use current logged in user's userid for implicit connection
eg: conn = ibm_db.pconnect('DSN=sample', '', '')
```

### ibm\_db.prepare ###

Description
> IBMDB\_Statement ibm\_db.prepare ( IBM\_DBConnection connection,
> > string statement [, array options] )

> ibm\_db.prepare() creates a prepared SQL statement which can include 0 or
> more parameter markers (? characters) representing parameters for input,
> output, or input/output. You can pass parameters to the prepared statement
> using ibm\_db.bind\_param(), or for input values only, as an array passed to
> ibm\_db.execute().
> There are three main advantages to using prepared statements in your
> application:
> > Performance: when you prepare a statement, the database server
> > creates an optimized access plan for retrieving data with that
> > statement. Subsequently issuing the prepared statement with
> > ibm\_db.execute() enables the statements to reuse that access plan
> > and avoids the overhead of dynamically creating a new access plan
> > for every statement you issue.
> > Security: when you prepare a statement, you can include parameter
> > markers for input values. When you execute a prepared statement
> > with input values for placeholders, the database server checks each
> > input value to ensure that the type matches the column definition or
> > parameter definition..
Parameters
connection
> > A valid database connection resource variable as returned from
> > ibm\_db.connect() or ibm\_db.pconnect().
statement
> > An SQL statement, optionally containing one or more parameter markers.
options
> > An dictionary containing statement options. You can use this parameter
> > to request a scrollable cursor on database servers that support this
> > functionality.
> > SQL\_ATTR\_CURSOR\_TYPE
> > > Passing the SQL\_SCROLL\_FORWARD\_ONLY value requests a forward-only
> > > cursor for this SQL statement. This is the default type of
> > > cursor, and it is supported by all database servers. It is also
> > > much faster than a scrollable cursor.
> > > Passing the SQL\_CURSOR\_KEYSET\_DRIVEN value requests a scrollable
> > > cursor for this SQL statement. This type of cursor enables you
> > > to fetch rows non-sequentially from the database server. However,
> > > it is only supported by DB2 servers, and is much slower than
> > > forward-only cursors.
Return Values

> Returns a IBM\_DBStatement object if the SQL statement was successfully
> parsed and prepared by the database server. Returns FALSE if the database
> server returned an error. You can determine which error was returned by
> calling ibm\_db.stmt\_error() or ibm\_db.stmt\_errormsg().


### ibm\_db.primary\_keys ###

Description
> resource ibm\_db.primary\_keys ( resource connection, string qualifier,
> string schema, string table-name )
> Returns a result set listing the primary keys for a table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. If schema is NULL,

> ibm\_db.primary\_keys() matches the schema for the current connection.
table-name
> > The name of the table.
Return Values

> Returns a statement resource with a result set containing rows describing the
> primary keys for the specified table.
> The result set is composed of the following columns:
> Column name:: Description
> TABLE\_CAT:: Name of the catalog for the table containing the primary key.
> The value is NULL if this table does not have catalogs.
> TABLE\_SCHEM:: Name of the schema for the table containing the primary key.
> TABLE\_NAME:: Name of the table containing the primary key.
> COLUMN\_NAME:: Name of the column containing the primary key.
> KEY\_SEQ:: 1-indexed position of the column in the key.
> PK\_NAME:: The name of the primary key.


### ibm\_db.procedure\_columns ###

Description
> resource ibm\_db.procedure\_columns ( resource connection, string qualifier,
> string schema, string procedure, string parameter )
> Returns a result set listing the parameters for one or more stored procedures
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the procedures. This parameter accepts a

> search pattern containing _and % as wildcards.
procedure
> > The name of the procedure. This parameter accepts a search pattern

> containing_ and % as wildcards.
parameter
> > The name of the parameter. This parameter accepts a search pattern

> containing _and % as wildcards.
> > If this parameter is NULL, all parameters for the specified stored

> procedures are returned.
Return Values
> Returns a statement resource with a result set containing rows describing the
> parameters for the stored procedures matching the specified parameters. The
> rows are composed of the following columns:
> Column name::   Description
> PROCEDURE\_CAT:: The catalog that contains the procedure. The value is NULL
> if this table does not have catalogs.
> PROCEDURE\_SCHEM:: Name of the schema that contains the stored procedure.
> PROCEDURE\_NAME:: Name of the procedure.
> COLUMN\_NAME:: Name of the parameter.
> COLUMN\_TYPE:: An integer value representing the type of the parameter:
> > Return value:: Parameter type
    1. : (SQL\_PARAM\_INPUT)   Input (IN) parameter.
> > 2:: (SQL\_PARAM\_INPUT\_OUTPUT) Input/output (INOUT)
> > > parameter.

> > 3:: (SQL\_PARAM\_OUTPUT) Output (OUT) parameter.

> DATA\_TYPE:: The SQL data type for the parameter represented as an integer
> value.
> TYPE\_NAME:: A string representing the data type for the parameter.
> COLUMN\_SIZE:: An integer value representing the size of the parameter.
> BUFFER\_LENGTH:: Maximum number of bytes necessary to store data for this
> parameter.
> DECIMAL\_DIGITS:: The scale of the parameter, or NULL where scale is not
> applicable.
> NUM\_PREC\_RADIX:: An integer value of either 10 (representing an exact numeric
> data type), 2 (representing anapproximate numeric data type), or NULL
> (representing a data type for which radix is not applicable).
> NULLABLE:: An integer value representing whether the parameter is nullable or
> not.
> REMARKS:: Description of the parameter.
> COLUMN\_DEF:: Default value for the parameter.
> SQL\_DATA\_TYPE:: An integer value representing the size of the parameter.
> SQL\_DATETIME\_SUB:: Returns an integer value representing a datetime subtype
> code, or NULL for SQL data types to which this does not apply.
> CHAR\_OCTET\_LENGTH:: Maximum length in octets for a character data type
> parameter, which matches COLUMN\_SIZE for single-byte character set data, or
> NULL for non-character data types.
> ORDINAL\_POSITION:: The 1-indexed position of the parameter in the CALL
> statement.
> IS\_NULLABLE:: A string value where 'YES' means that the parameter accepts or
> returns NULL values and 'NO' means that the parameter does not accept or
> return NULL values._


### ibm\_db.procedures ###

Description
> resource ibm\_db.procedures ( resource connection, string qualifier,
> string schema, string procedure )
> Returns a result set listing the stored procedures registered in a database.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the procedures. This parameter accepts a

> search pattern containing _and % as wildcards.
procedure
> > The name of the procedure. This parameter accepts a search pattern

> containing_ and % as wildcards.
Return Values
> Returns a statement resource with a result set containing rows describing the
> stored procedures matching the specified parameters. The rows are composed of
> the following columns:
> Column name:: Description
> PROCEDURE\_CAT:: The catalog that contains the procedure. The value is NULL if
> this table does not have catalogs.
> PROCEDURE\_SCHEM:: Name of the schema that contains the stored procedure.
> PROCEDURE\_NAME:: Name of the procedure.
> NUM\_INPUT\_PARAMS:: Number of input (IN) parameters for the stored procedure.
> NUM\_OUTPUT\_PARAMS:: Number of output (OUT) parameters for the stored
> procedure.
> NUM\_RESULT\_SETS:: Number of result sets returned by the stored procedure.
> REMARKS:: Any comments about the stored procedure.
> PROCEDURE\_TYPE:: Always returns 1, indicating that the stored procedure does
> not return a return value.


### ibm\_db.recreatedb ###

Description
> True/None ibm\_db.recreatedb ( IBM\_DBConnection connection, string dbName [, codeSet, mode] )
> Drop and then recreates a database by using the specified database name, code set, and mode
Parameters
connection
> > A valid database server instance connection resource variable as returned from ibm\_db.connect() by specifying the ATTACH keyword.
dbName
> > Name of the database that is to be created.
codeSet
> > Database code set information.
> > Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
mode
> > Database logging mode.
> > Note: This value is applicable only to IDS data servers.
Return Value

> Returns True if specified database created successfully else return None.


### ibm\_db.result ###

Description
> mixed ibm\_db.result ( resource stmt, mixed column )
> Returns a single column from a row in the result set
> Use ibm\_db.result() to return the value of a specified column in the current  **row of a result set. You must call ibm\_db.fetch\_row() before calling
> ibm\_db.result() to set the location of the result set pointer.
Parameters
stmt
> > A valid stmt resource.
column
> > Either an integer mapping to the 0-indexed field in the result set, or** a string matching the name of the column.
Return Values

> Returns the value of the requested field if the field exists in the result
> set. Returns NULL if the field does not exist, and issues a warning.


### ibm\_db.rollback ###

Description
> bool ibm\_db.rollback ( resource connection )
> Rolls back an in-progress transaction on the specified connection resource
> and begins a new transaction. Python applications normally default to
> AUTOCOMMIT mode, so ibm\_db.rollback() normally has no effect unless
> AUTOCOMMIT has been turned off for the connection resource.
> Note: If the specified connection resource is a persistent connection, all
> transactions in progress for all applications using that persistent
> connection will be rolled back. For this reason, persistent connections are
> not recommended for use in applications that require transactions.
Parameters
connection
> > A valid database connection resource variable as returned from

> ibm\_db.connect() or ibm\_db.pconnect().
Return Values
> Returns TRUE on success or FALSE on failure.


### ibm\_db.server\_info ###

Description
> object ibm\_db.server\_info ( resource connection )
> This function returns a read-only object with information about the IBM DB2
> or Informix.
> The following table lists the database server properties:
Table 1. Database server properties
> Property name:: Description (Return type)
> DBMS\_NAME:: The name of the database server to which you are connected. For
> DB2 servers this is a combination of DB2 followed by the operating system on
> which the database server is running. (string)
> DBMS\_VER:: The version of the database server, in the form of a string
> "MM.mm.uuuu" where MM is the major version, mm is the minor version, and
> uuuu is the update. For example, "08.02.0001" represents major version 8,
> minor version 2, update 1. (string)
> DB\_CODEPAGE:: The code page of the database to which you are connected. (int)
> DB\_NAME:: The name of the database to which you are connected. (string)
> DFT\_ISOLATION:: The default transaction isolation level supported by the
> server: (string)
> > UR:: Uncommitted read: changes are immediately

> visible by all concurrent transactions.
> > CS:: Cursor stability: a row read by one transaction

> can be altered and committed by a second concurrent transaction.
> > RS:: Read stability: a transaction can add or remove

> rows matching a search condition or a pending transaction.
> > RR:: Repeatable read: data affected by pending

> transaction is not available to other transactions.
> > NC:: No commit: any changes are visible at the end of

> a successful operation. Explicit commits and rollbacks are not allowed.
> IDENTIFIER\_QUOTE\_CHAR:: The character used to delimit an identifier. (string)
> INST\_NAME:: The instance on the database server that contains the database.
> (string)
> ISOLATION\_OPTION:: An array of the isolation options supported by the
> database server. The isolation options are described in the DFT\_ISOLATION
> property. (array)
> KEYWORDS:: An array of the keywords reserved by the database server. (array)
> LIKE\_ESCAPE\_CLAUSE:: TRUE if the database server supports the use of % and _> wildcard characters. FALSE if the database server does not support these
> wildcard characters. (bool)
> MAX\_COL\_NAME\_LEN:: Maximum length of a column name supported by the database
> server, expressed in bytes. (int)
> MAX\_IDENTIFIER\_LEN:: Maximum length of an SQL identifier supported by the
> database server, expressed in characters. (int)
> MAX\_INDEX\_SIZE:: Maximum size of columns combined in an index supported by
> the database server, expressed in bytes. (int)
> MAX\_PROC\_NAME\_LEN:: Maximum length of a procedure name supported by the
> database server, expressed in bytes. (int)
> MAX\_ROW\_SIZE:: Maximum length of a row in a base table supported by the
> database server, expressed in bytes. (int)
> MAX\_SCHEMA\_NAME\_LEN:: Maximum length of a schema name supported by the
> database server, expressed in bytes. (int)
> MAX\_STATEMENT\_LEN:: Maximum length of an SQL statement supported by the
> database server, expressed in bytes. (int)
> MAX\_TABLE\_NAME\_LEN:: Maximum length of a table name supported by the
> database server, expressed in bytes. (bool)
> NON\_NULLABLE\_COLUMNS:: TRUE if the database server supports columns that can
> be defined as NOT NULL, FALSE if the database server does not support columns
> defined as NOT NULL. (bool)
> PROCEDURES:: TRUE if the database server supports the use of the CALL
> statement to call stored procedures, FALSE if the database server does not
> support the CALL statement. (bool)
> SPECIAL\_CHARS:: A string containing all of the characters other than a-Z,
> 0-9, and underscore that can be used in an identifier name. (string)
> SQL\_CONFORMANCE:: The level of conformance to the ANSI/ISO SQL-92
> specification offered by the database server: (string)
> > ENTRY:: Entry-level SQL-92 compliance.
> > FIPS127:: FIPS-127-2 transitional compliance.
> > FULL:: Full level SQL-92 compliance.
> > INTERMEDIATE:: Intermediate level SQL-92
> > > compliance.
Parameters
connection

> > Specifies an active DB2 client connection.
Return Values

> Returns an object on a successful call. Returns FALSE on failure._


### ibm\_db.set\_option ###

Description
> bool ibm\_db.set\_option ( resource resc, array options, int type )
> Sets options for a connection or statement resource. You cannot set options
> for result set resources.
Parameters
resc
> > A valid connection or statement resource.
options
> > The options to be set
type
> > A field that specifies the resource type (1 = Connection,

> NON-1 = Statement)
Return Values
> Returns TRUE on success or FALSE on failure


### ibm\_db.special\_columns ###

Description
> resource ibm\_db.special\_columns ( resource connection, string qualifier,
> string schema, string table\_name, int scope )
> Returns a result set listing the unique row identifier columns for a table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables.
table\_name
> > The name of the table.
scope
> > Integer value representing the minimum duration for which the unique

> row identifier is valid. This can be one of the following values:
> > 0: Row identifier is valid only while the cursor is positioned on the

> row. (SQL\_SCOPE\_CURROW)
    1. Row identifier is valid for the duration of the transaction.
> (SQL\_SCOPE\_TRANSACTION)
> > 2: Row identifier is valid for the duration of the connection.

> (SQL\_SCOPE\_SESSION)
Return Values
> Returns a statement resource with a result set containing rows with unique
> row identifier information for a table.
> The rows are composed of the following columns:
> Column name:: Description
> SCOPE:: Integer value representing the minimum duration for which the unique
> row identifier is valid.
> > 0: Row identifier is valid only while the cursor is positioned on

> the row. (SQL\_SCOPE\_CURROW)
    1. Row identifier is valid for the duration of the transaction.
> (SQL\_SCOPE\_TRANSACTION)
> > 2: Row identifier is valid for the duration of the connection.

> (SQL\_SCOPE\_SESSION)
> COLUMN\_NAME:: Name of the unique column.
> DATA\_TYPE:: SQL data type for the column.
> TYPE\_NAME:: Character string representation of the SQL data type for the
> column.
> COLUMN\_SIZE:: An integer value representing the size of the column.
> BUFFER\_LENGTH:: Maximum number of bytes necessary to store data from this
> column.
> DECIMAL\_DIGITS:: The scale of the column, or NULL where scale is not
> applicable.
> NUM\_PREC\_RADIX:: An integer value of either 10 (representing an exact numeric
> data type),2 (representing an approximate numeric data type), or NULL
> (representing a data type for which radix is not applicable).
> PSEUDO\_COLUMN:: Always returns 1.


### ibm\_db.statistics ###

Description
> resource ibm\_db.statistics ( resource connection, string qualifier,
> string schema, string table-name, bool unique )
> Returns a result set listing the index and statistics for a table.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema that contains the targeted table. If this parameter is NULL,

> the statistics and indexes are returned for the schema of the current user.
table\_name
> > The name of the table.
unique
> > A boolean value representing the type of index information to return.
> > False     Return only the information for unique indexes on the table.
> > True      Return the information for all indexes on the table.
Return Values

> Returns a statement resource with a result set containing rows describing the
> statistics and indexes for the base tables matching the specified parameters.
> The rows are composed of the following columns:
> Column name:: Description
> TABLE\_CAT:: The catalog that contains the table. The value is NULL if this
> table does not have catalogs.
> TABLE\_SCHEM:: Name of the schema that contains the table.
> TABLE\_NAME:: Name of the table.
> NON\_UNIQUE:: An integer value representing whether the index prohibits unique
> values, or whether the row represents statistics on the table itself:
> > Return value:: Parameter type
> > 0 (SQL\_FALSE):: The index allows duplicate values.
    1. (SQL\_TRUE):: The index values must be unique.
> > NULL:: This row is statistics information for the table
> > itself.

> INDEX\_QUALIFIER:: A string value representing the qualifier that would have
> to be prepended to INDEX\_NAME to fully qualify the index.
> INDEX\_NAME:: A string representing the name of the index.
> TYPE:: An integer value representing the type of information contained in
> this row of the result set:
> > Return value:: Parameter type
> > 0 (SQL\_TABLE\_STAT):: The row contains statistics about the table
> > > itself.
    1. (SQL\_INDEX\_CLUSTERED):: The row contains information about a
> > > clustered index.

> > 2 (SQL\_INDEX\_HASH):: The row contains information about a hashed
> > > index.

> > 3 (SQL\_INDEX\_OTHER):: The row contains information about a type of

> index that is neither clustered nor hashed.
> ORDINAL\_POSITION:: The 1-indexed position of the column in the index. NULL if
> the row contains statistics information about the table itself.
> COLUMN\_NAME:: The name of the column in the index. NULL if the row contains
> statistics information about the table itself.
> ASC\_OR\_DESC:: A if the column is sorted in ascending order, D if the column
> is sorted in descending order, NULL if the row contains statistics
> information about the table itself.
> CARDINALITY:: If the row contains information about an index, this column
> contains an integer value representing the number of unique values in the
> index. If the row contains information about the table itself, this column
> contains an integer value representing the number of rows in the table.
> PAGES:: If the row contains information about an index, this column contains
> an integer value representing the number of pages used to store the index. If
> the row contains information about the table itself, this column contains an
> integer value representing the number of pages used to store the table.
> FILTER\_CONDITION:: Always returns NULL.


### ibm\_db.stmt\_error ###

Description
> string ibm\_db.stmt\_errormsg ( [stmt](resource.md) )
> Returns a string containing the last SQL statement error message.
> If you do not pass a statement resource as an argument to
> ibm\_db.stmt\_errormsg(), the driver returns the error message associated with
> the last attempt to return a statement resource, for example, from
> ibm\_db.prepare() or ibm\_db.exec\_immediate().
Parameters
stmt
> > A valid statement resource.
Return Values

> Returns a string containing the error message and SQLCODE value for the last
> error that occurred issuing an SQL statement.


### ibm\_db.stmt\_errormsg ###

Description
> string ibm\_db.stmt\_errormsg ( [stmt](resource.md) )
> Returns a string containing the last SQL statement error message.
> If you do not pass a statement resource as an argument to
> ibm\_db.stmt\_errormsg(), the driver returns the error message associated with
> the last attempt to return a statement resource, for example, from
> ibm\_db.prepare() or ibm\_db.exec\_immediate().
Parameters
stmt
> > A valid statement resource.
Return Values

> Returns a string containing the error message and SQLCODE value for the last
> error that occurred issuing an SQL statement.


### ibm\_db.table\_privileges ###

Description
> resource ibm\_db.table\_privileges ( resource connection [, string qualifier
> [, string schema [, string table\_name]]] )
> Returns a result set listing the tables and associated privileges in a
> database.
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. This parameter accepts a search

> pattern containing _and % as wildcards.
table\_name
> > The name of the table. This parameter accepts a search pattern

> containing_ and % as wildcards.
Return Values
> Returns a statement resource with a result set containing rows describing
> the privileges for the tables that match the specified parameters. The rows
> are composed of the following columns:
> Column name:: Description
> TABLE\_CAT:: The catalog that contains the table. The value is NULL if this
> table does not have catalogs.
> TABLE\_SCHEM:: Name of the schema that contains the table.
> TABLE\_NAME:: Name of the table.
> GRANTOR:: Authorization ID of the user who granted the privilege.
> GRANTEE:: Authorization ID of the user to whom the privilege was granted.
> PRIVILEGE:: The privilege that has been granted. This can be one of ALTER,
> CONTROL, DELETE, INDEX, INSERT, REFERENCES, SELECT, or UPDATE.
> IS\_GRANTABLE:: A string value of "YES" or "NO" indicating whether the grantee
> can grant the privilege to other users.


### ibm\_db.tables ###

Description
> resource ibm\_db.tables ( resource connection [, string qualifier [, string
> schema [, string table-name [, string table-type]]]] )
> Returns a result set listing the tables and associated metadata in a database
Parameters
connection
> > A valid connection to an IBM DB2, Cloudscape, or Apache Derby database.
qualifier
> > A qualifier for DB2 databases running on OS/390 or z/OS servers. For

> other databases, pass NULL or an empty string.
schema
> > The schema which contains the tables. This parameter accepts a search

> pattern containing _and % as wildcards.
table-name
> > The name of the table. This parameter accepts a search pattern

> containing_ and % as wildcards.
table-type
> > A list of comma-delimited table type identifiers. To match all table

> types, pass NULL or an empty string.
> > Valid table type identifiers include: ALIAS, HIERARCHY TABLE,

> INOPERATIVE VIEW, NICKNAME, MATERIALIZED QUERY TABLE, SYSTEM TABLE, TABLE,
> TYPED TABLE, TYPED VIEW, and VIEW.
Return Values
> Returns a statement resource with a result set containing rows describing
> the tables that match the specified parameters.
> The rows are composed of the following columns:
> Column name:: Description
> TABLE\_CAT:: The catalog that contains the table. The value is NULL if this
> table does not have catalogs.
> TABLE\_SCHEMA:: Name of the schema that contains the table.
> TABLE\_NAME:: Name of the table.
> TABLE\_TYPE:: Table type identifier for the table.
> REMARKS:: Description of the table.


### ibm\_db.callproc ###

Description
> `( resource[, parameters] ) ibm_db.callproc( IBM_DBConnection connection, string procname [, parameters] )`.  It calls a stored procedure with the given name. The parameters tuple must contain one entry for each argument (IN/OUT/INOUT) that the procedure expect. The result of call returns IBM\_DBStatement  containing result set and modified copy of the input sequence. IN parameters are left untouched whereas INOUT/OUT parameters are possibly replaced by new values. Call to a stored procedure may return zero or more result sets. You can retrieve a row as tuple/dictionary from the IBM\_DBStatement resource using ibm\_db.fetchassoc(), ibm\_db.fetch\_both(), or ibm\_db.fetch\_tuple(). Alternatively, you can use ibm\_db.fetch\_row() to move the result set pointer to next row and fetch a column at a time with ibm\_db.result(). Samples for the API usage can be referred from test\_146\_CallSPINAndOUTParams.py, test\_148\_CallSPDiffBindPattern\_01.py or test\_52949\_TestSPIntVarcharXml.py.

Parameters connection
> A valid database connection resource variable as returned from ibm\_db.connect() or ibm\_db.pconnect()

procname
> A valide strored procedure name

parameters
> An tuple  containing parameters .It must have one entry for each argument and in the same sequence that the procedure expect

Return Values
> It returns a tuple contains of stmt\_handle resource and modified copy of input parameters sequence if call of procedure executed sucessfully , or NULL if database failed to call procedure