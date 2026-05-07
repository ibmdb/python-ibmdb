# Async (asyncio) APIs for ibm_db_dbi

The `ibm_db_dbi` module provides full `asyncio` support through `AsyncConnection`, `AsyncCursor`, and module-level async functions. All async operations use `asyncio.to_thread()` internally, making the synchronous IBM CLI calls non-blocking in an async event loop.

> **Note:** All examples use `await` at the top level for brevity. In a script, wrap your code in `async def main()` and call `asyncio.run(main())`. For interactive testing, use `python -m asyncio` to start the asyncio REPL, which supports top-level `await`. The regular `python` REPL does not support `await` outside a function.

## Table of Contents

- [Module-Level Async Functions](#module-level-async-functions)
  - [connect_async](#connect_async)
  - [pconnect_async](#pconnect_async)
  - [conn_errormsg_async](#conn_errormsg_async)
  - [conn_error_async](#conn_error_async)
  - [get_sqlcode_async](#get_sqlcode_async)
  - [createdb_async](#createdb_async)
  - [dropdb_async](#dropdb_async)
  - [recreatedb_async](#recreatedb_async)
  - [createdbNX_async](#createdbnx_async)
- [AsyncConnection](#asyncconnection)
  - [AsyncConnection.connect](#asyncconnectionconnect)
  - [AsyncConnection.close](#asyncconnectionclose)
  - [AsyncConnection.commit](#asyncconnectioncommit)
  - [AsyncConnection.rollback](#asyncconnectionrollback)
  - [AsyncConnection.cursor](#asyncconnectioncursor)
  - [AsyncConnection.set_autocommit](#asyncconnectionset_autocommit)
  - [AsyncConnection.set_option / get_option](#asyncconnectionset_option--get_option)
  - [AsyncConnection.set_current_schema / get_current_schema](#asyncconnectionset_current_schema--get_current_schema)
  - [AsyncConnection.server_info](#asyncconnectionserver_info)
  - [AsyncConnection.set_fix_return_type](#asyncconnectionset_fix_return_type)
  - [AsyncConnection metadata methods](#asyncconnection-metadata-methods)
  - [AsyncConnection context manager](#asyncconnection-context-manager)
- [AsyncCursor](#asynccursor)
  - [AsyncCursor.execute](#asynccursorexecute)
  - [AsyncCursor.executemany](#asynccursorexecutemany)
  - [AsyncCursor.prepare](#asynccursorprepare)
  - [AsyncCursor.bind_param](#asynccursorbind_param)
  - [AsyncCursor.fetchone](#asynccursorfetchone)
  - [AsyncCursor.fetchmany](#asynccursorfetchmany)
  - [AsyncCursor.fetchall](#asynccursorfetchall)
  - [AsyncCursor.fetch_tuple](#asynccursorfetch_tuple)
  - [AsyncCursor.callproc](#asynccursorcallproc)
  - [AsyncCursor.fetch_callproc](#asynccursorfetch_callproc)
  - [AsyncCursor.nextset](#asynccursornextset)
  - [AsyncCursor.close](#asynccursorclose)
  - [AsyncCursor.stmt_errormsg / stmt_error](#asynccursorstmt_errormsg--stmt_error)
  - [AsyncCursor.description / rowcount](#asynccursordescription--rowcount)
  - [AsyncCursor context manager](#asynccursor-context-manager)
- [Stored Procedure Patterns](#stored-procedure-patterns)
- [Concurrent Queries with asyncio.gather](#concurrent-queries-with-asynciogather)

## Module-Level Async Functions

### connect_async

`Connection await ibm_db_dbi.connect_async(string dsn, string user, string password [, string host [, string database [, dict conn_options]]])`

**Description**

Async wrapper around `ibm_db_dbi.connect()`. Creates a connection asynchronously using `asyncio.to_thread()` and returns a **sync** `Connection` object.

> **Note:** Use `AsyncConnection.connect()` instead if you want a fully async connection and cursor lifecycle.

**Parameters**

- `dsn` - A connection string (e.g., `"DATABASE=sample;HOSTNAME=host;PORT=50000;PROTOCOL=TCPIP"`)
- `user` - The username for authentication
- `password` - The password for authentication
- `host` - (optional) Hostname
- `database` - (optional) Database name
- `conn_options` - (optional) A dict of connection options

> For full details on connection parameters, DSN formats, JWT access tokens, and connection options (`SQL_ATTR_*`), refer to [ibm_db.connect](https://github.com/ibmdb/python-ibmdb/wiki/APIs#ibm_dbconnect).

**Return Values**

- On success, a sync `Connection` object
- On failure, raises an exception

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    dsn = "DATABASE=sample;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    conn = await ibm_db_dbi.connect_async(dsn, "user", "password")
    # conn is a sync Connection object
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM SYSIBM.SYSDUMMY1")
    print(cursor.fetchone())
    conn.close()

asyncio.run(main())
```

### pconnect_async

`Connection await ibm_db_dbi.pconnect_async(string dsn, string user, string password [, string host [, string database [, dict conn_options]]])`

**Description**

Async wrapper around `ibm_db_dbi.pconnect()`. Returns a persistent **sync** `Connection`. Persistent connections are reused from a process-wide connection pool when `ibm_db.close()` is called.

**Parameters**

Same as [`connect_async`](#connect_async). For full details on connection parameters, refer to [ibm_db.pconnect](https://github.com/ibmdb/python-ibmdb/wiki/APIs#ibm_dbpconnect).

**Return Values**

- On success, a sync `Connection` object (persistent)
- On failure, raises an exception

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    dsn = "DATABASE=sample;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    conn = await ibm_db_dbi.pconnect_async(dsn, "user", "password")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM STAFF")
    print(cursor.fetchone())
    conn.close()  # returns to pool, not actually closed

asyncio.run(main())
```

### conn_errormsg_async

`string await ibm_db_dbi.conn_errormsg_async([Connection connection])`

**Description**

Async wrapper around `ibm_db.conn_errormsg()`. Returns the SQLCODE and error message for the last failed connection operation.

**Parameters**

- `connection` - (optional) A valid connection handler

**Return Values**

Returns a string containing the error message or an empty string if there was no error.

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    try:
        conn = await ibm_db_dbi.connect_async(
            "DATABASE=sample;HOSTNAME=host;PORT=50000;PROTOCOL=TCPIP",
            "invalid_user", "invalid_pwd")
    except Exception:
        msg = await ibm_db_dbi.conn_errormsg_async()
        print("Connection error:", msg)

asyncio.run(main())
```

### conn_error_async

`string await ibm_db_dbi.conn_error_async([Connection connection])`

**Description**

Async wrapper around `ibm_db.conn_error()`. Returns the SQLSTATE (5-character string) for the last failed connection operation.

**Parameters**

- `connection` - (optional) A valid connection handler

**Return Values**

Returns a string containing the SQLSTATE or an empty string if there was no error.

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    try:
        conn = await ibm_db_dbi.connect_async(
            "DATABASE=sample;HOSTNAME=host;PORT=50000;PROTOCOL=TCPIP",
            "invalid_user", "invalid_pwd")
    except Exception:
        sqlstate = await ibm_db_dbi.conn_error_async()
        print("SQLSTATE:", sqlstate)

asyncio.run(main())
```

### get_sqlcode_async

`string await ibm_db_dbi.get_sqlcode_async([Connection connection] / [Cursor cursor])`

**Description**

Async wrapper around `ibm_db.get_sqlcode()`. Returns the SQLCODE for the last failed operation.

**Parameters**

- `handle` - (optional) A valid connection or statement handler

**Return Values**

Returns a string containing the SQLCODE or an empty string if there was no error.

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    try:
        conn = await ibm_db_dbi.connect_async(
            "DATABASE=sample;HOSTNAME=host;PORT=50000;PROTOCOL=TCPIP",
            "invalid_user", "invalid_pwd")
    except Exception:
        sqlcode = await ibm_db_dbi.get_sqlcode_async()
        print("SQLCODE:", sqlcode)

asyncio.run(main())
```

### createdb_async

`bool await ibm_db_dbi.createdb_async(string database, string dsn, string user, string password [, string host [, string codeset [, string mode]]])`

**Description**

Async wrapper around `ibm_db_dbi.createdb()`. Creates a database asynchronously.

**Parameters**

- `database` - Name of the database to create
- `dsn` - Connection string with `ATTACH=true`
- `user` - Username
- `password` - Password
- `host` - Hostname
- `codeset` - (optional) Database code set
- `mode` - (optional) Database logging mode

**Return Values**

Returns `True` on success, `None` on failure.

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    dsn = "ATTACH=true;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    rc = await ibm_db_dbi.createdb_async("TESTDB", dsn, "user", "password")
    print("Created:", rc)

asyncio.run(main())
```

### dropdb_async

`bool await ibm_db_dbi.dropdb_async(string database, string dsn, string user, string password [, string host])`

**Description**

Async wrapper around `ibm_db_dbi.dropdb()`. Drops a database asynchronously.

**Parameters**

- `database` - Name of the database to drop
- `dsn` - Connection string with `ATTACH=true`
- `user` - Username
- `password` - Password
- `host` - Hostname

**Return Values**

Returns `True` on success, `None` on failure.

**Example**

```python
import asyncio
import ibm_db_dbi

async def main():
    dsn = "ATTACH=true;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    rc = await ibm_db_dbi.dropdb_async("TESTDB", dsn, "user", "password")
    print("Dropped:", rc)

asyncio.run(main())
```

### recreatedb_async

`bool await ibm_db_dbi.recreatedb_async(string database, string dsn, string user, string password [, string host [, string codeset [, string mode]]])`

**Description**

Async wrapper around `ibm_db_dbi.recreatedb()`. Drops and then recreates a database asynchronously.

**Parameters**

Same as `createdb_async`.

**Return Values**

Returns `True` on success, `None` on failure.

### createdbNX_async

`bool await ibm_db_dbi.createdbNX_async(string database, string dsn, string user, string password [, string host [, string codeset [, string mode]]])`

**Description**

Async wrapper around `ibm_db_dbi.createdbNX()`. Creates a database only if it does not already exist.

**Parameters**

Same as `createdb_async`.

**Return Values**

Returns `True` if database already exists or is created successfully, `None` on failure.

## AsyncConnection

`AsyncConnection` is a fully async connection class. All methods are coroutines. Obtain an instance via the `connect()` class method.

### AsyncConnection.connect

`AsyncConnection await AsyncConnection.connect(string dsn, string user, string password [, string host [, string database [, dict conn_options]]])`

**Description**

Class method that creates and returns an `AsyncConnection`. This is the recommended way to establish an async connection.

**Parameters**

- `dsn` - A connection string
- `user` - Username
- `password` - Password
- `host` - (optional) Hostname
- `database` - (optional) Database name
- `conn_options` - (optional) A dict of connection options

**Return Values**

Returns an `AsyncConnection` object.

**Example**

```python
import asyncio
from ibm_db_dbi import AsyncConnection

async def main():
    dsn = "DATABASE=sample;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    conn = await AsyncConnection.connect(dsn, "user", "password")

    cursor = await conn.cursor()
    await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
    rows = await cursor.fetchall()
    for row in rows:
        print(row)

    await cursor.close()
    await conn.close()

asyncio.run(main())
```

### AsyncConnection.close

`await conn.close()`

**Description**

Closes the async connection. Rolls back any uncommitted transactions before closing.

**Return Values**

None.

### AsyncConnection.commit

`await conn.commit()`

**Description**

Commits the current transaction.

**Return Values**

None.

**Example**

```python
from ibm_db_dbi import AsyncConnection

async def main():
    conn = await AsyncConnection.connect(dsn, user, password)
    await conn.set_autocommit(False)

    cursor = await conn.cursor()
    await cursor.execute("INSERT INTO STAFF (ID, NAME) VALUES (999, 'Test')")
    await conn.commit()

    await cursor.close()
    await conn.close()
```

### AsyncConnection.rollback

`await conn.rollback()`

**Description**

Rolls back an in-progress transaction on the `AsyncConnection` and begins a new transaction. Python applications normally default to AUTOCOMMIT mode, so `rollback()` normally has no effect unless AUTOCOMMIT has been turned off for the connection.

**Note:** If the `AsyncConnection` wraps a persistent connection (created via `pconnect_async`), all transactions in progress for all applications using that persistent connection will be rolled back. For this reason, persistent connections are not recommended for use in applications that require transactions.

**Parameters**

**Parameters**

None.

**Return Values**

None.

**Example**

```python
from ibm_db_dbi import AsyncConnection

async def main():
    conn = await AsyncConnection.connect(dsn, user, password)
    await conn.set_autocommit(False)

    cursor = await conn.cursor()
    await cursor.execute("DELETE FROM STAFF WHERE ID = 10")
    await conn.rollback()  # undo the delete

    await cursor.close()
    await conn.close()
```

### AsyncConnection.cursor

`AsyncCursor await conn.cursor()`

**Description**

Creates and returns an `AsyncCursor` bound to this connection.

**Return Values**

Returns an `AsyncCursor` object.

### AsyncConnection.set_autocommit

`await conn.set_autocommit(bool flag)`

**Description**

Enables or disables autocommit on the connection.

**Parameters**

- `flag` - `True` to enable autocommit, `False` to disable

### AsyncConnection.set_option / get_option

`await conn.set_option(dict options_dict)`
`mixed await conn.get_option(int option_key)`

**Description**

Sets or gets connection-level attributes.

**Parameters**

- `options_dict` - A dict of `{ibm_db_dbi.SQL_ATTR_*: value}`
- `option_key` - An `ibm_db_dbi.SQL_ATTR_*` constant

**Example**

```python
import ibm_db_dbi
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)
await conn.set_option({ibm_db_dbi.SQL_ATTR_AUTOCOMMIT: ibm_db_dbi.SQL_AUTOCOMMIT_OFF})
val = await conn.get_option(ibm_db_dbi.SQL_ATTR_AUTOCOMMIT)
print("Autocommit:", val)
```

### AsyncConnection.set_current_schema / get_current_schema

`await conn.set_current_schema(string schema_name)`
`string await conn.get_current_schema()`

**Description**

Sets or gets the current schema for the connection.

**Example**

```python
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)
await conn.set_current_schema("MYSCHEMA")
schema = await conn.get_current_schema()
print("Current schema:", schema)
```

### AsyncConnection.server_info

`tuple await conn.server_info()`

**Description**

Returns a tuple of `(DBMS_NAME, DBMS_VER)` for the connected server.

**Return Values**

A tuple: `(dbms_name_string, dbms_ver_string)`

**Example**

```python
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)
info = await conn.server_info()
print("Server:", info[0], "Version:", info[1])
```

### AsyncConnection.set_fix_return_type

`await conn.set_fix_return_type(bool flag)`

**Description**

Enables or disables `FIX_RETURN_TYPE`. When enabled, numeric columns return `Decimal` instead of string.

**Parameters**

- `flag` - `True` to enable, `False` to disable

### AsyncConnection metadata methods

`list await conn.tables([string schema_name [, string table_name]])`
`list await conn.columns([string schema_name [, string table_name [, string column_names]]])`
`list await conn.primary_keys([bool unique [, string schema_name [, string table_name]]])`
`list await conn.indexes([bool unique [, string schema_name [, string table_name]]])`
`list await conn.foreign_keys([bool unique [, string schema_name [, string table_name]]])`

**Description**

Query metadata about tables, columns, primary keys, indexes, and foreign keys. Each returns the result as fetched rows.

**Example**

```python
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)

# List tables
tables = await conn.tables(schema_name="DB2ADMIN", table_name="STAFF")
print(tables)

# List columns
columns = await conn.columns(schema_name="DB2ADMIN", table_name="STAFF")
for col in columns:
    print(col)

# Primary keys
pkeys = await conn.primary_keys(schema_name="DB2ADMIN", table_name="STAFF")
print(pkeys)

await conn.close()
```

### AsyncConnection context manager

**Description**

`AsyncConnection` supports `async with`. The connection is automatically closed when the block exits.

**Example**

```python
from ibm_db_dbi import AsyncConnection

async with await AsyncConnection.connect(dsn, user, password) as conn:
    cursor = await conn.cursor()
    await cursor.execute("SELECT 1 FROM SYSIBM.SYSDUMMY1")
    print(await cursor.fetchone())
# connection auto-closed on exit
```

## AsyncCursor

`AsyncCursor` is returned by `await conn.cursor()` on an `AsyncConnection`. All I/O methods are coroutines.

### AsyncCursor.execute

`await cursor.execute([string operation [, tuple parameters]])`

**Description**

Executes an SQL statement. Supports three calling patterns:
- `await cursor.execute(sql)` — execute a SQL string
- `await cursor.execute(sql, params)` — execute with parameter markers
- `await cursor.execute()` — execute a previously prepared statement (after `prepare` + `bind_param`)

**Parameters**

- `operation` - SQL statement string, or `None` to execute a prepared statement
- `parameters` - (optional) A tuple of parameter values for parameter markers (`?`)

**Return Values**

None.

**Example**

```python
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)
cursor = await conn.cursor()

# Simple query
await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 5 ROWS ONLY")
rows = await cursor.fetchall()
print(rows)

# With parameter markers
await cursor.execute("SELECT ID, NAME FROM STAFF WHERE ID = ?", (10,))
row = await cursor.fetchone()
print(row)

await cursor.close()
await conn.close()
```

### AsyncCursor.executemany

`await cursor.executemany(string operation, tuple seq_of_parameters)`

**Description**

Executes an SQL statement once for each set of parameters in the sequence.

**Parameters**

- `operation` - SQL statement string with parameter markers
- `seq_parameters` - A sequence of tuples, each containing parameter values

**Example**

```python
cursor = await conn.cursor()
await cursor.executemany(
    "INSERT INTO STAFF (ID, NAME) VALUES (?, ?)",
    ((901, 'Alice'), (902, 'Bob'), (903, 'Carol'))
)
print("Rows inserted:", cursor.rowcount)
```

### AsyncCursor.prepare

`await cursor.prepare(string operation)`

**Description**

Prepares an SQL statement for later execution with `execute()`. Use with `bind_param()` for the prepare/bind/execute workflow.

**Parameters**

- `operation` - SQL statement string, optionally containing parameter markers (`?`)

**Example**

```python
cursor = await conn.cursor()
await cursor.prepare("SELECT ID, NAME, SALARY FROM STAFF WHERE ID = ?")
await cursor.bind_param(1, 20)
await cursor.execute()
row = await cursor.fetchone()
print(row)
```

### AsyncCursor.bind_param

`await cursor.bind_param(int param_no, mixed value [, int param_type [, int data_type]])`

**Description**

Binds a parameter value to a prepared statement.

**Parameters**

- `index` - 1-based parameter position
- `value` - The Python value to bind (scalar or list for array parameters)
- `param_type` - (optional) `ibm_db.SQL_PARAM_INPUT`, `SQL_PARAM_OUTPUT`, or `SQL_PARAM_INPUT_OUTPUT`
- `data_type` - (optional) SQL data type constant (e.g. `ibm_db.SQL_INTEGER`, `ibm_db.SQL_VARCHAR`)

**Example**

```python
import ibm_db

cursor = await conn.cursor()
await cursor.prepare("INSERT INTO STAFF (ID, NAME) VALUES (?, ?)")
await cursor.bind_param(1, 999)
await cursor.bind_param(2, "TestName")
await cursor.execute()
```

For output parameters:

```python
await cursor.prepare("CALL MY_DOUBLE_PROC(?, ?)")
await cursor.bind_param(1, 42, ibm_db.SQL_PARAM_INPUT)
await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
await cursor.execute()
result = await cursor.fetch_callproc()
print(result)  # (stmt_handler, 42, 84)
```

### AsyncCursor.fetchone

`tuple await cursor.fetchone()`

**Description**

Fetches the next row from the result set as a tuple, or `None` if no more rows.

**Return Values**

- A tuple containing the column values, or `None`

**Example**

```python
await cursor.execute("SELECT ID, NAME FROM STAFF")
row = await cursor.fetchone()
while row:
    print(row)
    row = await cursor.fetchone()
```

### AsyncCursor.fetchmany

`list await cursor.fetchmany([int size])`

**Description**

Fetches up to `size` rows from the result set as a list of tuples.

**Parameters**

- `size` - (optional) Number of rows to fetch. Defaults to `cursor.arraysize`.

**Return Values**

A list of tuples. Empty list if no rows remain.

**Example**

```python
await cursor.execute("SELECT ID, NAME FROM STAFF")
rows = await cursor.fetchmany(3)
print(rows)
```

### AsyncCursor.fetchall

`list await cursor.fetchall()`

**Description**

Fetches all remaining rows from the result set as a list of tuples.

**Return Values**

A list of tuples. Empty list if no rows remain.

**Example**

```python
await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 5 ROWS ONLY")
rows = await cursor.fetchall()
for row in rows:
    print(row)
```

### AsyncCursor.fetch_tuple

`tuple await cursor.fetch_tuple()`

**Description**

Fetches one row as a tuple from the current result set. This is an async equivalent of `ibm_db.fetch_tuple()`.

**Return Values**

- A tuple containing the column values for the next row
- `None` if there are no more rows

**Example**

```python
cursor = await conn.cursor()
await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
row = await cursor.fetch_tuple()
while row:
    print(row)
    row = await cursor.fetch_tuple()
await cursor.close()
```

### AsyncCursor.callproc

`tuple await cursor.callproc(string procname [, tuple parameters])`

**Description**

Calls a stored procedure. Returns a tuple of the (possibly modified) parameters. OUT and INOUT parameters are updated with values returned by the database.

**Parameters**

- `procname` - Name of the stored procedure
- `parameters` - (optional) A tuple of IN/OUT/INOUT parameter values

**Return Values**

A tuple of parameter values (IN parameters unchanged, OUT/INOUT parameters updated).

**Example**

```python
cursor = await conn.cursor()

# Suppose MY_DOUBLE_PROC takes IN int, OUT int and sets OUT = IN * 2
result = await cursor.callproc("MY_DOUBLE_PROC", (42, 0))
print(result)  # (42, 84)
```

### AsyncCursor.fetch_callproc

`tuple await cursor.fetch_callproc()`

**Description**

Fetches the output parameters returned by a stored procedure that was executed via the prepare/bind/execute path (not `callproc`).

**Return Values**

A tuple containing the statement handler followed by the parameter values.

**Example**

```python
import ibm_db

cursor = await conn.cursor()
await cursor.prepare("CALL MY_DOUBLE_PROC(?, ?)")
await cursor.bind_param(1, 42, ibm_db.SQL_PARAM_INPUT)
await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
await cursor.execute()

result = await cursor.fetch_callproc()
print(result)  # (stmt_handler, 42, 84)
```

For array parameters:

```python
await cursor.prepare("CALL ARRAY_SUM_PROC(?, ?, ?)")
await cursor.bind_param(1, [10, 20, 30, 40, 50], ibm_db.SQL_PARAM_INPUT)
await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
await cursor.bind_param(3, 5, ibm_db.SQL_PARAM_INPUT)
await cursor.execute()

result = await cursor.fetch_callproc()
print(result)
```

### AsyncCursor.nextset

`bool await cursor.nextset()`

**Description**

Advances to the next result set when a stored procedure returns multiple result sets.

**Return Values**

- `True` if there is another result set
- `None` if there are no more result sets

**Example**

```python
await cursor.callproc("MULTI_RESULTSET_PROC")

# First result set
rows1 = await cursor.fetchall()
print("Result set 1:", rows1)

# Advance to next
has_next = await cursor.nextset()
if has_next:
    rows2 = await cursor.fetchall()
    print("Result set 2:", rows2)
```

### AsyncCursor.close

`await cursor.close()`

**Description**

Closes the cursor and releases associated resources.

### AsyncCursor.stmt_errormsg / stmt_error

`string await cursor.stmt_errormsg()`
`string await cursor.stmt_error()`

**Description**

Returns the error message or SQLSTATE for the last failed statement operation on this cursor.

**Example**

```python
cursor = await conn.cursor()
try:
    await cursor.execute("SELECT * FROM NONEXISTENT_TABLE")
except Exception:
    print("Error:", await cursor.stmt_errormsg())
    print("SQLSTATE:", await cursor.stmt_error())
```

### AsyncCursor.description / rowcount

**Description**

These are **sync properties** (no `await` needed):

- `cursor.description` — Column metadata after execute (list of 7-tuples per DB-API spec), or `None`
- `cursor.rowcount` — Number of rows affected by the last DML statement, or `-1`

**Example**

```python
await cursor.execute("SELECT ID, NAME, SALARY FROM STAFF FETCH FIRST 1 ROW ONLY")
for col in cursor.description:
    print(col[0], col[1])  # column name, type object

await cursor.execute("UPDATE STAFF SET SALARY = SALARY + 100 WHERE ID = 10")
print("Rows updated:", cursor.rowcount)
```

### AsyncCursor context manager

**Description**

`AsyncCursor` supports `async with`. The cursor is automatically closed when the block exits.

**Example**

```python
from ibm_db_dbi import AsyncConnection

conn = await AsyncConnection.connect(dsn, user, password)
cursor = await conn.cursor()
async with cursor:
    await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
    rows = await cursor.fetchall()
    for row in rows:
        print(row)
# cursor auto-closed on exit
```

## Stored Procedure Patterns

### callproc (simple IN/OUT)

```python
cursor = await conn.cursor()
result = await cursor.callproc("MY_DOUBLE_PROC", (42, 0))
print(result)  # (42, 84)
```

### prepare + bind_param + fetch_callproc (scalar)

```python
import ibm_db

cursor = await conn.cursor()
await cursor.prepare("CALL MY_DOUBLE_PROC(?, ?)")
await cursor.bind_param(1, 42, ibm_db.SQL_PARAM_INPUT)
await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
await cursor.execute()
result = await cursor.fetch_callproc()
print(result)  # (stmt_handler, 42, 84)
```

### Array bind + fetch_callproc

```python
await cursor.prepare("CALL ARRAY_SUM_PROC(?, ?, ?)")
await cursor.bind_param(1, [10, 20, 30, 40, 50], ibm_db.SQL_PARAM_INPUT)
await cursor.bind_param(2, 0, ibm_db.SQL_PARAM_OUTPUT)
await cursor.bind_param(3, 5, ibm_db.SQL_PARAM_INPUT)
await cursor.execute()
result = await cursor.fetch_callproc()
```

### INOUT parameter

```python
await cursor.prepare("CALL ADD_100(?)")
await cursor.bind_param(1, 42, ibm_db.SQL_PARAM_INPUT_OUTPUT)
await cursor.execute()
result = await cursor.fetch_callproc()
print(result)  # (stmt_handler, 142)
```

### Multiple result sets (nextset)

```python
await cursor.callproc("MULTI_RESULTSET_PROC")

# First result set
rows1 = await cursor.fetchall()

# Advance to next
has_next = await cursor.nextset()
if has_next:
    rows2 = await cursor.fetchall()
```

## Concurrent Queries with asyncio.gather

Since all async methods use `asyncio.to_thread()`, multiple queries can run concurrently using `asyncio.gather()`.

> **Note:** Each concurrent query should use its own cursor.

**Example**

```python
import asyncio
from ibm_db_dbi import AsyncConnection

async def query(conn, staff_id):
    cur = await conn.cursor()
    await cur.execute("SELECT ID, NAME FROM STAFF WHERE ID = ?", (staff_id,))
    row = await cur.fetchone()
    await cur.close()
    return row

async def main():
    dsn = "DATABASE=sample;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"
    conn = await AsyncConnection.connect(dsn, "user", "password")

    results = await asyncio.gather(
        query(conn, 10),
        query(conn, 20),
        query(conn, 30),
    )
    for r in results:
        print(r)

    await conn.close()

asyncio.run(main())
```

## Complete Example Script

```python
import asyncio
from ibm_db_dbi import AsyncConnection

async def main():
    dsn = "DATABASE=sample;HOSTNAME=host.example.com;PORT=50000;PROTOCOL=TCPIP"

    async with await AsyncConnection.connect(dsn, "user", "password") as conn:
        # Server info
        info = await conn.server_info()
        print("Connected to:", info[0], info[1])

        # Query
        cursor = await conn.cursor()
        await cursor.execute("SELECT ID, NAME, SALARY FROM STAFF FETCH FIRST 5 ROWS ONLY")
        rows = await cursor.fetchall()
        for row in rows:
            print(row)

        # Prepare + bind + execute
        await cursor.prepare("SELECT NAME FROM STAFF WHERE ID = ?")
        await cursor.bind_param(1, 10)
        await cursor.execute()
        print("Staff 10:", await cursor.fetchone())

        # DML with commit
        await conn.set_autocommit(False)
        await cursor.execute("UPDATE STAFF SET SALARY = SALARY + 1 WHERE ID = 10")
        print("Updated rows:", cursor.rowcount)
        await conn.rollback()

        await cursor.close()

asyncio.run(main())
```
