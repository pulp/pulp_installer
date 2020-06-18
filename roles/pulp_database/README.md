pulp_database
=============

Optionally install a database, then configure for Pulp.

More specifically, this role does the following:

1. Call the external role to install a database if `pulp_install_db` is true.
2. Install the Python bindings to interact with the specified database.
3. Create and run migrations.

Role Variables
--------------

* `pulp_settings_db_defaults`: This variable **should not be changed by users**, but serves as the
    defaults. Users wishing to set their own values should use the user-facing variable
    `pulp_settings.databases`. These settings define how Pulp will talk to the database, and
    produces default settings for the external database installer role. Default values are defined
    in `defaults/main.yml`. See [pulpcore
    docs](https://docs.pulpproject.org/en/3.0/nightly/installation/configuration.html#databases) or
    [Django docs](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) for more
    information.

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.
  This role sets the default to "auto", which is now more robust than
  "auto_legacy" on Ansible 2.8.

This role **is tightly coupled** with the required the `pulp_common` role and uses some of
variables which are documented in that role:

* `pulp_user`
* `pulp_default_admin_password`
* `pulp_settings`

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.
