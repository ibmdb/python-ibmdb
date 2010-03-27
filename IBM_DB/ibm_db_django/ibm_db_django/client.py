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
# | Authors: Ambrish Bhargava, Tarun Pasrija, Rahul Priyadarshi              |
# +--------------------------------------------------------------------------+

"""
This module implements command line interface for DB2 through Django.
"""

from django.db.backends import BaseDatabaseClient
from django import VERSION as djangoVersion
import types

import os

class DatabaseClient(BaseDatabaseClient):
    
    #Over-riding base method to provide shell support for DB2 through Django.
    def runshell(self):
        if (djangoVersion[0:2] <= (1, 0)):
            from django.conf import settings
            database_name = settings.DATABASE_NAME
            database_user = settings.DATABASE_USER
            database_password = settings.DATABASE_PASSWORD
        elif (djangoVersion[0:2] <= (1, 1)):
            settings_dict = self.connection.settings_dict
            database_name = settings_dict['DATABASE_NAME']
            database_user = settings_dict['DATABASE_USER']
            database_password = settings_dict['DATABASE_PASSWORD']
        else:
            settings_dict = self.connection.settings_dict
            database_name = settings_dict['NAME']
            database_user = settings_dict['USER']
            database_password = settings_dict['PASSWORD']
            
        cmdArgs = ["db2"]
        
        if (os.name == 'nt'):
            cmdArgs += ["db2 connect to %s" % database_name]
        else:
            cmdArgs += ["connect to %s" % database_name]
        
        if ((isinstance(database_user, types.StringType) or 
            isinstance(database_user, types.UnicodeType)) and 
            (database_user != '')):
            cmdArgs += ["user %s" % database_user]
            
            if ((isinstance(database_password, types.StringType) or 
                isinstance(database_password, types.UnicodeType)) and 
                (database_password != '')):
                cmdArgs += ["using %s" % database_password]
                
        # db2cmd is the shell which is required to run db2 commands on windows.
        if (os.name == 'nt'):
            os.execvp('db2cmd', cmdArgs)
        else:
            os.execvp('db2', cmdArgs)
