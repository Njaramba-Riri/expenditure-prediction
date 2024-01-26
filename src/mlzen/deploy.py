Metadata-Version: 2.1
Name: SQLAlchemy
Version: 1.4.51
Summary: Database Abstraction Library
Home-page: https://www.sqlalchemy.org
Author: Mike Bayer
Author-email: mike_mp@zzzcomputing.com
License: MIT
Project-URL: Documentation, https://docs.sqlalchemy.org
Project-URL: Issue Tracker, https://github.com/sqlalchemy/sqlalchemy/
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.6
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: 3.12
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Classifier: Topic :: Database :: Front-Ends
Requires-Python: !=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*,>=2.7
Description-Content-Type: text/x-rst
License-File: LICENSE
Requires-Dist: importlib-metadata ; python_version < "3.8"
Requires-Dist: greenlet !=0.4.17 ; python_version >= "3" and (platform_machine == "aarch64" or (platform_machine == "ppc64le" or (platform_machine == "x86_64" or (platform_machine == "amd64" or (platform_machine == "AMD64" or (platform_machine == "win32" or platform_machine == "WIN32"))))))
Provides-Extra: aiomysql
Requires-Dist: greenlet !=0.4.17 ; (python_version >= "3") and extra == 'aiomysql'
Requires-Dist: aiomysql >=0.2.0 ; (python_version >= "3") and extra == 'aiomysql'
Provides-Extra: aiosqlite
Requires-Dist: typing-extensions !=3.10.0.1 ; extra == 'aiosqlite'
Requires-Dist: greenlet !=0.4.17 ; (python_version >= "3") and extra == 'aiosqlite'
Requires-Dist: aiosqlite ; (python_version >= "3") and extra == 'aiosqlite'
Provides-Extra: asyncio
Requires-Dist: greenlet !=0.4.17 ; (python_version >= "3") and extra == 'asyncio'
Provides-Extra: asyncmy
Requires-Dist: greenlet !=0.4.17 ; (python_version >= "3") and extra == 'asyncmy'
Requires-Dist: asyncmy !=0.2.4,>=0.2.3 ; (python_version >= "3") and extra == 'asyncmy'
Provides-Extra: mariadb_connector
Requires-Dist: mariadb !=1.1.2,>=1.0.1 ; (python_version >= "3") and extra == 'mariadb_connector'
Provides-Extra: mssql
Requires-Dist: pyodbc ; extra == 'mssql'
Provides-Extra: mssql_pymssql
Requires-Dist: pymssql ; extra == 'mssql_pymssql'
Provides-Extra: mssql_pyodbc
Requires-Dist: pyodbc ; extra == 'mssql_pyodbc'
Provides-Extra: mypy
Requires-Dist: sqlalchemy2-stubs ; extra == 'mypy'
Requires-Dist: mypy >=0.910 ; (python_version >= "3") and extra == 'mypy'
Provides-Extra: mysql
Requires-Dist: mysqlclient <2,>=1.4.0 ; (python_version < "3") and extra == 'mysql'
Requires-Dist: mysqlclient >=1.4.0 ; (python_version >= "3") and extra == 'mysql'
Provides-Extra: mysql_connector
Requires-Dist: mysql-connector-python ; extra == 'mysql_connector'
Provides-Extra: oracle
Requires-Dist: cx-oracle <8,>=7 ; (python_version < "3") and extra == 'oracle'
Requires-Dist: cx-oracle >=7 ; (python_version >= "3") and extra == 'oracle'
Provides-Extra: postgresql
Requires-Dist: psycopg2 >=2.7 ; extra == 'postgresql'
Provides-Extra: postgresql_asyncpg
Requires-Dist: greenlet !=0.4.17 ; (python_version >= "3") and extra == 'postgresql_asyncpg'
Requires-Dist: asyncpg ; (python_version >= "3") and extra == 'postgresql_asyncpg'
Provides-Extra: postgresql_pg8000
Requires-Dist: pg8000 !=1.29.0,>=1.16.6 ; extra == 'postgresql_pg8000'
Provides-Extra: postgresql_psycopg2binary
Requires-Dist: psycopg2-binary ; extra == 'postgresql_psycopg2binary'
Provides-Extra: postgresql_psycopg2cffi
Requires-Dist: psycopg2cffi ; extra == 'postgresql_psycopg2cffi'
Provides-Extra: pymysql
Requires-Dist: pymysql <1 ; (python_version < "3") and extra == 'pymysql'
Requires-Dist: pymysql ; (python_version >= "3") and extra == 'pymysql'
Provides-Extra: sqlcipher
Requires-Dist: sqlcipher3-binary ; (python_version >= "3") and extra == 'sqlcipher'

SQLAlchemy
==========

|PyPI| |Python| |Downloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/sqlalchemy
    :target: https://pypi.org/project/sqlalchemy
    :alt: PyPI

.. |Python| image:: https://img.shields.io/pypi/pyversions/sqlalchemy
    :target: https://pypi.org/project/sqlalchemy
    :alt: PyPI - Python Version

.. |Downloads| image:: https://img.shields.io/pypi/dm/sqlalchemy
    :target: https://pypi.org/project/sqlalchemy
    :alt: PyPI - Downloads


The Python SQL Toolkit and Object Relational Mapper

Introduction
-------------

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
that gives application developers the full power and
flexibility of SQL. SQLAlchemy provides a full suite
of well known enterprise-level persistence patterns,
designed for efficient and high-performing database
access, adapted into a simple and Pythonic domain
language.

Major SQLAlchemy features include:

* An industrial strength ORM, built
  from the core on the identity map, unit of work,
  and data mapper patterns.   These patterns
  allow transparent persistence of objects
  using a declarative configuration system.
  Domain models
  can be constructed and manipulated naturally,
  and changes are synchronized with the
  current transaction automatically.
* A relationally-oriented query system, exposing
  the full range of SQL's capabilities
  explicitly, including joins, subqueries,
  correlation, and most everything else,
  in terms of the object model.
  Writing queries with the ORM uses the same
  techniques of relational composition you use
  when writing SQL.  While you can drop into
  literal SQL at any time, it's virtually never
  needed.
* A comprehensive and flexible system
  of eager loading for related collections and objects.
  Collections are cached within a session,
  and can be loaded on individual access, all
  at once using joins, or by query per collection
  across the full result set.
* A Core SQL construction system and DBAPI
  interaction layer.  The SQLAlchemy Core is
  separate from the ORM and is a full database
  abstraction layer in its own right, and includes
  an extensible Python-based SQL expression
  language, schema metadata, connection pooling,
  type coercion, and custom types.
* All primary and foreign key constraints are
  assumed to be composite and natural.  Surrogate
  integer primary keys are of course still the
  norm, but SQLAlchemy never assumes or hardcodes
  to this model.
* Database introspection and generation.  Database
  schemas can be "reflected" in one step into
  Python structures representing database metadata;
  those same structures can then generate
  CREATE statements right back out - all within
  the Core, independent of the ORM.

SQLAlchemy's philosophy:

* SQL databases behave less and less like object
  collections the more size and performance start to
  matter; object collections behave less and less like
  tables and rows the more abstraction starts to matter.
  SQLAlchemy aims to accommodate both of these
  principles.
* An ORM doesn't need to hide the "R".   A relational
  database provides rich, set-based functionality
  that should be fully exposed.   SQLAlchemy's
  ORM provides an open-ended set of patterns
  that allow a developer to construct a custom
  mediation layer between a domain model and
  a relational schema, turning the so-called
  "object relational impedance" issue into
  a distant memory.
* The developer, in all cases, makes all decisions
  regarding the design, structure, and naming conventions
  of both the object model as well as the relational
  schema.   SQLAlchemy only provides the means
  to automate the execution of these decisions.
* With SQLAlchemy, there's no such thing as
  "the ORM generated a bad query" - you
  retain full control over the structure of
  queries, including how joins are organized,
  how subqueries and correlation is used, what
  columns are requested.  Everything SQLAlchemy
  does is ultimately the result of a developer-
  initiated decision.
* Don't use an ORM if the problem doesn't need one.
  SQLAlchemy consists of a Core and separate ORM
  component.   The Core offers a full SQL expression
  language that allows Pythonic construction
  of SQL constructs that render directly to SQL
  strings for a target database, returning
  result sets that are essentially enhanced DBAPI
  cursors.
* Transactions should be the norm.  With SQLAlchemy's
  ORM, nothing goes to permanent storage until
  commit() is called.  SQLAlchemy encourages applications
  to create a consistent means of delineating
  the start and end of a series of operations.
* Never render a literal value in a SQL statement.
  Bound parameters are used to the greatest degree
  possible, allowing query optimizers to cache
  query plans effectively and making SQL injection
  attacks a non-issue.

Documentation
-------------

Latest documentation is at:

https://www.sqlalchemy.org/docs/

Installation / Requirements
---------------------------

Full documentation for installation is at
`Installation <https://www.sqlalchemy.org/docs/intro.html#installation>`_.

Getting Help / Development / Bug reporting
------------------------------------------

Please refer to the `SQLAlchemy Community Guide <https://www.sqlalchemy.org/support.html>`_.

Code of Conduct
---------------

Above all, SQLAlchemy places great emphasis on polite, thoughtful, and
constructive communication between users and developers.
Please see our current Code of Conduct at
`Code of Conduct <https://www.sqlalchemy.org/codeofconduct.html>`_.

License
-------

SQLAlchemy is distributed under the `MIT license
<https://www.opensource.org/licenses/mit-license.php>`_.

