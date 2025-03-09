2025-03-09, Version 3.2.6
=========================

 * fea: add support for env var CLIDRIVER_VERSION for autodownload (Bimal Jha)

 * update README file for SQL0805N error, #996 (Bimal Jha)

 * Update Installation Instructions for Python ibm_db on z/OS (#995) (bchoudhary6415)

 * Update .gitattributes file to fix unicode decode error on z/OS (bchoudhary6415)

 * Fix for memory leak issue (#991) (bchoudhary6415)

 * fix formatting and indentation issues (Bimal Jha)

 * Fix Polaris code scan issues (#990) (bchoudhary6415)

 * add support for column_name in ibm_db_column_privileges & issue #988 (Bimal Jha)

 * fix high severity code scan issues (Bimal Jha)

 * Add polaris.yml file for code scan (Bimal Jha)

 * Return error from fetchall() if any fetch get error (#987) (bchoudhary6415)

 * Polaris scan fix (#985) (bchoudhary6415)

2024-12-30, Version 3.2.5
=========================

 * update workflow file to fix macarm64 install issue (Bimal Jha)

 * Fix for issue#981 Django showing all migrations as unaplied (#982) (bchoudhary6415)

2024-12-11, Version 3.2.4
=========================

 * doc update for macos arm64 support (Bimal Jha)

 * update ibm_db_dbi logging and fix LogMag error issue #978 (bchoudhary6415)

 * Support python-ibm_db driver for MACOS ARM64 platform (#972) (Earammak)

 * Support Python 3.13 and add fetch APIs (fetchone, fetchmany, fetchall) (#971) (bchoudhary6415)

 * Added check to pass compilation issue for zos (#968) (Earammak)

 * New API to return SQLCODE (#966) (Earammak)

 * Added SQL_ATTR_CALL_RETURN attribute to return from stored procdure (#965) (Earammak)

 * Support for logging in ibm_db module (#964) (bchoudhary6415)

 * Fix Buffer Overflow Warning in sprintf and remove unused variables (#961) (Earammak)

 * Context manager support with connection object (#947) (Earammak)

 * doc: update readme file #955 (Bimal Jha)

 * Support for logging in ibm_db_dbi module (#954) (bchoudhary6415)

 * Fix for libdb2 for createdb and dropdb (#953) (Earammak)

 * change Beta relese to Production (Bimal Jha)

 * Adding .gitattributes file (#940) (bchoudhary6415)

 * Update bld_wheels_and_upload.yml (Earammak)

 * doc update for license error, issue #933 (Bimal Jha)

 * Added isolation level attribute support (#932) (Earammak)

 * doc update to addess issues #907, #926 (Bimal Jha)

 * Update INSTALL.md (#921) (Ankit Kumar)


2024-03-13, Version 3.2.3
=========================

 * Downgrade upload-artifact on 64 bit Windows (#919) (Bradley Reynolds)

 * Upgrade cibuildwheel on Linux & Mac OS job (#920) (Bradley Reynolds)


2024-03-02, Version 3.2.2
=========================

 * Support for python3.12 (#913) (bchoudhary6415)

 * fixed Typo on clidriver (#905) (Manoj K Jadwani)

 * doc: update readme file (Bimal Jha)


2023-11-22, Version 3.2.1
=========================

 * Updated readme.md with Note regarding ibm_db installation. (#896) (bchoudhary6415)

 * Enhance ibm_db driver to read Db2 credential from Env var for testing (#894) (bchoudhary6415)

 * Updated INSTALL.md (#889) (Earammak)

 * Fix typo in `SQL_ATTR_TXN_ISOLATION` (#884) (Nikita Sobolev)


2023-08-25, Version 3.2.0
=========================

 * Update setup.py to Honor GCC environment variables

 * Support for Python Wheels in ibm_db (Earammak)

 * Fix for exception thrown by read_sql_query() from pandas while invoking a stored-procedure

 * move files from IBM_DB/ibm_db to root directory

 * Support for Null value for an array (Earammak)
 
 * ibm_db_execute: arrays of PYTHON_DECIMAL fails for FLOAT and DOUBLE datatypes

 * Fix: uninitialized variable in _python_ibm_db_execute_helper1

 * Optimize _checkGcc in setup.py (pschoen-itsc)

 * Support for additional connect options - connection attributes

 * Fix: ibm_db.execute_many returns bind error with numpy.int64 values #828

2022-11-24, Version 3.1.4
=========================

 * Fix for issues #796, #764 and added python 3.11 support (#809) (Earammak)

 * Fix for issue #795 (#798) (Earammak)

 * Fix for issue #792 (#794) (Earammak)

 * Fix for pyhon issue #779 and #778 (#788) (Earammak)

 * Add more explicit mention for Apple Silicon users (#780) (Jonathan Herdt)

 * Added Py_BEGIN_ALLOW_THREADS and Py_END_ALLOW_THREADS for the API's (#781) (Earammak)

2022-08-03, Version 3.1.3
=========================

 * Commit for version change 3.1.3 (#776) (Earammak)

 * fix for install UnicodeDecodeError #772 (Bimal Jha)

 * fix install issue #761, #765, #770 (Bimal Jha)

 * Fix for path update and installation failure issue when IBM site down (#771) (Earammak)


2022-06-13, Version 3.1.2
=========================

 * release changes for 3.1.2 (amukherjee)

 * setup.py upgrade : better error handling while installation (Arnab Mukherjee)

 * Code fix for issue #413 (Arnab Mukherjee)

 * Code fix for issue #468 (Arnab Mukherjee)

 * Code change for issue #720 (Arnab Mukherjee)

 * documentation updates (Arnab Mukherjee)

 * add custom clidriver bin path to ibm_db.py file (Alexandre Duverger)

 * doc: update for issue #733 (Bimal Jha)

 * fix: for issue #708 (Bimal Jha)

 * doc: update about MacOS M1 Chip system (Bimal Jha)

 * Add issue template (Bimal Jha)

 * Add support for installing clidriver using another URL or artifactory URL. (#727) (MarcinMaciaszek)

 * updating the CHANGES.md file (Arnab Mukherjee)


2022-01-11, Version 3.1.1
=========================

 * Post release correction (Arnab Mukherjee)

 * fixing the NULL initialization (Arnab Mukherjee)

 * Changes for build fix with visual studio 2010 for python 3.4 and 2.7 (Arnab Mukherjee)

 * fix for #427 adding readme for pypi site (Arnab Mukherjee)

 * fix for #671 and restore python2 support (Arnab Mukherjee)

 * Changes in Documentation (Arnab Mukherjee)

 * Modification in readme--1 (Arnab Mukherjee)

 * test case changes for ZOS (Arnab Mukherjee)

 * correction in expectation (Arnab Mukherjee)

 * correction in test case 2 (Arnab Mukherjee)

 * correction in test case (Arnab Mukherjee)

 * adding test cases as part of the PR #418 (Arnab Mukherjee)

 * Changes from PR #689 and #407 (Arnab Mukherjee)

 * adding test case for unicode (Arnab Mukherjee)

 * Fixing the issue for fetch assoc (Arnab Mukherjee)

 * Adding the logic for fixing unicode values in windows (Arnab Mukherjee)

 * Fix for Unicode character (Arnab Mukherjee)

 * Test case modification (Arnab Mukherjee)

 * Support for arrays in python ibm_db driver (#698) (Praveen Narayanappa)


2021-10-21, Version 3.1.0
=========================

 * changes for new release 3.1.0 (Arnab Mukherjee)

 * Remove dependency on 2to3 and unpin Setuptools. (Jason R. Coombs)

 * Restore Python 2 compatibility. (Jason R. Coombs)

 * Apply lib2to3 to the python code (Jason R. Coombs)

 * fix for #641 (Arnab Mukherjee)

 * Pin to Setuptools < 58 to support builds until use_2to3 can be removed. (Jason R. Coombs)

 * update readme.md for known installation issues (Arnab Mukherjee)

 * updating: NOTES.md for more api (Arnab Mukherjee)

 * Update: documentation update in NOTES.md (Arnab Mukherjee)


2021-04-16, Version 3.0.4
=========================

 * Update README with new release version (Bimal Kumar Jha)

 * typo correction in README.md (Bimal Kumar Jha)

 * testcase change for ZOS platform and zos server (Arnab Mukherjee)

 * changing the release tag (Arnab Mukherjee)

 * Add comments (kotofos)

 * Fix error message formatting on python3 (kotofos)

 * Dev release304 (#621) (arnab mukherjee)

 * Update README.md (#617) (Alexander Manley)

 * Code fix in SQL_BOOLEAN (Arnab Mukherjee)

 * update install.md file with the latest information on ZOS platform documentation (Arnab Mukherjee)

 * Fix for #612 (Arnab Mukherjee)

 * Boolean support for django issue (Arnab Mukherjee)

 * Adding changes to handle env variable DB2_IBC and DB2_MACS in case user wants to define their own dataset names (Arnab Mukherjee)

 * Support ODBC keyword CURRENTSCHEMA (#581) (Ke Zhu)

 * Update Install.md (#605) (kparihar7)

 * Update setup.py file (#606) (kparihar7)

 * Get execute_many test running clean in CI (#524) (davidmmooney)

 * Update README.md (Bimal Kumar Jha)

 * Update file name in setup.py (Bimal Kumar Jha)

 * Update MANIFEST.in (arnab mukherjee)

 * Update notifications and add python 3.9 test (Bimal Kumar Jha)

 * Change in install.md as per input from IBM as the ++APAR is now available as PTF. (#597) (Binit Kumar)

 * fix: correct changes file (Bimal Jha)

 * upd: CHANGES (Bimal Jha)

 * deleting Install_z_ibm_db file (amukherjee)

 * Changes for Z/os support along with python 3.9 (amukherjee)

 * Readme and install file releated changes (Arnab Mukherjee)

 * Z odbc support (#579) (Binit Kumar)

 * Update README.md (Saba Kauser)

 * Update README.md (#544) (Saba Kauser)

 * add v11.1 support for win32 and mac (Saba Kauser)

 * add v11.1 support for win32 and Mac (Saba Kauser)

 * Add dependent libraries for docker linux in README (Saba Kauser)

 * new test canse for bool (#527) (Saba Kauser)

 * Update CHANGES (Saba Kauser)


2020-06-17, Version 3.0.2
=========================

 * Update README.md (Saba Kauser)

 * Update CHANGES (Saba Kauser)

 * add add_dll_directory for python 3.8 (#523) (Saba Kauser)

 * Use v2.7-compatible syntax instead of super(). (#522) (davidmmooney)

 * Bool (#519) (Saba Kauser)

 * Update image files in ibm_db_tests/ (#514) (davidmmooney)

 * Fix Segfault in case of NULL value returned by getSQLWCharAsPyUnicodeObject (#479) (Théophile Chevalier)

 * Release (#509) (Saba Kauser)

 * honor IBM_DB_HOME setting while running install_name_tool (#508) (Saba Kauser)

 * Support bdist for MacOS (#466) (killuazhu)

 * docs: Fix Travis status badge in README (#493) (Kevin Adler)

 * ci: Fix Docker setup for Travis CI (#492) (Kevin Adler)

 * change copyright (Saba Kauser)

 * added new testcase #489 (Saba Kauser)

 * addresses #489 (#490) (Saba Kauser)

 * Fix Python 3 syntax errors in ibm_db_dbi.py (#448) (Christian Clauss)

 * Release GIL during SQLEndTran (#482) (Zach Hoggard)

 * Avoid binary install in MacOS pip install (#463) (killuazhu)

 * Context Management (#437) (Andrew Sheridan)

 * stmt_errormsg() to handle non-ascii and hours mod 24 for Db2 LUW (#430) (Saba Kauser)

 * 421 and 429 (Saba Kauser)

 * ibm_db on Docker linux  (#425) (Saba Kauser)

 * fix for Blob data not inserted from ibm_db_sa orm (#408) (abhi7436)

 * Add Trove classifiers for supported Python versions. (#395) (Jannis Leidel)

 * Simplify by defining "long" in Python 3 (#397) (cclauss)

 * Doc changes (#393) (Saba Kauser)

 * Fix issue #388 and update README (#391) (Saba Kauser)


2019-03-14, Version 3.0.1
=========================

 * Release 3.0.1 (#385) (Saba Kauser)

 * New test cases and copying README, LICENSE and CHANGES to ibm_db install location (#384) (Saba Kauser)

 * Fix whitespace issues (#344) (Kevin Adler)

 * Ensure generated tarballs include IBM certificates (#382) (Kevin Adler)

 * Remove ibm_db_django directory (#375) (Kevin Adler)

 * Run install_name_tool post installation on mac_os (#377) (Saba Kauser)

 * Remove unused tests_1 directory (#376) (Kevin Adler)

 * Fix unpredictable returning bytes instead string for multiple result sets (#374) (Kevin Adler)

 * Add certificates needed to verify downloads from IBM FTP site (#367) (Kevin Adler)

 * Update ibm_db.c (#364) (Saba Kauser)

 * Update ibm_db.h (Saba Kauser)

 * "Merge bug_fixes" (#360) (Saba Kauser)

 * fix UnicodeDecodeError with ibm_db.get_option (#357) (Saba Kauser)

 * Update README.md (Saba Kauser)

 * fixed typo in error message (#347) (Henrik Loeser)

 * Add Appveyor support for Windows CI (#346) (Kevin Adler)

 * add email address (Saba Kauser)

 * Update .travis.yml (Saba Kauser)

 * Changing email to true for travis (Bimal Kumar Jha)

 * Update CHANGES (Saba Kauser)

 * Add support for Travis CI (#343) (Kevin Adler)

 * MANIFEST.in should reference renamed README.md not README (#342) (Kevin Adler)


2018-08-08, Version 2.0.9
=========================

 * Update README.md (Saba Kauser)

 * Update README.md (#331) (Saba Kauser)

 * Fix bug in setup.py where wrong cli file could be downloaded (#325) (Kevin McKenzie)

 * Fix the broken links (#324) (Kevin McKenzie)

 * add correct length to TIMESTAMP bindin (SabaKauser)

 * process unique persistent connections (#278) (Robert Redburn)

 * added support for ppc64le (#311) (vibkulkarni)

 * Remove reused = 1 outside connection check (#316) (David Poggi)

 * Support for DBCLOB (#307) (hemlatabhatt)

 * Update setup.py (SabaKauser)

 * new release 2.0.8 for ibm_db (SabaKauser)

 * Update README.md (SabaKauser)

 * New contribution guidelines for python ibm_db (#275) (SabaKauser)


2017-09-07, Version 2.0.8
=========================

 * Python 2.8  changes merge request (#274) (hemlatabhatt)

 * Python3 Support for ibm-db-django readme file Updated (#258) (hemlatabhatt)

 * Py3 Support for ibm_db_django (#257) (hemlatabhatt)

 * schema editor changes (hemlatabhatt)

 * changes in schemaeditor (hemlatabhatt)

 * change in schemaeditor file (hemlatabhatt)

 * change in schemaeditor (hemlatabhatt)

 * rel.through fixes in 1.0.0.0 release (hemlatabhatt)

 * fixes in 1.1.0.0 release (hemlatabhatt)

 * Updated release number to 1.1.0.0 (hemlatabhatt)

 * changed a error file (hemlatabhatt)

 * Django 1.1.0 release (hemlatabhatt)

 * use correct metadata views for z/OS for inspectdb (SabaKauser)

 * Update ibm_db_dbi.py (SabaKauser)

 * added new test case test_spinout_timestamp.py (SabaKauser)

 * added missing variables for use_wchar (SabaKauser)

 * correct handling of TIMESTAMP OUTPUT paramters of SP call in ibm_db.callproc API (SabaKauser)

 * Update Contributions.md (SabaKauser)

 * Adding the CLA documents that need to be signed for contributions (SabaKauser)

 * Adding the CLA documents that need to be signed for making contributions to the repository (SabaKauser)

 * CLA Docs (SabaKauser)

 * Update README.md (SabaKauser)

 * Update ibm_db.c (SabaKauser)

 * add zlinux support (SabaKauser)

 * Performance Improvements (SabaKauser)

 * Update test_264_InsertRetrieveBIGINTTypeColumn.py (SabaKauser)

 * Update CHANGES for ibm_db_django 1.0.9 (Kevin Adler)

 * Update pybase.py (SabaKauser)

 * Update base.py (SabaKauser)

 * Fix typo in caching bound parameters test (Kevin Adler)

 * Add test for caching bound parameters (Kevin Adler)

 * inc/dec bound Python objects and ensure cache is cleared properly (Kevin Adler)

 * Update schemaEditor.py (SabaKauser)

 * ATTACH keyword is not supported. (IBMAmar)

 * ATTACH property is not supported for non_luw. (IBMAmar)

 * Update test_warn.py (SabaKauser)

 * Update setup.py (SabaKauser)


2016-03-23, Version 2.0.7
=========================

 * Update ibm_db.c (SabaKauser)

 * Update CHANGES (SabaKauser)

 * Update README.md (SabaKauser)

 * Update setup.py (IBMAmar)

 * Update __init__.py (jospaul1)

 * Update README.md (jospaul1)

 * IBM_DB/ibm_db/tests/test_warn.py (hemlatabhatt)

 * IBM_DB/ibm_db/ibm_db.c (hemlatabhatt)

 * Version check (jospaul1)

 * In Django 1.8 convert_binaryfield_value method expect 5 arguments.Added Version check. (jospaul1)

 * added condition djangoVersion[0:2] >= ( 1, 8 ) (jospaul1)

 * if getattr(self.connection.connection, dbms_name) != 'DB2': edited .dbms_name may be DB2/NT ,to include this scenario ,the above line is changed to if 'DB2' not in getattr(self.connection.connection, dbms_name): (jospaul1)

 * Deprecated methods are replaced (jospaul1)

 * Added a condition for 1.8 check (jospaul1)

 * impleented unimplemented method format_for_duration_arithmetic (jospaul1)

 * This change is done to support changed method signature in DJango 1.8 date_interval_sql signature got changed . Also if we are substracting hours ,days etc minus sign should be applied to all values . (jospaul1)

 * Update README.md (ibmdb)

 * 'Latest2.6changes28oct' (hemlatabhatt)

 * changes2.6updated (hemlatabhatt)

 * from django.db.backends.util renamed (jospaul1)

 * from django.db.backends.util  renamed (jospaul1)

 * value='blob( %s'  %value + ')' to handle hex data as blob (jospaul1)

 * convert_empty_values commented (jospaul1)

 * Default value of '' is not allowed in DB2 ,changed to EMPTY_BLOB() (jospaul1)

 * Added self.data_type_check_constraints=self.creation.data_type_check_constraints (jospaul1)

 * New data type added 'UUIDField':                 'VARCHAR(255)', (jospaul1)

 * Revert "added UUIDField':                    'VARCHAR(255)'," (jospaul1)

 * added UUIDField':                    'VARCHAR(255)', (jospaul1)

 * removed tests (jospaul1)

 * initialized data_types (jospaul1)

 * in class BigD() set max_digit to 31 and decimal_places to 28 (jospaul1)

 * get_table_list method changed (jospaul1)

 * Added keepdb=False and serialize=False to suit the change in Django latest (jospaul1)

 * deleted (jospaul1)

 * Updated as per log file (jospaul1)

 * Signed-off-by: jospaul1 <jospaul1@in.ibm.com> (jospaul1)

 * Updated with change log (jospaul1)


2015-10-21, Version 2.0.6
=========================

 * 'UpdatedChangesFor2.6' (HEMLATA)

 * 'Updatedchanges' (HEMLATA)

 * 'TestingChanges' (HEMLATA)

 * Update Contributions.md (SabaKauser)

 * Create Contributions.md (SabaKauser)

 * Update README.md (SabaKauser)

 * Update README.md (jospaul1)

 * Update README (jospaul1)

 * Update and rename README to README.md (SabaKauser)

 * deleting ibm_db_sa directory form ibm_db (anandakshay44)

 * header to ## from == (mariobriggs)

 * Update README (mariobriggs)

 * main Reade from https://code.google.com/p/ibm-db/ (mariobriggs)

 * user facing ibm_db_sa doc from https://code.google.com/p/ibm-db/wiki/README (mariobriggs)

 * user face doc from https://code.google.com/p/ibm-db/wiki/ibm_db_django_README (mariobriggs)

 * Updated read me from https://code.google.com/p/ibm-db/wiki/ibm_db_README (mariobriggs)

 * Django 1.8 compatibility fixes (webuser)

 * Django 1.8 support (mizi)

 * Rename config.py to config.py.sample (Kevin Adler)

 * Update .gitignore (Kevin Adler)

 * Add .gitignore (Kevin Adler)

 * issue:167, ibm_db should return relevant error message in case of closed connection. (Rahul Priyadarshi)

 * ibm_db-2.0.5.1 Release (Rahul Priyadarshi)


2015-01-01, Version 2.0.5.1
===========================

 * ibm_db-2.0.5.1 Release (Rahul Priyadarshi)

 * ibm_db_django-1.0.7 release (Rahul Priyadarshi)

 * persistent connection usability check (Rahul Priyadarshi)

 * ibm_db_django-1.0.6 release (Rahul Priyadarshi)


2014-02-05, Version 2.0.5
=========================

 * ibm_db-2.0.5 release (Rahul Priyadarshi)

 * LOB performance fix memory leak (Rahul Priyadarshi)

 * LOB performance issue (Rahul Priyadarshi)


2013-09-25, Version 2.0.4.1
===========================

 * ibm_db-2.0.4.1 release (Rahul Priyadarshi)

 * Fix ISO8601 datetime with 'T' delimiter for unicode datetime (Rahul Priyadarshi)


2013-09-11, Version 2.0.4
=========================

 * ibm_db-2.0.4 release (Rahul Priyadarshi)

 * Fix for ISO8601 datetime with 'T' delimiter (Rahul Priyadarshi)


2013-06-17, Version 2.0.3
=========================

 * ibm_db-2.0.3 release (Rahul Priyadarshi)

 * ibm_db_django-1.0.5 release (Rahul Priyadarshi)


2013-03-04, Version 2.0.2
=========================

 * ibm_db-2.0.2 release (Rahul Priyadarshi)

 * memory leak in LONGVARCHAR (Rahul Priyadarshi)


2013-02-05, Version 2.0.1
=========================

 * ibm_ibm-2.0.1 release (Rahul Priyadarshi)


2012-09-21, Version 2.0.0
=========================

 * ibm_db-2.0.0 release (rahul.priyadarshi@in.ibm.com)


2012-05-24, Version 1.0.6
=========================

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@160 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@159 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@158 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@135 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2011-09-06, Version 1.0.5
=========================

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@134 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2011-05-17, Version 1.0.4
=========================

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@121 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@120 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@114 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2010-08-06, Version 1.0.3
=========================

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@113 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@108 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@107 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2010-04-29, Version 1.0.2
=========================

 * for ibm_db-1.0.2 release (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@102 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@99 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@98 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@97 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2010-03-26, Version 1.0.1
=========================

 * git-svn-id: https://ibm-db.googlecode.com/svn/trunk@96 1b047d87-d943-0410-8e89-5b5f2422cd04 (rahul.priyadarshi@in.ibm.com)


2009-10-27, Version 1.0
=======================

 * First release!
