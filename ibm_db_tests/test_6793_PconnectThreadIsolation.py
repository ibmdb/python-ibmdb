#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import threading
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_6793_PconnectThreadIsolation(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_6793)

    def run_test_6793(self):
        start_event = threading.Event()
        lock = threading.Lock()
        results = []
        errors = []

        def worker():
            try:
                start_event.wait()

                if sys.platform == 'zos':
                    conn = ibm_db.pconnect(config.database, '', '')
                else:
                    conn = ibm_db.pconnect(config.database, config.user, config.password)

                if not conn:
                    with lock:
                        errors.append("connect_failed")
                    return

                is_active = ibm_db.active(conn)
                conn_id = id(conn)
                ibm_db.close(conn)

                with lock:
                    results.append((conn_id, is_active))
            except Exception:
                with lock:
                    errors.append("worker_exception")

        threads = [threading.Thread(target=worker) for _ in range(2)]

        for t in threads:
            t.start()

        start_event.set()

        for t in threads:
            t.join()

        if errors:
            print("errors:", len(errors))
            return

        unique_conn_handles = len(set([conn_id for conn_id, _ in results]))
        active_count = sum(1 for _, is_active in results if is_active)

        print("workers:", len(results))
        print("active_count:", active_count)
        print("unique_conn_handles:", unique_conn_handles)


#__END__
#__LUW_EXPECTED__
#workers: 2
#active_count: 2
#unique_conn_handles: 2
#__ZOS_EXPECTED__
#workers: 2
#active_count: 2
#unique_conn_handles: 2
#__SYSTEMI_EXPECTED__
#workers: 2
#active_count: 2
#unique_conn_handles: 2
#__IDS_EXPECTED__
#workers: 2
#active_count: 2
#unique_conn_handles: 2
