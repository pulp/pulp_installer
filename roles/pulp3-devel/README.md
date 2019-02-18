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
package_retries: 5
developer_user: vagrant
developer_user_home: /home/vagrant
pulp_default_admin_password: password
```
