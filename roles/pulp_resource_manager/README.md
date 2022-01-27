pulp_resource_manager
=====================

Install, configure, and set the state of the pulp resouce manager.

Role Variables
--------------

* `pulp_resouce_manager_state`: This variable can be configured with any of the
  states allowed by the systemd module's "state" directive. Defaults to "started."
* `pulp_resouce_manager_enabled`: This variable can be configured with any of the
  states allowed by the systemd module's "enabled" directive. Defaults to "true."

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-resource-manager systemd process
* `pulp_settings_file`
* `pulp_user`
