import os
from os.path import basename, join
import argparse
import random
import sys
import unittest
import glob
import config
import importlib
# To log while testing
import ibm_db
# ibm_db.debug("log.txt")

# Ensure test directory is on sys.path so importlib can find test modules
sys.path.insert(0, config.test_dir)

_HTML_RUNNER = False

try:
    import HtmlTestRunner
    _HTML_RUNNER = True
except ImportError as e:
    print("HtmlTestRunner Package not found .. Running with normal unit test runs")

# Test runner for ibm_db.
#
# Usage:
#   python ibmdb_tests.py                                        # run both sync + async
#   python ibmdb_tests.py --async                                # run only async tests
#   python ibmdb_tests.py --sync                                 # run only sync tests
#   python ibmdb_tests.py --async --test test_05_async_fetch.py  # single async test
#   python ibmdb_tests.py --sync  --test test_006_ConnPassingOpts.py  # single sync test
#
# Legacy: SINGLE_PYTHON_TEST env var is also supported for backward compatibility.
#   set SINGLE_PYTHON_TEST=test_006_ConnPassingOpts.py
#   python ibmdb_tests.py

# Parse command-line arguments before unittest sees them
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('--async', dest='async_only', action='store_true',
                     help='Run only async tests')
_parser.add_argument('--sync', dest='sync_only', action='store_true',
                     help='Run only sync tests')
_parser.add_argument('--test', dest='single_test', default=None,
                     help='Run a single test file (glob pattern)')
_args, _remaining_argv = _parser.parse_known_args()
sys.argv = [sys.argv[0]] + _remaining_argv  # pass remaining args to unittest

# Support legacy SINGLE_PYTHON_TEST env var
if _args.single_test is None:
    _args.single_test = os.environ.get('SINGLE_PYTHON_TEST')

# Override standard test-loading behavior
def _load_sync_tests(suite, test_glob=None):
    """Load sync tests from ibm_db_tests/."""
    test_glob_default = "test_*.py"
    if test_glob is None:
        test_glob = test_glob_default
    # We need files of a given size for some of the test units, so create them
    # here.
    with open("ibm_db_tests/spook.png", "wb") as f:
        f.write(bytearray([random.getrandbits(8) for _ in range(0, 10291)]))
    with open("ibm_db_tests/pic1.jpg", "wb") as f:
        f.write(bytearray([random.getrandbits(8) for _ in range(0, 15398)]))

    files = glob.glob(join(config.test_dir, test_glob))
    tests = [ basename(_).replace('.py', '') for _ in files ]
    tests = [ t for t in tests if t ]  # Filter out any empty module names
    tests.sort()

    for test in tests:
        skip = (test.startswith('test_002') or \
                test.startswith('test_007') or \
                test.startswith('test_080') or \
                test.startswith('test_090') or \
                test.startswith('test_053') or \
                test.startswith('test_196') or \
                test.startswith('test_220') or \
                test.startswith('test_221') or \
                test.startswith('test_264') or \
                test.startswith('test_6792'))
        if test_glob != test_glob_default or not skip:
            mod = importlib.import_module(test)
            suite.addTest(mod.IbmDbTestCase(test))


def _load_async_tests(suite, test_glob=None):
    """Load async tests from asyncio_testsuite/."""
    if test_glob is None:
        test_glob = "test_*.py"
    async_test_dir = 'asyncio_testsuite'
    if async_test_dir not in sys.path:
        sys.path.insert(0, async_test_dir)
    async_files = glob.glob(join(async_test_dir, test_glob))
    async_tests = [basename(_).replace('.py', '') for _ in async_files]
    async_tests = [t for t in async_tests if t not in ('test_utils', 'run_all')]
    async_tests.sort()
    for test in async_tests:
        mod = importlib.import_module(test)
        suite.addTest(mod.IbmDbTestCase(test))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    single = _args.single_test

    if _args.async_only:
        _load_async_tests(suite, single)
    elif _args.sync_only:
        _load_sync_tests(suite, single)
    else:
        # Default: run both
        _load_sync_tests(suite, single)
        _load_async_tests(suite, single)

    return suite

if __name__ == '__main__':
    sys.path.insert(0, 'asyncio_testsuite')
    if(_HTML_RUNNER):
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(report_name='result',combine_reports=True))
    else:
        unittest.main(verbosity=3)
