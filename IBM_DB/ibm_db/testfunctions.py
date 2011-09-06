import os
import sys
import unittest
import StringIO
import re
import glob
import inspect

import ibm_db
import config

class IbmDbTestFunctions(unittest.TestCase):
  
  # See the tests.py comments for this function.
  def setUp(self):
    pass
 
  # This function captures the output of the current test file.
  def capture(self, func):
    buffer = StringIO.StringIO()
    sys.stdout = buffer
    func()
    sys.stdout = sys.__stdout__
    var = buffer.getvalue()
    var = var.replace('\n', '').replace('\r', '')
    return var
  
  # This function grabs the expected output of the current test function for LUW,
  #   located at the bottom of the current test file.
  def expected_LUW(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__LUW_EXPECTED__')[-1].split('#__ZOS_EXPECTED__')[0].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for IDS,
  #   located at the bottom of the current test file.
  def expected_IDS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__IDS_EXPECTED__')[-1].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for zOS,
  #   located at the bottom of the current test file.
  def expected_ZOS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__ZOS_EXPECTED__')[-1].split('#__SYSTEMI_EXPECTED__')[0].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for zOS,
  #   located at the bottom of the current test file.
  def expected_AS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__SYSTEMI_EXPECTED__')[-1].split('#__IDS_EXPECTED__')[0].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput
    
  # This function compares the captured outout with the expected out of
  #   the current test file.
  def assert_expect(self, testFuncName):
    callstack = inspect.stack(0)
    try:
      prepconn = ibm_db.connect(config.database, config.user, config.password)
      server = ibm_db.server_info(prepconn)
      ibm_db.close(prepconn)
      if (server.DBMS_NAME[0:2] == "AS"):
          self.assertEqual(self.capture(testFuncName), self.expected_AS(callstack[1][1]))
      elif (server.DBMS_NAME == "DB2"):
          self.assertEqual(self.capture(testFuncName), self.expected_ZOS(callstack[1][1]))
      elif (server.DBMS_NAME[0:3] == "IDS"):
          self.assertEqual(self.capture(testFuncName), self.expected_IDS(callstack[1][1]))
      else:
          self.assertEqual(self.capture(testFuncName), self.expected_LUW(callstack[1][1]))
      
    finally:
      del callstack

  # This function will compare using Regular Expressions
  # based on the servre
  def assert_expectf(self, testFuncName):
    callstack = inspect.stack(0)
    try:
      prepconn = ibm_db.connect(config.database, config.user, config.password)
      server = ibm_db.server_info(prepconn)
      ibm_db.close(prepconn)
      if (server.DBMS_NAME[0:2] == "AS"):
          pattern = self.expected_AS(callstack[1][1])
      elif (server.DBMS_NAME == "DB2"):
          pattern = self.expected_ZOS(callstack[1][1])
      elif (server.DBMS_NAME[0:3] == "IDS"):
          pattern = self.expected_IDS(callstack[1][1])
      else:
          pattern = self.expected_LUW(callstack[1][1])
      
      sym = ['\[','\]','\(','\)']
      for chr in sym:
          pattern = re.sub(chr, '\\' + chr, pattern)

      pattern = re.sub('%s', '.*?', pattern)
      pattern = re.sub('%d', '\\d+', pattern)

      result = re.match(pattern, self.capture(testFuncName))
      self.assertNotEqual(result, None)
    finally:
      del callstack
      
  #def assert_throw_blocks(self, testFuncName):
  #  callstack = inspect.stack(0)
  #  try:

  # This function needs to be declared here, regardless of if there 
  #   is any body to this function
  def runTest(self):
    pass
