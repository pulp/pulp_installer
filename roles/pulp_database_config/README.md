pulp_database_config
====================

Configure the database for Pulp 3

More specifically, this role does the following via `django-admin`:

1. Create and run migrations.
2. Set the Pulp admin user's password.

Role Variables
--------------

* `pulp_default_admin_password`: Initial password for the Pulp admin. Only affects Pulp
  during initial install, not upgrades/updates or re-running the installer for any other
  reason. **Required**.

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.
  This role sets the default to "auto", which is now more robust than
  "auto_legacy" on Ansible 2.8.

This role **is tightly coupled** with the required the `pulp_common` role and uses some of
variables which are documented in that role:

* `pulp_django_admin_paths`
* `pulp_settings_file`
* `pulp_user`

This role understands how to talk to the database server via `pulp_settings_file`,
which is written to disk in the `pulp_common` role, and whose relevant
values are set via the following variables:

* `pulp_settings_db_defaults`: See pulp_database README.
