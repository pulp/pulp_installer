pulp3-resource-manager
=============

Install, configure, and set the state of the pulp resouce manager.

Configurable Variables:
-----------------------

* `pulp_resouce_manager_state`: This variable can be configured with any of the
  states allowed by the systemd module's "state" directive. Defaults to "started."
* `pulp_resouce_manager_enabled`: This variable can be configured with any of the
  states allowed by the systemd module's "enabled" directive. Defaults to "true."

Shared variables:
-----------------

This role **is not tightly coupled** with the `pulp3-postgresql` role, but it does
use some of the same variables. When used together, the values are inherited from
the role. When not used together, these values are **required**.

* `postgresql_version`

This role **is tightly coupled** to the required `pulp3-redis` role, and inherits
some of its variables.

* `pulp_user`
* `pulp_install_dir`

Dependencies:
-------------

* `pulp3-redis`
