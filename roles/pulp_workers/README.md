pulp_workers
============

Install, configure, and set the state of pulp workers.

This role depends on the [pulp_common](../../roles/pulp_common) role, see it for many more variables on configuring pulp_database_workers.

Role Variables
--------------

* `pulp_workers`: Specify how many workers. Defaults to 2 workers.

Shared variables
----------------

This role depends upon the the [`pulp_common`](../helper_roles/pulp_common) role, which in turn depends on on [pulp_repos](../helper_roles/pulp_repos). You should consult [`pulp_common`](../helper_roles/pulp_common) in particular for variables that effectively control the behavior of this role.

This role also utilizes some of the pulp_common role's variables in its logic:

* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-worker systemd processes
* `pulp_settings_file`
* `pulp_user`
