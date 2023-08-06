SQLiteMinor
========================

SQLiteMinor is a simple Python class for reading- and deleting from, updating and adding to a table in an sqlite database. 

The SQLiteMinor object provides basic database table access functionality without the need for writing any sql statements,
writing code for connection and cursor objects, etc.  The operations are handled with simple method calls on the
object.  The functionality is also limited, as the sql statements which are used to work with the database are mostly fixed;
therefore the name of this module is "minor".  

The main goal of writing this module was to provide a means of working with sqlite databases without the user/developer having 
to actually write any sql or python code which directly executes it. Instead, the object and methods make what is hopefully a
cleaner and more intuitive interface.  Naturally there is also the advantage of having most or all the sql/python database code needed
in one class.

This module was written as a companion to the sqlitemgr module (https://github.com/aescwork/sqlitemgr).  

This module was originally conceived for the waxtablet Python application, along with the FileWork module (https://github.com/aescwork/filework)
and the sqlitemgr module (https://github.com/aescwork/sqlitemgr).  

Complete documentation for this module is available in the docs/html directory of this repository.
