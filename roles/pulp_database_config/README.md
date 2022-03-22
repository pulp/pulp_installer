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
* `pulp_db_fields_key`: Relative or absolute path to the Fernet symmetric encryption key
   one wants to import. The path is on the Ansible management node.
   It is used to encrypt certain fields in the database (such as credentials.)
   If not specified, a new key will be generated. (Only generated if one doesn't exist.)

Role Variables for advanced usage
---------------------------------

* `pulp_database_config_host`: pulp_database_config is designed to be run against only 1
  host. In the event that it is accidentally run against multiple hosts, this is the only
  host that will run pulp_database_config's tasks that actually modify the state of the
  host/application. Its database fields encryption key will be copied to all the other
  hosts in later roles. If not specified, a host is randomly picked from suitable hosts
  (hosts that already have the database fields encryption key.) If specified, it must
  match the host's name in the Ansible inventory exactly.

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
* `pulp_user_home`
* `pulp_certs_dir`: Path where to generate or drop the keys for database fields encryption.
   Defaults to '{{ pulp_config_dir }}/certs' .
* `pulp_config_dir`
* `pulp_scripts_dir`: The collection signing service script must exist under this directory
  with the filename `collection_sign.sh` when `galaxy_create_default_collection_signing_service==true`.

This role **is tightly coupled** with the required the `galaxy_post_install` role (which is called
by pulp_common when galaxy-ng is an installed plugin) and uses some of variables which are
documented in that role:
*  `galaxy_create_default_collection_signing_service` Defaults to `false`.

This role understands how to talk to the database server via `pulp_settings_file`,
which is written to disk in the `pulp_common` role, and whose relevant
values are set via the following variables:

* `pulp_settings_db_defaults`: See pulp_database README.

Limitations
-----------
* pulp_database_config is designed to be run against only 1 host.

If it is accidentally run against multiple hosts (which will happen if
pulp_services is run against multiple hosts), 1 host will be picked to
actually run the tasks in pulp_database_config.

* pulp_database_config must be run against an existing host in a cluster if the
cluster is being expanded with this ansible playbook run.

For example, if you run pulp_database_config against host1 and host2, and you
later re-run pulp_installer to add host3 to the cluster, then either host1
or host2 must have pulp_database_config run against it.
