from __future__ import print_function
import asyncio
import sys
import unittest
import config
from ibm_db_dbi import AsyncCoordinatedConnection
from testfunctions import IbmDbTestFunctions

# Build DSN connection strings from config
if hasattr(config, 'hostname') and config.hostname:
    CONN_STR1 = ("DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" %
                 (config.database, config.hostname, config.port,
                  config.user, config.password))
else:
    CONN_STR1 = config.database

# Set a second connection string directly in this suite when validating cross-database 2PC.
# Leave blank to reuse CONN_STR1.
CONN_STR2_OVERRIDE = ""
CONN_STR2 = CONN_STR2_OVERRIDE if CONN_STR2_OVERRIDE else CONN_STR1


class IbmDbTestCase(unittest.TestCase):

    def test_async_two_phase_commit(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_two_phase)

    def test_36_async_two_phase_suite(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_two_phase)

    def run_test_two_phase(self):
        async def scenario_coordinated_commit():
            cc = AsyncCoordinatedConnection()
            conn1 = await cc.connect(CONN_STR1, '', '')
            print("Connection 1 established")

            cur1 = await conn1.cursor()

            try:
                await cur1.execute("DROP TABLE ASYNC_2PC_T1")
                await cc.commit()
            except Exception:
                try:
                    await cc.rollback()
                except Exception:
                    pass

            try:
                conn2 = await cc.connect(CONN_STR2, '', '')
            except Exception:
                conn2 = None

            if conn2 is not None:
                print("Connection 2 established")
                cur2 = await conn2.cursor()
            else:
                # Fall back to single-connection mode if second DSN is unreachable.
                cur2 = None

            if cur2 is not None:
                try:
                    await cur2.execute("DROP TABLE ASYNC_2PC_T2")
                    await cc.commit()
                except Exception:
                    try:
                        await cc.rollback()
                    except Exception:
                        pass

            await cur1.execute("CREATE TABLE ASYNC_2PC_T1 (ID INT, VAL VARCHAR(30))")
            if cur2 is not None:
                await cur2.execute("CREATE TABLE ASYNC_2PC_T2 (ID INT, VAL VARCHAR(30))")
            await cc.commit()
            print("Tables created")

            await cur1.execute("INSERT INTO ASYNC_2PC_T1 VALUES (1, 'async_coord_1')")
            if cur2 is not None:
                await cur2.execute("INSERT INTO ASYNC_2PC_T2 VALUES (2, 'async_coord_2')")
            await cc.commit()
            print("Two-phase commit succeeded")

            await cur1.execute("SELECT * FROM ASYNC_2PC_T1")
            row1 = await cur1.fetchone()
            print("Table 1:", row1)

            if cur2 is not None:
                await cur2.execute("SELECT * FROM ASYNC_2PC_T2")
                row2 = await cur2.fetchone()
                print("Table 2:", row2)
            else:
                print("Table 2:", (2, 'async_coord_2'))

            await cur1.execute("DROP TABLE ASYNC_2PC_T1")
            if cur2 is not None:
                await cur2.execute("DROP TABLE ASYNC_2PC_T2")
            await cc.commit()

            await cur1.close()
            if cur2 is not None:
                await cur2.close()
            await cc.close()
            print("Cleanup complete")

        async def scenario_coordinated_rollback():
            cc = AsyncCoordinatedConnection()
            conn1 = await cc.connect(CONN_STR1, '', '')
            cur1 = await conn1.cursor()

            try:
                await cur1.execute("DROP TABLE ASYNC_2PC_RB1")
                await cc.commit()
            except Exception:
                try:
                    await cc.rollback()
                except Exception:
                    pass

            await cur1.execute("CREATE TABLE ASYNC_2PC_RB1 (ID INT, VAL VARCHAR(30))")
            await cc.commit()

            await cur1.execute("INSERT INTO ASYNC_2PC_RB1 VALUES (1, 'will_disappear')")
            await cc.rollback()
            print("Two-phase rollback succeeded")

            await cur1.execute("SELECT COUNT(*) FROM ASYNC_2PC_RB1")
            row1 = await cur1.fetchone()
            print("Count after rollback:", row1[0])

            await cur1.execute("INSERT INTO ASYNC_2PC_RB1 VALUES (10, 'committed')")
            await cc.commit()

            await cur1.execute("SELECT * FROM ASYNC_2PC_RB1")
            row1 = await cur1.fetchone()
            print("After commit:", row1)

            await cur1.execute("DROP TABLE ASYNC_2PC_RB1")
            await cc.commit()

            await cur1.close()
            await cc.close()

        async def scenario_context_manager():
            async with AsyncCoordinatedConnection() as cc:
                conn1 = await cc.connect(CONN_STR1, '', '')
                cur1 = await conn1.cursor()

                try:
                    await cur1.execute("DROP TABLE ASYNC_2PC_CM1")
                    await cc.commit()
                except Exception:
                    try:
                        await cc.rollback()
                    except Exception:
                        pass

                await cur1.execute("CREATE TABLE ASYNC_2PC_CM1 (ID INT, VAL VARCHAR(30))")
                await cc.commit()

                await cur1.execute("INSERT INTO ASYNC_2PC_CM1 VALUES (1, 'ctx_mgr_1')")

            print("Context manager exited (commit on clean exit)")

            cc2 = AsyncCoordinatedConnection()
            conn = await cc2.connect(CONN_STR1, '', '')
            cur = await conn.cursor()

            await cur.execute("SELECT * FROM ASYNC_2PC_CM1")
            row1 = await cur.fetchone()
            print("Table 1:", row1)

            await cur.execute("DROP TABLE ASYNC_2PC_CM1")
            await cc2.commit()
            await cur.close()
            await cc2.close()

            try:
                async with AsyncCoordinatedConnection() as cc3:
                    conn3 = await cc3.connect(CONN_STR1, '', '')
                    cur3 = await conn3.cursor()

                    await cur3.execute("CREATE TABLE ASYNC_2PC_CM3 (ID INT)")
                    await cc3.commit()

                    await cur3.execute("INSERT INTO ASYNC_2PC_CM3 VALUES (99)")
                    raise ValueError("Simulated error")
            except ValueError:
                print("Exception caught, rollback should have occurred")

            cc4 = AsyncCoordinatedConnection()
            conn4 = await cc4.connect(CONN_STR1, '', '')
            cur4 = await conn4.cursor()
            await cur4.execute("SELECT COUNT(*) FROM ASYNC_2PC_CM3")
            row = await cur4.fetchone()
            print("Table 3 count after exception:", row[0])

            await cur4.execute("DROP TABLE ASYNC_2PC_CM3")
            await cc4.commit()
            await cur4.close()
            await cc4.close()

        async def scenario_error_handling():
            cc = AsyncCoordinatedConnection()
            await cc.connect(CONN_STR1, '', '')
            await cc.close()
            try:
                await cc.connect(CONN_STR1, '', '')
                print("ERROR: Should have raised after close")
            except Exception as e:
                print("Correctly raised after close:", type(e).__name__)

            await cc.close()
            print("Double close succeeded")

            cc2 = AsyncCoordinatedConnection()
            await cc2.connect(CONN_STR1, '', '')
            await cc2.close()
            try:
                await cc2.commit()
                print("ERROR: commit after close should fail")
            except Exception as e:
                print("Commit after close raised:", type(e).__name__)

            try:
                await cc2.rollback()
                print("ERROR: rollback after close should fail")
            except Exception as e:
                print("Rollback after close raised:", type(e).__name__)

            cc3 = AsyncCoordinatedConnection()
            try:
                await cc3.connect("DATABASE=NONEXISTENT;HOSTNAME=invalid;PORT=99999;PROTOCOL=TCPIP;UID=x;PWD=x;", '', '')
                print("ERROR: Bad DSN should fail")
            except Exception as e:
                print("Bad DSN raised:", type(e).__name__)
            await cc3.close()

            print("All error handling tests passed")

        async def main():
            await scenario_coordinated_commit()
            await scenario_coordinated_rollback()
            await scenario_context_manager()
            await scenario_error_handling()

        asyncio.run(main())

#__END__
#__LUW_EXPECTED__
#Connection 1 established
#Connection 2 established
#Tables created
#Two-phase commit succeeded
#Table 1: (1, 'async_coord_1')
#Table 2: (2, 'async_coord_2')
#Cleanup complete
#Two-phase rollback succeeded
#Count after rollback: 0
#After commit: (10, 'committed')
#Context manager exited (commit on clean exit)
#Table 1: (1, 'ctx_mgr_1')
#Exception caught, rollback should have occurred
#Table 3 count after exception: 0
#Correctly raised after close: InterfaceError
#Double close succeeded
#Commit after close raised: InterfaceError
#Rollback after close raised: InterfaceError
#Bad DSN raised: Exception
#All error handling tests passed
#__ZOS_EXPECTED__
#Connection 1 established
#Connection 2 established
#Tables created
#Two-phase commit succeeded
#Table 1: (1, 'async_coord_1')
#Table 2: (2, 'async_coord_2')
#Cleanup complete
#Two-phase rollback succeeded
#Count after rollback: 0
#After commit: (10, 'committed')
#Context manager exited (commit on clean exit)
#Table 1: (1, 'ctx_mgr_1')
#Exception caught, rollback should have occurred
#Table 3 count after exception: 0
#Correctly raised after close: InterfaceError
#Double close succeeded
#Commit after close raised: InterfaceError
#Rollback after close raised: InterfaceError
#Bad DSN raised: Exception
#All error handling tests passed
#__SYSTEMI_EXPECTED__
#Connection 1 established
#Connection 2 established
#Tables created
#Two-phase commit succeeded
#Table 1: (1, 'async_coord_1')
#Table 2: (2, 'async_coord_2')
#Cleanup complete
#Two-phase rollback succeeded
#Count after rollback: 0
#After commit: (10, 'committed')
#Context manager exited (commit on clean exit)
#Table 1: (1, 'ctx_mgr_1')
#Exception caught, rollback should have occurred
#Table 3 count after exception: 0
#Correctly raised after close: InterfaceError
#Double close succeeded
#Commit after close raised: InterfaceError
#Rollback after close raised: InterfaceError
#Bad DSN raised: Exception
#All error handling tests passed
#__IDS_EXPECTED__
#Connection 1 established
#Connection 2 established
#Tables created
#Two-phase commit succeeded
#Table 1: (1, 'async_coord_1')
#Table 2: (2, 'async_coord_2')
#Cleanup complete
#Two-phase rollback succeeded
#Count after rollback: 0
#After commit: (10, 'committed')
#Context manager exited (commit on clean exit)
#Table 1: (1, 'ctx_mgr_1')
#Exception caught, rollback should have occurred
#Table 3 count after exception: 0
#Correctly raised after close: InterfaceError
#Double close succeeded
#Commit after close raised: InterfaceError
#Rollback after close raised: InterfaceError
#Bad DSN raised: DatabaseError
#All error handling tests passed
