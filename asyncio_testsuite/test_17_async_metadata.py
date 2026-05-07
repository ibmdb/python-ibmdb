from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_17_async_metadata(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_17)

    def run_test_17(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            schema = config.user.upper()

            # Tables
            tables = await conn.tables(schema_name=schema, table_name="STAFF")
            print("Tables (%d found):" % len(tables))
            for t in tables[:3]:
                print("  ", t.get("TABLE_NAME", t))

            # Columns
            columns = await conn.columns(schema_name=schema, table_name="STAFF")
            print("Columns (%d found):" % len(columns))
            for c in columns[:5]:
                print("  ", c.get("COLUMN_NAME", c), "-", c.get("TYPE_NAME", ""))

            # Primary keys
            pks = await conn.primary_keys(schema_name=schema, table_name="STAFF")
            print("Primary keys (%d found):" % len(pks))
            for pk in pks:
                print("  ", pk.get("COLUMN_NAME", pk))

            # Indexes
            idxs = await conn.indexes(schema_name=schema, table_name="STAFF")
            print("Indexes (%d found):" % len(idxs))
            for idx in idxs[:5]:
                print("  ", idx.get("INDEX_NAME", idx))

            # Foreign keys
            fks = await conn.foreign_keys(schema_name=schema, table_name="STAFF")
            print("Foreign keys (%d found):" % len(fks))
            for fk in fks[:3]:
                print("  ", fk.get("FK_NAME", fk))

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Tables (%d found):
#   STAFF
#Columns (%d found):
#   ID - SMALLINT
#   NAME - VARCHAR
#   DEPT - SMALLINT
#   JOB - CHAR
#   YEARS - SMALLINT
#Primary keys (%d found):
#Indexes (%d found):
#Foreign keys (%d found):
#__ZOS_EXPECTED__
#Tables (%d found):
#   STAFF
#Columns (%d found):
#   ID - SMALLINT
#   NAME - VARCHAR
#   DEPT - SMALLINT
#   JOB - CHAR
#   YEARS - SMALLINT
#Primary keys (%d found):
#Indexes (%d found):
#Foreign keys (%d found):
#__SYSTEMI_EXPECTED__
#Tables (%d found):
#   STAFF
#Columns (%d found):
#   ID - SMALLINT
#   NAME - VARCHAR
#   DEPT - SMALLINT
#   JOB - CHAR
#   YEARS - SMALLINT
#Primary keys (%d found):
#Indexes (%d found):
#Foreign keys (%d found):
#__IDS_EXPECTED__
#Tables (%d found):
#   STAFF
#Columns (%d found):
#   ID - SMALLINT
#   NAME - VARCHAR
#   DEPT - SMALLINT
#   JOB - CHAR
#   YEARS - SMALLINT
#Primary keys (%d found):
#Indexes (%d found):
#Foreign keys (%d found):
