pulp3-database
================

Optionally install a database, then configure for Pulp.

More specifically, this role does the following:

1. Call the external role to install a database if `pulp_install_db` is true.
2. Install the Python bindings to interact with the specified database.
3. Create and run migrations.

Role Variables:
---------------

* `pulp_database_config`: Defines how Pulp will talk to PostgreSQL. Default values are constructed
*                         from the other variables defined here. See `defaults/main.yml`.
* `pulp_db_host`: Host of the database instance. Defaults to localhost.
* `pulp_db_name`: Name of the database, defaults to pulp.
* `pulp_db_user`: Database user, should match linux user. Defaults to pulp
* `pulp_db_password`: Password for Postgresql user. Defaults to pulp
* `pulp_db_backend`: Django setting for db backend. for databasePassword for Postgresql user.
                     Defaults to "django.db.backends.postgresql_psycopg2"
* `pulp_install_db`: Defaults to true. Whether to install a database.

Shared Variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** with the required the `pulp3` role and uses some of
variables which are documented in that role:

* `pulp_user`
* `pulp_install_dir`
* `pulp_install_plugins`
* `pulp_default_admin_password`


This role optionally depends on other roles to install a database.

Operating Systems Variables:
----------------------------

Each currently supported operating system has a matching file in the "vars"
directory.
