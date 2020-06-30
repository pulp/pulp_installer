pulp_database
=============

Install a suitable database server for Pulp.

More specifically, this role does the following:

1. Install and enable the appropriate SCL (EL7)
2. Call the external role to install a PostgreSQL database server.
3. Install the Python bindings to interact with the specified database via
   the role.
4. Configures the PostgreSQL database to listen on all addresses if the
   database is running on separate server.

Role Variables
--------------

* `pulp_settings_db_defaults`: This variable **should not be changed by users**, but serves as the
    defaults. Users wishing to set their own values should use the user-facing variable
    `pulp_settings.databases`. These settings define how Pulp will talk to the database, and
    produces default settings for the external database installer role. Default values are defined
    in `defaults/main.yml`. See [pulpcore
    docs](https://docs.pulpproject.org/en/master/nightly/installation/configuration.html#databases) or
    [Django docs](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) for more
    information.

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.
  This role sets the default to "auto", which is now more robust than
  "auto_legacy" on Ansible 2.8.

This role is **not tightly coupled** to the `pulp_common` role, but uses some of the same
variables. When used in the same play, the values are inherited from the role.
When not used together, this role provides identical defaults.

* `pulp_settings`

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.
