# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2009.                                      |
# +--------------------------------------------------------------------------+
# | This module complies with Django 1.0 and is                              |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Ambrish Bhargava                                                |
# | Version: 0.1.0                                                           |
# +--------------------------------------------------------------------------+

"""
This module implements command line interface for DB2 through Django.
"""

from django.conf import settings
from django.db.backends import BaseDatabaseClient
import types

import os

class DatabaseClient (BaseDatabaseClient):
    
    #Over-riding base method to provide shell support for DB2 through Django.
    def runshell(self):
        cmdArgs = ["db2"]
        
        if (os.name == 'nt'):
            cmdArgs += ["db2 connect to %s" % settings.DATABASE_NAME]
        else:
            cmdArgs += ["connect to %s" % settings.DATABASE_NAME]
        
        user = settings.DATABASE_USER
        if((isinstance(user, types.StringType) or 
            isinstance(user, types.UnicodeType)) and 
            (user != '')):
            cmdArgs += ["user %s" % user]
            
            password = settings.DATABASE_PASSWORD
            if((isinstance(password, types.StringType) or 
                isinstance(password, types.UnicodeType)) and 
                (password != '')):
                cmdArgs += ["using %s" % password]
                
        # db2cmd is the shell which is required to run db2 commands on windows.
        if (os.name == 'nt'):
            os.execvp('db2cmd', cmdArgs)
        else:
            os.execvp('db2', cmdArgs)
                