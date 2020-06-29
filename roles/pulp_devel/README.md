pulp_devel
==========

This role installs useful tools and adds some config files for a Pulp 3
development environment.

Example Usage
-------------

```yaml
- hosts: all
  roles:
    - pulp_all_services
    - pulp_devel
```

Variables
---------

The variables that this role uses are listed below:

The following variables have a default value:
```yaml
pulp_devel_package_retries: 5
```

The following variables have no default value, and we recommend the following
for development purposes on vagrant (as part of [pulplift](https://github.com/pulp/pulplift).)
```yaml
developer_user: vagrant
developer_user_home: /home/vagrant
pulp_default_admin_password: password
```

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** with the `pulp_common` role and it depends on some of the values set
used in that role.

* `pulp_user`
* `pulp_install_dir`
* `pulp_source_dir` (Note: Pip VCS URLs will not work with pulp_devel.)

This role **is not tightly coupled** with the `pulp_workers` role, but it does
use some of the same variables. When not used together, these values are **required**.

* `pulp_workers`

This role **is not tightly coupled** with the `pulp_database_config` role,
but it does use some of the same variables. When not used together, these values
are **required**.

* `pulp_default_admin_password`


Aliases
-------

This role provides the following aliases:

* `phelp`: List all available aliases.
* `pstart`: Start all pulp-related services
* `pstop`: Stop all pulp-related services
* `prestart`: Restart all pulp-related services
* `pstatus`: Report the status of all pulp-related services
* `pdbreset`: Reset the Pulp database - **THIS DESTROYS YOUR PULP DATA**
* `pclean`: Restore pulp to a clean-installed state - **THIS DESTROYS YOUR PULP DATA**
* `pjournal`: Interact with the journal for pulp-related unit
* `reset_pulp2`: Resets Pulp 2 - drop the DB, remove content and publications from FS, restart services.
* `populate_pulp2_iso`: Syncs 4 ISO repos.
* `populate_pulp2_rpm`: Sync 1 RPM repo.
* `populate_pulp2_docker`: Sync 1 Docker repo.
* `populate_pulp2`: Reset Pulp 2 and sync ISO, RPM, Docker repos.
* `pyclean`: Cleanup extra python files
* `pfixtures`: Run pulp-fixtures container in foreground
* `pbindings`: Create and install bindings. Example usage: `pbindings pulpcore python`
* `pminio`: Switch to minio for S3 testing. For stopping it: `pminio stop`
