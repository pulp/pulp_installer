pulp-workers
============

Install, configure, and set the state of pulp workers.

Configurable Variables:
-----------------------

* `pulp_workers`: Specify how many workers and configuration for each. Defaults to
  2 workers which are started and enabled by systemd. See "defaults/main.yml" for an
  example of the syntax.

Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is not tightly coupled** with the `pulp-postgresql` role, but it does
use some of the same variables. When used together, the values are inherited from
the role. When not used together, these values are **required**.

* `postgresql_version`

This role **is tightly coupled** to the required `pulp-redis` role, and inherits
some of its variables.

* `pulp_user`
* `pulp_install_dir`

Dependencies:
-------------

* `pulp-redis`
