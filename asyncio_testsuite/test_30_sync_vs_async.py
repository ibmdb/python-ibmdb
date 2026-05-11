from __future__ import print_function
import asyncio
import sys
import unittest
import ibm_db_dbi
import config
from ibm_db_dbi import AsyncConnection
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_30_sync_vs_async(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_30)

    def run_test_30(self):
        def run_sync():
            print("--- Sync ---")
            conn = ibm_db_dbi.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = conn.cursor()

            # Simple query
            cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
            rows = cursor.fetchall()
            print("Sync fetchall:", rows)

            # Prepare + bind_param + execute
            cursor.prepare("SELECT ID, NAME FROM STAFF WHERE ID = ?")
            cursor.bind_param(1, 20)
            cursor.execute()
            row = cursor.fetchone()
            print("Sync bind_param result:", row)

            cursor.close()
            conn.close()

        async def run_async():
            print("--- Async ---")
            conn = await AsyncConnection.connect(
                "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                    config.database, config.hostname, config.port,
                    config.user, config.password),
                '', '')
            cursor = await conn.cursor()

            # Simple query
            await cursor.execute("SELECT ID, NAME FROM STAFF FETCH FIRST 3 ROWS ONLY")
            rows = await cursor.fetchall()
            print("Async fetchall:", rows)

            # Prepare + bind_param + execute
            await cursor.prepare("SELECT ID, NAME FROM STAFF WHERE ID = ?")
            await cursor.bind_param(1, 20)
            await cursor.execute()
            row = await cursor.fetchone()
            print("Async bind_param result:", row)

            await cursor.close()
            await conn.close()

        run_sync()
        asyncio.run(run_async())

#__END__
#__LUW_EXPECTED__
#--- Sync ---
#Sync fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Sync bind_param result: (20, 'Pernal')
#--- Async ---
#Async fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Async bind_param result: (20, 'Pernal')
#__ZOS_EXPECTED__
#--- Sync ---
#Sync fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Sync bind_param result: (20, 'Pernal')
#--- Async ---
#Async fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Async bind_param result: (20, 'Pernal')
#__SYSTEMI_EXPECTED__
#--- Sync ---
#Sync fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Sync bind_param result: (20, 'Pernal')
#--- Async ---
#Async fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Async bind_param result: (20, 'Pernal')
#__IDS_EXPECTED__
#--- Sync ---
#Sync fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Sync bind_param result: (20, 'Pernal')
#--- Async ---
#Async fetchall: [(10, 'Sanders'), (20, 'Pernal'), (30, 'Marenghi')]
#Async bind_param result: (20, 'Pernal')
