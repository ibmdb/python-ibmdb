#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import unittest
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

    def test_300_ServerInfo(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_300)

    def run_test_300(self):
        conn = ibm_db.connect(config.database, config.user, config.password)

        server = ibm_db.server_info(conn)

        if server:
            print("DBMS_NAME: string(%d) \"%s\"" % (len(server.DBMS_NAME), server.DBMS_NAME))
            print("DBMS_VER: string(%d) \"%s\"" % (len(server.DBMS_VER), server.DBMS_VER))
            print("DB_CODEPAGE: int(%d)" % server.DB_CODEPAGE)
            print("DB_NAME: string(%d) \"%s\"" % (len(server.DB_NAME), server.DB_NAME))
            print("INST_NAME: string(%d) \"%s\"" % (len(server.INST_NAME), server.INST_NAME))
            print("SPECIAL_CHARS: string(%d) \"%s\"" % (len(server.SPECIAL_CHARS), server.SPECIAL_CHARS))
            print("KEYWORDS: int(%d)" % len(server.KEYWORDS))
            print("DFT_ISOLATION: string(%d) \"%s\"" % (len(server.DFT_ISOLATION), server.DFT_ISOLATION))
            il = ''
            for opt in server.ISOLATION_OPTION:
                il += opt + " "
            print("ISOLATION_OPTION: string(%d) \"%s\"" % (len(il), il))
            print("SQL_CONFORMANCE: string(%d) \"%s\"" % (len(server.SQL_CONFORMANCE), server.SQL_CONFORMANCE))
            print("PROCEDURES:", server.PROCEDURES)
            print("IDENTIFIER_QUOTE_CHAR: string(%d) \"%s\"" % (len(server.IDENTIFIER_QUOTE_CHAR), server.IDENTIFIER_QUOTE_CHAR))
            print("LIKE_ESCAPE_CLAUSE:", server.LIKE_ESCAPE_CLAUSE)
            print("MAX_COL_NAME_LEN: int(%d)" % server.MAX_COL_NAME_LEN)
            print("MAX_ROW_SIZE: int(%d)" % server.MAX_ROW_SIZE)
            print("MAX_IDENTIFIER_LEN: int(%d)" % server.MAX_IDENTIFIER_LEN)
            print("MAX_INDEX_SIZE: int(%d)" % server.MAX_INDEX_SIZE)
            print("MAX_PROC_NAME_LEN: int(%d)" % server.MAX_PROC_NAME_LEN)
            print("MAX_SCHEMA_NAME_LEN: int(%d)" % server.MAX_SCHEMA_NAME_LEN)
            print("MAX_STATEMENT_LEN: int(%d)" % server.MAX_STATEMENT_LEN)
            print("MAX_TABLE_NAME_LEN: int(%d)" % server.MAX_TABLE_NAME_LEN)
            print("NON_NULLABLE_COLUMNS:", server.NON_NULLABLE_COLUMNS)

            ibm_db.close(conn)
        else:
            print("Error.")

#__END__
#__LUW_EXPECTED__
#DBMS_NAME: string(%d) %s
#DBMS_VER: string(%d) %s
#DB_CODEPAGE: int(%d)
#DB_NAME: string(%d) %s
#INST_NAME: string(%d) %s
#SPECIAL_CHARS: string(%d) %s
#KEYWORDS: int(%d)
#DFT_ISOLATION: string(%d) %s
#ISOLATION_OPTION: string(%d) %s
#SQL_CONFORMANCE: string(%d) %s
#PROCEDURES: %s
#IDENTIFIER_QUOTE_CHAR: string(%d) %s
#LIKE_ESCAPE_CLAUSE: %s
#MAX_COL_NAME_LEN: int(%d)
#MAX_ROW_SIZE: int(%d)
#MAX_IDENTIFIER_LEN: int(%d)
#MAX_INDEX_SIZE: int(%d)
#MAX_PROC_NAME_LEN: int(%d)
#MAX_SCHEMA_NAME_LEN: int(%d)
#MAX_STATEMENT_LEN: int(%d)
#MAX_TABLE_NAME_LEN: int(%d)
#NON_NULLABLE_COLUMNS: %s
#__ZOS_EXPECTED__
#DBMS_NAME: string(%d) %s
#DBMS_VER: string(%d) %s
#DB_CODEPAGE: int(%d)
#DB_NAME: string(%d) %s
#INST_NAME: string(%d) %s
#SPECIAL_CHARS: string(%d) %s
#KEYWORDS: int(%d)
#DFT_ISOLATION: string(%d) %s
#ISOLATION_OPTION: string(%d) %s
#SQL_CONFORMANCE: string(%d) %s
#PROCEDURES: %s
#IDENTIFIER_QUOTE_CHAR: string(%d) %s
#LIKE_ESCAPE_CLAUSE: %s
#MAX_COL_NAME_LEN: int(%d)
#MAX_ROW_SIZE: int(%d)
#MAX_IDENTIFIER_LEN: int(%d)
#MAX_INDEX_SIZE: int(%d)
#MAX_PROC_NAME_LEN: int(%d)
#MAX_SCHEMA_NAME_LEN: int(%d)
#MAX_STATEMENT_LEN: int(%d)
#MAX_TABLE_NAME_LEN: int(%d)
#NON_NULLABLE_COLUMNS: %s
#__SYSTEMI_EXPECTED__
#DBMS_NAME: string(%d) %s
#DBMS_VER: string(%d) %s
#DB_CODEPAGE: int(%d)
#DB_NAME: string(%d) %s
#INST_NAME: string(%d) %s
#SPECIAL_CHARS: string(%d) %s
#KEYWORDS: int(%d)
#DFT_ISOLATION: string(%d) %s
#ISOLATION_OPTION: string(%d) %s
#SQL_CONFORMANCE: string(%d) %s
#PROCEDURES: %s
#IDENTIFIER_QUOTE_CHAR: string(%d) %s
#LIKE_ESCAPE_CLAUSE: %s
#MAX_COL_NAME_LEN: int(%d)
#MAX_ROW_SIZE: int(%d)
#MAX_IDENTIFIER_LEN: int(%d)
#MAX_INDEX_SIZE: int(%d)
#MAX_PROC_NAME_LEN: int(%d)
#MAX_SCHEMA_NAME_LEN: int(%d)
#MAX_STATEMENT_LEN: int(%d)
#MAX_TABLE_NAME_LEN: int(%d)
#NON_NULLABLE_COLUMNS: %s
#__IDS_EXPECTED__
#DBMS_NAME: string(%d) %s
#DBMS_VER: string(%d) %s
#DB_CODEPAGE: int(%d)
#DB_NAME: string(%d) %s
#INST_NAME: string(%d) %s
#SPECIAL_CHARS: string(%d) %s
#KEYWORDS: int(%d)
#DFT_ISOLATION: string(%d) %s
#ISOLATION_OPTION: string(%d) %s
#SQL_CONFORMANCE: string(%d) %s
#PROCEDURES: %s
#IDENTIFIER_QUOTE_CHAR: string(%d) %s
#LIKE_ESCAPE_CLAUSE: %s
#MAX_COL_NAME_LEN: int(%d)
#MAX_ROW_SIZE: int(%d)
#MAX_IDENTIFIER_LEN: int(%d)
#MAX_INDEX_SIZE: int(%d)
#MAX_PROC_NAME_LEN: int(%d)
#MAX_SCHEMA_NAME_LEN: int(%d)
#MAX_STATEMENT_LEN: int(%d)
#MAX_TABLE_NAME_LEN: int(%d)
#NON_NULLABLE_COLUMNS: %s
