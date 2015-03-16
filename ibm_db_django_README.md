# Getting started with IBM DB Django adapter #

**IBM DB2 support for the Django application Framework.**

ibm\_db\_django enables access to IBM DB2 from Django applications
http://www.djangoproject.com/

The adapter has been developed and is supported by IBM.

## Prerequisites for Django on Python ##

  * Python 2.5.
  * Django Framework 1.0.x or above.
  * IBM\_DB driver and IBM\_DB\_DBI wrapper 1.0 or higher

We are assuming that you have IBM DB2 installed. If you need to connect from Django to a DB2 server on the same local machine, just proceed to the Install steps below. If you need to connect from Django to a DB2 server on different machine, then you will need to at minimum install the [IBM Data Server Driver Package](https://www-304.ibm.com/support/docview.wss?uid=swg27016878) on the machine where you install Django.

## Prerequisites for Django on Jython ##

  * Jython-2.5
  * Django Framework 1.0.x or 1.1.x
  * IBM DB2 JDBC Driver (db2jcc.jar) on CLASSPATH


## Installation ##

### 1. Install Django ###

Install Django as per instructions from the Django [website](http://docs.djangoproject.com/en/dev/topics/install/#installing-an-official-release).

  * For 1.0.2, you need to apply a patch in django in-order to remove Non-standard SQL generation issue.
  * The patch is located at http://code.djangoproject.com/ticket/9862.
  * You can extract creation.py file from http://code.djangoproject.com/changeset/9703?format=zip&new=9703 and paste it to /django/db/backends/
  * For versions greater than 1.0.2 no patch is required.

### 2. Install DB2 Django adapter (ibm\_db\_django) ###

**Download latest release of ibm\_db\_django from official release**

  * http://code.google.com/p/ibm-db/downloads/list
  * http://pypi.python.org/pypi/ibm_db_django/

> To install DB2 Django adapter on Linux
> > $ easy\_install ibm\_db\_django

> To install DB2 Django adapter on Windows
> > c:\> easy\_install ibm\_db\_django

## Tested Operating Systems ##

  * Ubuntu Linux 7.04 64 bit
  * Windows XP 32 bit

## Supported Databases ##

  * IBM DB2 Database for Linux, Unix and Windows, version 8.2 or higher.
  * Remote connections to z/OS (DB2 UDB for zOS)

## Future Supported Databases ##

  * IBM Cloudscape
  * Apache Derby
  * IBM Informix Cheetah version 11.10 onwards
  * Remote connections to i5/OS (iSeries)

## Testing ##
Note for Django on Python: Before you run Django to connect to DB2, you need to ensure that IBM CLI  (which the DB2 Django adapter uses to connect to DB2) is accessible from Django. On Linux, set the LD\_LIBRARY\_PATH variable (for the user executing Django) to include the folder where the IBM CLI shared library (libdb2.so) resides - <br> for local DB2 access: export LD_LIBRARY_PATH=<code>&lt;</code>DB2_HOME<code>&gt;</code>/sqllib/lib:$LD_LIBRARY_PATH .<br> for remote DB2 access with DS Driver: export LD_LIBRARY_PATH=<code>&lt;</code>DS_DRIVER_FOLDER<code>&gt;</code>/odbc_cli_driver/linux/clidriver/lib:$LD_LIBRARY_PATH<br>
<br>
<br>
<ul><li>Create a new Django project by executing "django-admin.py startproject myproj".<br>
</li><li>Now go to this newly create directory, and edit settings.py file to access DB2.<br>
</li><li>In case of nix the steps will be like:<br>
<pre><code>  $ django-admin.py startproject myproj<br>
  $ cd myproj<br>
  $ vi settings.py<br>
</code></pre>
</li><li>The settings.py will be like (after adding DB2 properties):<br>
<pre><code>   DATABASES = {<br>
      'default': {<br>
         'ENGINE'     : 'ibm_db_django',<br>
         'NAME'       : 'mydb',<br>
         'USER'       : 'db2inst1',<br>
         'PASSWORD'   : 'ibmdb2',<br>
         'HOST'       : 'localhost',<br>
         'PORT'       : '50000',<br>
         'PCONNECT'   :  True,      #Optional property, default is false<br>
      }<br>
   }<br>
</code></pre>
</li><li>To enable DB2 support you need to set value of DATABASE_ENGINE to 'ibm_db_django' in settings.py.<br>
</li><li>In the tuple INSTALLED_APPS in settings.py add the following lines:<br>
<pre><code>   'django.contrib.flatpages',<br>
   'django.contrib.redirects',<br>
   'django.contrib.comments',<br>
   'django.contrib.admin',<br>
</code></pre>
</li><li>Next step is to run a simple test suite. To do this just execute following command in the project we created earlier:<br>
<pre><code>   $ python manage.py test #for Django-1.5.x or older<br>
   $ Python manage.py test django.contrib.auth #For Django-1.6.x onwards, since test discovery behavior have changed<br>
</code></pre>
</li><li>For Windows, steps are same as above. In case of editing settings.py file, use notepad (or any other) editor.</li></ul>

<h2>Database Transactions</h2>
<ul><li>Django by default executes without transactions i.e. in auto-commit mode. This default is generally not what you want in web-applications. <a href='http://docs.djangoproject.com/en/dev/topics/db/transactions/'>Remember to turn on transaction support in Django</a></li></ul>

<h2>Known Limitations of ibm_db_django adapter</h2>

<ul><li>Non-standard SQL queries are not supported. e.g. "SELECT ? FROM TAB1"<br>
</li><li>dbshell will not work if server is remote and client is DB2 thin client.<br>
</li><li>For updations involving primary/foreign key references, the entries should be made in correct order. Integrity check is always on and thus the primary keys referenced by the foreign keys in the referencing tables should always exist in the parent table.<br>
</li><li>DB2 Timestamps do not support timezone aware information. Thus a Datetime field including tzinfo(timezone aware info) would fail.</li></ul>

<h2>Feedback</h2>

<ul><li>ibm-db_django wiki: <a href='http://code.google.com/p/ibm-db/wiki/ibm_db_django_README'>http://code.google.com/p/ibm-db/wiki/ibm_db_django_README</a>
</li><li>ibm-db issues reports: <a href='http://code.google.com/p/ibm-db/issues/list'>http://code.google.com/p/ibm-db/issues/list</a>
</li><li>ibm-db developers: opendev@us.ibm.com