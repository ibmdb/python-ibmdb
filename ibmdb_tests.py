import os
from os.path import basename, join
import random
import sys
import unittest
import glob
import config
import importlib
# To log while testing
import ibm_db
ibm_db.debug("log.txt")

_HTML_RUNNER = False

try:
    import HtmlTestRunner
    _HTML_RUNNER = True
except ImportError as e:
    print("HtmlTestRunner Package not found .. Running with normal unit test runs")

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

    test_glob_default = "test_*.py"
    test_glob = os.environ.get("SINGLE_PYTHON_TEST", test_glob_default)
    # We need files of a given size for some of the test units, so create them
    # here.
    with open("ibm_db_tests/spook.png", "wb") as f:
        f.write(bytearray([random.getrandbits(8) for _ in range(0, 10291)]))
    with open("ibm_db_tests/pic1.jpg", "wb") as f:
        f.write(bytearray([random.getrandbits(8) for _ in range(0, 15398)]))

    files = glob.glob(join(config.test_dir, test_glob))
    tests = [ basename(_).replace('.py', '') for _ in files ]
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

    return suite

if __name__ == '__main__':
    sys.path.insert(0, config.test_dir)
    if(_HTML_RUNNER):
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(report_name='result',combine_reports=True))
    else:
        unittest.main(verbosity=3)
