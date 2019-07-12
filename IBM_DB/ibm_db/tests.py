import os
from os.path import basename, join
import sys
import unittest
import glob
import config
import importlib

# Test runner for ibm_db. Normally one could use something like:
#
# Run all in the tests directory:
#   python -m unittest discover -v -s tests
#
# Run all tests matching specified pattern or specific test:
#   python -m unittest discover -v -s tests -p 'test_*FetchAssocSelect*.py'
#   python -m unittest discover -v -s tests -p test_006_ConnPassingOpts.py
#
# However, for running all the tests, we need to ensure that test_000_PrepareDb
# is run first to set up the database. Possibly this could be moved to a
# separate task which is run by itself prior to running any tests, which
# would simplify things a bit.

# Override standard test-loading behavior
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    test_glob = os.environ.get("SINGLE_PYTHON_TEST", "test_*.py")
    files = glob.glob(join(config.test_dir, test_glob))
    tests = [ basename(_).replace('.py', '') for _ in files ]
    tests.sort()

    for test in tests:
        mod = importlib.import_module(test)
        suite.addTest(mod.IbmDbTestCase(test))

    return suite

if __name__ == '__main__':
    sys.path.insert(0, config.test_dir)
    unittest.main(verbosity=2)
