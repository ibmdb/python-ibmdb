from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_14_async_set_get_option(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_14)

    def run_test_14(self):
        async def main():
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')

            # Get current autocommit setting
            val = await conn.get_option(ibm_db.SQL_ATTR_AUTOCOMMIT)
            print("SQL_ATTR_AUTOCOMMIT:", val)

            # Set autocommit via set_option
            await conn.set_option({ibm_db.SQL_ATTR_AUTOCOMMIT: ibm_db.SQL_AUTOCOMMIT_ON})
            val = await conn.get_option(ibm_db.SQL_ATTR_AUTOCOMMIT)
            print("After set ON, SQL_ATTR_AUTOCOMMIT:", val)

            await conn.close()
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#SQL_ATTR_AUTOCOMMIT: 0
#After set ON, SQL_ATTR_AUTOCOMMIT: 1
#__ZOS_EXPECTED__
#SQL_ATTR_AUTOCOMMIT: 0
#After set ON, SQL_ATTR_AUTOCOMMIT: 1
#__SYSTEMI_EXPECTED__
#SQL_ATTR_AUTOCOMMIT: 0
#After set ON, SQL_ATTR_AUTOCOMMIT: 1
#__IDS_EXPECTED__
#SQL_ATTR_AUTOCOMMIT: 0
#After set ON, SQL_ATTR_AUTOCOMMIT: 1
