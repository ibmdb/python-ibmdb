import os
import sys
import unittest
import StringIO
import re
import glob
import config

class IbmDbTest(unittest.TestCase):
  
  slash = '/'
  
  # Currently, this function serves no purpose.
  # However, this function has to be defined if the
  #   unittest.TestCase is inherited in the given class.
  # For future reference, this function is called 
  #   everytime a test is ran in this testsuite.
  def setUp(self):
    pass

  # This function gets a list of all the test files located
  #   in the current_dir/config.test_dir directory.
  def getFileList(self):
    if (sys.platform[0:3] == 'win'):
      self.slash = '\\'
    dir = config.test_dir + self.slash
    if (os.environ.get("SINGLE_PYTHON_TEST", None)):
      testfile = dir + os.environ.get("SINGLE_PYTHON_TEST", None)
      filelist = glob.glob(testfile)
    else:
      filelist = glob.glob(dir + "test_*.py")
      
    for i in range(0, len(filelist)):
      filelist[i] = filelist[i].replace('.py', '')
      filelist[i] = filelist[i].replace(config.test_dir + self.slash, '')
    filelist.sort()
    return filelist

  # This function is called to run all the tests.
  def runTest(self):
    filelist = self.getFileList();
    suite = unittest.TestSuite()
    
    sys.path = [os.path.dirname(os.path.abspath(__file__)) + self.slash + config.test_dir] + sys.path[0:]
    
    for i in range(0, len(filelist)):
      exec("import %s" % filelist[i])
      testFuncName = filelist[i].replace(config.test_dir + self.slash, '')
      exec("suite.addTest(%s.IbmDbTestCase(testFuncName))" % filelist[i])
      
    unittest.TextTestRunner(verbosity=2).run(suite) 

obj = IbmDbTest()
suite = obj.runTest()
