pulp3-content
=============

Install, configure, and set the state of pulp content app.

Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is not tightly coupled** with the `pulp3-postgresql` role, but it does
use some of the same variables. When used together, the values are inherited from
the role. When not used together, these values are **required**.

* `pulp_user`
* `pulp_install_dir`
