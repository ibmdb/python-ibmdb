from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db_dbi
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_01_async_connect(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_01)

    def run_test_01(self):
        async def main():
            # Cataloged connection
            conn = await ibm_db_dbi.connect_async(config.database, config.user, config.password)
            if conn:
                print("Cataloged connection succeeded.")
                conn.close()
            else:
                print("Cataloged connection failed.")

            # Uncataloged connection
            conn = await ibm_db_dbi.connect_async(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            if conn:
                print("Uncataloged connection succeeded.")
                conn.close()
            else:
                print("Uncataloged connection failed.")
        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Cataloged connection succeeded.
#Uncataloged connection succeeded.
#__ZOS_EXPECTED__
#Cataloged connection succeeded.
#Uncataloged connection succeeded.
#__SYSTEMI_EXPECTED__
#Cataloged connection succeeded.
#Uncataloged connection succeeded.
#__IDS_EXPECTED__
#Cataloged connection succeeded.
#Uncataloged connection succeeded.
