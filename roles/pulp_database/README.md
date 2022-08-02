pulp_database
=============

Install a suitable database server for Pulp.

More specifically, this role does the following:

1. Call the `pulp_repos` role to enable the appropriate SCL (EL7)
2. Call the external role
   ([geerlingguy.postgresql](https://github.com/geerlingguy/ansible-role-postgresql#readme))
   to install a PostgreSQL database server.
3. Install the Python bindings to interact with the specified database via
   the role.
4. Configures the PostgreSQL database to listen on all addresses if the
   database is running on separate server.

Role Variables
--------------

None, but see `pulp_settings.databases.default` below

Shared Variables
----------------

This role is **not tightly coupled** to the [pulp_common](../../roles/pulp_common)  role, but uses some of same  variables, listed below. This role provides identical default values.

* `pulp_settings.databases.default`: A dictionary. Its primary use is by the
  [pulp_common](../../roles/pulp_common) role, where it configures Pulp on how to talk to the database via a larger set of settings.
  Its secondary use is by the this role, where it configures the database server according to a
  smaller set of settings. The smaller set of settings is listed below. Note that these default settings are merged by the
  installer with your own; merely setting pulp_settings with 1 setting under it will not blow away all
  the other default settings.
    * `HOST` The hostname or IP address of the pulp database that pulp_common will connect to. This
      determines the default value of `postgresql_global_config_options`. Defaults to "localhost".
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

* `postgresql_global_config_options`: A list of dictionaries. It is a variable for the
  [external role](https://github.com/geerlingguy/ansible-role-postgresql#readme)
  to set multiple options. Pulp has 2 possible default values for this.

  If `pulp_settings.databases.default.HOST==localhost`

```yaml
  - option: unix_socket_directories
    value: '{{ postgresql_unix_socket_directories | join(",") }}'
  - option: log_directory
    value: 'log'
```

  If `pulp_settings.databases.default.HOST!=localhost`

```yaml
  - option: unix_socket_directories
    value: '{{ postgresql_unix_socket_directories | join(",") }}'
  - option: listen_addresses
    value: "*"
  - option: log_directory
    value: 'log'
```

  In other words, if set to localhost, postgresql will listen on UNIX sockets (specified by the
  [external role](https://github.com/geerlingguy/ansible-role-postgresql#readme)), in addition to the
  default of the loopback interface. If not set to localhost, postgresql will listen on all network interfaces.

* `postgresql_hba_entries`: A list of dictionaries. It is a variable for the
  [external role](https://github.com/geerlingguy/ansible-role-postgresql#readme)
  to configure [client authentication.](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)

  If `pulp_settings.databases.default.HOST==localhost`

```yaml
  - { type: local, database: all, user: postgres, auth_method: peer }
  - { type: local, database: all, user: all, auth_method: peer }
  - { type: host, database: all, user: all, address: '127.0.0.1/32', auth_method: md5 }
  - { type: host, database: all, user: all, address: '::1/128', auth_method: md5 }
```

  If `pulp_settings.databases.default.HOST!=localhost`

```yaml
  - { type: local, database: all, user: postgres, auth_method: peer }
  - { type: local, database: all, user: all, auth_method: peer }
  - { type: host, database: all, user: all, address: '0.0.0.0/0', auth_method: md5 }
  - { type: host, database: all, user: all, address: '::0/0', auth_method: md5 }
```

  In other words, if set to localhost, postgresql will authenticate on UNIX sockets and on the loopback interface.
  If not set to localhost, postgresql will authenticate on a UNIX socket and on all network interfaces.

  For security, you may also consider setting it to the following, which will limit it to local networks:

```yaml

  - { type: local, database: all, user: postgres, auth_method: peer }
  - { type: local, database: all, user: all, auth_method: peer }
  - { type: host, database: all, user: all, address: '127.0.0.1/32', auth_method: md5 }
  - { type: host, database: all, user: all, address: '::1/128', auth_method: md5 }
  - { type: host, database: all, user: all, ip_address: '{{ ansible_default_ipv4.network }}', ip_mask: '{{ ansible_default_ipv4.netmask }}', auth_method: md5 }
```

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.
