pulp_database
=============

Install a suitable database server for Pulp.

More specifically, this role does the following:

1. Call the `pulp_repos` role to enable the appropriate SCL (EL7)
2. Call the external role to install a PostgreSQL database server.
3. Install the Python bindings to interact with the specified database via
   the role.
4. Configures the PostgreSQL database to listen on all addresses if the
   database is running on separate server.

Role Variables
--------------

None, but see `pulp_settings.databases.default` below

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.
  This role sets the default to "auto", which is now more robust than
  "auto_legacy" on Ansible 2.8.

This role is **not tightly coupled** to the [pulp_common](../../roles/pulp_common)  role, but uses some of same  variables, listed below. This role provides identical default values.

* `pulp_settings.databases.default`: A dictionary. Its primary use is by the
  [pulp_common](../../roles/pulp_common) role, where it configures Pulp on how to talk to the database via a larger set of settings.
  Its secondary use is by the this role, where it configures the database server according to a
  smaller set of settings. The smaller set of settings is listed below. Note that these default settings are merged by the
  installer with your own; merely setting pulp_settings with 1 setting under it will not blow away all
  the other default settings.
    * `NAME` The name of the Pulp database to create.  Defaults to `pulp`.
    * `USER` The user account to be created with permissions on the database.  Defaults to `pulp`.
    * `PASSWORD` The password to be created for the user account to talk to the Pulp database.
    Defaults to `pulp`, but please change it to something secure!
    * **Example**:

    ```yaml
    pulp_settings:
      databases:
        default:
          NAME: pulp
          USER: pulp
          PASSWORD: password
    ```

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.
