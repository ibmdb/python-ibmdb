import os
import sys
import platform
import unittest
if sys.version_info >= (3, ):
    from io import StringIO
else:
    from cStringIO import StringIO
import re
import glob
import inspect

import ibm_db
import config

class IbmDbTestFunctions(unittest.TestCase):
  prepconn = ibm_db.connect(config.database, config.user, config.password)
  server = ibm_db.server_info(prepconn)
  ibm_db.close(prepconn)
  
  # See the tests.py comments for this function.
  def setUp(self):
    pass
 
  # This function captures the output of the current test file.
  def capture(self, func):
    buffer = StringIO()
    sys.stdout = buffer
    func()
    sys.stdout = sys.__stdout__
    var = buffer.getvalue()
    #print('\n')
    #print(var)
    return var
  
  # This function grabs the expected output of the current test function for LUW,
  #   located at the bottom of the current test file.
  def expected_LUW(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__LUW_EXPECTED__\n')[-1].split('#__ZOS_EXPECTED__\n')[0]
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for IDS,
  #   located at the bottom of the current test file.
  def expected_IDS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__IDS_EXPECTED__\n')[-1]
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for zOS,
  #   located at the bottom of the current test file.
  def expected_ZOS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__ZOS_EXPECTED__\n')[-1].split('#__SYSTEMI_EXPECTED__\n')[0]
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for zOS,
  #   located at the bottom of the current test file.
  def expected_AS(self, fileName):
    fileHandle = open(fileName, 'r')
    data = fileHandle.read()
    
    start = '#__SYSTEMI_EXPECTED__\n'
    end = '#__IDS_EXPECTED__\n'
    
    if(self.isClientIBMi() and '#__PASE_EXPECTED__' in data):
      start = '#__PASE_EXPECTED__\n'
    elif(not self.isClientIBMi() and '#__PASE_EXPECTED__' in data):
      end = '#__PASE_EXPECTED__\n'
    
    fileInput = data.split(start)[-1].split(end)[0]
    fileHandle.close()
    return fileInput
    
  # This function compares the captured outout with the expected out of
  #   the current test file.
  def assert_expect(self, testFuncName):
    callstack = inspect.stack(0)
    expected = None
    output = self.capture(testFuncName)
    
    try:
      if (self.isServerIBMi(self.server)):
        expected = self.expected_AS(callstack[1][1])
      elif (self.isServerZOS(self.server)):
        expected = self.expected_ZOS(callstack[1][1])
      elif (self.isServerInformix(self.server)):
        expected = self.expected_IDS(callstack[1][1])
      else:
        expected = self.expected_LUW(callstack[1][1])
    finally:
      del callstack
    
    expected = expected.replace('#', '')
    
    if sys.version_info >= (2, 7):
      self.maxDiff = None
      self.assertMultiLineEqual(expected, output)
    else:
      self.assertEqual(expected, output)

  # This function will compare using Regular Expressions
  # based on the servre
  def assert_expectf(self, testFuncName):
    callstack = inspect.stack(0)
    try:
      if (self.isServerIBMi(self.server)):
          pattern = self.expected_AS(callstack[1][1])
      elif (self.isServerZOS(self.server)):
          pattern = self.expected_ZOS(callstack[1][1])
      elif (self.isServerInformix(self.server)):
          pattern = self.expected_IDS(callstack[1][1])
      else:
          pattern = self.expected_LUW(callstack[1][1])
      
      sym = ['\[','\]','\(','\)']
      for chr in sym:
          pattern = re.sub(chr, '\\' + chr, pattern)

      pattern = pattern.replace('#', '')
      #pattern = pattern.replace('\r', '')
      pattern = re.sub('%s', '.*?', pattern)
      pattern = re.sub('%d', '\\d+', pattern)

      output = self.capture(testFuncName)
      #output = output.replace('\r', '')
      if sys.version_info >= (2, 7):
        self.assertRegexpMatches(output, pattern)
      else:
        result = re.match(pattern, output)
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
  
  def isServerIBMi(self, serverinfo):
    return serverinfo.DBMS_NAME == 'AS'
  
  def isServerZOS(self, serverinfo):
    return serverinfo.DBMS_NAME == 'DB2'
  
  def isServerInformix(self, serverinfo):
    return serverinfo.DBMS_NAME[0:3] == 'IDS'
  
  def isServerLUW(self, serverinfo):
    return serverinfo.DBMS_NAME[0:4] == 'DB2/'
  
  def isClientIBMi(self):
    return platform.system() == 'OS400'
