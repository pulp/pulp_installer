pulp3-postgresql
================

Optionally call anxs/postgresql, and configure Pulp's database.

More specifically, this role does the following:

1. Call the anxs/postgresql role if `pulp_postgresql_call_anxs_postgresql` is
   true. This role installs and configures PostgreSQL.
2. Install the package needed to talk to PostgreSQL from Python, if any.
3. Create and run migrations for `core`.

Role Variables:
---------------

* `pulp_install_postgresql`: Defaults to true. Whether to install Postgresql.
* `pulp_database_config`: Defines how Pulp will talk to PostgreSQL. Defaults
  to values for a single-machine Pulp instance. See `defaults/main.yml` for
  specific values and syntax.
* `pulp_postgresql_host`: Host of the postgresql instance. Defaults to localhost.
* `pulp_postgresql_database`: Name of the postgresql database, defaults to pulp.
* `pulp_postgresql_user`: Postgresql user, (not linux user). Defaults to pulp
* `pulp_postgresql_password`: Password for Postgresql user. Defaults to pulp

Shared Variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** with the required the `pulp3` role and uses some of
variables which are documented in that role:

* `pulp_user`
* `pulp_install_dir`
* `pulp_install_plugins`
* `pulp_default_admin_password`


This role optionally depends on anxs.postgresql to install and configure the
database. To customize PostgreSQL's configuration, set the variables accepted by that
role. Default values for the anxs.postgresql role are set in `vars/main.yml`:

* `postgresql_databases`
* `postgresql_users`
* `postgresql_user_privilages`
* `postgresql_version`

Operating Systems Variables:
----------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

Dependencies:
-------------

* [anxs.postgresql](https://galaxy.ansible.com/anxs/postgresql), when
  `pulp_postgresql_call_anxs_postgresql` is true.
