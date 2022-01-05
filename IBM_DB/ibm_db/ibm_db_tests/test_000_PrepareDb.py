#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function
import sys
import os
import unittest
import ibm_db
#need to add this line below to each file to make the connect parameters available to all the test files
import config
from testfunctions import IbmDbTestFunctions

name = 'name'
picture = 'picture'

class IbmDbTestCase(unittest.TestCase):

    def test_000_PrepareDb(self):
        obj = IbmDbTestFunctions()
        obj.assert_expect(self.run_test_000)

    def run_test_000(self):
        # Make a connection
        conn = ibm_db.connect(config.database, config.user, config.password)

        # Get the server type
        server = ibm_db.server_info( conn )

        # Drop the animal table, in case it exists
        drop = 'DROP TABLE animals'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the animal table
        create = 'CREATE TABLE animals (id INTEGER, breed VARCHAR(32), name CHAR(16), weight DECIMAL(7,2))'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the animal table
        animals = (
            (0, 'cat',        'Pook',         3.2),
            (1, 'dog',        'Peaches',      12.3),
            (2, 'horse',      'Smarty',       350.0),
            (3, 'gold fish',  'Bubbles',      0.1),
            (4, 'budgerigar', 'Gizmo',        0.2),
            (5, 'goat',       'Rickety Ride', 9.7),
            (6, 'llama',      'Sweater',      150)
        )
        insert = 'INSERT INTO animals (id, breed, name, weight) VALUES (?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for animal in animals:
                result = ibm_db.execute(stmt, animal)

        # Drop the test view, in case it exists
        drop = 'DROP VIEW anime_cat'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create test view
        ibm_db.exec_immediate(conn, """CREATE VIEW anime_cat AS
            SELECT name, breed FROM animals
            WHERE id = 0""")

        # Drop the animal_pics table
        drop = 'DROP TABLE animal_pics'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the animal_pics table
        create = 'CREATE TABLE animal_pics (name VARCHAR(32), picture BLOB)'
        result = ibm_db.exec_immediate(conn, create)

        # Populate the view table
        animals = (
            ('Spook', 'spook.png'),
            ('Helmut', 'pic1.jpg'),
        )
        insert = 'INSERT INTO animal_pics (name, picture) VALUES (?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if (not stmt):
            print ("Attempt to prepare statement failed.")
            return 0
        for animal in animals:
            name = animal[0]

            with open(os.path.dirname(os.path.abspath(__file__)) + '/' + animal[1], 'rb') as fileHandle:
                picture = fileHandle.read()
                if (not picture):
                    print ("Could not retrieve picture '%s'" % animal[1])
                    return 0
                ibm_db.bind_param(stmt, 1, name, ibm_db.SQL_PARAM_INPUT)
                ibm_db.bind_param(stmt, 2, picture, ibm_db.SQL_PARAM_INPUT)
                result = ibm_db.execute(stmt)

        # Drop the department table, in case it exists
        drop = 'DROP TABLE department'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the department table
        create = 'CREATE TABLE department (deptno CHAR(3) NOT NULL, deptname VARCHAR(29) NOT NULL, mgrno CHAR(6), admrdept CHAR(3) NOT NULL, location CHAR(16))'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the department table
        department = (
            ('A00', 'SPIFFY COMPUTER SERVICE DIV.', '000010', 'A00', None),
            ('B01', 'PLANNING',                     '000020', 'A00', None),
            ('C01', 'INFORMATION CENTER',           '000030', 'A00', None),
            ('D01', 'DEVELOPMENT CENTER',           None,     'A00', None),
            ('D11', 'MANUFACTURING SYSTEMS',        '000060', 'D01', None),
            ('D21', 'ADMINISTRATION SYSTEMS',       '000070', 'D01', None),
            ('E01', 'SUPPORT SERVICES',             '000050', 'A00', None),
            ('E11', 'OPERATIONS',                   '000090', 'E01', None),
            ('E21', 'SOFTWARE SUPPORT',             '000100', 'E01', None)
        )
        insert = 'INSERT INTO department (deptno, deptname, mgrno, admrdept, location) VALUES (?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for dept in department:
                result = ibm_db.execute(stmt, dept)

        # Drop the emp_act table, in case it exists
        drop = 'DROP TABLE emp_act'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the emp_act table
        create = 'CREATE TABLE emp_act (empno CHAR(6) NOT NULL, projno CHAR(6) NOT NULL, actno SMALLINT NOT NULL, emptime DECIMAL(5,2), emstdate DATE, emendate DATE)'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the emp_act table
        emp_act = (
            ('000010', 'MA2100',   10,   0.50,  '1982-01-01',  '1982-11-01'),
            ('000010', 'MA2110',   10,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000010', 'AD3100',   10,   0.50,  '1982-01-01',  '1982-07-01'),
            ('000020', 'PL2100',   30,   1.00,  '1982-01-01',  '1982-09-15'),
            ('000030', 'IF1000',   10,   0.50,  '1982-06-01',  '1983-01-01'),
            ('000030', 'IF2000',   10,   0.50,  '1982-01-01',  '1983-01-01'),
            ('000050', 'OP1000',   10,   0.25,  '1982-01-01',  '1983-02-01'),
            ('000050', 'OP2010',   10,   0.75,  '1982-01-01',  '1983-02-01'),
            ('000070', 'AD3110',   10,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000090', 'OP1010',   10,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000100', 'OP2010',   10,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000110', 'MA2100',   20,   1.00,  '1982-01-01',  '1982-03-01'),
            ('000130', 'IF1000',   90,   1.00,  '1982-01-01',  '1982-10-01'),
            ('000130', 'IF1000',  100,   0.50,  '1982-10-01',  '1983-01-01'),
            ('000140', 'IF1000',   90,   0.50,  '1982-10-01',  '1983-01-01'),
            ('000140', 'IF2000',  100,   1.00,  '1982-01-01',  '1982-03-01'),
            ('000140', 'IF2000',  100,   0.50,  '1982-03-01',  '1982-07-01'),
            ('000140', 'IF2000',  110,   0.50,  '1982-03-01',  '1982-07-01'),
            ('000140', 'IF2000',  110,   0.50,  '1982-10-01',  '1983-01-01'),
            ('000150', 'MA2112',   60,   1.00,  '1982-01-01',  '1982-07-15'),
            ('000150', 'MA2112',  180,   1.00,  '1982-07-15',  '1983-02-01'),
            ('000160', 'MA2113',   60,   1.00,  '1982-07-15',  '1983-02-01'),
            ('000170', 'MA2112',   60,   1.00,  '1982-01-01',  '1983-06-01'),
            ('000170', 'MA2112',   70,   1.00,  '1982-06-01',  '1983-02-01'),
            ('000170', 'MA2113',   80,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000180', 'MA2113',   70,   1.00,  '1982-04-01',  '1982-06-15'),
            ('000190', 'MA2112',   70,   1.00,  '1982-02-01',  '1982-10-01'),
            ('000190', 'MA2112',   80,   1.00,  '1982-10-01',  '1983-10-01'),
            ('000200', 'MA2111',   50,   1.00,  '1982-01-01',  '1982-06-15'),
            ('000200', 'MA2111',   60,   1.00,  '1982-06-15',  '1983-02-01'),
            ('000210', 'MA2113',   80,   0.50,  '1982-10-01',  '1983-02-01'),
            ('000210', 'MA2113',  180,   0.50,  '1982-10-01',  '1983-02-01'),
            ('000220', 'MA2111',   40,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000230', 'AD3111',   60,   1.00,  '1982-01-01',  '1982-03-15'),
            ('000230', 'AD3111',   60,   0.50,  '1982-03-15',  '1982-04-15'),
            ('000230', 'AD3111',   70,   0.50,  '1982-03-15',  '1982-10-15'),
            ('000230', 'AD3111',   80,   0.50,  '1982-04-15',  '1982-10-15'),
            ('000230', 'AD3111',  180,   1.00,  '1982-10-15',  '1983-01-01'),
            ('000240', 'AD3111',   70,   1.00,  '1982-02-15',  '1982-09-15'),
            ('000240', 'AD3111',   80,   1.00,  '1982-09-15',  '1983-01-01'),
            ('000250', 'AD3112',   60,   1.00,  '1982-01-01',  '1982-02-01'),
            ('000250', 'AD3112',   60,   0.50,  '1982-02-01',  '1982-03-15'),
            ('000250', 'AD3112',   60,   0.50,  '1982-12-01',  '1983-01-01'),
            ('000250', 'AD3112',   60,   1.00,  '1983-01-01',  '1983-02-01'),
            ('000250', 'AD3112',   70,   0.50,  '1982-02-01',  '1982-03-15'),
            ('000250', 'AD3112',   70,   1.00,  '1982-03-15',  '1982-08-15'),
            ('000250', 'AD3112',   70,   0.25,  '1982-08-15',  '1982-10-15'),
            ('000250', 'AD3112',   80,   0.25,  '1982-08-15',  '1982-10-15'),
            ('000250', 'AD3112',   80,   0.50,  '1982-10-15',  '1982-12-01'),
            ('000250', 'AD3112',  180,   0.50,  '1982-08-15',  '1983-01-01'),
            ('000260', 'AD3113',   70,   0.50,  '1982-06-15',  '1982-07-01'),
            ('000260', 'AD3113',   70,   1.00,  '1982-07-01',  '1983-02-01'),
            ('000260', 'AD3113',   80,   1.00,  '1982-01-01',  '1982-03-01'),
            ('000260', 'AD3113',   80,   0.50,  '1982-03-01',  '1982-04-15'),
            ('000260', 'AD3113',  180,   0.50,  '1982-03-01',  '1982-04-15'),
            ('000260', 'AD3113',  180,   1.00,  '1982-04-15',  '1982-06-01'),
            ('000260', 'AD3113',  180,   0.50,  '1982-06-01',  '1982-07-01'),
            ('000270', 'AD3113',   60,   0.50,  '1982-03-01',  '1982-04-01'),
            ('000270', 'AD3113',   60,   1.00,  '1982-04-01',  '1982-09-01'),
            ('000270', 'AD3113',   60,   0.25,  '1982-09-01',  '1982-10-15'),
            ('000270', 'AD3113',   70,   0.75,  '1982-09-01',  '1982-10-15'),
            ('000270', 'AD3113',   70,   1.00,  '1982-10-15',  '1983-02-01'),
            ('000270', 'AD3113',   80,   1.00,  '1982-01-01',  '1982-03-01'),
            ('000270', 'AD3113',   80,   0.50,  '1982-03-01',  '1982-04-01'),
            ('000280', 'OP1010',  130,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000290', 'OP1010',  130,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000300', 'OP1010',  130,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000310', 'OP1010',  130,   1.00,  '1982-01-01',  '1983-02-01'),
            ('000320', 'OP2011',  140,   0.75,  '1982-01-01',  '1983-02-01'),
            ('000320', 'OP2011',  150,   0.25,  '1982-01-01',  '1983-02-01'),
            ('000330', 'OP2012',  140,   0.25,  '1982-01-01',  '1983-02-01'),
            ('000330', 'OP2012',  160,   0.75,  '1982-01-01',  '1983-02-01'),
            ('000340', 'OP2013',  140,   0.50,  '1982-01-01',  '1983-02-01'),
            ('000340', 'OP2013',  170,   0.50,  '1982-01-01',  '1983-02-01'),
            ('000020', 'PL2100',   30,   1.00,  '1982-01-01',  '1982-09-15')
        )
        insert = 'INSERT INTO emp_act (empno, projno, actno, emptime, emstdate, emendate) VALUES (?, ?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for emp in emp_act:
                result = ibm_db.execute(stmt, emp)

        # Drop the employee table, in case it exists
        drop = 'DROP TABLE employee'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the employee table
        create = 'CREATE TABLE employee (empno CHAR(6) NOT NULL, firstnme VARCHAR(12) NOT NULL, midinit CHAR(1) NOT NULL, lastname VARCHAR(15) NOT NULL, workdept CHAR(3), phoneno CHAR(4), hiredate DATE, job CHAR(8), edlevel SMALLINT NOT NULL, sex CHAR(1), birthdate DATE, salary DECIMAL(9,2), bonus DECIMAL(9,2), comm DECIMAL(9,2))'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the employee table
        if('zos' in sys.platform):
            employee = (
                ('000010', 'CHRISTINE', 'I', 'HAAS',       'A00', '3978', '1965-01-01', 'PRES',     18, 'F', '1933-08-24', 52750.00, 1000, 4220),
                ('000020', 'MICHAEL',   'L', 'THOMPSON',   'B01', '3476', '1973-10-10', 'MANAGER',  18, 'M' ,'1948-02-02', 41250.00,  800, 3300),
                ('000030', 'SALLY',     'A', 'KWAN',       'C01', '4738', '1975-04-05', 'MANAGER',  20, 'F' ,'1941-05-11', 38250.00,  800, 3060),
                ('000050', 'JOHN',      'B', 'GEYER',      'E01', '6789', '1949-08-17', 'MANAGER',  16, 'M' ,'1925-09-15', 40175.00,  800, 3214),
                ('000060', 'IRVING',    'F', 'STERN',      'D11', '6423', '1973-09-14', 'MANAGER',  16, 'M' ,'1945-07-07', 32250.00,  500, 2580),
                ('000070', 'EVA',       'D', 'PULASKI',    'D21', '7831', '1980-09-30', 'MANAGER',  16, 'F' ,'1953-05-26', 36170.00,  700, 2893),
                ('000090', 'EILEEN',    'W', 'HENDERSON',  'E11', '5498', '1970-08-15', 'MANAGER',  16, 'F' ,'1941-05-15', 29750.00,  600, 2380),
                ('000100', 'THEODORE',  'Q', 'SPENSER',    'E21', '0972', '1980-06-19', 'MANAGER',  14, 'M' ,'1956-12-18', 26150.00,  500, 2092),
                ('000110', 'VINCENZO',  'G', 'LUCCHESSI',  'A00', '3490', '1958-05-16', 'SALESREP', 19, 'M' ,'1929-11-05', 46500.00,  900, 3720),
                ('000120', 'SEAN',      ' ' , 'OCONNELL',   'A00', '2167', '1963-12-05', 'CLERK',    14, 'M' ,'1942-10-18', 29250.00,  600, 2340),
                ('000130', 'DOLORES',   'M', 'QUINTANA',   'C01', '4578', '1971-07-28', 'ANALYST',  16, 'F' ,'1925-09-15', 23800.00,  500, 1904),
                ('000140', 'HEATHER',   'A', 'NICHOLLS',   'C01', '1793', '1976-12-15', 'ANALYST',  18, 'F' ,'1946-01-19', 28420.00,  600, 2274),
                ('000150', 'BRUCE',     ' ' , 'ADAMSON',    'D11', '4510', '1972-02-12', 'DESIGNER', 16, 'M' ,'1947-05-17', 25280.00,  500, 2022),
                ('000160', 'ELIZABETH', 'R', 'PIANKA',     'D11', '3782', '1977-10-11', 'DESIGNER', 17, 'F' ,'1955-04-12', 22250.00,  400, 1780),
                ('000170', 'MASATOSHI', 'J', 'YOSHIMURA',  'D11', '2890', '1978-09-15', 'DESIGNER', 16, 'M' ,'1951-01-05', 24680.00,  500, 1974),
                ('000180', 'MARILYN',   'S', 'SCOUTTEN',   'D11', '1682', '1973-07-07', 'DESIGNER', 17, 'F' ,'1949-02-21', 21340.00,  500, 1707),
                ('000190', 'JAMES',     'H', 'WALKER',     'D11', '2986', '1974-07-26', 'DESIGNER', 16, 'M' ,'1952-06-25', 20450.00,  400, 1636),
                ('000200', 'DAVID',     ' ' , 'BROWN',      'D11', '4501', '1966-03-03', 'DESIGNER', 16, 'M' ,'1941-05-29', 27740.00,  600, 2217),
                ('000210', 'WILLIAM',   'T', 'JONES',      'D11', '0942', '1979-04-11', 'DESIGNER', 17, 'M' ,'1953-02-23', 18270.00,  400, 1462),
                ('000220', 'JENNIFER',  'K', 'LUTZ',       'D11', '0672', '1968-08-29', 'DESIGNER', 18, 'F' ,'1948-03-19', 29840.00,  600, 2387),
                ('000230', 'JAMES',     'J', 'JEFFERSON',  'D21', '2094', '1966-11-21', 'CLERK',    14, 'M' ,'1935-05-30', 22180.00,  400, 1774),
                ('000240', 'SALVATORE', 'M', 'MARINO',     'D21', '3780', '1979-12-05', 'CLERK',    17, 'M' ,'1954-03-31', 28760.00,  600, 2301),
                ('000250', 'DANIEL',    'S', 'SMITH',      'D21', '0961', '1969-10-30', 'CLERK',    15, 'M' ,'1939-11-12', 19180.00,  400, 1534),
                ('000260', 'SYBIL',     'P', 'JOHNSON',    'D21', '8953', '1975-09-11', 'CLERK',    16, 'F' ,'1936-10-05', 17250.00,  300, 1380),
                ('000270', 'MARIA',     'L', 'PEREZ',      'D21', '9001', '1980-09-30', 'CLERK',    15, 'F' ,'1953-05-26', 27380.00,  500, 2190),
                ('000280', 'ETHEL',     'R', 'SCHNEIDER',  'E11', '8997', '1967-03-24', 'OPERATOR', 17, 'F' ,'1936-03-28', 26250.00,  500, 2100),
                ('000290', 'JOHN',      'R', 'PARKER',     'E11', '4502', '1980-05-30', 'OPERATOR', 12, 'M' ,'1946-07-09', 15340.00,  300, 1227),
                ('000300', 'PHILIP',    'X', 'SMITH',      'E11', '2095', '1972-06-19', 'OPERATOR', 14, 'M' ,'1936-10-27', 17750.00,  400, 1420),
                ('000310', 'MAUDE',     'F', 'SETRIGHT',   'E11', '3332', '1964-09-12', 'OPERATOR', 12, 'F' ,'1931-04-21', 15900.00,  300, 1272),
                ('000320', 'RAMLAL',    'V', 'MEHTA',      'E21', '9990', '1965-07-07', 'FIELDREP', 16, 'M' ,'1932-08-11', 19950.00,  400, 1596),
                ('000330', 'WING',      ' ' , 'LEE',        'E21', '2103', '1976-02-23', 'FIELDREP', 14, 'M' ,'1941-07-18', 25370.00,  500, 2030),
                ('000340', 'JASON',     'R', 'GOUNOT',     'E21', '5698', '1947-05-05', 'FIELDREP', 16, 'M' ,'1926-05-17', 23840.00,  500, 1907)
            )            
        else:			
            employee = (
                ('000010', 'CHRISTINE', 'I', 'HAAS',       'A00', '3978', '1965-01-01', 'PRES',     18, 'F', '1933-08-24', 52750.00, 1000, 4220),
                ('000020', 'MICHAEL',   'L', 'THOMPSON',   'B01', '3476', '1973-10-10', 'MANAGER',  18, 'M' ,'1948-02-02', 41250.00,  800, 3300),
                ('000030', 'SALLY',     'A', 'KWAN',       'C01', '4738', '1975-04-05', 'MANAGER',  20, 'F' ,'1941-05-11', 38250.00,  800, 3060),
                ('000050', 'JOHN',      'B', 'GEYER',      'E01', '6789', '1949-08-17', 'MANAGER',  16, 'M' ,'1925-09-15', 40175.00,  800, 3214),
                ('000060', 'IRVING',    'F', 'STERN',      'D11', '6423', '1973-09-14', 'MANAGER',  16, 'M' ,'1945-07-07', 32250.00,  500, 2580),
                ('000070', 'EVA',       'D', 'PULASKI',    'D21', '7831', '1980-09-30', 'MANAGER',  16, 'F' ,'1953-05-26', 36170.00,  700, 2893),
                ('000090', 'EILEEN',    'W', 'HENDERSON',  'E11', '5498', '1970-08-15', 'MANAGER',  16, 'F' ,'1941-05-15', 29750.00,  600, 2380),
                ('000100', 'THEODORE',  'Q', 'SPENSER',    'E21', '0972', '1980-06-19', 'MANAGER',  14, 'M' ,'1956-12-18', 26150.00,  500, 2092),
                ('000110', 'VINCENZO',  'G', 'LUCCHESSI',  'A00', '3490', '1958-05-16', 'SALESREP', 19, 'M' ,'1929-11-05', 46500.00,  900, 3720),
                ('000120', 'SEAN',      '' , 'OCONNELL',   'A00', '2167', '1963-12-05', 'CLERK',    14, 'M' ,'1942-10-18', 29250.00,  600, 2340),
                ('000130', 'DOLORES',   'M', 'QUINTANA',   'C01', '4578', '1971-07-28', 'ANALYST',  16, 'F' ,'1925-09-15', 23800.00,  500, 1904),
                ('000140', 'HEATHER',   'A', 'NICHOLLS',   'C01', '1793', '1976-12-15', 'ANALYST',  18, 'F' ,'1946-01-19', 28420.00,  600, 2274),
                ('000150', 'BRUCE',     '' , 'ADAMSON',    'D11', '4510', '1972-02-12', 'DESIGNER', 16, 'M' ,'1947-05-17', 25280.00,  500, 2022),
                ('000160', 'ELIZABETH', 'R', 'PIANKA',     'D11', '3782', '1977-10-11', 'DESIGNER', 17, 'F' ,'1955-04-12', 22250.00,  400, 1780),
                ('000170', 'MASATOSHI', 'J', 'YOSHIMURA',  'D11', '2890', '1978-09-15', 'DESIGNER', 16, 'M' ,'1951-01-05', 24680.00,  500, 1974),
                ('000180', 'MARILYN',   'S', 'SCOUTTEN',   'D11', '1682', '1973-07-07', 'DESIGNER', 17, 'F' ,'1949-02-21', 21340.00,  500, 1707),
                ('000190', 'JAMES',     'H', 'WALKER',     'D11', '2986', '1974-07-26', 'DESIGNER', 16, 'M' ,'1952-06-25', 20450.00,  400, 1636),
                ('000200', 'DAVID',     '' , 'BROWN',      'D11', '4501', '1966-03-03', 'DESIGNER', 16, 'M' ,'1941-05-29', 27740.00,  600, 2217),
                ('000210', 'WILLIAM',   'T', 'JONES',      'D11', '0942', '1979-04-11', 'DESIGNER', 17, 'M' ,'1953-02-23', 18270.00,  400, 1462),
                ('000220', 'JENNIFER',  'K', 'LUTZ',       'D11', '0672', '1968-08-29', 'DESIGNER', 18, 'F' ,'1948-03-19', 29840.00,  600, 2387),
                ('000230', 'JAMES',     'J', 'JEFFERSON',  'D21', '2094', '1966-11-21', 'CLERK',    14, 'M' ,'1935-05-30', 22180.00,  400, 1774),
                ('000240', 'SALVATORE', 'M', 'MARINO',     'D21', '3780', '1979-12-05', 'CLERK',    17, 'M' ,'1954-03-31', 28760.00,  600, 2301),
                ('000250', 'DANIEL',    'S', 'SMITH',      'D21', '0961', '1969-10-30', 'CLERK',    15, 'M' ,'1939-11-12', 19180.00,  400, 1534),
                ('000260', 'SYBIL',     'P', 'JOHNSON',    'D21', '8953', '1975-09-11', 'CLERK',    16, 'F' ,'1936-10-05', 17250.00,  300, 1380),
                ('000270', 'MARIA',     'L', 'PEREZ',      'D21', '9001', '1980-09-30', 'CLERK',    15, 'F' ,'1953-05-26', 27380.00,  500, 2190),
                ('000280', 'ETHEL',     'R', 'SCHNEIDER',  'E11', '8997', '1967-03-24', 'OPERATOR', 17, 'F' ,'1936-03-28', 26250.00,  500, 2100),
                ('000290', 'JOHN',      'R', 'PARKER',     'E11', '4502', '1980-05-30', 'OPERATOR', 12, 'M' ,'1946-07-09', 15340.00,  300, 1227),
                ('000300', 'PHILIP',    'X', 'SMITH',      'E11', '2095', '1972-06-19', 'OPERATOR', 14, 'M' ,'1936-10-27', 17750.00,  400, 1420),
                ('000310', 'MAUDE',     'F', 'SETRIGHT',   'E11', '3332', '1964-09-12', 'OPERATOR', 12, 'F' ,'1931-04-21', 15900.00,  300, 1272),
                ('000320', 'RAMLAL',    'V', 'MEHTA',      'E21', '9990', '1965-07-07', 'FIELDREP', 16, 'M' ,'1932-08-11', 19950.00,  400, 1596),
                ('000330', 'WING',      '' , 'LEE',        'E21', '2103', '1976-02-23', 'FIELDREP', 14, 'M' ,'1941-07-18', 25370.00,  500, 2030),
                ('000340', 'JASON',     'R', 'GOUNOT',     'E21', '5698', '1947-05-05', 'FIELDREP', 16, 'M' ,'1926-05-17', 23840.00,  500, 1907)
            )
        insert = 'INSERT INTO employee (empno, firstnme, midinit, lastname, workdept, phoneno, hiredate, job, edlevel, sex, birthdate, salary, bonus, comm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for emp in employee:
                result = ibm_db.execute(stmt, emp)

        # Drop the emp_photo table, in case it exists
        drop = 'DROP TABLE emp_photo'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the emp_photo table
        create = 'CREATE TABLE emp_photo (empno CHAR(6) NOT NULL, photo_format VARCHAR(10) NOT NULL, picture BLOB, PRIMARY KEY(empno, photo_format))'
        try:
            result = ibm_db.exec_immediate(conn, create)
        except:
            pass
        # Populate the emp_photo table
        emp_photo = (
            ('000130', 'jpg', 'pic1.jpg'),
            ('000130', 'png', 'spook.png'),
            ('000140', 'jpg', 'pic1.jpg'),
            ('000140', 'png', 'spook.png'),
            ('000150', 'jpg', 'pic1.jpg'),
            ('000150', 'png', 'spook.png'),
            ('000190', 'jpg', 'pic1.jpg'),
            ('000190', 'png', 'spook.png')
        )
        insert = 'INSERT INTO emp_photo (empno, photo_format, picture) VALUES (?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for photo in emp_photo:
                empno = photo[0]
                photo_format = photo[1]
                with open(os.path.dirname(os.path.abspath(__file__)) + '/' + photo[2], 'rb') as fileHandler:
                    picture = fileHandler.read()
                    ibm_db.bind_param(stmt, 1, empno, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 2, photo_format, ibm_db.SQL_PARAM_INPUT)
                    ibm_db.bind_param(stmt, 3, picture, ibm_db.SQL_PARAM_INPUT)
                    result = ibm_db.execute(stmt)

        # Drop the org table, in case it exists
        drop = 'DROP TABLE org'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the org table
        create = 'CREATE TABLE org (deptnumb SMALLINT NOT NULL, deptname VARCHAR(14), manager SMALLINT, division VARCHAR(10), location VARCHAR(13))'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the org table
        org = (
            (10, 'Head Office',    160, 'Corporate', 'New York'),
            (15, 'New England',    50,  'Eastern',   'Boston'),
            (20, 'Mid Atlantic',   10,  'Eastern',   'Washington'),
            (38, 'South Atlantic', 30,  'Eastern',   'Atlanta'),
            (42, 'Great Lakes',    100, 'Midwest',   'Chicago'),
            (51, 'Plains',         140, 'Midwest',   'Dallas'),
            (66, 'Pacific',        270, 'Western',   'San Francisco'),
            (84, 'Mountain',       290, 'Western',   'Denver')
        )
        insert = 'INSERT INTO org (deptnumb, deptname, manager, division, location) VALUES (?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for orgpart in org:
                result = ibm_db.execute(stmt, orgpart)

        # Drop the project table, in case it exists
        drop = 'DROP TABLE project'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the project table
        create = 'CREATE TABLE project (projno CHAR(6) NOT NULL, projname VARCHAR(24) NOT NULL, deptno CHAR(3) NOT NULL, respemp CHAR(6) NOT NULL, prstaff DECIMAL(5,2), prstdate DATE, prendate DATE, majproj CHAR(6))'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the project table
        project = (
            ('AD3110', 'GENERAL ADMIN SYSTEMS', 'D21', '000070',   6, '1982-01-01', '1983-02-01', 'AD3100'),
            ('AD3111', 'PAYROLL PROGRAMMING',   'D21', '000230',   2, '1982-01-01', '1983-02-01', 'AD3110'),
            ('AD3112', 'PERSONNEL PROGRAMMING', 'D21', '000250',   1, '1982-01-01', '1983-02-01', 'AD3110'),
            ('AD3113', 'ACCOUNT PROGRAMMING',   'D21', '000270',   2, '1982-01-01', '1983-02-01', 'AD3110'),
            ('IF1000', 'QUERY SERVICES',        'C01', '000030',   2, '1982-01-01', '1983-02-01', None),
            ('IF2000', 'USER EDUCATION',        'C01', '000030',   1, '1982-01-01', '1983-02-01', None),
            ('MA2100', 'WELD LINE AUTOMATION',  'D01', '000010',  12, '1982-01-01', '1983-02-01', None),
            ('MA2110', 'W L PROGRAMMING',       'D11', '000060',   9, '1982-01-01', '1983-02-01', 'MA2100'),
            ('MA2111', 'W L PROGRAM DESIGN',    'D11', '000220',   2, '1982-01-01', '1982-12-01', 'MA2110'),
            ('MA2112', 'W L ROBOT DESIGN',      'D11', '000150',   3, '1982-01-01', '1982-12-01', 'MA2110'),
            ('MA2113', 'W L PROD CONT PROGS',   'D11', '000160',   3, '1982-02-15', '1982-12-01', 'MA2110'),
            ('OP1000', 'OPERATION SUPPORT',     'E01', '000050',   6, '1982-01-01', '1983-02-01', None),
            ('OP1010', 'OPERATION',             'E11', '000090',   5, '1982-01-01', '1983-02-01', 'OP1000'),
            ('OP2000', 'GEN SYSTEMS SERVICES',  'E01', '000050',   5, '1982-01-01', '1983-02-01', None),
            ('OP2010', 'SYSTEMS SUPPORT',       'E21', '000100',   4, '1982-01-01', '1983-02-01', 'OP2000'),
            ('OP2011', 'SCP SYSTEMS SUPPORT',   'E21', '000320',   1, '1982-01-01', '1983-02-01', 'OP2010'),
            ('OP2012', 'APPLICATIONS SUPPORT',  'E21', '000330',   1, '1982-01-01', '1983-02-01', 'OP2010'),
            ('OP2013', 'DB/DC SUPPORT',         'E21', '000340',   1, '1982-01-01', '1983-02-01', 'OP2010'),
            ('PL2100', 'WELD LINE PLANNING',    'B01', '000020',   1, '1982-01-01', '1982-09-15', 'MA2100')
        )

        if ('zos' in sys.platform):
            project = (('AD3100', 'ADMIN SERVICES',        'D01', '000010', 6.5, '1982-01-01', '1983-02-01', None),) + project
        else:
            project = (('AD3100', 'ADMIN SERVICES',        'D01', '000010', 6.5, '1982-01-01', '1983-02-01', ''),) + project

        insert = 'INSERT INTO project (projno, projname, deptno, respemp, prstaff, prstdate, prendate, majproj) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for proj in project:
                result = ibm_db.execute(stmt, proj)

        # Drop the sales table, in case it exists
        drop = 'DROP TABLE sales'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the sales table
        create = 'CREATE TABLE sales (sales_date DATE, sales_person VARCHAR(15), region VARCHAR(15), sales INT)'
        result = ibm_db.exec_immediate(conn, create)
        # Populate the sales table
        sales = (
            ('1995-12-31', 'LUCCHESSI',   'Ontario-South',  1),
            ('1995-12-31', 'LEE',         'Ontario-South',  3),
            ('1995-12-31', 'LEE',         'Quebec',         1),
            ('1995-12-31', 'LEE',         'Manitoba',       2),
            ('1995-12-31', 'GOUNOT',      'Quebec',         1),
            ('1996-03-29', 'LUCCHESSI',   'Ontario-South',  3),
            ('1996-03-29', 'LUCCHESSI',   'Quebec',         1),
            ('1996-03-29', 'LEE',         'Ontario-South',  2),
            ('1996-03-29', 'LEE',         'Ontario-North',  2),
            ('1996-03-29', 'LEE',         'Quebec',         3),
            ('1996-03-29', 'LEE',         'Manitoba',       5),
            ('1996-03-29', 'GOUNOT',      'Ontario-South',  3),
            ('1996-03-29', 'GOUNOT',      'Quebec',         1),
            ('1996-03-29', 'GOUNOT',      'Manitoba',       7),
            ('1996-03-30', 'LUCCHESSI',   'Ontario-South',  1),
            ('1996-03-30', 'LUCCHESSI',   'Quebec',         2),
            ('1996-03-30', 'LUCCHESSI',   'Manitoba',       1),
            ('1996-03-30', 'LEE',         'Ontario-South',  7),
            ('1996-03-30', 'LEE',         'Ontario-North',  3),
            ('1996-03-30', 'LEE',         'Quebec',         7),
            ('1996-03-30', 'LEE',         'Manitoba',       4),
            ('1996-03-30', 'GOUNOT',      'Ontario-South',  2),
            ('1996-03-30', 'GOUNOT',      'Quebec',        18),
            ('1996-03-30', 'GOUNOT',      'Manitoba',       1),
            ('1996-03-31', 'LUCCHESSI',   'Manitoba',       1),
            ('1996-03-31', 'LEE',         'Ontario-South', 14),
            ('1996-03-31', 'LEE',         'Ontario-North',  3),
            ('1996-03-31', 'LEE',         'Quebec',         7),
            ('1996-03-31', 'LEE',         'Manitoba',       3),
            ('1996-03-31', 'GOUNOT',      'Ontario-South',  2),
            ('1996-03-31', 'GOUNOT',      'Quebec',         1),
            ('1996-04-01', 'LUCCHESSI',   'Ontario-South',  3),
            ('1996-04-01', 'LUCCHESSI',   'Manitoba',       1),
            ('1996-04-01', 'LEE',         'Ontario-South',  8),
            ('1996-04-01', 'LEE',         'Ontario-North', None),
            ('1996-04-01', 'LEE',         'Quebec',         8),
            ('1996-04-01', 'LEE',         'Manitoba',       9),
            ('1996-04-01', 'GOUNOT',      'Ontario-South',  3),
            ('1996-04-01', 'GOUNOT',      'Ontario-North',  1),
            ('1996-04-01', 'GOUNOT',      'Quebec',         3),
            ('1996-04-01', 'GOUNOT',      'Manitoba',       7)
        )
        insert = 'INSERT INTO sales (sales_date, sales_person, region, sales) VALUES (?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for sale in sales:
                result = ibm_db.execute(stmt, sale)

        #Creating the procedure out_blob
        drop = "DROP PROCEDURE out_blob"
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass

        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE out_blob(OUT P1 BLOB(100))
                LET P1 = BLOB('1234567801234567890');
            END PROCEDURE;""")
        else:
            result = ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE out_blob(OUT P1 BLOB(100))
            LANGUAGE SQL
            DYNAMIC RESULT SETS 0 
            BEGIN
                SET P1 = BLOB('1234567801234567890');
            END""")
        result = None

        # Drop the stored procedure, in case it exists
        drop = 'DROP PROCEDURE match_animal'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass

        # Create the stored procedure
        if (server.DBMS_NAME[0:3] == 'IDS'):
            result = ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE match_animal(first_name VARCHAR(128), INOUT second_name VARCHAR(128), OUT animal_weight DOUBLE PRECISION )
                DEFINE match_name INT;
                LET match_name = 0;

                FOREACH c1 FOR
                    SELECT COUNT(*) INTO match_name FROM animals
                                            WHERE name IN (second_name)
                    IF (match_name > 0)
                        THEN LET second_name = 'TRUE';
                    END IF;
                END FOREACH;

                FOREACH c2 FOR
                    SELECT SUM(weight) INTO animal_weight FROM animals WHERE name in (first_name, second_name)
                END FOREACH;
            END PROCEDURE;""")
        else:
            result = ibm_db.exec_immediate(conn, """
            CREATE PROCEDURE match_animal(IN first_name VARCHAR(128), INOUT second_name VARCHAR(128), OUT animal_weight DOUBLE)
            DYNAMIC RESULT SETS 1
            LANGUAGE SQL
            BEGIN
                DECLARE match_name INT DEFAULT 0;
                DECLARE c1 CURSOR FOR
                    SELECT COUNT(*) FROM animals
                    WHERE name IN (second_name);

                DECLARE c2 CURSOR FOR
                    SELECT SUM(weight) FROM animals
                    WHERE name in (first_name, second_name);

                DECLARE c3 CURSOR WITH RETURN FOR
                    SELECT name, breed, weight FROM animals
                    WHERE name BETWEEN first_name AND second_name
                    ORDER BY name;

                OPEN c1;
                FETCH c1 INTO match_name;
                IF (match_name > 0)
                    THEN SET second_name = 'TRUE';
                END IF;
                CLOSE c1;

                OPEN c2;
                FETCH c2 INTO animal_weight;
                CLOSE c2;

                OPEN c3;
            END""")
        result = None

        # Drop the staff table, in case it exists
        drop = 'DROP TABLE staff'
        try:
            result = ibm_db.exec_immediate(conn, drop)
        except:
            pass
        # Create the staff table
        create = 'CREATE TABLE staff (id SMALLINT NOT NULL, name VARCHAR(9), dept SMALLINT, job CHAR(5), years SMALLINT, salary DECIMAL(7,2), comm DECIMAL(7,2))';
        result = ibm_db.exec_immediate(conn, create)
        # Populate the staff table
        staff = (
            (10, 'Sanders',    20, 'Mgr',   7,    18357.50, None),
            (20, 'Pernal',     20, 'Sales', 8,    18171.25, 612.45),
            (30, 'Marenghi',   38, 'Mgr',   5,    17506.75, None),
            (40, 'OBrien',     38, 'Sales', 6,    18006.00, 846.55),
            (50, 'Hanes',      15, 'Mgr',   10,   20659.80, None),
            (60, 'Quigley',    38, 'Sales', None,  16808.30, 650.25),
            (70, 'Rothman',    15, 'Sales', 7,    16502.83, 1152.00),
            (80, 'James',      20, 'Clerk', None,  13504.60, 128.20),
            (90, 'Koonitz',    42, 'Sales', 6,    18001.75, 1386.70),
            (100, 'Plotz',     42, 'Mgr'  , 7,    18352.80, None),
            (110, 'Ngan',      15, 'Clerk', 5,    12508.20, 206.60),
            (120, 'Naughton',  38, 'Clerk', None,  12954.75, 180.00),
            (130, 'Yamaguchi', 42, 'Clerk', 6,    10505.90, 75.60),
            (140, 'Fraye',     51, 'Mgr'  , 6,    21150.00, None),
            (150, 'Williams',  51, 'Sales', 6,    19456.50, 637.65),
            (160, 'Molinare',  10, 'Mgr'  , 7,    22959.20, None),
            (170, 'Kermisch',  15, 'Clerk', 4,    12258.50, 110.10),
            (180, 'Abrahams',  38, 'Clerk', 3,    12009.75, 236.50),
            (190, 'Sneider',   20, 'Clerk', 8,    14252.75, 126.50),
            (200, 'Scoutten',  42, 'Clerk', None,  11508.60, 84.20),
            (210, 'Lu',        10, 'Mgr'  , 10,   20010.00, None),
            (220, 'Smith',     51, 'Sales', 7,    17654.50, 992.80),
            (230, 'Lundquist', 51, 'Clerk', 3,    13369.80, 189.65),
            (240, 'Daniels',   10, 'Mgr'  , 5,    19260.25, None),
            (250, 'Wheeler',   51, 'Clerk', 6,    14460.00, 513.30),
            (260, 'Jones',     10, 'Mgr'  , 12,   21234.00, None),
            (270, 'Lea',       66, 'Mgr'  , 9,    18555.50, None),
            (280, 'Wilson',    66, 'Sales', 9,    18674.50, 811.50),
            (290, 'Quill',     84, 'Mgr'  , 10,   19818.00, None),
            (300, 'Davis',     84, 'Sales', 5,    15454.50, 806.10),
            (310, 'Graham',    66, 'Sales', 13,   21000.00, 200.30),
            (320, 'Gonzales',  66, 'Sales', 4,    16858.20, 844.00),
            (330, 'Burke',     66, 'Clerk', 1,    10988.00, 55.50),
            (340, 'Edwards',   84, 'Sales', 7,    17844.00, 1285.00),
            (350, 'Gafney',    84, 'Clerk', 5,    13030.50, 188.00)
        )
        insert = 'INSERT INTO staff (id, name, dept, job, years, salary, comm) VALUES (?, ?, ?, ?, ?, ?, ?)'
        stmt = ibm_db.prepare(conn, insert)
        if stmt:
            for emp in staff:
                result = ibm_db.execute(stmt, emp)

        try:
            result = ibm_db.exec_immediate(conn, 'DROP TABLE t_string')
        except:
            pass
        result = ibm_db.exec_immediate(conn, 'CREATE TABLE t_string(a INTEGER, b DOUBLE PRECISION, c VARCHAR(100))')

        print ("Preperation complete")

#__END__
#__LUW_EXPECTED__
#Preperation complete
#__ZOS_EXPECTED__
#Preperation complete
#__SYSTEMI_EXPECTED__
#Preperation complete
#__IDS_EXPECTED__
#Preperation complete
