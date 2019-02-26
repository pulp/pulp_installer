Pulp3 Devel
===========

This role installs useful tools and adds some config files for a Pulp 3
development environment.

Example Usage
-------------

```yaml
- hosts: all
  roles:
    - pulp3-devel
```

Variables
---------

The variables that this role uses, along with their default values, are listed
below:

```yaml
pulp_devel_package_retries: 5
developer_user: vagrant
developer_user_home: /home/vagrant
pulp_default_admin_password: password
```

Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** with the `pulp3` role and it depends on some of the values set
used in that role.

* `pulp_user`
* `pulp_install_dir`
* `pulp_source_dir`
