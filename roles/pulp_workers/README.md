pulp_workers
============

Install, configure, and set the state of pulp workers.

Role Variables
--------------

* `pulp_workers`: Specify how many workers. Defaults to 2 workers.

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-worker systemd processes
* `pulp_settings_file`
* `pulp_user`
