pulp3-postgresql
================

Optionally call anxs/postgresql, and configure Pulp's database.

More specifically, this role does the following:

1. Call the anxs/postgresql role if `pulp_postgresql_call_anxs_postgresql` is
   true. This role installs and configures PostgreSQL.
2. Install the package needed to talk to PostgreSQL from Python, if any.
3. Create and run migrations for `pulp_app`.

Variables:

* `pulp_postgresql_call_anxs_postgresql`: Optional, defaults to true. Whether to
  call [anxs.postgresql](https://galaxy.ansible.com/anxs/postgresql).
* `pulp_database_config`: Optional. Defines how Pulp will talk to PostgreSQL.
* `pulp_config_dir`, `pulp_install_dir`, `pulp_user`: Optional. The meaning is
  the same as for the `pulp3` role.

This role depends on anxs.postgresql to install and configure the database. To
customize PostgreSQL's configuration, set the variables accepted by that role,
e.g. `postgresql_databases`.

Dependencies:

* [anxs.postgresql](https://galaxy.ansible.com/anxs/postgresql), when
  `pulp_postgresql_call_anxs_postgresql` is true.
