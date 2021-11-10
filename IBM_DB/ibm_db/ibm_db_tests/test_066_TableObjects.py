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

    def test_066_TableObjects(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_066)

    def run_test_066(self):
        conn = ibm_db.connect(config.database, config.user, config.password)
        server = ibm_db.server_info( conn )

        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.tables(conn, None, config.user.lower(), 'animals')
        else:
            result = ibm_db.tables(conn, None, config.user.upper(), 'ANIMALS')

#    NOTE: This is a workaround
#    function fetch_object() to be implemented...
#    row = ibm_db.fetch_object(result)

        class Row:
            pass

        data = ibm_db.fetch_assoc(result)
        while ( data ):
            row = Row()
            if (server.DBMS_NAME[0:3] == 'IDS'):
                row.table_schem = data['table_schem']
                row.table_name = data['table_name']
                row.table_type = data['table_type']
                row.remarks = data['remarks']

                print("Schema:  %s" % row.table_schem)
                print("Name:    %s" % row.table_name)
                print("Type:    %s" % row.table_type)
                print("Remarks: %s\n" % row.remarks)
            else:
                row.TABLE_SCHEM = data['TABLE_SCHEM']
                row.TABLE_NAME = data['TABLE_NAME']
                row.TABLE_TYPE = data['TABLE_TYPE']
                row.REMARKS = data['REMARKS']

                print("Schema:  %s" % row.TABLE_SCHEM)
                print("Name:    %s" % row.TABLE_NAME)
                print("Type:    %s" % row.TABLE_TYPE)
                print("Remarks: %s\n" % row.REMARKS)
#      row = ibm_db.fetch_object(result)
            data = ibm_db.fetch_assoc(result)

        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.tables(conn, None, config.user.lower(), 'animal_pics')
        else:
            result = ibm_db.tables(conn, None, config.user.upper(), 'ANIMAL_PICS')

#    row = ibm_db.fetch_object(result)
        data = ibm_db.fetch_assoc(result)
        while (data ):
            row = Row()
            if (server.DBMS_NAME[0:3] == 'IDS'):
                row.table_schem = data['table_schem']
                row.table_name = data['table_name']
                row.table_type = data['table_type']
                row.remarks = data['remarks']

                print("Schema:  %s" % row.table_schem)
                print("Name:    %s" % row.table_name)
                print("Type:    %s" % row.table_type)
                print("Remarks: %s\n" % row.remarks)
            else:
                row.TABLE_SCHEM = data['TABLE_SCHEM']
                row.TABLE_NAME = data['TABLE_NAME']
                row.TABLE_TYPE = data['TABLE_TYPE']
                row.REMARKS = data['REMARKS']

                print("Schema:  %s" % row.TABLE_SCHEM)
                print("Name:    %s" % row.TABLE_NAME)
                print("Type:    %s" % row.TABLE_TYPE)
                print("Remarks: %s\n" % row.REMARKS)
#      row = ibm_db.fetch_object(result)
            data = ibm_db.fetch_assoc(result)

        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.tables(conn, None, config.user.lower(), 'anime_cat')
        else:
            result = ibm_db.tables(conn, None, config.user.upper(), 'ANIME_CAT')

#    row = ibm_db.fetch_object(result)
        data = ibm_db.fetch_assoc(result)
        while ( data ):
            row = Row()
            if (server.DBMS_NAME[0:3] == 'IDS'):
                row.table_schem = data['table_schem']
                row.table_name = data['table_name']
                row.table_type = data['table_type']
                row.remarks = data['remarks']

                print("Schema:  %s" % row.table_schem)
                print("Name:    %s" % row.table_name)
                print("Type:    %s" % row.table_type)
                print("Remarks: %s\n" % row.remarks)
            else:
                row.TABLE_SCHEM = data['TABLE_SCHEM']
                row.TABLE_NAME = data['TABLE_NAME']
                row.TABLE_TYPE = data['TABLE_TYPE']
                row.REMARKS = data['REMARKS']

                print("Schema:  %s" % row.TABLE_SCHEM)
                print("Name:    %s" % row.TABLE_NAME)
                print("Type:    %s" % row.TABLE_TYPE)
                print("Remarks: %s\n" % row.REMARKS)
#      row = ibm_db.fetch_object(result)
            data = ibm_db.fetch_assoc(result)

        ibm_db.free_result(result)
        ibm_db.close(conn)

#__END__
#__LUW_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: None
#__ZOS_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: 
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: 
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: 
#__SYSTEMI_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: None
#__IDS_EXPECTED__
#Schema:  %s
#Name:    animals
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    animal_pics
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    anime_cat
#Type:    VIEW
#Remarks: None
